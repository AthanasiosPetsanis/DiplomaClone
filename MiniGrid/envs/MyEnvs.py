from __future__ import annotations

from turtle import color

from gymnasium.core import ActType, ObsType
from typing import Any, Iterable, SupportsFloat, TypeVar

from minigrid.core.grid import Grid
from minigrid.core.mission import MissionSpace
from minigrid.core.world_object import Door, Goal, Key, Ball, Box
from minigrid.minigrid_env import MiniGridEnv
import pickle, numpy as np


# from matplotlib.pyplot import cla

# Load TextWorld output
with open('/usr/local/lib/python3.10/dist-packages/rl-starter-files/storage/action_courses', 'rb') as fp:
    action_courses = pickle.load(fp)

# action_courses = {'Easy': ['take apple', 'put apple on table'], \
#     'Easy_2': ['open door', 'take apple', 'put apple on table'], \
#     'Medium': ['open door', 'open fridge', 'take apple from fridge', 'put apple on table'], \
#     'Medium_2': ['open door', 'open fridge', 'take apple from fridge', 'put apple on table'],
#     'Hard': ['take key', 'open door', 'open fridge', 'take apple from fridge', 'put apple on table']}

# Make progressive rewards
max_course = 0
for course in action_courses:
    course = action_courses[str(course)]
    if len(course) > max_course:
        max_course = len(course)
goal_rewards = []
for i in range(max_course):
    goal_rewards.append(10/(max_course-i+1))

# Make regressive rewards
# goal_rewards.reverse()

def find_goals(self, course_of_action):
    self.take_goals, self.open_goals, self.put_goals = [], [], []
    for act_idx, action in enumerate(course_of_action):
        action = action.split()
        act_item = action[1]
        act_verb = action[0]
        act_supp = action[-1]

        if act_verb == 'open':
            self.open_goals.append([act_idx, act_item])
        elif act_verb == 'take':
            self.take_goals.append([act_idx, act_item]) # We don't need the act_supp here \
            # because we care about the distinct name of the item we take not \
            # where we take it from
        elif act_verb == 'put':
            self.put_goals = [act_idx, act_item, act_supp] # Not append because we \
            # assume only 1 ultimate goal since multiple goals would higly likely mean \
            # carrying more than 1 object which it can't

class MyMG_Env(MiniGridEnv):
    """
    Environment with a door and key, sparse reward
    """
    def __init__(self, size=8, max_steps: int | None = None, **kwargs):
        if max_steps is None:
            max_steps = 1000
        mission_space = MissionSpace(mission_func=self._gen_mission)
        super().__init__(
            mission_space=mission_space, grid_size=size, max_steps=max_steps, **kwargs
        )
        self.goals_done = 0

    @staticmethod
    def _gen_mission():
        return "use the key to open the door and then get to the goal"


class Easy_Env(MyMG_Env):
    def __init__(self, size=5):
        super().__init__(size)
        course_of_action = action_courses['Easy']
        self.nof_goals = len(course_of_action)
        find_goals(self, course_of_action)

    def _gen_grid(self, width, height):
        # Create an empty grid
        self.grid = Grid(width, height)

        # Generate the surrounding walls
        self.grid.wall_rect(0, 0, width, height)

        # Place the agent on the top left corner of the room
        self.place_agent(top=(1, 1), size=(1,1))

        # Place a ball (i.e. the apple)
        apple = Ball(color='red')
        apple.name = 'apple'
        self.put_obj(apple, width-2, 1)

        self.goal_width = round(width/4)
        self.goal_height = height-2
        table = Goal()
        table.name = 'table'
        self.put_obj(table, self.goal_width, self.goal_height)

        self.mission = "put apple on table"

class Easy_Env_2(MyMG_Env):
    def __init__(self, size=5):
        super().__init__(size)
        course_of_action = action_courses['Easy_2']
        self.nof_goals = len(course_of_action)
        find_goals(self, course_of_action)

    def _gen_grid(self, width, height):
        # Create an empty grid
        self.grid = Grid(width, height)

        # Generate the surrounding walls
        self.grid.wall_rect(0, 0, width, height)

        # Place the agent on the top left corner of the room
        self.place_agent(top=(1, 1), size=(1,1))

        # Place a ball (i.e. the apple)
        apple = Ball(color='red')
        apple.name = 'apple'
        self.put_obj(apple, width-1, 1)

        # Place a door
        door = Door(color='yellow')
        door.name = 'door'
        self.put_obj(door, width-2, 1)

        self.goal_width = round(width/4)
        self.goal_height = height-2
        table = Goal()
        table.name = 'table'
        self.put_obj(table, self.goal_width, self.goal_height)

        self.mission = "put apple on table"

class Medium_Env(MyMG_Env):
    def __init__(self):
        super().__init__(size=5)
        course_of_action = action_courses['Medium']
        self.nof_goals = len(course_of_action)
        find_goals(self, course_of_action)

    def _gen_grid(self, width, height):
        # Create an empty grid
        self.grid = Grid(width, height)

        # Generate the surrounding walls
        self.grid.wall_rect(0, 0, width, height)

        # Create a vertical splitting wall
        splitIdx = round(width/2)
        self.grid.vert_wall(splitIdx, 0)

        # Place the agent on the top left corner of the room
        self.place_agent(top=(1, 1), size=(1,1))

        # Place a door in the wall
        doorIdx = round(height/2)
        door = Door('yellow')
        door.name = 'door'
        self.put_obj(door, splitIdx, doorIdx)

        # Place a ball (i.e. the apple) inside a box (i.e. the fridge) and that in the env
        apple = Ball(color='red')
        apple.name = 'apple'
        fridge = Box('blue', contains=apple, pickable=False)
        fridge.name = 'fridge'
        self.put_obj(fridge, round(width*3/4), 1)

        self.goal_width = round(width/4)
        self.goal_height = height-2
        table = Goal()
        table.name = 'table'
        self.put_obj(table, self.goal_width, self.goal_height)

        self.mission = "put apple on table" 

class Medium_Env_2(MyMG_Env):
    def __init__(self):
        super().__init__(size=6)
        course_of_action = action_courses['Medium_2']
        self.nof_goals = len(course_of_action)
        find_goals(self, course_of_action)

    def _gen_grid(self, width, height):
        # Create an empty grid
        self.grid = Grid(width, height)

        # Generate the surrounding walls
        self.grid.wall_rect(0, 0, width, height)

        # Create a vertical splitting wall
        splitIdx = round(width/2)
        self.grid.vert_wall(splitIdx, 0)

        # Place the agent on the top left corner of the room
        self.place_agent(top=(1, 1), size=(1,1))

        # Place a door in the wall
        doorIdx = round(height/2)
        door = Door('yellow')
        door.name = 'door'
        self.put_obj(door, splitIdx, doorIdx)

        # Place a ball (i.e. the apple) inside a box (i.e. the fridge) and that in the env
        apple = Ball(color='red')
        apple.name = 'apple'
        fridge = Box('blue', contains=apple, pickable=False)
        fridge.name = 'fridge'
        self.put_obj(fridge, round(width*3/4), 1)

        self.goal_width = round(width/4)
        self.goal_height = height-2
        table = Goal()
        table.name = 'table'
        self.put_obj(table, self.goal_width, self.goal_height)

        self.mission = "put apple on table"

class Hard_Env(MyMG_Env):
    def __init__(self):
        super().__init__(size=7)
        course_of_action = action_courses['Hard']
        self.nof_goals = len(course_of_action)
        find_goals(self, course_of_action)

    def _gen_grid(self, width, height):
        # Create an empty grid
        self.grid = Grid(width, height)

        # Generate the surrounding walls
        self.grid.wall_rect(0, 0, width, height)

        # Create a vertical splitting wall
        splitIdx = round(width/2)
        self.grid.vert_wall(splitIdx, 0)

        # Place the agent on the top left corner of the room
        self.place_agent(top=(1, 1), size=(1,1))

        # Place a door in the wall
        doorIdx = round(height/2)
        door = Door('yellow', is_locked=True)
        door.name = 'door'
        self.put_obj(door, splitIdx, doorIdx)

        # Make key for door
        key = Key('yellow')
        key.name = 'key'
        self.put_obj(key, splitIdx-1, 1)

        # Place a ball (i.e. the apple) inside a box (i.e. the fridge) and that in the env
        apple = Ball(color='red')
        apple.name = 'apple'
        fridge = Box('blue', contains=apple, pickable=False)
        fridge.name = 'fridge'
        self.put_obj(fridge, round(width*3/4), 1)

        self.goal_width = round(width/4)
        self.goal_height = height-2
        table = Goal()
        table.name = 'table'
        self.put_obj(table, self.goal_width, self.goal_height)

        self.mission = "put apple on table"

class Hard_Env_2(MyMG_Env):
    def __init__(self):
        super().__init__(size=17)
    def _gen_grid(self, width, height):
        # Create the grid
        self.grid = Grid(width, height)

        room_w = width // 2
        room_h = height // 2
        room_mid_w = room_w // 2
        room_mid_h = room_h // 2

        # Generate the surrounding walls
        self.grid.horz_wall(0, 0)
        self.grid.horz_wall(0, height - 1)
        self.grid.vert_wall(0, 0)
        self.grid.vert_wall(width - 1, 0)


        
        # For each row of rooms
        for j in range(0, 2):

            # For each column
            for i in range(0, 2):
                xL = i * room_w
                yT = j * room_h
                xR = xL + room_w
                yB = yT + room_h

                # Bottom wall
                if i + 1 < 2:
                    self.grid.vert_wall(xR, yT, room_h)

                # Bottom wall
                if j + 1 < 2:
                    self.grid.horz_wall(xL, yB, room_w)

        # Define doors
        doorA_B = Door(color='yellow')
        doorC_D = Door(color='yellow')
        doorA_C = Door(color='yellow')
        doorB_D = Door(color='yellow')

        # Place doors
        self.put_obj(doorA_B, room_w, room_mid_h)
        self.put_obj(doorC_D, room_w, room_mid_h+room_h)
        self.put_obj(doorA_C, room_mid_w, room_h)
        self.put_obj(doorB_D, room_mid_w+room_h, room_h)

        # Make & Place counter
        counter = Goal(color='brown')
        for i in range(room_h-1):
            self.put_obj(counter, room_w+1+i, 1)
        self.put_obj(counter, room_w+1, 2)
        self.put_obj(counter, room_w+1, 3)

        # Make & Place table
        table_B = Goal()
        table_B_size = 3
        for i in range(table_B_size):
            for j in range(table_B_size):
                self.put_obj(table_B, 3+i+room_w, 3+j)          

        # Place objects
        coffee = Ball(color='custom', rgb=[0,0,255])
        self.put_obj(coffee, 4, 4)

        # Place agent
        self.place_agent(top=(1, 1), size=(1,1))

        # Place goal
        self.put_obj(Goal(), 2*room_w-1, 2*room_h-1)
        self.mission = 'Reach the goal'
 

class Dense_Env(MyMG_Env):
    def __init__(self):
        super().__init__()

    def step(
        self, action: ActType
    ) -> tuple[ObsType, SupportsFloat, bool, bool, dict[str, Any]]:
        
        self.step_count += 1
        reward = 0
        terminated = False
        truncated = False

        # Get the position in front of the agent
        fwd_pos = self.front_pos

        # Get the contents of the cell in front of the agent
        fwd_cell = self.grid.get(*fwd_pos)

        # Rotate left
        if action == self.actions.left:
            self.agent_dir -= 1
            if self.agent_dir < 0:
                self.agent_dir += 4

        # Rotate right
        elif action == self.actions.right:
            self.agent_dir = (self.agent_dir + 1) % 4

        # Move forward
        elif action == self.actions.forward:
            if fwd_cell == None or fwd_cell.can_overlap():
                self.agent_pos = fwd_pos  
            if fwd_cell != None and fwd_cell.type == 'lava':
                terminated = True

        # Pick up an object
        elif action == self.actions.pickup: 
            if fwd_cell and fwd_cell.can_pickup():
                if self.carrying is None:
                    self.carrying = fwd_cell
                    self.carrying.cur_pos = np.array([-1, -1])
                    self.grid.set(*fwd_pos, None)
            if self.carrying != None:
                for act in self.take_goals: # If 2 take actions followed one another there would be a problem \
                    # but that will never happen in MiniGrid 
                    if self.goals_done == act[0] and self.carrying.name == act[1]:
                        self.goals_done += 1
                        # reward = self._myreward()
                        # reward = self._reward()
                        reward = goal_rewards[self.goals_done] * self._reward()

        # Drop an object
        elif action == self.actions.drop:
#             if not fwd_cell and self.carrying:
#                 self.grid.set(*fwd_pos, self.carrying)
#                 self.carrying.cur_pos = fwd_pos
#                 self.carrying = None
            if self.carrying != None:
                if (fwd_pos == [self.goal_width, self.goal_height]).all() \
                and self.goals_done == self.put_goals[0] \
                and self.carrying.name == self.put_goals[1] \
                and fwd_cell.name == self.put_goals[2]:
                    self.goals_done = 0
                    terminated = True
                    reward = 100 * self._reward()
                    # reward = self._reward()

        # Toggle/activate an object
        elif action == self.actions.toggle:
            if fwd_cell:
                fwd_cell.toggle(self, fwd_pos)
                for act in self.open_goals:
                    if self.goals_done == act[0] and hasattr(fwd_cell, 'name'): # If 2 open actions followed \     
                    # one another there would be a problem but that will never happen in MiniGrid 
                        if fwd_cell.name == act[1]:
                            self.goals_done += 1
                            # reward = self._myreward()
                            # reward = self._reward()
                            reward = goal_rewards[self.goals_done] * self._reward()


        # Done action (not used by default)
        elif action == self.actions.done:
            pass

        else:
            assert False, "unknown action"

        if self.step_count >= self.max_steps:
            truncated = True

        obs = self.gen_obs()

        return obs, reward, terminated, truncated, {}
    

class Sparse_Env(MyMG_Env):
    def __init__(self):
        super().__init__()

    def step(
        self, action: ActType
    ) -> tuple[ObsType, SupportsFloat, bool, bool, dict[str, Any]]:
        # Get names of end goal item and supporter
        self.step_count += 1
        reward = 0
        terminated = False
        truncated = False

        # Get the position in front of the agent
        fwd_pos = self.front_pos

        # Get the contents of the cell in front of the agent
        fwd_cell = self.grid.get(*fwd_pos)

        # Rotate left
        if action == self.actions.left:
            self.agent_dir -= 1
            if self.agent_dir < 0:
                self.agent_dir += 4

        # Rotate right
        elif action == self.actions.right:
            self.agent_dir = (self.agent_dir + 1) % 4

        # Move forward
        elif action == self.actions.forward:
            if fwd_cell == None or fwd_cell.can_overlap():
                self.agent_pos = fwd_pos  
            if fwd_cell != None and fwd_cell.type == 'lava':
                terminated = True

        # Pick up an object
        elif action == self.actions.pickup: 
            if fwd_cell and fwd_cell.can_pickup():
                if self.carrying is None:
                    self.carrying = fwd_cell
                    self.carrying.cur_pos = np.array([-1, -1])
                    self.grid.set(*fwd_pos, None)

        # Drop an object
        elif action == self.actions.drop:
            if not fwd_cell and self.carrying:
                self.grid.set(*fwd_pos, self.carrying)
                self.carrying.cur_pos = fwd_pos
                self.carrying = None
            if self.carrying != None:
                if (fwd_pos == [self.goal_width, self.goal_height]).all() \
                and self.carrying.name == self.put_goals[1] and fwd_cell.name == self.put_goals[-1]:
                    terminated = True
                    reward = 100 * self._reward()


        # Toggle/activate an object
        elif action == self.actions.toggle:
            if fwd_cell:
                fwd_cell.toggle(self, fwd_pos)



        # Done action (not used by default)
        elif action == self.actions.done:
            pass

        else:
            assert False, "unknown action"

        if self.step_count >= self.max_steps:
            truncated = True

        obs = self.gen_obs()

        return obs, reward, terminated, truncated, {}
    
# Easy envs
class Dense_Easy(Dense_Env, Easy_Env):
    def __init__(self, **kwargs):
        super().__init__()

class Sparse_Easy(Sparse_Env, Easy_Env):
    def __init__(self, **kwargs):
        super().__init__()

# Easy 2
class Dense_Easy_2(Dense_Env, Easy_Env_2):
    def __init__(self, **kwargs):
        super().__init__()

class Sparse_Easy_2(Sparse_Env, Easy_Env_2):
    def __init__(self, **kwargs):
        super().__init__()

# Medium
class Dense_Medium(Dense_Env, Medium_Env):
    def __init__(self, **kwargs):
        super().__init__()

class Sparse_Medium(Sparse_Env, Medium_Env):
    def __init__(self, **kwargs):
        super().__init__()


# Medium_2
class Dense_Medium_2(Dense_Env, Medium_Env_2):
    def __init__(self, **kwargs):
        super().__init__()

class Sparse_Medium_2(Sparse_Env, Medium_Env_2):
    def __init__(self, **kwargs):
        super().__init__()


# Hard
class Dense_Hard(Dense_Env, Hard_Env):
    def __init__(self, **kwargs):
        super().__init__()

class Sparse_Hard(Sparse_Env, Hard_Env):
    def __init__(self, **kwargs):
        super().__init__()


class Dense_Hard_2(Dense_Env, Hard_Env_2):
    def __init__(self, **kwargs):
        super().__init__()

class Sparse_Hard_2(Sparse_Env, Hard_Env_2):
    def __init__(self, **kwargs):
        super().__init__()
