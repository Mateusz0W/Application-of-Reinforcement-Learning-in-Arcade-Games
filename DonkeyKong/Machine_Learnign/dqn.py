import torch
import torch.nn as nn
import torch.nn.functional as F


class DQN(nn.Module):

    def __init__(self,n_obs,n_actions,n_neurons):
        super(DQN, self).__init__()
        self.layer1 = nn.Linear(n_obs,n_neurons)
        self.layer2 = nn.Linear(n_neurons, n_neurons)
        self.layer3 = nn.Linear(n_neurons, n_actions)

    def forward(self, x):
        x = F.relu(self.layer1(x))
        x = F.relu(self.layer2(x))
        return F.relu(self.layer3(x))
    

