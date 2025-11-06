import numpy as np

BETA_START = 0.4
BETA_FRAMES = 100000

class PrioReplayMemory:
    def __init__(self, buf_size, prob_alpha=0.6):
        self.prob_alpha = prob_alpha
        self.capacity = buf_size
        self.pos = 0
        self.buffer = []
        self.priorities = np.zeros((buf_size,), dtype=np.float32)
        self.beta = BETA_START

    def update_beta(self, idx):
        self.beta =  min(1. , BETA_START + idx * (1.0 - BETA_START) / BETA_FRAMES)
        return self.beta
    
    def __len__(self):
        return len(self.buffer)

    def push(self, experience):
        max_prio = self.priorities.max() if self.buffer else 1.

        if len(self.buffer) < self.capacity:
            self.buffer.append(experience)
        else:
            self.buffer[self.pos] = experience
        self.priorities[self.pos] = max_prio
        self.pos = (self.pos + 1) % self.capacity

    def sample(self, batch_size):
        if len(self.buffer) == self.capacity:
            prios = self.priorities
        else:
            prios = self.priorities[:self.pos]
        probs = prios ** self.prob_alpha
        probs /= probs.sum()

        indices = np.random.choice(len(self.buffer),
                                   batch_size, p=probs)
        samples = [self.buffer[idx] for idx in indices]
        total = len(self.buffer)
        weights = (total * probs[indices]) ** (-self.beta)
        weights /= weights.max()
        return samples, indices, np.array(weights, dtype=np.float32)
    
    def update_priorities(self, batch_indices,batch_priorities):
        for idx, prio in zip(batch_indices, batch_priorities):
            self.priorities[idx] = prio