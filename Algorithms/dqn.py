import torch
from torch import nn
import numpy as np
from collections import namedtuple

Experience = namedtuple('Experience',
                        field_names=['state', 'action', 'reward', 'done', 'next_state'])

class DQN:

    def __init__(self, env, exp_buffer, n_agents=1, exp_buffers=None):
        self.env = env
        self.exp_buffer = exp_buffer
        self.n_agents = n_agents
        self.exp_buffers = exp_buffers
        self._reset()

    def _reset(self):
        self.state, _ = self.env.reset()
        self.total_reward = 0.
        self.total_rewards = [0.] * self.n_agents

    @torch.no_grad()
    def play_step(self, net, epsilon = 0., device = "cpu"):
        done_reward = None

        if np.random.random() < epsilon:
            action = self.env.action_space.sample()
        else:
            state_a = np.asarray([self.state])
            state_v = torch.tensor(state_a).to(device)
            q_vals_v = net(state_v)
            _, act_v = torch.max(q_vals_v, dim = 1)
            action = int(act_v.item())

        new_state, reward, is_done, truncated, _ = self.env.step(action)
        self.total_reward += reward
        #clipped_reward = np.clip(reward, -1, 1).astype(np.float32)

        exp = Experience(self.state, action, reward, is_done, new_state)
        self.exp_buffer.push(exp)
        self.state = new_state
        if is_done or truncated:
            done_reward = self.total_reward
            self._reset()

        return done_reward
    
    @staticmethod
    def calc_loss(batch, net, tgt_net, GAMMA, device = 'cpu'):
        states, actions, rewards, dones, next_states = zip(*batch)
        states_v = torch.tensor(np.asarray(states)).to(device)
        next_states_v = torch.tensor(np.asarray(next_states)).to(device)
        actions_v = torch.tensor(actions).to(device)
        rewards_v = torch.tensor(rewards).to(device)
        done_mask = torch.BoolTensor(dones).to(device)

        state_action_values = net(states_v).gather(1, actions_v.unsqueeze(-1)).squeeze(-1)
        next_state_values = tgt_net(next_states_v).max(1)[0]
        next_state_values[done_mask] = 0.
        next_state_values = next_state_values.detach()
        mean_q = state_action_values.mean().item()

        expected_state_action_values = next_state_values * GAMMA + rewards_v
        return nn.MSELoss()(state_action_values, expected_state_action_values), mean_q
    

@torch.no_grad()
def multi_agent_play_step(agents, env, nets, epsilons, device = "cpu"):
    done_rewards = [None] * len(agents)
    actions = []

    for idx, agent in enumerate(agents):

        if np.random.random() < epsilons[idx]:
            actions.append(env.action_space.sample())
        else:
            state_a = np.asarray([agent.state])
            state_v = torch.tensor(state_a).to(device)
            q_vals_v = nets[idx](state_v)
            _, act_v = torch.max(q_vals_v, dim = 1)
            actions.append(int(act_v.item()))

    new_state, rewards, is_done, truncated, _ = env.step(actions)
    
    for idx, agent in enumerate(agents): 
        agent.total_reward += rewards[idx]
        exp = Experience(agent.state, actions[idx], rewards[idx], is_done, new_state)
        agent.exp_buffer.push(exp)
        agent.state = new_state
    
    if is_done or truncated:
        for idx, agent in enumerate(agents): 
            done_rewards[idx] = agent.total_reward
            agent.total_reward = 0.
        
        reset_obs, _ = env.reset()
        for agent in agents:
            agent.state = reset_obs

    return done_rewards