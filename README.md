# Application-of-Reinforcement-Learning-in-Arcade-Games

## Project Objective
The main objective of this thesis was to design and implement an agent based on the DQN algorithm, capable of operating effectively in environments belonging to the arcade game category, such as Pong, Breakout, and Snake.

As part of the research, the impact of training parameters on learning speed, stability, and efficiency was examined. For this purpose, the Dueling DQN algorithm was used, for which the training process was conducted multiple times in the Boxing environment provided by the Gymnasium module, each time with a different hyperparameter configuration.

Subsequently, the performance of the DQN, Double DQN, N-step DQN, and Dueling DQN algorithms was compared in two different environments belonging to the Atari 2600 game family. In these experiments, the same initial parameter configuration was applied to ensure that the final results were not influenced by better or worse algorithm tuning.

An important aspect of the study was the comparison of the obtained results with other control approaches, such as manual control by a human and purely random control. Another significant part of the thesis involved the creation of a multi-agent environment from the same game category. The developed game consists of a confrontation between two bots that can hide behind obstacles and shoot at each other.

The environment was implemented using the Python programming language, and integration with the Gymnasium module was provided to standardize and facilitate the implementation of various reinforcement learning algorithms. In the conducted experiments, the Double Dueling DQN (DDDQN) algorithm was employed.

The agent’s performance was evaluated depending on the level of map complexity, specifically examining how the presence or absence of obstacles affects the effectiveness of learning to fight an opponent. The influence of two different reward system structures on the training process was also investigated.

The final experiment analyzed the effectiveness of the DDDQN algorithm in gameplay against another reinforcement learning algorithm, where the opponent was a DQN-based agent.


## Dueling DQN – Hyperparameter Study (Boxing)

### Base Configuration (Configuration 1)

The following settings were used as the initial configuration:

- Replay buffer size: 1,000,000
- Replay initial size: 50,000
- Target network synchronization interval: 10,000
- Epsilon decay frames: 5 × 10⁵
- Epsilon start: 1.0
- Epsilon final: 0.02
- Learning rate: 0.0001
- Discount factor (γ): 0.99
- Batch size: 32

---

### Configuration 2 – Reduced Replay Buffer

Compared to the base configuration, the replay buffer parameters were modified:

- Replay buffer size: **100,000**
- Replay initial size: **1,000**

All other hyperparameters remained unchanged.

---

### Configuration 3 – Faster Target Network Updates

Compared to Configuration 2, the target network synchronization interval was reduced:

- Target network synchronization interval: **1,000**

All remaining parameters were kept the same as in Configuration 2.

---

### Configuration 4 – Faster Epsilon Decay

Compared to Configuration 3, the epsilon decay duration was shortened:

- Epsilon decay frames: **1 × 10⁵**

No other hyperparameters were modified.

---

### Configuration 5 – Increased Learning Rate

Compared to Configuration 4, the learning rate was increased:

- Learning rate: **0.0003**

All remaining hyperparameters were unchanged.

---

### Result

<img width="640" height="480" alt="mean_rewards" src="https://github.com/user-attachments/assets/cf146a43-35fa-4f1d-b09a-a9102a6a6421" />


## Comparison of the effectiveness of random control , human control,  DQN, N-step DQN, Double DQN, and Dueling DQN in Pong and Boxing

### Pong

#### Random

<img width="640" height="480" alt="pong_random" src="https://github.com/user-attachments/assets/b2b29c23-f886-4903-a7b9-67fe26ab9a13" />

---

#### Human

<img width="640" height="480" alt="pong_human" src="https://github.com/user-attachments/assets/135c66ba-6eb3-4ac6-a99e-9233de62529c" />

---

#### Algorithms

<img width="640" height="480" alt="pong_mean_rewards" src="https://github.com/user-attachments/assets/47415ab4-1d25-4dc5-b390-d652f86d05ec" />

---

### Boxing

#### Random

<img width="640" height="480" alt="boxing_random" src="https://github.com/user-attachments/assets/4f800e0a-d402-4f0f-9b6c-bac839e9a944" />

---

#### Human

<img width="640" height="480" alt="boxing_human" src="https://github.com/user-attachments/assets/ea666aad-a64d-4cdf-8002-1b2d82a01cee" />

---

#### Algorithms

<img width="640" height="480" alt="boxing_mean_rewards" src="https://github.com/user-attachments/assets/6c2daee2-0534-4c84-a4b6-abefd6f2dc4c" />

---
