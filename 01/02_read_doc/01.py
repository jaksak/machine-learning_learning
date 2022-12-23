import gymnasium as gym
# render mode
## human: najblizszy czlowiekowi, aktualizacje rysowane automatycznie
# rgb_array/ansi: uproszczenie, zeby zobaczyc efekt zawolac env.render()
env = gym.make("FrozenLake-v1", render_mode="human")
# dolozenie limitu czasowego: po 3 krokach: koniec truncated=True
env = gym.wrappers.TimeLimit(env, max_episode_steps=3)
# For Custom environments, the first line of reset() should be super().reset(seed=seed) which implements the seeding correctly.
observation, info = env.reset()

# info o tym co moge wykonac / co bedzie obserwowane
# Discrete/Box: obiekty opisane w doc
# print(env.action_space)
# print(env.observation_space)
# print(env.reward_range)

for _ in range(1000):
    action = env.action_space.sample()

    # terminated = agent osiagnal stan koncowy - zabil sie/przeszedl gre
    # truncated = osiagnieto warunek zakonczenia iteracji - limit czasowy itp
    observation, reward, terminated, truncated, info = env.step(action)

    if terminated or truncated:
        observation, info = env.reset()

# wrappery: rozszerzanie srodowiska, mozliwosc korzystania ze srodowiska unwrapped:
# env.unwrapped

env.close()