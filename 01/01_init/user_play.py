import gymnasium as gym
import numpy as np
from gymnasium.utils.play import play

play(gym.make("FrozenLake-v1", render_mode="rgb_array", is_slippery=False), keys_to_action={
                                               "w": 3,
                                               "a": 0,
                                               "s": 1,
                                               "d": 2,
                                              })