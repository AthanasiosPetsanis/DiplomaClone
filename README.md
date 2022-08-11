# MiniGrid_Temp
This repository is cloned on Google's remote computer when the Main.ipynb file is run in GoogleColab. This way all prerequisites are installed remotely and anyone can easily run our code as long as you have a Google account.

Our method is described in the following paper: TBA


##  Method Synopsis
In a synopsis, an agent is trained to execute a user-defined command in a simulation of a home environment. The simulator used is [MiniGrid](https://github.com/Farama-Foundation/gym-minigrid). Our novelty lies in using [TextWorld](https://github.com/microsoft/TextWorld) as a high-level agent for decomposing the user-defined tasks into sub-tasks that contribute in faster convergence and better solving of the low-level MiniGrid agent. TextWorld is a text-based game, but can also be thought of and used as a conceptually more abstract simulator of home environments.

A simple diagram of this method is depicted below:
![](https://user-images.githubusercontent.com/54399132/184197141-8e32962f-412a-45e2-a5a3-b0ddb1467fef.png)


## Agents
For _MiniGrid_, the algorithm used for training and the architecture of the agent are defined as recommended by the designers of MiniGrid, i.e. a [PPO](https://arxiv.org/pdf/1707.06347.pdf) (Proximal Policy Optimization) algorithm and a neural network respectively. 
More details on these can be found in the designated repository: [rl-torch](https://github.com/lcswillems/rl-starter-files)

For _TextWorld_, we use a simple Q-learning algorithm and the architecture is a Q-matrix that saves a weight for every State-Action pair discovered during exploration. The code can be found here: [Q-agent](https://github.com/AthanasiosPetsanis/Diploma_Temp/blob/main/TextWorld/MyPy/Q_agent.py)


## Training
Training is done in preconstructed environments of increasing difficulty which we made. The user-defined command is always moving an apple and placing it on the table[^1]

[^1]: It helps with better comparison of the results as the diffuctly increases.
