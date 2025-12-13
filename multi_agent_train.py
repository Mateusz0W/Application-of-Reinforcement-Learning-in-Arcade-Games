import torch
import torch.optim as optim
import numpy as np
import gymnasium as gym
import os
import ale_py
import Wrappers
import time
import sys

from Algorithms.dqn import DQN, multi_agent_play_step
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
    "Env": ["Shooter-v0"]
    }

def setup(algs: str, env, hyparams: list[Hyp], n_agents: int):

    nets = []
    target_nets = []
    dqns = []
    agents = []
    optimizers = []
    buffers = []

    for idx in range(n_agents):

        if algs[idx] in ["DQN","Double_DQN"]:
            net = Conv(env.observation_space.shape, env.action_space.n).to(device)
            target_net = Conv(env.observation_space.shape, env.action_space.n).to(device)
            dqn = DQN if algs[idx] == "DQN" else DoubleDQN
            buffer = ReplayMemory(hyparams[idx].REPLAY_SIZE)
            agent = dqn(env, buffer)
            optimizer = optim.Adam(net.parameters(), lr=hyparams[idx].LEARNING_RATE)

        elif algs[idx] in ["DuelingDQN", "NoisyDQN"]:
            Network = Dueling if algs[idx] == "DuelingDQN" else Noisy
            net = Network(env.observation_space.shape, env.action_space.n).to(device)
            target_net = Network(env.observation_space.shape, env.action_space.n).to(device)
            dqn = DQN 
            buffer = ReplayMemory(hyparams[idx].REPLAY_SIZE)
            agent = dqn(env, buffer)
            optimizer = optim.Adam(net.parameters(), lr=hyparams[idx].LEARNING_RATE)

        elif algs[idx] == "NStepDQN":
            n = sys.argv[2]
            net = Conv(env.observation_space.shape, env.action_space.n).to(device)
            target_net = Conv(env.observation_space.shape, env.action_space.n).to(device)
            dqn = DQN 
            buffer = NStepReplayMemory(hyparams[idx].REPLAY_SIZE, n)
            agent = dqn(env, buffer)
            optimizer = optim.Adam(net.parameters(), lr=hyparams[idx].LEARNING_RATE)
         
        nets.append(net)
        target_nets.append(target_net)
        dqns.append(dqn)
        agents.append(agent)
        optimizers.append(optimizer)
        buffers.append(buffer)

    return nets, target_nets, dqns, agents, optimizers, buffers

def process_batch_dqn(optimizer, buffer, dqn, batch_size, net, target_net, SYNC_TARGET_FRAMES, gamma, device, frame_idx):
        if frame_idx % SYNC_TARGET_FRAMES == 0:
            target_net.load_state_dict(net.state_dict())

        optimizer.zero_grad()
        batch = buffer.sample(batch_size)
        loss_t, mean_q = dqn.calc_loss(batch, net, target_net, gamma, device)
        loss_t.backward()
        optimizer.step()
        return loss_t.item(), mean_q



if __name__ == "__main__":
    assert len(sys.argv) >= 4, "Error Missing arguments" 

    env_name = sys.argv[1]
    algorithms = [sys.argv[2], sys.argv[3]]
    algorithm_param = sys.argv[4]
    plots = []
    n_agents = 2
    
    assert env_name in metadata["Env"], "Error: Wrong env name"
    fnames = []
    
    for idx, algorithm in enumerate(algorithms):
        assert algorithm in metadata["DQNs"], "Error: Wrong algortihm name"
        fname = f"models/{algorithm}_{idx}"
        fnames.append(fname)
        os.makedirs(fname, exist_ok=True)
        plots.append(Plotter(f"{algorithm}_{idx}")) 

    #assert algorithm == "NStepDQN" and len(sys.argv) != 4 and int(algorithm_param) < 0, "Error: Missing n argument or n must be non-negative"

 
    env = Wrappers.make_env(env_name, render_mode='human')
        #env = Wrappers.make_env(env_name)
    hyparams = [
        Hyp(
            MEAN_REWARD_BOUND = 800,
            GAMMA = 0.99 if algorithm != "NStepDQN" else 0.99 ** int(algorithm_param),
            BATCH_SIZE = 32,
            REPLAY_SIZE = 10_000,
            REPLAY_START_SIZE = 10_000,
            LEARNING_RATE = 1e-4,
            SYNC_TARGET_FRAMES = 1_000,
            EPSILON_DECAY_LAST_FRAME = 150_000,
            EPSILON_START = 1.0,
            EPSILON_FINAL = 0.01
        ),
        Hyp(
            MEAN_REWARD_BOUND = 800,
            GAMMA = 0.99 if algorithm != "NStepDQN" else 0.99 ** int(algorithm_param),
            BATCH_SIZE = 32,
            REPLAY_SIZE = 10_000,
            REPLAY_START_SIZE = 10_000,
            LEARNING_RATE = 1e-4,
            SYNC_TARGET_FRAMES = 1_000,
            EPSILON_DECAY_LAST_FRAME = 150_000,
            EPSILON_START = 1.0,
            EPSILON_FINAL = 0.01
        )]
    nets, target_nets, dqns, agents, optimizers, buffers = setup(algorithms, env, hyparams, n_agents)

    epsilons = [hyparams[0].EPSILON_START, hyparams[1].EPSILON_START]
    total_rewards = {
        "agent_1": [],
        "agent_2": []
    }
    frame_idx = 0

    ts_frame = 0
    ts = time.time()
    best_mean_rewards = [None, None] 
    print(f"device = {device}\nnetwork = {nets}")
    print(hyparams)
    start_time = time.time()
    current_ep_steps = 0
    run = True

    try:
        while run:
            current_ep_steps += 1
            frame_idx += 1
            for idx in range(n_agents):
                epsilons[idx] = max(hyparams[idx].EPSILON_FINAL, hyparams[idx].EPSILON_START - frame_idx / hyparams[idx].EPSILON_DECAY_LAST_FRAME)
            rewards = multi_agent_play_step(agents, env, nets, epsilons, device=device)
            if all(r is not None for r in rewards):
                total_rewards["agent_1"].append(rewards[0])
                total_rewards["agent_2"].append(rewards[1])
                speed = (frame_idx - ts_frame) / (time.time() - ts)
                ts_frame = frame_idx
                ts = time.time()
                hour = (ts - start_time) / 3600
                mean_rewards = [np.mean(total_rewards["agent_1"][-100:]),np.mean(total_rewards["agent_2"][-100:])]
                for idx in range(n_agents):
                    plots[idx].save_data(rewards=rewards[idx], mean_rewards=mean_rewards[idx], steps=frame_idx, episode_lengths=current_ep_steps, hours=hour, fps=speed)
                current_ep_steps = 0
                print(f"{frame_idx}: done {len(total_rewards['agent_1'])} games,[ Agent 1 ]: reward {mean_rewards[0]:.3f}, eps {epsilons[0]:.2f},[ Agent 2 ]: reward {mean_rewards[1]:.3f}, eps {epsilons[1]:.2f}, speed {speed:.2f} f/s")

                for idx, best_mean_reward in enumerate(best_mean_rewards):
                    if best_mean_reward is None or best_mean_reward < mean_rewards[idx]:
                        torch.save(nets[idx].state_dict(), f"{fnames[idx]}/{env_name[3:] if 'ALE/' in env_name else env_name}-best_{mean_rewards[idx]}_{int(time.time())}.dat")

                        if best_mean_reward is not None:
                            print(f"Best reward updated %.3f -> %.3f for Agent[{idx}]" % (best_mean_reward, mean_rewards[idx]))
                        best_mean_rewards[idx] = mean_rewards[idx]
                
                    if best_mean_rewards[idx] > hyparams[idx].MEAN_REWARD_BOUND:
                        torch.save(nets[idx].state_dict(),"models/Best_model.dat")
                        print("Solved in %d frames!" % frame_idx)
                        run = False
            
            for idx, best_mean_reward in enumerate(best_mean_rewards):
                if len(buffers[idx]) < hyparams[idx].REPLAY_START_SIZE:
                    continue

                loss_t, mean_q = process_batch_dqn(optimizers[idx], buffers[idx], dqns[idx], hyparams[idx].BATCH_SIZE, nets[idx], target_nets[idx],hyparams[idx].SYNC_TARGET_FRAMES, hyparams[idx].GAMMA, device, frame_idx)
                plots[idx].save_data(losses=loss_t, steps_loss=frame_idx, q_vals=mean_q)

    except Exception as e:
        print(f"Training interrupted: {e}")
    finally:
        total_time = (time.time() - start_time) / 3600
        print(f"total learnig time = {total_time}")
        time.sleep(0.5)
        for buffer in buffers:
            print(len(buffer))
        for plot in plots:
            plot.run()