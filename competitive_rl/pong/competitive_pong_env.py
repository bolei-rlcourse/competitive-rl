import random

import numpy as np

from competitive_rl.pong.builtin_policies import get_compute_action_function, \
    get_builtin_agent_names


class TournamentEnvWrapper:
    def __init__(self, env, num_envs):
        self.env = env
        self.agents = {
            agent_name: get_compute_action_function(agent_name, num_envs)
            for agent_name in get_builtin_agent_names()
            if agent_name != "ALPHA_PONG"
        }
        self.agent_names = list(self.agents)
        self.prev_opponent_obs = None
        self.current_agent_name = "RULE_BASED"
        self.current_agent = self.agents[self.current_agent_name]
        self.observation_space = env.observation_space[0]
        self.action_space = env.action_space[0]
        self.num_envs = num_envs

    def get_agent_names(self):
        return self.agent_names

    def reset_opponent(self, agent_name=None):
        if agent_name is None:
            self.current_agent_name = random.choice(self.agent_names)
        else:
            assert agent_name in self.agent_names, self.agent_names
            self.current_agent_name = agent_name
        self.current_agent = self.agents[self.current_agent_name]

    def step(self, action):
        tuple_action = np.stack([
            np.asarray(action).reshape(-1),
            np.asarray(self.current_agent(self.prev_opponent_obs)).reshape(-1)
        ], axis=1)
        obs, rew, done, info = self.env.step(tuple_action)
        self.prev_opponent_obs = obs[1]
        if done.ndim == 2:
            done = done[:, 0]
        return obs[0], rew[:, 0].reshape(-1, 1), done.reshape(-1, 1), info

    def reset(self, **kwargs):
        obs = self.env.reset(**kwargs)
        self.prev_opponent_obs = obs[1]
        return obs[0]

    def seed(self, s):
        self.env.seed(s)
