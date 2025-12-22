import numpy as np
import torch

class NumpyReplayMemory:
    def __init__(self, capacity, state_shape, action_shape=(), device='cpu', dtype_state=np.float32):
        self.device = device
        self.capacity = int(capacity)
        self.ptr = 0
        self.size = 0

        
        self.states = np.zeros((self.capacity, *state_shape), dtype=dtype_state)
        self.next_states = np.zeros((self.capacity, *state_shape), dtype=dtype_state)
        self.actions = np.zeros((self.capacity, *action_shape), dtype=np.int64) # lub inny typ zależnie od akcji
        self.rewards = np.zeros((self.capacity,), dtype=np.float32)
        self.dones = np.zeros((self.capacity,), dtype=np.bool_) # bool zajmuje 1 bajt

    def push(self, experience):
       
        state, action, reward, done, next_state = experience

        self.states[self.ptr] = state
        self.next_states[self.ptr] = next_state
        self.actions[self.ptr] = action
        self.rewards[self.ptr] = reward
        self.dones[self.ptr] = done

        
        self.ptr = (self.ptr + 1) % self.capacity
        self.size = min(self.size + 1, self.capacity)

    def sample(self, batch_size):
        idxs = np.random.randint(0, self.size, size=batch_size)

      
        return (
            self.states[idxs],
            self.actions[idxs],
            self.rewards[idxs],
            self.dones[idxs],
            self.next_states[idxs]
        )

    def __len__(self):
        return self.size