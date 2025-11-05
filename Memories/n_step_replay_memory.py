from Memories.replay_memory import ReplayMemory
import numpy as np
from collections import namedtuple

Experience = namedtuple('Experience',
                        field_names=['state', 'action', 'reward', 'done', 'next_state'])

class NStepReplayMemory(ReplayMemory):

    def __init__(self, capacity, n):
        super().__init__(capacity)
        self.n = n

    def sample(self, batch_size, gamma):
        experiences = []

        for _ in range(batch_size):
            start_idx = np.random.randint(0, len(self.memory))
            state_0 = self.memory[start_idx].state
            action_0 = self.memory[start_idx].action
            reward = self.memory[start_idx].reward
            done = self.memory[start_idx].done
            last_idx = start_idx
            
            for idx in range(start_idx + 1, min(start_idx + self.n, len(self.memory))):
                if done:
                    break
                done = self.memory[idx].done
                last_idx = idx
                reward += (gamma ** (idx - start_idx)) * self.memory[idx].reward

            next_state = self.memory[last_idx].next_state

            experiences.append(Experience(state_0, action_0, reward, done, next_state))

        return experiences
            

