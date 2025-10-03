import torch
import torch.optim as optim
import numpy as np
import gymnasium as gym
import os
import ale_py
import Wrappers
from  tensorboardX import SummaryWriter
import time

from Algorithms.dqn import DQN
from Config.config import Hyperparameters as Hyp
from Networks.conv import Conv
from Memories.replay_memory import ReplayMemory

device = torch.device(
    "cuda" if torch.cuda.is_available() else
    "mps" if torch.backends.mps.is_available() else
    "cpu"
)

os.makedirs("models", exist_ok=True)


if __name__ == "__main__":
    gym.register_envs(ale_py)
    env = Wrappers.make_env("ALE/MsPacman-v5")
    net = Conv(env.observation_space.shape, env.action_space.n).to(device)
    target_net = Conv(env.observation_space.shape, env.action_space.n).to(device)
    hyp = Hyp(
        MEAN_REWARD_BOUND = 2500,
        GAMMA = 0.99,
        BATCH_SIZE = 32,
        REPLAY_SIZE = 10_000,
        REPLAY_START_SIZE = 10_000,
        LEARNING_RATE = 1e-4,
        SYNC_TARGET_FRAMES = 1_000,
        EPSILON_DECAY_LAST_FRAME = 150_000,
        EPSILON_START = 1.0,
        EPSILON_FINAL = 0.01
    )
    writer = SummaryWriter(comment="Donkey Kong")
    buffer = ReplayMemory(hyp.REPLAY_SIZE)
    agent = DQN(env, buffer)
    epsilon = hyp.EPSILON_START
    optimizer = optim.Adam(net.parameters(), lr=hyp.LEARNING_RATE)
    total_rewards = []
    frame_idx = 0
    ts_frame = 0
    ts = time.time()
    best_mean_reward = None 
    print(f"device = {device}\nnetwork = {net}")

    while True:
        frame_idx += 1
        epsilon = max(hyp.EPSILON_FINAL, hyp.EPSILON_START - frame_idx / hyp.EPSILON_DECAY_LAST_FRAME)
        epsilon = max(hyp.EPSILON_FINAL, hyp.EPSILON_START - frame_idx / hyp.EPSILON_DECAY_LAST_FRAME)
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
            
            if best_mean_reward > hyp.MEAN_REWARD_BOUND:
                torch.save(net.state_dict(),"models/Best_model.dat")
                print("Solved in %d frames!" % frame_idx)
                break
        
        if len(buffer) < hyp.REPLAY_START_SIZE:
            continue

        if frame_idx % hyp.SYNC_TARGET_FRAMES == 0:
            target_net.load_state_dict(net.state_dict())

        optimizer.zero_grad()
        batch = buffer.sample(hyp.BATCH_SIZE)
        loss_t = DQN.calc_loss(batch, net, target_net, hyp.GAMMA, device)
        loss_t.backward()
        optimizer.step()