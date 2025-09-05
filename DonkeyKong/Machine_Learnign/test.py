import gymnasium as gym
import environment  # <- to ładuje i rejestruje env

env = gym.make("DonkeyKong-v0",render_mode='human')
obs, info = env.reset()

done = False
while True:
    action = 4
    obs, reward, done, truncated, info = env.step(action)
    print(f"Reward: {reward}")
