# MiniGrid_Temp

This repository is cloned on Google's remote computer when the Main.ipynb file is run in GoogleColab. This way all prerequisites are installed remotely and anyone can easily run our code as long as you have a Google account.

Our method is described in the following paper: TBA

##  Method Synopsis
In a synopsis, an agent is trained to execute a user-defined command in a simulation of a home environment. The simulator used is [MiniGrid](https://github.com/Farama-Foundation/gym-minigrid). Our novelty lies in using [TextWorld](https://github.com/microsoft/TextWorld) as a high-level agent for decomposing the user-defined tasks into sub-tasks that contribute in faster convergence and better solving of the low-level MiniGrid agent. TextWorld is a text-based game, but can also be thought of and used as a conceptually more abstract simulator of home environments.

## Agents
