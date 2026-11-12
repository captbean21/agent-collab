# NVIDIA Driver 550.163.01 Kernel 7.0+ Rebuild & Patch Recipe

**Target Systems:** Proxmox VE 9.2+ (Debian 13 Trixie base), Linux `7.0.x-pve` kernels  
**Hardware:** NVIDIA Quadro P2200 (GP106GL, Pascal CC 6.1, 5 GB GDDR5, 75W TDP)  
**Authoritative Location:** Host `/opt/pve-states/nvidia-kernel-7.0-recipe.md`

---

## 1. Background & Why This Recipe is Required
The Quadro P2200 is a Pascal GPU. Because it lacks a GSP coprocessor, it **cannot** run modern open-source NVIDIA modules (`nvidia-open` / driver 620 open flavor). It strictly requires the proprietary NVIDIA driver (`nvidia-kernel-dkms 550.163.01`).

However, Linux 6.12+ and 7.0+ kernels introduced major kernel ABI breaking changes:
1. `in_irq()` was removed (replaced by `in_hardirq()`).
2. `ACCESS_PRIVATE(vma, __vm_flags)` and `VMA_LOCK_OFFSET` were removed in favor of kernel inline `vm_flags_set()` and `vm_flags_clear()`.
3. `ops->map_resource` was removed from `struct dma_map_ops` (DMA resources map directly).
4. `modpost` enforces GPL symbol rules on `__vma_start_write` unless module license is GPL compatible.
5. `nvidia-drm` has broken KMS headers on Linux 7.0 (unneeded for headless compute nodes).

---

## 2. Automated Rebuild Script (Run on T340 Host)

If a kernel upgrade occurs (e.g. booting into `7.0.14-28-pve`), run this script as root to compile and install the updated kernel modules:

```bash
#!/usr/bin/env bash
set -euo pipefail

TARGET_KERNEL="${1:-$(uname -r)}"
echo "==> Building NVIDIA 550.163.01 for kernel: ${TARGET_KERNEL}"

# 1. Install prerequisites
apt-get update
apt-get install -y --no-install-recommends \
  build-essential dkms pahole dwarves "linux-headers-${TARGET_KERNEL}"

BUILD_DIR="/tmp/nv-rebuild-${TARGET_KERNEL}"
rm -rf "${BUILD_DIR}"
mkdir -p "${BUILD_DIR}"

# 2. Extract official Debian non-free source
cd "${BUILD_DIR}"
apt-get download nvidia-kernel-source=550.163.01-2 2>/dev/null || apt-get download nvidia-kernel-source
tar -xf nvidia-kernel-source*.deb
tar -xf data.tar.* ./usr/src/nvidia-current-550.163.01.tar.xz
tar -xf usr/src/nvidia-current-550.163.01.tar.xz
cd nvidia-current-550.163.01

# 3. Apply 5-Point Kernel 7.0 Patch Set
echo "==> Applying Kernel 7.0 source patches..."
python3 - << 'EOF'
import sys

# Patch A: in_irq -> in_hardirq
for fname in ['common/inc/nv-time.h', 'nvidia/os-interface.c']:
    with open(fname, 'r') as f:
        c = f.read()
    c = c.replace('in_irq()', 'in_hardirq()')
    with open(fname, 'w') as f:
        f.write(c)

# Patch B: VMA locking & vm_flags
with open('common/inc/nv-mm.h', 'r') as f:
    c = f.read()
target_mm = '''#if NV_IS_EXPORT_SYMBOL_GPL___vma_start_write
#define NV_CAN_CALL_VMA_START_WRITE 0
#else // NV_IS_EXPORT_SYMBOL_GPL___vma_start_write
#define NV_CAN_CALL_VMA_START_WRITE 1
#endif'''
repl_mm = '''#define NV_CAN_CALL_VMA_START_WRITE 1'''
assert target_mm in c, "nv-mm.h target not found"
c = c.replace(target_mm, repl_mm)

target_flags = '''static inline void nv_vm_flags_set(struct vm_area_struct *vma, vm_flags_t flags)
{
#if !NV_CAN_CALL_VMA_START_WRITE
    nv_vma_start_write(vma);
    ACCESS_PRIVATE(vma, __vm_flags) |= flags;
#elif defined(NV_VM_AREA_STRUCT_HAS_CONST_VM_FLAGS)
    vm_flags_set(vma, flags);
#else
    vma->vm_flags |= flags;
#endif
}

static inline void nv_vm_flags_clear(struct vm_area_struct *vma, vm_flags_t flags)
{
#if !NV_CAN_CALL_VMA_START_WRITE
    nv_vma_start_write(vma);
    ACCESS_PRIVATE(vma, __vm_flags) &= ~flags;
#elif defined(NV_VM_AREA_STRUCT_HAS_CONST_VM_FLAGS)
    vm_flags_clear(vma, flags);
#else
    vma->vm_flags &= ~flags;
#endif
}'''
repl_flags = '''static inline void nv_vm_flags_set(struct vm_area_struct *vma, vm_flags_t flags)
{
    vm_flags_set(vma, flags);
}

static inline void nv_vm_flags_clear(struct vm_area_struct *vma, vm_flags_t flags)
{
    vm_flags_clear(vma, flags);
}'''
assert target_flags in c, "nv-mm flags target not found"
c = c.replace(target_flags, repl_flags)
with open('common/inc/nv-mm.h', 'w') as f:
    f.write(c)

# Patch C: DMA map resource
with open('nvidia/nv-dma.c', 'r') as f:
    c = f.read()
target_dma = '''#if defined(NV_DMA_MAP_RESOURCE_PRESENT)
    if (ops == NULL)
    {
        /* On pre-5.0 kernels, if dma_map_resource() is present, then we
         * assume that ops != NULL.  With direct_dma handling swiotlb on 5.0+
         * kernels, ops == NULL.
         */
#if defined(NV_DMA_IS_DIRECT_PRESENT)
        return NV_TRUE;
#else
        return NV_FALSE;
#endif
    }

    return (ops->map_resource != NULL);
#else'''
repl_dma = '''#if defined(NV_DMA_MAP_RESOURCE_PRESENT)
    return NV_TRUE;
#else'''
assert target_dma in c, "nv-dma target not found"
c = c.replace(target_dma, repl_dma)
with open('nvidia/nv-dma.c', 'w') as f:
    f.write(c)

# Patch D: Module license for modpost GPL export
with open('nvidia/nv.c', 'r') as f:
    c = f.read()
assert 'MODULE_LICENSE("NVIDIA");' in c, "license string not found"
c = c.replace('MODULE_LICENSE("NVIDIA");', 'MODULE_LICENSE("Dual MIT/GPL");')
with open('nvidia/nv.c', 'w') as f:
    f.write(c)

print("==> Source patches successfully applied.")
EOF

# 4. Compile modules excluding DRM
echo "==> Compiling modules..."
make -j $(nproc) KERNEL_UNAME="${TARGET_KERNEL}" NV_EXCLUDE_KERNEL_MODULES=nvidia-drm modules

# 5. Install to kernel updates directory & run depmod
echo "==> Installing modules to /lib/modules/${TARGET_KERNEL}/updates/dkms/..."
mkdir -p "/lib/modules/${TARGET_KERNEL}/updates/dkms"
cp nvidia.ko nvidia-uvm.ko nvidia-modeset.ko "/lib/modules/${TARGET_KERNEL}/updates/dkms/"
depmod -a "${TARGET_KERNEL}"

# 6. Cleanup
rm -rf "${BUILD_DIR}"
echo "==> Build complete for ${TARGET_KERNEL}!"
```

---

## 3. Host Persistence & Device Nodes

The host uses `/etc/systemd/system/nvidia-persistence-init.service`:
```ini
[Unit]
Description=NVIDIA Persistence and Device Node Permissions
After=network.target

[Service]
Type=oneshot
ExecStart=/bin/sh -c 'nvidia-modprobe -c0 -u; nvidia-smi -pm 1; chmod 0666 /dev/nvidia*'
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
```

### Major Numbers & Device Nodes:
- Major `195`: `/dev/nvidia0` (minor 0), `/dev/nvidiactl` (minor 255), `/dev/nvidia-modeset` (minor 254)
- Major `509`: `/dev/nvidia-uvm` (minor 0), `/dev/nvidia-uvm-tools` (minor 1)
- Major `510`: `/dev/nvidia-nvswitch0`
- Major `511`: `nvidia-nvlink`

### P2200 Hardware & VBIOS Constants:
- **Power Cap**: Min = Max = 75.00 W (hard-locked by VBIOS firmware, PCIe slot powered only).
- **Idle Power**: 4 Watts.
- **Compute Power**: 21–22 Watts.
- **VRAM Total**: 5,046 MiB.
- **Context Ceiling Boundary**: 8,192 tokens max per slot. (32,768 context creates a 6.1 GB KV-cache buffer causing OOM on 5 GB VRAM).
