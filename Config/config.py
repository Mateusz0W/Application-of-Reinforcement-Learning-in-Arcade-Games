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

    def __str__(self):
        return f"Hyperparameters:\n\
        Mean reward bound = {self.MEAN_REWARD_BOUND}\n\
        Gamma = {self.GAMMA}\n\
        Batch size = {self.BATCH_SIZE}\n\
        Replay size = {self.REPLAY_SIZE}\n\
        Replay start size = {self.REPLAY_START_SIZE}\n\
        Learning rate = {self.LEARNING_RATE}\n\
        Sync target frames = {self.SYNC_TARGET_FRAMES}\n\
        Epsilon decay last frame = {self.EPSILON_DECAY_LAST_FRAME}\n\
        Epsilon start = {self.EPSILON_START}\n\
        Epsilon final = {self.EPSILON_FINAL}\n\
        "