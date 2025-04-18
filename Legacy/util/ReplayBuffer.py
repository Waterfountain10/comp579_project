from typing import Dict, Tuple
import numpy as np


class ReplayBuffer:
    def __init__(self, obs_shape: Tuple[int, ...], size: int, batch_size: int = 32):
        obs_buffer_shape = [size] + list(obs_shape)
        self.obs_dim = obs_shape
        self.state_buf = np.zeros(obs_buffer_shape, dtype=np.float64)
        self.next_state_buf = np.zeros(obs_buffer_shape, dtype=np.float64)
        self.acts_buf = np.zeros(size, dtype=np.int64)
        self.rewards_buf = np.zeros(size, dtype=np.float64)
        self.done_buf = np.zeros(size)
        self.max_size = size
        self.batch_size = batch_size
        self.curr_ind = 0
        self.size = 0

    def store(
        self,
        state: np.ndarray,
        action: int,
        reward: float,
        next_state: np.ndarray,
        done: bool,
    ) -> bool | None:
        self.state_buf[self.curr_ind] = state
        self.next_state_buf[self.curr_ind] = next_state
        self.acts_buf[self.curr_ind] = action
        self.rewards_buf[self.curr_ind] = reward
        self.done_buf[self.curr_ind] = done

        self.curr_ind = (
            (self.curr_ind + 1) % self.max_size
        )  # if at end, go back to start and replace the oldest experiences
        self.size = min(
            self.size + 1, self.max_size
        )  # buffer size increase (capped at max_size) -> replace oldest back in start

    def sample_batch(self) -> Dict[str, np.ndarray]:
        """
        returns:
            dict with keys: (obs, next_obs, acts, rews, done)
        """
        if (
            self.size < self.batch_size
        ):  # buffer is not yet filled, sample with replacement
            idxs = np.random.choice(self.size, size=self.batch_size, replace=True)
        else:
            idxs = np.random.choice(self.size, size=self.batch_size, replace=False)

        return {
            "obs": self.state_buf[idxs],
            "next_obs": self.next_state_buf[idxs],
            "acts": self.acts_buf[idxs],
            "rews": self.rewards_buf[idxs],
            "done": self.done_buf[idxs],
        }

    def __len__(self) -> int:
        return min(self.size, self.max_size)
