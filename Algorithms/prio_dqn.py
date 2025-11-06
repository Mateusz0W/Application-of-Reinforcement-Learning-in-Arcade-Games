from Algorithms.dqn import DQN
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
        batch_weights_v = torch.tensor(batch_weights).to(device)

        state_action_values = net(states_v).gather(1, actions_v.unsqueeze(-1)).squeeze(-1)
        with torch.no_grad():
            next_state_values = tgt_net(next_states_v).max(1)[0]
            next_state_values[done_mask] = 0.
            exp_state_values = next_state_values.detach() * gamma + rewards_v
        loss = (state_action_values - exp_state_values) ** 2
        losses_v = batch_weights_v * loss
        return losses_v.mean(), (losses_v + 1e-5).data.cpu().numpy()

