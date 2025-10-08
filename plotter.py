import matplotlib.pyplot as plt
import numpy as np

class Plotter:

    @staticmethod
    def plot(rewards, frame_idx, speed, title):
        fig, axs = plt.subplots(2, 2, figsize=(10, 8))

        episodes = list(range(1, len(rewards)+1))
        mean_rewards = [np.mean(rewards[-100:i]) for i in range(len(rewards))]
        std_rewards = [np.std(rewards[-100:i]) for i in range(len(rewards))]

        axs[0,0].plot(frame_idx, mean_rewards)
        axs[0,0].set_title("Mean rewards")

        axs[0,1].plot(frame_idx, std_rewards)
        axs[0,1].set_title("Std")

        axs[1,0].plot(frame_idx, speed)
        axs[1,0].set_title("speed")

        axs[1,1].plot(frame_idx, rewards)
        axs[1,1].set_title("rewards")

        plt.tight_layout()
        plt.savefig(f"{title}.png")
        plt.show()

