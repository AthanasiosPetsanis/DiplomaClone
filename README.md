# General
This repository is cloned on Google's remote computer when the Main.ipynb file is run in GoogleColab. This way all prerequisites are installed remotely and anyone can easily run our code as long as you have a Google account.
It is called "Diploma_Clone" because it is the work of my diploma thesis and its purpose is to get cloned.

Our method is described in the following paper: https://www.frontiersin.org/journals/robotics-and-ai/articles/10.3389/frobt.2023.1280578/full


##  Method Synopsis
In a synopsis, an agent is trained to execute a user-defined command in a simulation of a home environment. The simulator used is [MiniGrid](https://github.com/Farama-Foundation/gym-minigrid). Our novelty lies in using [TextWorld](https://github.com/microsoft/TextWorld) as a high-level agent for decomposing the user-defined tasks into sub-tasks that contribute in faster convergence and better solving of the low-level MiniGrid agent. TextWorld is a text-based game, but can also be thought of and used as a conceptually more abstract simulator of home environments.

A simple diagram of this method is depicted below:
![](https://user-images.githubusercontent.com/54399132/184197141-8e32962f-412a-45e2-a5a3-b0ddb1467fef.png)


## Agents
For _MiniGrid_, the algorithm used for training and the architecture of the agent are defined as recommended by the designers of MiniGrid, i.e. a [PPO](https://arxiv.org/pdf/1707.06347.pdf) (Proximal Policy Optimization) algorithm and a neural network respectively. 
More details on these can be found in the designated repository: [rl-torch](https://github.com/lcswillems/rl-starter-files)

For _TextWorld_, we use a simple Q-learning algorithm and the architecture is a Q-matrix that saves a weight for every State-Action pair discovered during exploration. The code can be found here: [Q-agent](https://github.com/AthanasiosPetsanis/Diploma_Temp/blob/main/TextWorld/MyPy/Q_agent.py)


## Training
Training is done in preconstructed environments of increasing difficulty which we made. The user-defined command is always moving an apple and placing it on the table[^1] The environments are the following[^2]:

![Dense_Easy](https://user-images.githubusercontent.com/54399132/184203097-d93aff84-2723-413f-bbb1-5b476834317a.png) ![Dense_Easy_2](https://user-images.githubusercontent.com/54399132/184203239-594e1cdc-b8da-40c0-bb66-cdb5095924b1.png) ![Dense_Medium](https://user-images.githubusercontent.com/54399132/184203857-e7237d45-29dc-4dbf-9961-0ade382d7476.png) ![Dense_Medium_2_size6](https://user-images.githubusercontent.com/54399132/184203935-c6165d03-6268-4b4a-9671-1e208169ef8f.png) ![Dense_Hard](https://user-images.githubusercontent.com/54399132/184203696-80652a0f-9e59-49c3-b543-d143a75b72fa.png)

## Results
TextWorld successfully decomposes the user-defined task into an optimal (i.e. shortest) sequence of sub-tasks and the comparison of average return between our method (using TextWolrd) and without it (without using TextWorld) shows increasing efficacy as the difficulty increases.

The graphs for the corresponding environments can be found in the [Results](https://github.com/AthanasiosPetsanis/Diploma_Clone/tree/main/Results) folder of this repository. 


## Future Work
The results are encouraging, but there is still a long way to go for a practical implementation on a robotic home assistant. Firstly, we aim to generalize the learning more and broaden the possible commands as well as environments. Secondly, we want to find a more realistic low level simulator that will also include manipulation tasks (i.e. robotic-arm movements). Ultimately, we hope our method in tangem with state-of-the-art existing research will produce a more reliable and smart robotic home assistant.


# Cite as:
*Petsanis, T., Keroglou, C., Kapoutsis, A. C., Kosmatopoulos E. B., & Sirakoulis G. Ch. (2023). Decomposing user-defined tasks in a reinforcement learning setup using TextWorld.* [[Link](https://www.frontiersin.org/journals/robotics-and-ai/articles/10.3389/frobt.2023.1280578/full)]

```bibtex
@ARTICLE{10.3389/frobt.2023.1280578,

AUTHOR={Petsanis, Thanos  and Keroglou, Christoforos  and Ch. Kapoutsis, Athanasios  and Kosmatopoulos, Elias B.  and Sirakoulis, Georgios Ch. },

TITLE={Decomposing user-defined tasks in a reinforcement learning setup using TextWorld},

JOURNAL={Frontiers in Robotics and AI},

VOLUME={10},

YEAR={2023},

URL={https://www.frontiersin.org/journals/robotics-and-ai/articles/10.3389/frobt.2023.1280578},

DOI={10.3389/frobt.2023.1280578},

ISSN={2296-9144},

ABSTRACT={<p>The current paper proposes a hierarchical reinforcement learning (HRL) method to decompose a complex task into simpler sub-tasks and leverage those to improve the training of an autonomous agent in a simulated environment. For practical reasons (i.e., illustrating purposes, easy implementation, user-friendly interface, and useful functionalities), we employ two Python frameworks called TextWorld and MiniGrid. MiniGrid functions as a 2D simulated representation of the real environment, while TextWorld functions as a high-level abstraction of this simulated environment. Training on this abstraction disentangles manipulation from navigation actions and allows us to design a dense reward function instead of a sparse reward function for the lower-level environment, which, as we show, improves the performance of training. Formal methods are utilized throughout the paper to establish that our algorithm is not prevented from deriving solutions.</p>}}
}

```





[^1]: It's always the same command because it helps with better comparison of the results as the diffuctly increases, but it can easily be changed.
[^2]: The ones are show here are the MiniGrid environments. The ones in TextWorld are a bit different.
