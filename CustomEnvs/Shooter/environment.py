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
        self.n_agents = 2

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
    
    def _get_rewards(self) -> list[int]:
        rewards = [0] * self.n_agents
        for idx in range(self.n_agents):
            player = self.simulation.players[idx]
            enemy = self.simulation.players[int(not idx)]

            rewards[idx] += 1 * enemy.bullet_hits
            rewards[idx] -= 1 * player.bullet_hits
            #rewards[idx] -= 1 * player.own_bullet_hits
            if player.health <= 0:
                rewards[idx] -= 1
            if enemy.health <= 0:
                rewards[idx] += 1

            rewards[idx] -= 0.1 *player.missed_shots
            
        return rewards
    
    def reset(self, seed: int|None =None, options: dict|None =None) -> tuple:
        super().reset(seed=seed)
        self.simulation.game_over = True
        self.simulation.restart_game()
        observation = self._get_obs()
        info = self._get_info()
        return observation, info
    
    def step(self, actions: list[int]) -> tuple:

        actions = [self._map_action(action) for action in actions]
        self.simulation.run(actions)
        terminated = self.simulation.game_over
        observation = self._get_obs()
        info = self._get_info()
        truncated = False
        rewards = self._get_rewards()
        
        return observation, rewards, terminated, truncated, info
    

gym.register(
    id = 'Shooter-v0',
    entry_point = 'CustomEnvs.Shooter.environment:ShooterEnv',
    max_episode_steps = 4_000,
)



