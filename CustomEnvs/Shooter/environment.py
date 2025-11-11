import gymnasium as gym
from gymnasium.spaces import Box, Discrete
from CustomEnvs.Shooter.simulation import Simulation
import numpy as np
from CustomEnvs.Shooter.config import Direction

class ShooterEnv(gym.Env):
    metadata = {"render_modes": ["human"]} 

    def __init__(self, render_mode = None):
        super().__init__()

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode
        self.simulation = Simulation(render= True if self.render_mode == "human" else False)

        self.observation_space = Box(
            low=0,
            high=255,
            shape=(250, 160, 3),
            dtype=np.uint8
        )

        self.action_space = Discrete(16)

    def _map_action(self, action: int) -> Direction|int:
        match action:
            case 12:
                return Direction.DOWN
            case 13:
                return Direction.UP
            case 14:
                return Direction.LEFT
            case 15: 
                return Direction.RIGHT
            case _:
                return action * 30
            
    def _get_obs(self) -> tuple:
        return self.simulation.image
    
    def _get_info(self) -> tuple:
        return {}
    
    def _get_reward(self) -> int:
        reward = 0
        player = self.simulation.players[1]
        enemy = self.simulation.players[0]

        reward += 10 * enemy.bullet_hits
        reward -= 10 * player.bullet_hits
        reward -= 50 * player.own_bullet_hits
        if player.health <= 0:
            reward -= 100
        if enemy.health <= 0:
            reward += 100
        
        #reward -= 0.01
    
        return reward
    
    def reset(self, seed: int|None =None, options: dict|None =None) -> tuple:
        super().reset(seed=seed)

        self.simulation.restart_game()
        observation = self._get_obs()
        info = self._get_info()
        return observation, info
    
    def step(self, action: int) -> tuple:

        action = self._map_action(action)
        self.simulation.run(action)
        terminated = self.simulation.game_over
        observation = self._get_obs()
        info = self._get_info()
        truncated = False
        reward = self._get_reward()
        
        return observation, reward, terminated, truncated, info
    

gym.register(
    id = 'Shooter-v0',
    entry_point = 'CustomEnvs.Shooter.environment:ShooterEnv',
    #max_episode_steps = 1_000,
)



