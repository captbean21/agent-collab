use anyhow::Result;
use ash::{vk, Entry};
use std::sync::Arc;
use wav::{Header, bit_depth::Sixteen};

#[repr(C)]
#[derive(Clone, Copy, Debug)]
struct Patch {
    sample_rate: f32,
    duration: f32,
    bpm: f32,
    osc1_freq: f32,
    osc1_shape: f32,
    osc1_detune: f32,
    osc2_freq_ratio: f32,
    osc2_shape: f32,
    osc2_level: f32,
    filter_cutoff: f32,
    filter_res: f32,
    filter_env_amt: f32,
    env_attack: f32,
    env_decay: f32,
    env_sustain: f32,
    env_release: f32,
    fenv_attack: f32,
    fenv_decay: f32,
    fenv_sustain: f32,
    fenv_release: f32,
    fenv_amt: f32,
    arp_rate: f32,
    arp_pattern: i32,
    arp_octaves: i32,
    delay_time: f32,
    delay_feedback: f32,
    delay_mix: f32,
    master_gain: f32,
}

fn default_patch() -> Patch {
    Patch {
        sample_rate: 44100.0,
        duration: 20.0,
        bpm: 118.0,
        osc1_freq: 55.0,      // A1
        osc1_shape: 1.0,      // saw
        osc1_detune: 0.0,
        osc2_freq_ratio: 0.5, // octave down
        osc2_shape: 2.0,      // square
        osc2_level: 0.3,
        filter_cutoff: 800.0,
        filter_res: 0.6,
        filter_env_amt: 1.0,
        env_attack: 0.01,
        env_decay: 0.3,
        env_sustain: 0.4,
        env_release: 0.5,
        fenv_attack: 0.001,
        fenv_decay: 0.2,
        fenv_sustain: 0.3,
        fenv_release: 0.3,
        fenv_amt: 1.0,
        arp_rate: 118.0 / 60.0 * 4.0, // 16th notes
        arp_pattern: 2,              // updown
        arp_octaves: 2,
        delay_time: 0.254,
        delay_feedback: 0.3,
        delay_mix: 0.2,
        master_gain: 0.5,
    }
}

fn read_shader_spirv(path: &str) -> Result<Vec<u32>> {
    use std::fs::File;
    use std::io::Read;
    let mut file = File::open(path)?;
    let mut bytes = Vec::new();
    file.read_to_end(&mut bytes)?;
    let words: Vec<u32> = bytes
        .chunks_exact(4)
        .map(|chunk| u32::from_le_bytes([chunk[0], chunk[1], chunk[2], chunk[3]]))
        .collect();
    Ok(words)
}

fn main() -> Result<()> {
    let patch = default_patch();
    let sample_count = (patch.sample_rate * patch.duration) as usize;
    let buffer_size = sample_count * 2 * std::mem::size_of::<f32>(); // stereo f32

    // === Load SPIR-V ===
    let spirv = read_shader_spirv("../synth.spv")?;

    // === Vulkan Setup ===
    let entry = Entry::linked();
    let instance = {
        let app_info = vk::ApplicationInfo::default()
            .application_name(c"Vulkan Synth")
            .api_version(vk::API_VERSION_1_3);
        let create_info = vk::InstanceCreateInfo::default().application_info(&app_info);
        unsafe { entry.create_instance(&create_info, None)? }
    };

    // Pick physical device (prefer discrete GPU)
    let physical_devices = unsafe { instance.enumerate_physical_devices()? };
    let physical_device = physical_devices
        .into_iter()
        .find(|pd| {
            let props = unsafe { instance.get_physical_device_properties(*pd) };
            props.device_type == vk::PhysicalDeviceType::DISCRETE_GPU
        })
        .or_else(|| {
            physical_devices
                .into_iter()
                .find(|pd| {
                    let props = unsafe { instance.get_physical_device_properties(*pd) };
                    props.device_type == vk::PhysicalDeviceType::INTEGRATED_GPU
                })
        })
        .expect("No suitable GPU found");

    let props = unsafe { instance.get_physical_device_properties(physical_device) };
    println!("Using GPU: {:?}", unsafe { std::ffi::CStr::from_ptr(props.device_name.as_ptr()) });

    // Find compute queue
    let queue_props = unsafe { instance.get_physical_device_queue_family_properties(physical_device) };
    let compute_queue_family = queue_props
        .iter()
        .position(|qp| qp.queue_flags.contains(vk::QueueFlags::COMPUTE))
        .expect("No compute queue family") as u32;

    // Create logical device
    let queue_priorities = [1.0];
    let queue_info = vk::DeviceQueueCreateInfo::default()
        .queue_family_index(compute_queue_family)
        .queue_priorities(&queue_priorities);
    let features = vk::PhysicalDeviceFeatures::default().shader_float64(true);
    let device_info = vk::DeviceCreateInfo::default()
        .queue_create_infos(std::slice::from_ref(&queue_info))
        .enabled_features(&features);
    let device = Arc::new(unsafe { instance.create_device(physical_device, &device_info, None)? });

    let compute_queue = unsafe { device.get_device_queue(compute_queue_family, 0) };

    // === Create Shader Module ===
    let shader_module = {
        let create_info = vk::ShaderModuleCreateInfo::default().code(&spirv);
        unsafe { device.create_shader_module(&create_info, None)? }
    };

    // === Create Storage Buffer ===
    let buffer_info = vk::BufferCreateInfo::default()
        .size(buffer_size as u64)
        .usage(vk::BufferUsageFlags::STORAGE_BUFFER | vk::BufferUsageFlags::TRANSFER_SRC)
        .sharing_mode(vk::SharingMode::EXCLUSIVE);
    let buffer = unsafe { device.create_buffer(&buffer_info, None)? };
    let mem_req = unsafe { device.get_buffer_memory_requirements(buffer) };
    let mem_props = unsafe { instance.get_physical_device_memory_properties(physical_device) };
    let mem_type = (0..mem_props.memory_type_count)
        .find(|i| {
            mem_req.memory_type_bits & (1 << i) != 0
                && mem_props.memory_types[*i as usize].property_flags
                    .contains(vk::MemoryPropertyFlags::HOST_VISIBLE | vk::MemoryPropertyFlags::HOST_COHERENT)
        })
        .expect("No suitable memory type") as u32;
    let alloc_info = vk::MemoryAllocateInfo::default()
        .allocation_size(mem_req.size)
        .memory_type_index(mem_type);
    let buffer_memory = unsafe { device.allocate_memory(&alloc_info, None)? };
    unsafe { device.bind_buffer_memory(buffer, buffer_memory, 0)? };

    // === Descriptor Set Layout ===
    let binding = vk::DescriptorSetLayoutBinding::default()
        .binding(0)
        .descriptor_type(vk::DescriptorType::STORAGE_BUFFER)
        .descriptor_count(1)
        .stage_flags(vk::ShaderStageFlags::COMPUTE);
    let layout_info = vk::DescriptorSetLayoutCreateInfo::default().bindings(std::slice::from_ref(&binding));
    let desc_layout = unsafe { device.create_descriptor_set_layout(&layout_info, None)? };

    // === Pipeline Layout ===
    let push_constant_range = vk::PushConstantRange::default()
        .stage_flags(vk::ShaderStageFlags::COMPUTE)
        .offset(0)
        .size(std::mem::size_of::<Patch>() as u32);
    let pipeline_layout_info = vk::PipelineLayoutCreateInfo::default()
        .set_layouts(std::slice::from_ref(&desc_layout))
        .push_constant_ranges(std::slice::from_ref(&push_constant_range));
    let pipeline_layout = unsafe { device.create_pipeline_layout(&pipeline_layout_info, None)? };

    // === Descriptor Pool & Set ===
    let pool_size = vk::DescriptorPoolSize::default()
        .ty(vk::DescriptorType::STORAGE_BUFFER)
        .descriptor_count(1);
    let pool_info = vk::DescriptorPoolCreateInfo::default()
        .max_sets(1)
        .pool_sizes(std::slice::from_ref(&pool_size));
    let desc_pool = unsafe { device.create_descriptor_pool(&pool_info, None)? };
    let alloc_info = vk::DescriptorSetAllocateInfo::default()
        .descriptor_pool(desc_pool)
        .set_layouts(std::slice::from_ref(&desc_layout));
    let desc_set = unsafe { device.allocate_descriptor_sets(&alloc_info)? }[0];

    let buffer_info = vk::DescriptorBufferInfo::default()
        .buffer(buffer)
        .offset(0)
        .range(vk::WHOLE_SIZE);
    let write = vk::WriteDescriptorSet::default()
        .dst_set(desc_set)
        .dst_binding(0)
        .descriptor_type(vk::DescriptorType::STORAGE_BUFFER)
        .buffer_info(std::slice::from_ref(&buffer_info));
    unsafe { device.update_descriptor_sets(std::slice::from_ref(&write), &[]) };

    // === Compute Pipeline ===
    let stage_info = vk::PipelineShaderStageCreateInfo::default()
        .stage(vk::ShaderStageFlags::COMPUTE)
        .module(shader_module)
        .name(c"main");
    let pipeline_info = vk::ComputePipelineCreateInfo::default()
        .stage(stage_info)
        .layout(pipeline_layout);
    let pipeline = unsafe { device.create_compute_pipelines(vk::PipelineCache::null(), std::slice::from_ref(&pipeline_info), None)? }[0];

    // === Command Buffer ===
    let cmd_pool_info = vk::CommandPoolCreateInfo::default()
        .queue_family_index(compute_queue_family)
        .flags(vk::CommandPoolCreateFlags::RESET_COMMAND_BUFFER);
    let cmd_pool = unsafe { device.create_command_pool(&cmd_pool_info, None)? };
    let cmd_alloc_info = vk::CommandBufferAllocateInfo::default()
        .command_pool(cmd_pool)
        .level(vk::CommandBufferLevel::PRIMARY)
        .command_buffer_count(1);
    let cmd_buffer = unsafe { device.allocate_command_buffers(&cmd_alloc_info)? }[0];

    // === Record Commands ===
    let begin_info = vk::CommandBufferBeginInfo::default().flags(vk::CommandBufferUsageFlags::ONE_TIME_SUBMIT);
    unsafe { device.begin_command_buffer(cmd_buffer, &begin_info)? };
    unsafe {
        device.cmd_bind_pipeline(cmd_buffer, vk::PipelineBindPoint::COMPUTE, pipeline);
        device.cmd_bind_descriptor_sets(
            cmd_buffer,
            vk::PipelineBindPoint::COMPUTE,
            pipeline_layout,
            0,
            std::slice::from_ref(&desc_set),
            &[],
        );
        let patch_bytes = unsafe {
            std::slice::from_raw_parts(
                &patch as *const Patch as *const u8,
                std::mem::size_of::<Patch>(),
            )
        };
        device.cmd_push_constants(cmd_buffer, pipeline_layout, vk::ShaderStageFlags::COMPUTE, 0, patch_bytes);
        let workgroups = (sample_count * 2 + 255) / 256;
        device.cmd_dispatch(cmd_buffer, workgroups as u32, 1, 1);
    }
    unsafe { device.end_command_buffer(cmd_buffer)? };

    // === Submit & Wait ===
    let submit_info = vk::SubmitInfo::default().command_buffers(std::slice::from_ref(&cmd_buffer));
    let fence = unsafe { device.create_fence(&vk::FenceCreateInfo::default(), None)? };
    unsafe { device.queue_submit(compute_queue, std::slice::from_ref(&submit_info), fence)? };
    unsafe { device.wait_for_fences(std::slice::from_ref(&fence), true, u64::MAX)? };

    // === Read Back Results ===
    let mapped = unsafe { device.map_memory(buffer_memory, 0, buffer_size as u64, vk::MemoryMapFlags::empty())? };
    let samples: &[f32] = unsafe { std::slice::from_raw_parts(mapped as *const f32, sample_count * 2) };

    // Convert to i16 for WAV
    let mut output = Vec::with_capacity(sample_count * 2);
    for &s in samples {
        let clamped = s.clamp(-1.0, 1.0);
        output.push((clamped * 32767.0) as i16);
    }

    // === Write WAV ===
    let header = Header::new(
        wav::bit_depth::Sixteen,
        2, // stereo
        patch.sample_rate as u32,
        sample_count as u32,
    );
    let mut file = std::fs::File::create("output.wav")?;
    header.write(&mut file, &mut output.iter().copied())?;

    println!("Generated output.wav ({} seconds, {} Hz, stereo)", patch.duration, patch.sample_rate);

    // Cleanup
    unsafe {
        device.unmap_memory(buffer_memory);
        device.destroy_fence(fence, None);
        device.free_command_buffers(cmd_pool, std::slice::from_ref(&cmd_buffer));
        device.destroy_command_pool(cmd_pool, None);
        device.destroy_pipeline(pipeline, None);
        device.destroy_pipeline_layout(pipeline_layout, None);
        device.destroy_descriptor_pool(desc_pool, None);
        device.destroy_descriptor_set_layout(desc_layout, None);
        device.destroy_buffer(buffer, None);
        device.free_memory(buffer_memory, None);
        device.destroy_shader_module(shader_module, None);
        device.destroy_device(None);
        instance.destroy_instance(None);
    }

    Ok(())
}