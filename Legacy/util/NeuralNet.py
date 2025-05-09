from typing import Tuple
import torch.nn as nn
import torch.nn.functional as F
import torch
import numpy as np


class NeuralNet(nn.Module):
    def __init__(self, input_dim: Tuple[int, ...], ouput_dim: int, hidden_dim=512):
        super().__init__()
        flat_input_dim = int(np.prod(input_dim))
        self.fc1 = nn.Linear(flat_input_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, hidden_dim)
        self.fc3 = nn.Linear(hidden_dim, hidden_dim // 2)
        self.fc4 = nn.Linear(hidden_dim // 2, ouput_dim)

        # TODO: how to init neural net?
        for layer in [self.fc1, self.fc2, self.fc3]:
            nn.init.kaiming_normal_(layer.weight, nonlinearity='relu')
            nn.init.constant_(layer.bias, 0.01)

    def forward(self, x):
        x = torch.flatten(x, start_dim=1)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))
        return self.fc4(x) # Q(s,a) info
