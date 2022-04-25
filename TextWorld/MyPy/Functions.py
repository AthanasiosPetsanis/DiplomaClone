import gym
import textworld
from textworld import EnvInfos

def load_game(game_file, max_steps=100):

    request_infos = EnvInfos(inventory=True, admissible_commands=True, entities=True, won=True, lost=True, intermediate_reward=True,
                             description=True, location=True, objective=True, score=True, moves=True)

    env_id = textworld.gym.register_games([game_file], request_infos, max_episode_steps=max_steps)

    env = gym.make(env_id)  # Start the environment.

    obs, infos = env.reset()# Start new episode.

    print(obs)

    score, moves, done = 0, 0, False
    return env, obs, infos