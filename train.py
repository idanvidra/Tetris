# '''
# inspired by: https://keras.io/examples/rl/deep_q_network_breakout/

# '''

# import numpy as np
# import tensorflow as tf
# from tensorflow import keras
# from tensorflow.keras import layers

# # configuration params for the whole setup
# seed = 42
# gamma = 0.99  # discount factor for past rewards
# epsilon = 1.0  # epsilon greedy param
# epsilon_min = 0.1  # min epsilon greedy param
# epsilon_max = 1.0  # max epsilon greedy param
# epsilon_interval = (
#     epsilon_max - epsilon_min
# )  # rate at which to reduce chance of random action being taken
# batch_size = 32  # size of batch taken from replay buffer
# max_steps_per_episode = 10000

# import os
# import shutil
# from random import random, randint, sample

# import numpy as np
# import torch
# import torch.nn as nn
# from tensorboardX import SummaryWriter

# from deep_q import DeepQNetwork
# from Tetris import Tetris
# from collections import deque

# width = 10  # The common width for all images
# height = 20  # The common height for all images
# block_size = 30  # Size of a block
# batch_size = 512  # The number of images per batch
# lr = 1e-3
# gamma = 0.99
# initial_epsilon = 1.0
# final_epsilon = 1e-3
# num_decay_epochs = 2000
# num_epochs = 3000
# save_interval = 1000
# replay_memory_size = 30000  # Number of epoches between testing phases
# log_path = "tensorboard"
# saved_path = "trained_models"


# def train(opt):
#     torch.manual_seed(42)

#     if os.path.isdir(log_path):
#         shutil.rmtree(log_path)

#     os.makedirs(log_path)

#     writer = SummaryWriter(log_path)
#     env = Tetris(width=width, height=height)
#     model = DeepQNetwork()
#     optimizer = torch.optim.Adam(model.parameters, lr=lr)
#     criterion = nn.MSELoss()

#     state =
