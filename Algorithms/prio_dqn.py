from dqn import DQN
import torch
import numpy as np

class PrioDQN(DQN):

    def __init__(self, env, exp_buffer):
        super().__init__(env, exp_buffer)

    @staticmethod
    def calc_loss(batch, batch_weights, net, tgt_net, gamma, device = 'cpu'):
        states, actions, rewards, dones, next_states = zip(*batch)
        states_v = torch.tensor(np.asarray(states)).to(device)
        next_states_v = torch.tensor(np.asarray(next_states)).to(device)
        actions_v = torch.tensor(actions).to(device)
        rewards_v = torch.tensor(rewards).to(device)
        done_mask = torch.BoolTensor(dones).to(device)