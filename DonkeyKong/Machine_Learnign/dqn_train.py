import gymnasium as gym
import environment
from dqn import DQN
from collections import namedtuple, deque
import torch
import numpy as np
import torch.nn as nn
from  tensorboardX import SummaryWriter
import torch
import torch.optim as optim
import time
import os
import random

MEAN_REWARD_BOUND = 200.
GAMMA = 0.99
BATCH_SIZE = 32
REPLAY_SIZE = 10_000
REPLAY_START_SIZE = 10_000
LEARNING_RATE = 1e-4
SYNC_TARGET_FRAMES = 1_000
EPSILON_DECAY_LAST_FRAME = 150_000
EPSILON_START = 1.0
EPSILON_FINAL = 0.01

device = torch.device(
    "cuda" if torch.cuda.is_available() else
    "mps" if torch.backends.mps.is_available() else
    "cpu"
)

os.makedirs("models", exist_ok=True)

Experience = namedtuple('Experience',
                        field_names=['state', 'action', 'reward', 'done', 'next_state'])

class ReplayMemory:

    def __init__(self, capacity):
        self.memory = deque([], maxlen=capacity)
    
    def push(self, experience):
        self.memory.append(experience)

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)
    
    def __len__(self):
        return len(self.memory)
    
class Agent:

    def __init__(self, env, exp_buffer):
        self.env = env
        self.exp_buffer = exp_buffer
        self._reset()

    def _reset(self):
        self.state, _ = self.env.reset()
        self.total_reward = 0.

    @torch.no_grad()
    def play_step(self, net, epsilon = 0., device = "cpu"):
        done_reward = None

        if np.random.random() < epsilon:
            action = self.env.action_space.sample()
        else:
            state_a = np.array([self.state], copy = False)
            state_v = torch.tensor(state_a).to(device)
            q_vals_v = net(state_v)
            _, act_v = torch.max(q_vals_v, dim = 1)
            action = int(act_v.item())

        new_state, reward, is_done, _, _ = self.env.step(action)
        self.total_reward += reward

        exp = Experience(self.state, action, reward, is_done, new_state)
        self.exp_buffer.push(exp)
        self.state = new_state
        if is_done:
            done_reward = self.total_reward
            self._reset()

        return done_reward

def calc_loss(batch, net, tgt_net, device = 'cpu'):
    states, actions, rewards, dones, next_states = zip(*batch)
    states_v = torch.tensor(np.array(states, copy = False)).to(device)
    next_states_v = torch.tensor(np.array(next_states, copy = False)).to(device)
    actions_v = torch.tensor(actions).to(device)
    rewards_v = torch.tensor(rewards).to(device)
    done_mask = torch.BoolTensor(dones).to(device)

    state_action_values = net(states_v).gather(1, actions_v.unsqueeze(-1)).squeeze(-1)
    next_state_values = tgt_net(next_states_v).max(1)[0]
    next_state_values[done_mask] = 0.
    next_state_values = next_state_values.detach()

    expected_state_action_values = next_state_values * GAMMA + rewards_v
    return nn.MSELoss()(state_action_values, expected_state_action_values)
    

if __name__ == "__main__":
    env = gym.make("DonkeyKong-v0")
    net = DQN(env.observation_space.shape[0], env.action_space.n, 100).to(device)
    target_net = DQN(env.observation_space.shape[0], env.action_space.n, 100).to(device)

    writer = SummaryWriter(comment="Donkey Kong")
    buffer = ReplayMemory(REPLAY_SIZE)
    agent = Agent(env, buffer)
    epsilon = EPSILON_START
    optimizer = optim.Adam(net.parameters(), lr=LEARNING_RATE)
    total_rewards = []
    frame_idx = 0
    ts_frame = 0
    ts = time.time()
    best_mean_reward = None 
    print(f"device = {device}\nnetwork = {net}")

    while True:
        frame_idx += 1
        epsilon = max(EPSILON_FINAL, EPSILON_START - frame_idx / EPSILON_DECAY_LAST_FRAME)
        reward = agent.play_step(net, epsilon, device=device)
        if reward is not None:
            total_rewards.append(reward)
            speed = (frame_idx - ts_frame) / (time.time() - ts)
            ts_frame = frame_idx
            ts = time.time()
            mean_reward = np.mean(total_rewards[-100:])
            print(f"\r{frame_idx}: done {len(total_rewards)} games, reward {mean_reward:.3f}, eps {epsilon:.2f}, speed {speed:.2f} f/s", end="", flush=True)
            writer.add_scalar("epsilon", epsilon, frame_idx)
            writer.add_scalar("speed", speed, frame_idx)
            writer.add_scalar("reward_100", mean_reward, frame_idx)
            writer.add_scalar("reward", reward, frame_idx)

            if best_mean_reward is None or best_mean_reward < mean_reward:
                torch.save(net.state_dict(), f"models/Donkey-Kong-best_{mean_reward}_{int(time.time())}.dat")

                if best_mean_reward is not None:
                    print("\nBest reward updated %.3f -> %.3f" % (best_mean_reward, mean_reward))
                best_mean_reward = mean_reward
            
            if best_mean_reward > MEAN_REWARD_BOUND:
                torch.save(net.state_dict(),"models/Best_model.dat")
                print("Solved in %d frames!" % frame_idx)
                break
        
        if len(buffer) < REPLAY_START_SIZE:
            continue

        if frame_idx % SYNC_TARGET_FRAMES == 0:
            target_net.load_state_dict(net.state_dict())

        optimizer.zero_grad()
        batch = buffer.sample(BATCH_SIZE)
        loss_t = calc_loss(batch, net, target_net, device)
        loss_t.backward()
        optimizer.step()
        
        



            


    
        

