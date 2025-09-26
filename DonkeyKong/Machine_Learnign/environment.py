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

        self.observation_space = Box(low = -np.inf, high = np.inf, shape = (31,), dtype = np.float32)
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

        jm_pos = self.simulation.getJumpmanPosition()
        self.prev_distance = (abs(jm_pos[0] - 450),abs(jm_pos[1] - 70)) #450 is x 70 is y princess position

        self.stages = {
            "1": [1116, False],
            "2": [894, False],
            "3": [674, False],
            "4": [454, False],
            "5": [234, False]
        }
        self.ladders = [
            600, 180,
            1225, 310,
            250, 540,
            575, 520,
            1275, 760,
            750, 730,
            350, 980,
            875, 950,
            1275, 1200,
        ]

    def __get_obs(self):
        obs = self.simulation.getBarrelsPositions()
        obs.append(self.simulation.getJumpmanPosition())
        obs.append(self.ladders)
        obs.append(int(self.jumpman.ladderContact))

        return np.array(np.concatenate([np.atleast_1d(el) for el in obs]), dtype = np.float32)

    def __get_info(self):
        return {}

    def __get_reward(self):
        reward = 0
        princess_position = (450,70)
        jumpman_position = self.simulation.getJumpmanPosition()
        distance_x = abs(princess_position[0] - jumpman_position[0])
        distance_y = abs(princess_position[1] - jumpman_position[1])
        if distance_y < self.prev_distance[1] and not self.jumpman.jumping: 
            reward += 10
        if distance_y - self.prev_distance[1] > 1 and not self.jumpman.jumping and not self.jumpman.fallingAfterJump:
            reward -= 1 
        if distance_x < self.prev_distance[0]:
            reward += 0.05
        if self.simulation.getReset():
            reward -= 50
        if self.simulation.getWin():
            reward += 100

        reward += self.__reach_next_stage(jumpman_position[1])    
        self.prev_distance = (distance_x ,distance_y)

        return reward  
    
    def __reach_next_stage(self,y_pos):
        reward = 0
        for key in self.stages:
            if y_pos < self.stages[key][0] and not self.stages[key][1]:
                reward = 20
                self.stages[key][1] = True
                break

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
    #max_episode_steps = 1_000,
)


