"""
This file defines a helper function to build our environment.

Usages:
    make_envs(
        env_id="cPong-v0",      # Environment name, must in [
                                    "cPongTournament-v0",
                                    "cPongDouble-v0",
                                    "cPong-v0",
                                    "CartPole-v0"
                                    ].
        seed=0,                 # Random seed
        log_dir="data",         # Which directory to store data and checkpoints
        num_envs=5,             # How many concurrent environments to run
        asynchronous=True,      # Whether to use asynchronous envrionments.
                                # This can extremely accelerate the system
        resized_dim=42          # Resized the observation to a 42x42 image
    )

Notes:
    1. If you wish to use asynchronous environments, you should run it in python
        scripts under "if __name__ == '__main__'" line.
    2. CartPole-v0 environment can be used for testing algorithms.
"""
import os
import shutil
import warnings

import gym

from competitive_rl.car_racing import make_car_racing, make_car_racing_double
from competitive_rl.pong.competitive_pong_env import TournamentEnvWrapper
from competitive_rl.register import register_competitive_envs
from competitive_rl.utils import DummyVecEnv, SubprocVecEnv, make_env_a2c_atari

register_competitive_envs()

__all__ = ["make_envs"]

msg = """
Multiprocessing vectorized environments need to be created under 
"if __name__ == '__main__'" line due to the limitation of multiprocessing 
module. 

If you are testing codes within interactive interface like jupyter notebook, please set the num_envs to 1, 
i.e. make_envs(num_envs=1) to avoid such error. We return envs = None now.
"""


def _verify_env_id(env_id):
    """For compatibility reason, we allow using old names here."""
    replace_names = {
        "CompetitivePongTournament-v0": "cPongTournament-v0",
        "CompetitivePongDouble-v0": "cPongDouble-v0",
        "CompetitivePong-v0": "cPong-v0"
    }
    msg = "Environment id {} is deprecated. Please use the short version {}."
    if env_id in replace_names:
        warnings.warn(msg.format(env_id, replace_names[env_id]))
        env_id = replace_names[env_id]
    assert env_id in [
        "cPongTournament-v0", "cPongDouble-v0", "cPong-v0", "CartPole-v0", "cCarRacing-v0", "cCarRacingDouble-v0"
    ]
    return env_id


def make_envs(env_id="cPong-v0", seed=0, log_dir="data", num_envs=3, asynchronous=False, resized_dim=42, frame_stack=4,
              action_repeat=None):
    """
    Create CUHKPong-v0, CUHKPongDouble-v0 or CartPole-v0 environments. If
    num_envs > 1, put them into different processes.

    :param env_id: The name of environment you want to create
    :param seed: The random seed
    :param log_dir: The path to store the learning stats
    :param num_envs: How many environments you want to run concurrently (Too
        large number will block your program.)
    :param asynchronous: whether to use multiprocessing
    :param resized_dim: resize the observation to image with shape (1,
        resized_dim, resized_dim)
    :return: A vectorized environment
    """
    asynchronous = asynchronous and num_envs > 1

    # env_id = _verify_env_id(env_id)

    if env_id == "CartPole-v0":
        print("Setup easy environment CartPole-v0 for testing.")
        envs = [lambda: gym.make("CartPole-v0") for i in range(num_envs)]
        envs = SubprocVecEnv(envs) if asynchronous else DummyVecEnv(envs)
        return envs

    if env_id == "cPongTournament-v0":
        envs = make_envs("cPongDouble-v0", seed, log_dir, num_envs,
                         asynchronous, resized_dim)
        return TournamentEnvWrapper(envs, num_envs)

    if log_dir:
        os.makedirs(log_dir, exist_ok=True)

    if env_id == "cCarRacing-v0":
        envs = [make_car_racing(env_id, seed, i, frame_stack=frame_stack, action_repeat=action_repeat) for i in
                range(num_envs)]
    elif env_id == "cPong-v0" or env_id == "cPongDouble-v0":
        if env_id == "cPongDouble-v0":
            assert frame_stack is None
        envs = [make_env_a2c_atari(env_id, seed, i, log_dir, resized_dim, frame_stack) for i in range(num_envs)]
    elif env_id == "cCarRacingDouble-v0":
        envs = [make_car_racing_double(seed, i, frame_stack=frame_stack, action_repeat=action_repeat) for i in
                range(num_envs)]
    else:
        envs = [lambda: gym.make(env_id) for i in range(num_envs)]

    if asynchronous:
        envs = SubprocVecEnv(envs)
    else:
        envs = DummyVecEnv(envs)
    return envs


if __name__ == '__main__':
    # Testing

    double_envs = make_envs("cPongDouble-v0", num_envs=3,
                            log_dir="tmp", asynchronous=False)
    double_envs.reset()
    double_obs, double_rew, double_done, double_info = double_envs.step(
        [[0, 0], [1, 0], [2, 1]])

    tournament_envs = make_envs("cPongTournament-v0", num_envs=3,
                                log_dir="tmp", asynchronous=True)
    tournament_envs.reset()
    tournament_envs.step([0, 1, 2])

    double_envs = make_envs("cPongDouble-v0", num_envs=3,
                            log_dir="tmp", asynchronous=True)
    double_envs.reset()
    double_obs_a, double_rew_a, double_done_a, double_info_a = double_envs.step(
        [[0, 0], [1, 0], [2, 1]])

    envs = make_envs("cPong-v0", num_envs=3, log_dir="tmp",
                     asynchronous=False)
    envs.reset()
    obs, rew, done, info = envs.step([0, 1, 2])

    # Test consistency between cPongTournament and cPong
    envs = make_envs("cPong-v0", num_envs=3, log_dir="tmp",
                     asynchronous=False)

    tournament_envs = make_envs("cPongTournament-v0", num_envs=3,
                                log_dir="tmp", asynchronous=False)
    assert envs.reset().shape == tournament_envs.reset().shape
    o1, r1, d1, i1 = envs.step([0, 1, 0])
    o2, r2, d2, i2 = tournament_envs.step([0, 1, 0])
    assert o1.shape == o2.shape
    assert r1.shape == r2.shape, (r1.shape, r2.shape)
    assert d1.shape == d2.shape, (d1.shape, d2.shape)

    envs = make_envs("cPong-v0", num_envs=1, log_dir="tmp",
                     asynchronous=False)
    tournament_envs = make_envs("cPongTournament-v0", num_envs=1,
                                log_dir="tmp", asynchronous=False)
    assert envs.reset().shape == tournament_envs.reset().shape
    o1, r1, d1, i1 = envs.step([0])
    o2, r2, d2, i2 = tournament_envs.step([0])
    assert o1.shape == o2.shape
    assert r1.shape == r2.shape, (r1.shape, r2.shape)
    assert d1.shape == d2.shape, (d1.shape, d2.shape)

    shutil.rmtree("./tmp", ignore_errors=True)
