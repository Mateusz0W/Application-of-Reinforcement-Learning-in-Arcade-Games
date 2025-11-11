import torch
import torch.optim as optim
import numpy as np
import gymnasium as gym
import os
import ale_py
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
from Networks.noisy import Noisy

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
    "Env": ["ALE/MsPacman-v5", "Shooter-v0"]
    }

def setup(alg, env, hyp: Hyp):

    if alg == "DQN" or "Double_DQN":
        net = Conv(env.observation_space.shape, env.action_space.n).to(device)
        target_net = Conv(env.observation_space.shape, env.action_space.n).to(device)
        dqn = DQN if "DQN" else DoubleDQN
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

    elif alg == "DuelingDQN" or "NoisyDQN":
        Network = Dueling if "DuelingDQN" else Noisy
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
        buffer = NStepReplayMemory(hyp.REPLAY_SIZE, n)
        agent = dqn(env, buffer)
        optimizer = optim.Adam(net.parameters(), lr=hyp.LEARNING_RATE)
        process_batch = process_batch_dqn
         
    return net, target_net, dqn, agent, optimizer, process_batch, buffer

def process_batch_dqn(optimizer, buffer, dqn, batch_size, net, target_net, gamma, device, frame_idx):
        if frame_idx % hyp.SYNC_TARGET_FRAMES == 0:
            target_net.load_state_dict(net.state_dict())

        optimizer.zero_grad()
        batch = buffer.sample(batch_size)
        loss_t = dqn.calc_loss(batch, net, target_net, gamma, device)
        loss_t.backward()
        optimizer.step()
        return loss_t.item()

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

    assert env_name in metadata["Env"], "Error: Wrong env name"
    assert algorithm in metadata["DQNs"], "Error: Wrong algortihm name"
    #assert algorithm == "NStepDQN" and len(sys.argv) != 4 and int(algorithm_param) < 0, "Error: Missing n argument or n must be non-negative"

    gym.register_envs(ale_py)
    if env_name == "ALE/MsPacman-v5":
        env = Wrappers.make_env(env_name)
    else:
        env = Wrappers.make_env(env_name, render_mode='human')
        #env = Wrappers.make_env(env_name)
    hyp = Hyp(
        MEAN_REWARD_BOUND = 1_000,
        GAMMA = 0.99 if algorithm != "NStepDQN" else 0.99 ** int(algorithm_param),
        BATCH_SIZE = 32,
        REPLAY_SIZE = 10_000,
        REPLAY_START_SIZE = 10_000,
        LEARNING_RATE = 1e-4,
        SYNC_TARGET_FRAMES = 1_000,
        EPSILON_DECAY_LAST_FRAME = 75_000, #150_000
        EPSILON_START = 1.0,
        EPSILON_FINAL = 0.01
    )
    net, target_net, dqn, agent, optimizer, process_batch, buffer = setup(algorithm, env, hyp)
    writer = SummaryWriter(comment=env_name)
    epsilon = hyp.EPSILON_START
    total_rewards = []
    frame_idx = 0
    ts_frame = 0
    ts = time.time()
    best_mean_reward = None 
    print(f"device = {device}\nnetwork = {net}")
    start_time = time.time()
    loss = []
    fps = []
    steps = []

    while True:
        frame_idx += 1
        epsilon = max(hyp.EPSILON_FINAL, hyp.EPSILON_START - frame_idx / hyp.EPSILON_DECAY_LAST_FRAME)
        reward = agent.play_step(net, epsilon, device=device)
        if reward is not None:
            total_rewards.append(reward)
            speed = (frame_idx - ts_frame) / (time.time() - ts)
            fps.append(speed)
            steps.append(frame_idx)
            ts_frame = frame_idx
            ts = time.time()
            mean_reward = np.mean(total_rewards[-100:])
            print(f"\r{frame_idx}: done {len(total_rewards)} games, reward {mean_reward:.3f}, eps {epsilon:.2f}, speed {speed:.2f} f/s", end="", flush=True)
            writer.add_scalar("epsilon", epsilon, frame_idx)
            writer.add_scalar("speed", speed, frame_idx)
            writer.add_scalar("reward_100", mean_reward, frame_idx)
            writer.add_scalar("reward", reward, frame_idx)

            if best_mean_reward is None or best_mean_reward < mean_reward:
                torch.save(net.state_dict(), f"models/{env_name}-best_{mean_reward}_{int(time.time())}.dat")

                if best_mean_reward is not None:
                    print("\nBest reward updated %.3f -> %.3f" % (best_mean_reward, mean_reward))
                best_mean_reward = mean_reward
            
            if best_mean_reward > hyp.MEAN_REWARD_BOUND:
                torch.save(net.state_dict(),"models/Best_model.dat")
                print("Solved in %d frames!" % frame_idx)
                break
        
        if len(buffer) < hyp.REPLAY_START_SIZE:
            continue

        loss_t = process_batch(optimizer, buffer, dqn, hyp.BATCH_SIZE, net, target_net, hyp.GAMMA, device, frame_idx)
        loss.append(loss_t)

    total_time = (time.time() - start_time) / 3600
    Plotter.plot(total_rewards,steps,fps,str(algorithm))
