import torch
from torch import nn
import numpy as np
from collections import namedtuple

Experience = namedtuple('Experience',
                        field_names=['state', 'action', 'reward', 'done', 'next_state'])

class DQN:

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
    
    @staticmethod
    def calc_loss(batch, net, tgt_net, GAMMA, device = 'cpu'):
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