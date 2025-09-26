import gymnasium as gym
import environment  # <- to ładuje i rejestruje env

env = gym.make("DonkeyKong-v0",render_mode='human')
obs, info = env.reset()

done = False
r = 0
while True:
    action = env.action_space.sample()
    obs, reward, done, truncated, info = env.step(action)
    r += reward
    print(f"Reward: {r}")
