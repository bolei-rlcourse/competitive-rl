

<table border="0" width=1000px align="center" style="margin-bottom: 100px;">
        <tr>
        <td align="center">
            <b>Compeititive Pong</b>
      </td>
        <td align="center">
            <b>Compeititive Car-Racing</b>
      </td>
    </tr>
    <tr>
        <td align="center">
            <img align="center" width=300px  src="resources/repo-cover-large.gif" />
      </td>
        <td align="center" width=400px>
            <img align="center" width=350px  src="resources/repo-cover-racing.gif" />
      </td>
    </tr>
</table>


# Competitive RL Environments

In this repo, we provide two interesting competitive RL environments:

1. Competitive Pong (cPong): The environment extends the classic Atari Game Pong into a competitive environment, where both side can be trainable agents.
2. Competitive Car-Racing (cCarRacing): The environment allows multiple cars to race and compete in the same map.



## Installation

```bash
pip install git+https://github.com/cuhkrlcourse/competitive-rl.git
```


## Usage

```python
import gym
import competitive_rl

competitive_rl.register_competitive_envs()

pong_single_env = gym.make("cPong-v0")
pong_double_env = gym.make("cPongDouble-v0")

racing_single_env = gym.make("cCarRacing-v0")
racing_double_env = gym.make("cCarRacingDouble-v0")
```

The observation spaces:

1. `cPong-v0`: `Box(210, 160, 3)`
2. `cPongDouble-v0`: `Tuple(Box(210, 160, 3), Box(210, 160, 3))`
3. `cCarRacing-v0`: `Box(96, 96, 1)`
4. `cCarRacingDouble-v0`: `Box(96, 96, 1)`

The action spaces:

1. `cPong-v0`: `Discrete(3)`
2. `cPongDouble-v0`: `Tuple(Discrete(3), Discrete(3))`
3. `cCarRacing-v0`: `Box(2,)`
4. `cCarRacingDouble-v0`: `Dict(0:Box(2,), 1:Box(2,))`


## Acknowledgement

This repo is contributed by many students from CUHK:

* Zhenghao Peng ([@pengzhenghao](https://github.com/pengzhenghao))
* Edward Hui ([@Edwardhk](https://github.com/Edwardhk))
* Yi Zhang ([@1155107756](https://github.com/1155107756))
* Billy Ho ([@Poiutrew1004](https://github.com/Poiutrew1004))
* Joe Lam ([@JoeLamKC](https://github.com/JoeLamKC))

Please enjoy this repo, and we welcome any contribution and further development! Thanks!

