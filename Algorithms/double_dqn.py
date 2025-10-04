from dqn import DQN
import torch
from torch import nn
import numpy as np

class DoubleDQN(DQN):
    def __init__(self, env, exp_buffer):
        super().__init__(env, exp_buffer)
    
    @staticmethod
    def calc_loss_double_dqn(batch, net, tgt_net, GAMMA, device = 'cpu'):
        states, actions, rewards, dones, next_states = zip(*batch)
        states_v = torch.tensor(np.array(states, copy = False)).to(device)
        next_states_v = torch.tensor(np.array(next_states, copy = False)).to(device)
        actions_v = torch.tensor(actions).to(device)
        rewards_v = torch.tensor(rewards).to(device)
        done_mask = torch.BoolTensor(dones).to(device)

        state_action_values = net(states_v).gather(1, actions_v.unsqueeze(-1)).squeeze(-1)
        
        next_state_actions = net(next_states_v).max(1)[1]
        next_state_actions = next_state_actions.unsqueeze(-1)
        next_state_values = tgt_net(next_states_v).gather(1, next_state_actions).squeeze(-1)
        next_state_values[done_mask] = 0.
        next_state_values = next_state_values.detach()

        expected_state_action_values = next_state_values * GAMMA + rewards_v
        return nn.MSELoss()(state_action_values, expected_state_action_values)