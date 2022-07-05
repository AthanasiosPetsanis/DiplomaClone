from textworld.MyPy.Functions import *
import numpy as np
import random
from time import time
import matplotlib.pyplot as plt

class Q_agent():
    def __init__(self, env) -> None:
        self.things, self.rooms, self.obj = [], [], []
        self.States, self.Q_matrix = [], []
        self.expl = 1
        self.total_eps = 0
        self.expl_history, self.moves_history = [self.expl], []
        self.avg_moves = []
        self.env = env

    def reset(self):
        self.env.reset()
        self.__init__(self.env)

    def check_state(self, infos):
        
        infos['location'] = find_location(infos["description"])
        # Command preprocess doesn't change the number of states
        # This preprocess significantly improves timing.
        commands = cmd_remover(infos['admissible_commands'])
        infos['inventory'] = inv_process(infos['inventory'])
        state = [infos['location'], infos['inventory'], commands]
        cmd_len = len(commands)

        if state not in self.States:
            self.States.append(state)
            self.Q_matrix.append(np.zeros([cmd_len]))

        st_index = self.States.index(state)
        
        return st_index, commands, cmd_len
    
    def ask_obj(self):
        things = self.things; rooms = self.rooms; obj = self.obj

        another_one = True
        while another_one:
            things.append(input('What would you like? '))
            rooms.append(input('What room would you like it in? '))
            supporter = input('Where would you like it onto? ')
            # if supporter.lower()=='floor': obj.append(f'drop {things[-1]}')
            obj.append(f'put {things[-1]} on {supporter}')

            not_done = True
            while not_done:
                in_put = input('Would you like to input another objective? y/n ').lower()
                if in_put=='y' or in_put=='yes': another_one = True; not_done=False
                elif in_put=='n' or in_put=='no': another_one = False; not_done=False
                else: print('Unidentified input'); not_done = True
            
        self.things = things; self.rooms = rooms; self.obj = obj

    def back_prop(self, Ep_indexes, gamma, learning_rate, new_st_index):

        Ep_indexes.reverse()
        for pair in Ep_indexes:
            st_index = pair[0]
            action_index = pair[1]
            reward = pair[2]
            self.Q_matrix[st_index][action_index] = (1-learning_rate) * self.Q_matrix[st_index][action_index]\
                                            + learning_rate * (reward + gamma*np.max(self.Q_matrix[new_st_index]))
            new_st_index = st_index
    
    def train(self, max_epochs=5, max_eps=1000, render=False, min_expl=0.01, max_expl=1, manual=False,
            learning_rate=0.8, expl_decay_rate=0.005, gamma=0.95, title='Q_Agent', neg_reward=0, user_input=None):

        start = time()
        if manual and user_input != None:
            print('Either manual input a command via the command line or inputed using user_input argument, but not both')
        elif manual:
            self.ask_obj()
            rooms = self.rooms; obj = self.obj
            self.obj_len = len(self.obj)
        elif user_input != None:
            self.things = [user_input[0]]; self.rooms = [user_input[1]]
            things = self.things; rooms = self.rooms
            self.obj = [f'put {user_input[0]} on {user_input[2]}']; obj = self.obj
            self.obj_len = len(self.obj)


        for epoch in range(max_epochs):
            for ep in range(max_eps):
                obs, infos = self.env.reset()
                step = 0
                self.total_eps += 1
                try:
                    goals_done = [0] * self.obj_len
                except: self.obj_len = 0
                Ep_indexes = []

                while True:
                    
                    reached_goal=False
                    step += 1

                    if render:
                        self.env.render()

                    st_index, commands, cmd_len = self.check_state(infos)

                    # Randomly choose whether to explore or exploit based on probability expl
                    if random.uniform(0,1) > self.expl:
                        # Exploit
                        action_index = self.Q_matrix[st_index].argmax() 
                        action = commands[action_index]
                    else:
                        # Explore
                        action_index = np.random.choice(cmd_len)
                        action = commands[action_index] 
            
                    

                    obs, score, done, infos = self.env.step(action)
                    reward = infos['intermediate_reward']

                    if neg_reward: reward -= neg_reward
                    if infos['won']: reward += 10


                    new_st_index, _, _ = self.check_state(infos)

                    try:
                        for i in range(self.obj_len):
                            if action==obj[i] and infos['location'].lower()==rooms[i].lower() and goals_done[i]==0:
                                reward += 200 #/step
                                goals_done[i] = 1
                                if sum(goals_done)==self.obj_len: done = True
                    except: print('Unable to reward the inputed goal')

                    Ep_indexes.append([st_index, action_index, reward])

                    # Q_matrix[st_index][action_index] = (1-learning_rate) * Q_matrix[st_index][action_index]\
                    #                                     + learning_rate * (reward + gamma*np.max(Q_matrix[new_st_index]))

                    if done:
                        break

                self.back_prop(Ep_indexes, gamma, learning_rate, new_st_index)

                self.expl = min_expl + (max_expl - min_expl)*np.exp(-expl_decay_rate*self.total_eps) 

                self.moves_history.append(infos['moves'])
                if (ep+1)%10==0:
                    self.expl_history.append(self.expl)
                    self.avg_moves.append(sum(self.moves_history[-10::])/10)
                    

        print(f"Training detected {np.shape(self.Q_matrix)} possible states")
        Q_printer = []
        for i in self.Q_matrix:
            Q_printer.append(np.shape(i))
        length = len(Q_printer) if len(Q_printer)<30 else 30
        print(f"Number of commands for each state: \n{Q_printer[0:length]}")
        np.warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)

        plt.figure(1)
        moves_plt, = plt.plot(np.arange(1,len(self.avg_moves)+1), self.avg_moves, label='Moves')
        plt.xlabel('Every 10nth episode')
        plt.ylabel('Average of 10 eps', color='C0')
        plt.twinx()
        expl_plt, = plt.plot(np.arange(1,len(self.expl_history)+1), self.expl_history, label='Expl', color='orange')
        plt.ylabel('Exploration value', color='orange')
        plt.legend(handles=[moves_plt, expl_plt], loc='upper right')
        plt.title(title)
        plt.show()

        end = time(); t_sec = end-start; mins = t_sec//60; secs = t_sec-mins*60
        print(f"Training took {mins} minutes and {secs} seconds")
        
        cnt = 0
        for state in self.States:
            if cnt<20:
                cnt += 1
                print(f'S{cnt}: {state}')
            else:
                break

    def test(self, render=False):
        obj = self.obj; rooms = self.rooms

        self.obj_len = len(obj)
        actions_taken = []
        step = 0
        goals_done = [0] * self.obj_len
        obs, infos = self.env.reset()


        while True:
            step += 1
            if render:
                self.env.render()

            st_index, commands, cmd_len = self.check_state(infos)
            
            action_index = self.Q_matrix[st_index].argmax() 
            action = commands[action_index]
            print(f"Action taken in step {step}: {action}")
            actions_taken.append(action)
            
            obs, reward, done, infos = self.env.step(action)

            _ = self.check_state(infos)
            
            self.obj_len = len(obj)
            for i in range(self.obj_len):
                if action==obj[i] and infos['location'].lower()==rooms[i].lower():
                    goals_done[i] = 1
                    if sum(goals_done)==self.obj_len: done = True

            if done:
                print(f"Finished in {infos['moves']} moves")
                print("Actions taken:")
                for action in actions_taken:
                    print(f"{action} >", end=" ")
                break

        return actions_taken
