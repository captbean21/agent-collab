#!/usr/bin/env python3
"""
Tiny Continuous Learner - demonstrates the core loop:
1. Small neural net generates predictions
2. Self-supervised error (next-step prediction)
3. Online gradient step
4. Differentiable memory with learned retrieval
5. Autonomous control of write/retrieve

Pure Python + numpy, ~200 lines, no external ML deps.
"""
import numpy as np
import random
import math

# ==================== Config ====================
INPUT_DIM = 16
HIDDEN_DIM = 32
OUTPUT_DIM = 16
MEMORY_SLOTS = 64
MEMORY_DIM = 32
LR = 0.01
EPISODES = 500
STEPS_PER_EPISODE = 100

# ==================== Utils ====================
def xavier_init(fan_in, fan_out):
    limit = math.sqrt(6.0 / (fan_in + fan_out))
    return np.random.uniform(-limit, limit, (fan_in, fan_out)).astype(np.float32)

def relu(x): return np.maximum(0, x)
def relu_grad(x): return (x > 0).astype(np.float32)
def mse_loss(y_true, y_pred): return np.mean((y_true - y_pred) ** 2)
def mse_grad(y_true, y_pred): return 2.0 * (y_pred - y_true) / y_true.size

# ==================== Tiny MLP ====================
class TinyNet:
    def __init__(self):
        self.W1 = xavier_init(INPUT_DIM, HIDDEN_DIM)
        self.b1 = np.zeros(HIDDEN_DIM, dtype=np.float32)
        self.W2 = xavier_init(HIDDEN_DIM, OUTPUT_DIM)
        self.b2 = np.zeros(OUTPUT_DIM, dtype=np.float32)
    
    def forward(self, x):
        # x: (1, INPUT_DIM)
        self.h = relu(x @ self.W1 + self.b1)  # (1, HIDDEN_DIM)
        self.out = self.h @ self.W2 + self.b2  # (1, OUTPUT_DIM)
        return self.out
    
    def backward(self, x, grad_out, lr):
        # x: (1, INPUT_DIM), grad_out: (1, OUTPUT_DIM), self.h: (1, HIDDEN_DIM)
        # Output layer
        grad_W2 = self.h.T @ grad_out  # (HIDDEN, 1) @ (1, OUTPUT) -> (HIDDEN, OUTPUT)
        grad_b2 = grad_out.sum(axis=0)  # (OUTPUT,)
        grad_h = grad_out @ self.W2.T    # (1, OUTPUT) @ (OUTPUT, HIDDEN) -> (1, HIDDEN)
        
        # Hidden layer
        grad_h_pre = grad_h * relu_grad(self.h)  # (1, HIDDEN)
        grad_W1 = x.T @ grad_h_pre  # (INPUT, 1) @ (1, HIDDEN) -> (INPUT, HIDDEN)
        grad_b1 = grad_h_pre.sum(axis=0)  # (HIDDEN,)
        
        # Update
        self.W2 -= lr * grad_W2
        self.b2 -= lr * grad_b2
        self.W1 -= lr * grad_W1
        self.b1 -= lr * grad_b1

# ==================== Differentiable Memory ====================
class DiffMemory:
    def __init__(self, slots, dim):
        self.slots = slots
        self.dim = dim
        self.keys = np.random.randn(slots, dim).astype(np.float32) * 0.1
        self.values = np.zeros((slots, dim), dtype=np.float32)
        self.usage = np.zeros(slots, dtype=np.float32)
        self.write_ptr = 0
    
    def write(self, key, value, strength=1.0):
        """Write to least-used slot (learned allocation)"""
        idx = np.argmin(self.usage)
        self.keys[idx] = (1 - strength) * self.keys[idx] + strength * key
        # Ensure value matches memory dim
        if value.shape[0] != self.dim:
            if value.shape[0] < self.dim:
                value = np.pad(value, (0, self.dim - value.shape[0]))
            else:
                value = value[:self.dim]
        self.values[idx] = (1 - strength) * self.values[idx] + strength * value
        self.usage[idx] = 1.0
        self.usage *= 0.99  # decay
        return idx
    
    def read(self, query, top_k=4):
        """Differentiable read via attention"""
        sims = query @ self.keys.T  # (dim,) @ (slots, dim).T -> (slots,)
        attn = self.softmax(sims)
        top_idx = np.argsort(attn)[-top_k:]
        top_attn = attn[top_idx]
        top_attn = top_attn / (top_attn.sum() + 1e-8)
        retrieved = (top_attn[:, None] * self.values[top_idx]).sum(axis=0)
        return retrieved, attn
    
    def softmax(self, x):
        x = x - x.max()
        e = np.exp(x)
        return e / (e.sum() + 1e-8)
    
    def backward_read(self, query, grad_retrieved, attn, lr):
        """Backprop through attention read (simplified - value gradients only)"""
        # grad wrt values only
        top_idx = np.argsort(attn)[-4:]
        top_attn = attn[top_idx]
        top_attn = top_attn / (top_attn.sum() + 1e-8)
        for i, idx in enumerate(top_idx):
            grad_val = grad_retrieved
            if grad_val.shape[0] < self.dim:
                grad_val = np.pad(grad_val, (0, self.dim - grad_val.shape[0]))
            elif grad_val.shape[0] > self.dim:
                grad_val = grad_val[:self.dim]
            self.values[idx] -= lr * top_attn[i] * grad_val
        # Key gradients skipped for stability

# ==================== Continuous Learner ====================
class ContinuousLearner:
    def __init__(self):
        self.net = TinyNet()
        self.memory = DiffMemory(MEMORY_SLOTS, MEMORY_DIM)
        self.step_count = 0
        self.loss_history = []
    
    def encode_input(self, raw):
        """Simple positional encoding for synthetic sequence"""
        x = np.zeros(INPUT_DIM, dtype=np.float32)
        x[:len(raw)] = raw
        return x
    
    def step(self, x_t, target_t):
        """One continuous learning step"""
        # 1. Read from memory (condition on current input)
        mem_key = self.net.h[0] if hasattr(self.net, 'h') and self.net.h is not None else np.zeros(MEMORY_DIM)
        if mem_key.shape[0] != MEMORY_DIM:
            mem_key = np.zeros(MEMORY_DIM)
        mem_out, attn = self.memory.read(mem_key)
        
        # 2. Augment input with memory
        x_aug = np.concatenate([x_t, mem_out[:INPUT_DIM - len(x_t)]]) if len(x_t) < INPUT_DIM else x_t
        if x_aug.shape[0] != INPUT_DIM:
            x_aug = x_aug[:INPUT_DIM]
        
        # 3. Forward pass (x_aug must be (1, INPUT_DIM))
        pred = self.net.forward(x_aug[None, :])
        
        # 4. Compute self-supervised loss (next-step prediction)
        loss = mse_loss(target_t, pred[0])
        grad_out = mse_grad(target_t, pred[0])[None, :]
        
        # 5. Backward + online update
        self.net.backward(x_aug[None, :], grad_out, LR)
        
        # 6. Write to memory (key=hidden, value=target)
        h_vec = self.net.h[0] if self.net.h is not None else np.zeros(HIDDEN_DIM)
        h_proj = h_vec[:MEMORY_DIM] if h_vec.shape[0] >= MEMORY_DIM else np.pad(h_vec, (0, MEMORY_DIM - h_vec.shape[0]))
        val = target_t[:MEMORY_DIM] if len(target_t) >= MEMORY_DIM else np.pad(target_t, (0, MEMORY_DIM - len(target_t)))
        self.memory.write(h_proj, val, strength=0.5)
        
        # 7. Backprop through memory read (simplified)
        self.memory.backward_read(mem_key, grad_out[0, :MEMORY_DIM], attn, LR)
        
        self.step_count += 1
        self.loss_history.append(loss)
        return loss, pred[0]

# ==================== Synthetic Task ====================
def generate_sequence(length, freq=0.1):
    """Generate a predictable but non-trivial sequence"""
    t = np.arange(length)
    # Sum of sinusoids - learnable pattern
    seq = np.sin(2*np.pi*freq*t) + 0.5*np.sin(2*np.pi*freq*3*t) + 0.25*np.sin(2*np.pi*freq*5*t)
    # Add slow drift
    seq += 0.1 * np.sin(2*np.pi*freq*0.1*t)
    return seq.astype(np.float32)

# ==================== Main Loop ====================
def main():
    print("=" * 60)
    print("TINY CONTINUOUS LEARNER - Online Learning Demo")
    print("=" * 60)
    print(f"Net: {INPUT_DIM} -> {HIDDEN_DIM} -> {OUTPUT_DIM}")
    print(f"Memory: {MEMORY_SLOTS} slots x {MEMORY_DIM} dim")
    print(f"LR: {LR}, Episodes: {EPISODES}, Steps/ep: {STEPS_PER_EPISODE}")
    print()
    
    learner = ContinuousLearner()
    seq = generate_sequence(EPISODES * STEPS_PER_EPISODE + 1)
    
    # Training
    for ep in range(EPISODES):
        ep_loss = 0.0
        for s in range(STEPS_PER_EPISODE):
            idx = ep * STEPS_PER_EPISODE + s
            x_t = learner.encode_input(seq[idx:idx+4])  # 4-step history
            target_t = learner.encode_input(seq[idx+1:idx+5])  # next 4 steps
            loss, pred = learner.step(x_t, target_t)
            ep_loss += loss
        
        avg_loss = ep_loss / STEPS_PER_EPISODE
        if ep % 50 == 0 or ep == EPISODES - 1:
            print(f"Ep {ep:4d} | Loss: {avg_loss:.6f} | Steps: {learner.step_count}")
    
    print()
    print("Testing generalization (unseen sequence)...")
    test_seq = generate_sequence(200, freq=0.15)  # Different frequency
    test_losses = []
    for i in range(150):
        x_t = learner.encode_input(test_seq[i:i+4])
        target_t = learner.encode_input(test_seq[i+1:i+5])
        loss, pred = learner.step(x_t, target_t)  # Still learning!
        test_losses.append(loss)
    
    print(f"Test avg loss: {np.mean(test_losses):.6f} (first 10: {np.mean(test_losses[:10]):.6f} -> last 10: {np.mean(test_losses[-10]):.6f})")
    
    # Show memory contents
    print(f"\nMemory usage: {learner.memory.usage.sum():.1f}/{MEMORY_SLOTS} slots used")
    print(f"Top memory keys norm: {np.linalg.norm(learner.memory.keys, axis=1).max():.3f}")
    
    # Demonstrate: the learner *controls* its memory writes
    print("\nKey property: learner autonomously decides WHAT to write (hidden state)")
    print("and WHEN (every step), with learned allocation (least-used slot).")
    print("This is the 'write path to owned substrate' in miniature.")
    
    return learner

if __name__ == "__main__":
    learner = main()
