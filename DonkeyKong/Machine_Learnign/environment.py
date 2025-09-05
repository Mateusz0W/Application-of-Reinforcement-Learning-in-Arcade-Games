import gymnasium as gym
from gymnasium.spaces import Discrete, Box
import sys
import os
import numpy as np

sys.path.append(os.path.join('..', 'Game'))
import build.Debug.DonkeyKongPy as DK

class DonkeyKongEnv(gym.Env):
    metadata={"render_modes": ["human"]}

    def __init__(self, render_mode=None):

        self.jumpman = DK.Jumpman()
        self.simulation = DK.Simulation(self.jumpman,1700,1500,False)
        self.simulation.loadMapFromJson("../Game/map.json")
        self.renderer = DK.Renderer(self.simulation,1700,1500)

        self.observation_space = Box(low = -np.inf, high = np.inf, shape = (12,), dtype = np.float32)
        self.action_space = Discrete(5)

        self.action_to_direction = {
            0: "Left",
            1: "Right",
            2: "Up",
            3: "Down",
            4: "Jump",
        }

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

        self.prev_distance = self.simulation.getJumpmanPosition()[1] - 70 # 70 is priness y position

    def __get_obs(self):
        obs = self.simulation.getBarrelsPositions()
        obs.append(self.simulation.getJumpmanPosition())

        return np.array([el for elements in obs for el in elements], dtype = np.float32)

    def __get_info(self):
        return {}

    def __get_reward(self):
        reward = 0
        princess_position = (450,70)
        jumpman_position = self.simulation.getJumpmanPosition()
        distance = princess_position[1] - jumpman_position[1]
        if distance < self.prev_distance: 
            reward += 1
        if self.simulation.getReset():
            reward -= 50
        if self.simulation.getWin():
            reward += 100

        self.prev_distance = distance

        return reward  

    def reset(self, seed: int | None = None, options: dict | None = None):
        super().reset(seed=seed)

        self.simulation.restart()
        observation = self.__get_obs()
        info = self.__get_info()

        return observation, info
    
    def step(self, action):

        direction = self.action_to_direction[action]
        self.simulation.action = direction
        terminated = bool(self.simulation.run())
        reward = self.__get_reward()
        observation = self.__get_obs()
        info = self.__get_info()
        truncated = False

        if self.render_mode == 'human':
            self.renderer.run()

        return observation, reward, terminated, truncated, info
           

gym.register(
    id = 'DonkeyKong-v0',
    entry_point = 'environment:DonkeyKongEnv',
    max_episode_steps = 1_000,
)


