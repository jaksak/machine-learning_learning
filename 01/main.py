import gymnasium as gym
import matplotlib.pyplot as plt
import numpy as np

environment = gym.make("FrozenLake-v1", is_slippery=True, render_mode="ansi")
environment.reset()

# We re-initialize the Q-table
qtable = np.zeros((environment.observation_space.n, environment.action_space.n))

# jakub: zmiana w api? brak nagrody na polu koncowym?
qtable[15] = np.array([1, 1, 1, 1])

# Hyperparameters
episodes = 15000  # Total number of episodes
alpha = 0.5  # Learning rate
gamma = 0.9  # Discount factor
epsilon = 1.0  # Amount of randomness in the action selection
epsilon_decay = 0.001  # Fixed amount to decrease
show_training_charts = False

# List of outcomes to plot
outcomes = []


# print('Q-table before training:')
# print(qtable)
def print_qtable(qtable):
    for index in range(len(qtable)):
        value = qtable[index] * 100
        with np.printoptions(formatter={'float': '{: 6.2f}'.format}):
            if ((index - 3) % 4) == 0:
                print(value)
            else:
                print(value, end=' ')
    print()


# Training
for i in range(episodes):
    state = environment.reset()[0]
    done = False

    # By default, we consider our outcome to be a failure
    outcomes.append("Failure")

    # Until the agent gets stuck in a hole or reaches the goal, keep training it
    while not done:
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

if show_training_charts:
    fig = plt.figure(figsize=(12, 5))
    plt.xlabel("Run number")
    plt.ylabel("Outcome")
    ax = plt.gca()
    ax.set_facecolor('#efeeea')
    plt.bar(range(len(outcomes)), outcomes, color="#0A047A", width=1.0)
    plt.show()

episodes = 100
nb_success = 0

environment.close()
environment = gym.make("FrozenLake-v1", is_slippery=True, render_mode="human")

# Evaluation
for _ in range(episodes):

    state = environment.reset()[0]
    done = False

    # Until the agent gets stuck or reaches the goal, keep training it
    while not done:
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
