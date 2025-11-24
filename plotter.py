import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

class Plotter:
    def __init__(self, title: str):
        self.rewards = []
        self.mean_rewards = []
        self.steps = []
        self.episode_lengths = []
        self.losses = []
        self.hours = []
        self.fps = []
        self.steps_loss = []
        self.q_vals = []
        self.title = title
        self.fname = f"Plots/{self.title}"

    def _moving_average(data, window_size=100):
        if len(data) < window_size:
            return data
        return np.convolve(data, np.ones(window_size)/window_size, mode='valid')

    def _add_hours_to_x_axis(ax, hours: list[float]) -> None:  
        if len(hours) > 0:
            ax_time = ax.twiny()
            ax_time.set_xlim(ax.get_xlim()) 

            num_ticks = 5
            if len(hours) < num_ticks:
                return 
            
            ticks_indices = np.linspace(0, len(hours)-1, num=num_ticks).astype(int)    
            ax_time.set_xticks(ticks_indices)
            ax_time.set_xticklabels([f"{hours[t]:.1f}" for t in ticks_indices])
            ax_time.set_xlabel("Godziny")

    def _set_legends(ax, title: str, x_label: str, y_label: str) -> None:
        ax.set_title(title)
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.grid(True, alpha=0.3)
        handles, labels = ax.get_legend_handles_labels()
        if labels:
            ax.legend(loc='upper left')

    def save_data(self, **kwargs) -> None:
        for key, value in kwargs.items():
            if hasattr(self, key) and value is not None:
                    getattr(self, key).append(value)

    def _save_to_csv(self):
        data = self.__dict__
        data = {k: v for k, v in self.__dict__.items() if isinstance(v, list)}
        max_len = max(len(values) for values in data.values())

        for _, v in data.items():
            if len(v) < max_len:
                v.extend([np.nan] * (max_len - len(v)))

        df = pd.DataFrame(data)
        df.to_csv(f"{self.fname}/{self.title}.csv", index=False, sep=';')

    def _plot(self):
        os.makedirs(self.fname, exist_ok=True)

        fig_names = ["rewards", "loss", "ep_len", "ep_len_hours", "fps", "loss_steps", "mean_reward", "q_vals"]
        fig, axs = plt.subplots(4, 2, figsize=(16, 16))

        # --- 1. Rewards (per Episode) ---
        axs[0,0].plot(self.rewards, alpha=0.3, color='gray', label='Dane surowe')
        if len(self.rewards) > 0:
            ma_rewards = Plotter._moving_average(self.rewards)
            axs[0,0].plot(np.arange(len(self.rewards)-len(ma_rewards), len(self.rewards)), ma_rewards, color='blue', label='Średnia (100)')
        Plotter._set_legends(axs[0,0],"Nagorda na epizod", "Epizod", "Nagroda") 
        Plotter._add_hours_to_x_axis(axs[0,0], self.hours)

        # --- 2. Loss (per Training Step) ---
        #axs[0,1].plot(self.losses, alpha=0.3, color='red', label='Dane surowe')
        if len(self.losses) > 0:
            sampled_loss = Plotter._moving_average(self.losses, window_size=1000)
            axs[0,1].plot(np.arange(len(self.losses)-len(sampled_loss), len(self.losses)), sampled_loss, color='darkred', label=f'Średnia (1000)')
        Plotter._set_legends(axs[0,1], "Strata (Wygładzona)", "Kroki treningowe (≈ x1000)", "Nagroda")

        # --- 3. Episode Length (per Episode) ---
        if len(self.episode_lengths) > 0:
            ma_len = Plotter._moving_average(self.episode_lengths)
            axs[1,0].plot(self.episode_lengths, alpha=0.3, color='gray' ,label='Dane surowe')
            if len(ma_len) > 0:
                axs[1,0].plot(np.arange(len(self.episode_lengths)-len(ma_len), len(self.episode_lengths)), ma_len, color='darkorange',label='Średnia (100)')
        Plotter._set_legends(axs[1,0], "Długość epizodu (kroki)", "Epizod", "Kroki")
        Plotter._add_hours_to_x_axis(axs[1,0], self.hours)

        # --- 4. Episode Length vs Hours ---
        if len(self.episode_lengths) > 0:
            ma_len = Plotter._moving_average(self.episode_lengths)
            if len(ma_len) > 0:
                axs[1,1].plot(np.arange(len(self.episode_lengths)-len(ma_len), len(self.episode_lengths)), ma_len, color='limegreen',label='Średnia (100)')
        Plotter._set_legends(axs[1,1], "Średnia długości epizodu w czasie", "Godziny", "Kroki w epizodzie")
        Plotter._add_hours_to_x_axis(axs[1,0], self.hours)

        # --- 5. FPS vs Steps ---
        axs[2,0].plot(self.steps, self.fps, alpha=0.6, color='black')
        Plotter._set_legends(axs[2,0], "Prędkość treningu", "Całkowita liczba klatek (Steps)", "FPS")

        # --- 6. Loss vs Steps ---
        axs[2,1].plot(self.steps_loss, self.losses,alpha=0.6, color='olive')
        Plotter._set_legends(axs[2,1], "Strata względem kroków", "Kroki", "Strata")

        # --- 7. Mean Rewards vs Steps ---
        axs[3,0].plot(self.steps, self.mean_rewards, alpha=0.6, color='purple')
        Plotter._set_legends(axs[3,0],"Średnia nagroda (ostatnie 100)", "Kroki", "Średnia Nagroda")

        # --- 8. Q_val vs Steps ---
        axs[3,1].plot(self.steps_loss, self.q_vals, alpha=0.3, color='gray', label='Dane surowe')
        if len(self.q_vals) > 0:
            window_q = 500 
            sampled_q = Plotter._moving_average(self.q_vals, window_size=window_q)
            axs[3,1].plot(self.steps_loss[len(self.steps_loss)-len(sampled_q):], sampled_q, color='darkblue', linewidth=1.5, label=f'Średnia ({window_q})')
        Plotter._set_legends(axs[3,1], "Średnia wartość Q (Estymacja)", "Kroki", "Wartość Q")

        # --- Save ---
        plt.tight_layout()
        plt.savefig(f"{self.fname}/{self.title}.png")

        for idx, ax in enumerate(axs.flatten()):
            fig_single, ax_single = plt.subplots(figsize=(8, 6))
            for line in ax.get_lines():
                ax_single.plot(*line.get_data(), color=line.get_color(), alpha=line.get_alpha(), label=line.get_label())
            
            ax_single.set_title(ax.get_title())
            ax_single.set_xlabel(ax.get_xlabel())
            ax_single.set_ylabel(ax.get_ylabel())
            ax_single.grid(True, alpha=0.3)

            handles, labels = ax.get_legend_handles_labels()
            if labels:
                ax_single.legend()

            fig_single.tight_layout()
            fig_single.savefig(f"{self.fname}/{fig_names[idx]}.png")
            plt.close(fig_single)

        plt.show() 
        plt.close(fig)

    def run(self):
        self._plot()
        self._save_to_csv()
