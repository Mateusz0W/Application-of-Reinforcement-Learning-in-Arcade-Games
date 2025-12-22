import torch
import torch.optim as optim
import numpy as np
import gymnasium as gym
import os
#import ale_py
import Wrappers
from  tensorboardX import SummaryWriter
import time
import sys

from Algorithms.dqn import DQN
from Algorithms.double_dqn import DoubleDQN
from Algorithms.prio_dqn import PrioDQN

from Config.config import Hyperparameters as Hyp

from Networks.conv import Conv
from Networks.dueling import Dueling
from Networks.noisy import NoisyDQN

from Memories.replay_memory import ReplayMemory
from Memories.prio_replay_memory import PrioReplayMemory
from Memories.n_step_replay_memory import NStepReplayMemory

from plotter import Plotter

import CustomEnvs.Shooter.environment 

device = torch.device(
    "cuda" if torch.cuda.is_available() else
    "mps" if torch.backends.mps.is_available() else
    "cpu"
)

os.makedirs("models", exist_ok=True)

metadata = {
    "DQNs": ["DQN", "Double_DQN", "PrioDQN", "DuelingDQN", "NoisyDQN", "NStepDQN"],
    "Env": ["BoxingNoFrameskip-v4", "PongNoFrameskip-v4"]
    }

def setup(alg, env, hyp: Hyp):

    if alg in ["DQN", "Double_DQN"]:
        net = Conv(env.observation_space.shape, env.action_space.n).to(device)
        target_net = Conv(env.observation_space.shape, env.action_space.n).to(device)
        dqn = DQN if alg == "DQN" else DoubleDQN
        buffer = ReplayMemory(hyp.REPLAY_SIZE)
        agent = dqn(env, buffer)
        optimizer = optim.Adam(net.parameters(), lr=hyp.LEARNING_RATE)
        process_batch = process_batch_dqn

    elif alg == "PrioDQN":
        net = Conv(env.observation_space.shape, env.action_space.n).to(device)
        target_net = Conv(env.observation_space.shape, env.action_space.n).to(device)
        dqn = PrioDQN
        buffer = PrioReplayMemory(hyp.REPLAY_SIZE)
        agent = dqn(env, buffer)
        optimizer = optim.Adam(net.parameters(), lr=hyp.LEARNING_RATE)
        process_batch = process_batch_prio_dqn

    elif alg in ["DuelingDQN", "NoisyDQN"]:
        Network = Dueling if alg == "DuelingDQN" else NoisyDQN
        net = Network(env.observation_space.shape, env.action_space.n).to(device)
        target_net = Network(env.observation_space.shape, env.action_space.n).to(device)
        dqn = DQN 
        buffer = ReplayMemory(hyp.REPLAY_SIZE)
        agent = dqn(env, buffer)
        optimizer = optim.Adam(net.parameters(), lr=hyp.LEARNING_RATE)
        process_batch = process_batch_dqn

    elif alg == "NStepDQN":
        n = sys.argv[2]
        net = Conv(env.observation_space.shape, env.action_space.n).to(device)
        target_net = Conv(env.observation_space.shape, env.action_space.n).to(device)
        dqn = DQN 
        buffer = NStepReplayMemory(hyp.REPLAY_SIZE, n, hyp.GAMMA)
        agent = dqn(env, buffer)
        optimizer = optim.Adam(net.parameters(), lr=hyp.LEARNING_RATE)
        process_batch = process_batch_dqn
         
    return net, target_net, dqn, agent, optimizer, process_batch, buffer

def process_batch_dqn(optimizer, buffer, dqn, batch_size, net, target_net, gamma, device, frame_idx):
        if frame_idx % hyp.SYNC_TARGET_FRAMES == 0:
            target_net.load_state_dict(net.state_dict())

        optimizer.zero_grad()
        batch = buffer.sample(batch_size)
        loss_t, mean_q = dqn.calc_loss(batch, net, target_net, gamma, device)
        loss_t.backward()
        optimizer.step()
        return loss_t.item(), mean_q

def process_batch_prio_dqn(optimizer, buffer, dqn, batch_size, net, target_net, gamma, device, frame_idx):
    batch, batch_indices, batch_weights = buffer.sample(batch_size)
    optimizer.zero_grad()
    loss_v, sample_prios = dqn.calc_loss(batch, batch_weights, net, target_net, gamma, device)
    loss_v.backward()
    optimizer.step()
    buffer.update_priorities(batch_indices, sample_prios)

    if frame_idx % hyp.SYNC_TARGET_FRAMES == 0:
            target_net.load_state_dict(net.state_dict())
    
    buffer.update_beta(frame_idx)
    
    return loss_v


if __name__ == "__main__":
    assert len(sys.argv) >= 3, "Error Missing arguments" 

    env_name = sys.argv[1]
    algorithm = sys.argv[2]
    algorithm_param = sys.argv[3]
    fname = f"models/{algorithm}"
    os.makedirs(fname, exist_ok=True)
    plot = Plotter(algorithm) 

    assert env_name in metadata["Env"], "Error: Wrong env name"
    assert algorithm in metadata["DQNs"], "Error: Wrong algortihm name"
    #assert algorithm == "NStepDQN" and len(sys.argv) != 4 and int(algorithm_param) < 0, "Error: Missing n argument or n must be non-negative"

    #gym.register_envs(ale_py)
    env = Wrappers.make_env(env_name)

    hyp = Hyp(
        MEAN_REWARD_BOUND = 2500,
        GAMMA = 0.99,
        BATCH_SIZE = 32,
        REPLAY_SIZE = 10_000,
        REPLAY_START_SIZE = 10_000,
        LEARNING_RATE = 1e-4,
        SYNC_TARGET_FRAMES = 1_000,
        EPSILON_DECAY_LAST_FRAME = 150_000,
        EPSILON_START = 0.0,
        EPSILON_FINAL = 0.0
    )
    net, target_net, dqn, agent, optimizer, process_batch, buffer = setup(algorithm, env, hyp)
    writer = SummaryWriter(comment=env_name)
    epsilon = hyp.EPSILON_START
    total_rewards = []
    frame_idx = 0
    ts_frame = 0
    ts = time.time()
    best_mean_reward = None 
    print(f"alg = {dqn}\ndevice = {device}\nnetwork = {net}")
    print(hyp)
    start_time = time.time()
    current_ep_steps = 0

    while True:
        current_ep_steps += 1
        frame_idx += 1
        epsilon = max(hyp.EPSILON_FINAL, hyp.EPSILON_START - frame_idx / hyp.EPSILON_DECAY_LAST_FRAME)
        reward = agent.play_step(net, epsilon, device=device)
        if reward is not None:
            total_rewards.append(reward)
            speed = (frame_idx - ts_frame) / (time.time() - ts)
            ts_frame = frame_idx
            ts = time.time()
            hour = (ts - start_time) / 3600
            mean_reward = np.mean(total_rewards[-100:])
            plot.save_data(rewards=reward, mean_rewards=mean_reward, steps=frame_idx, episode_lengths=current_ep_steps, hours=hour, fps=speed)
            current_ep_steps = 0
            print(f"\r{frame_idx}: done {len(total_rewards)} games, reward {mean_reward:.3f}, eps {epsilon:.2f}, speed {speed:.2f} f/s", end="", flush=True)
            writer.add_scalar("epsilon", epsilon, frame_idx)
            writer.add_scalar("speed", speed, frame_idx)
            writer.add_scalar("reward_100", mean_reward, frame_idx)
            writer.add_scalar("reward", reward, frame_idx)

            if best_mean_reward is None or best_mean_reward < mean_reward:
                torch.save(net.state_dict(), f"{fname}/{env_name[3:] if 'ALE/' in env_name else env_name}-best_{mean_reward}_{int(time.time())}.dat")

                if best_mean_reward is not None:
                    print("\nBest reward updated %.3f -> %.3f" % (best_mean_reward, mean_reward))
                best_mean_reward = mean_reward
            
            if best_mean_reward > hyp.MEAN_REWARD_BOUND:
                torch.save(net.state_dict(),"models/Best_model.dat")
                print("Solved in %d frames!" % frame_idx)
                break
        
        if len(buffer) < hyp.REPLAY_START_SIZE:
            continue

        loss_t, mean_q = process_batch(optimizer, buffer, dqn, hyp.BATCH_SIZE, net, target_net, hyp.GAMMA, device, frame_idx)
        plot.save_data(losses=loss_t, steps_loss=frame_idx, q_vals=mean_q)

    total_time = (time.time() - start_time) / 3600
    writer.close()
    print(f"total learnig time = {total_time}")
    plot.run()