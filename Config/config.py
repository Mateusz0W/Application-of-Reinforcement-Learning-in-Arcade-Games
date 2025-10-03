from dataclasses import dataclass

@dataclass(frozen=True)
class Hyperparameters:
    MEAN_REWARD_BOUND: int
    GAMMA: float
    BATCH_SIZE: int 
    REPLAY_SIZE: int
    REPLAY_START_SIZE: int
    LEARNING_RATE: float
    SYNC_TARGET_FRAMES: int
    EPSILON_DECAY_LAST_FRAME: int
    EPSILON_START: float
    EPSILON_FINAL: float



