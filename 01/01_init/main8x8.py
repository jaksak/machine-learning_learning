import random

import gymnasium as gym
import matplotlib.pyplot as plt
import numpy as np
map_name = '8x8'
environment = gym.make("FrozenLake-v1", is_slippery=True, map_name=map_name, render_mode=None)
environment.reset()

# We re-initialize the Q-table
qtable = np.zeros((environment.observation_space.n, environment.action_space.n))

# jakub: zmiana w api? brak nagrody na polu koncowym?
# qtable[15] = np.array([1, 1, 1, 1])

# Hyperparameters
episodes = 100000  # Total number of episodes
alpha = 0.5  # Learning rate
gamma = 0.9  # Discount factor
epsilon = 1.0  # Amount of randomness in the action selection
epsilon_decay = 0.00001  # Fixed amount to decrease
show_training_charts = False
nrows = 8

# List of outcomes to plot
outcomes = []


# historia przejsc

# print('Q-table before training:')
# print(qtable)
def print_qtable(qtable):
    for index in range(len(qtable)):
        value = qtable[index] * 100
        with np.printoptions(formatter={'float': '{: 7.2f}'.format}):
            if ((index - (nrows - 1)) % nrows) == 0:
                print(value)
            else:
                print(value, end=' ')
    print()

def print_qtable_argmax(qtable):
    for index in range(len(qtable)):
        value = np.argmax(qtable[index])
        tmp0 = np.array([0] * 4)
        if np.array_equal(qtable[index], tmp0):
            value = 'X'
        elif value == 0:
            value = 'L'
        elif value == 1:
            value = 'D'
        elif value == 2:
            value = 'R'
        else:
            value = 'U'
        if ((index - (nrows - 1)) % nrows) == 0:
            print(value)
        else:
            print(value, end=' ')
    print()

def disable_impossible_actions(current_state, prob):
    prob = np.copy(prob)
    x = current_state % nrows
    y = current_state // nrows
    if y == 0:
        prob[3] = -100
    if x == 0:
        prob[0] = -100
    if y == nrows - 1:
        prob[1] = -100
    if x == nrows - 1:
        prob[2] = -100
    prob[random.randint(0, len(prob) - 1)] = -100
    return prob

# Training
for i in range(episodes):
    state = environment.reset()[0]
    done = False
    truncated = False

    # By default, we consider our outcome to be a failure
    outcomes.append("Failure")

    visitedPath = []

    # Until the agent gets stuck in a hole or reaches the goal, keep training it
    while not done and not truncated:
        # Generate a random number between 0 and 1
        rnd = np.random.random()

        # If random number < epsilon, take a random action
        if rnd < epsilon:
            # eskploracja
            action = environment.action_space.sample()
        # Else, take the action with the highest value in the current state
        else:
            # eksploatacja
            action = np.argmax(qtable[state])

        # Implement this action and move the agent in the desired direction
        new_state, reward, done, truncated, info = environment.step(action)
        visitedPath.append(state)

        if done and reward == 0:
            reward = -5
        elif new_state == state:
            reward = -1
            truncated = True
        elif new_state in visitedPath:
            reward = 0
        elif reward == 0:
            reward = 0.0
        elif reward == 1:
            reward = 500

        # Update Q(s,a)
        qtable[state, action] = qtable[state, action] + \
                                alpha * (reward + gamma * np.max(qtable[new_state]) - qtable[state, action])

        # Update our current state
        state = new_state

        # If we have a reward, it means that our outcome is a success
        if reward:
            outcomes[-1] = "Success"

    # Update epsilon
    epsilon = max(epsilon - epsilon_decay, 0)

print()
print('===========================================')
print('Q-table after training:')
print_qtable(qtable)
print_qtable_argmax(qtable)

if show_training_charts:
    fig = plt.figure(figsize=(12, 5))
    plt.xlabel("Run number")
    plt.ylabel("Outcome")
    ax = plt.gca()
    ax.set_facecolor('#efeeea')
    plt.bar(range(len(outcomes)), outcomes, color="#0A047A", width=1.0)
    plt.show()

episodes = 1000
nb_success = 0

environment.close()
environment = gym.make("FrozenLake-v1", is_slippery=True, map_name=map_name, render_mode=None)
# environment = gym.make("FrozenLake-v1", is_slippery=True, map_name=map_name, render_mode='human')
# environment = gym.wrappers.TimeLimit(environment, max_episode_steps=30)

# Evaluation
for _ in range(episodes):

    state = environment.reset()[0]
    done = False
    truncated = False

    # Until the agent gets stuck or reaches the goal, keep training it
    while not done and not truncated:
        # Choose the action with the highest value in the current state
        action = np.argmax(qtable[state])

        # Implement this action and move the agent in the desired direction
        new_state, reward, done, truncated, info = environment.step(action)

        # Update our current state
        state = new_state

        # When we get a reward, it means we solved the game
        nb_success += reward

# Let's check our success rate!
print(f"Success rate = {nb_success / episodes * 100}%")
