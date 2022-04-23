from gym_minigrid.minigrid import *
from gym_minigrid.register import register
import pickle

# Load TextWorld output
with open('/usr/local/lib/python3.7/dist-packages/rl-starter-files/storage/actions_taken', 'rb') as fp:
    course_of_action = pickle.load(fp)

# course_of_action = ['open door', 'open fridge', 'take apple from fridge', 'put apple on table']
class MyMG_Env(MiniGridEnv):
    """
    Environment with a door and key, sparse reward
    """

    def __init__(self, size=8):
        super().__init__(
            grid_size=size,
            max_steps=10*size*size
        )
        self.goals_done = 0
        self.size = size;

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
        fridge = Box('blue', contains=apple)
        fridge.name = 'fridge'
        self.put_obj(fridge, round(width*3/4), 1)

        # Place a yellow key on the left side
        # self.place_obj(
        #     obj=Key('yellow'),
        #     top=(0, 0),
        #     size=(splitIdx, height)
        # )
        self.goal_width = round(width/4)
        self.goal_height = height-2
        table = Goal()
        table.name = 'table'
        self.put_obj(table, self.goal_width, self.goal_height)

        self.mission = "put apple on table"


    
    

class Dense_Env(MyMG_Env):
    def __init__(self):
        super().__init__(size=6)

    def step(self, action):

        self.step_count += 1
        reward = 0
        done = False

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
                done = True

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
                        reward = self._reward()

        # Drop an object
        elif action == self.actions.drop:
            if not fwd_cell and self.carrying:
                self.grid.set(*fwd_pos, self.carrying)
                self.carrying.cur_pos = fwd_pos
                self.carrying = None
            if self.carrying != None:
                if (fwd_pos == [self.goal_width, self.goal_height]).all() \
                and self.carrying.name == self.put_goals[1] and fwd_cell.name == self.put_goals[-1]:
                    self.goals_done = 0
                    done = True
                    reward = self._reward()

        # Toggle/activate an object
        elif action == self.actions.toggle:
            if fwd_cell:
                fwd_cell.toggle(self, fwd_pos)
                for act in self.open_goals:
                    if self.goals_done == act[0] and fwd_cell.name == act[1]: # If 2 open actions followed \     
                    # one another there would be a problem but that will never happen in MiniGrid 
                        self.goals_done += 1
                        reward = self._reward()


        # Done action (not used by default)
        elif action == self.actions.done:
            pass

        else:
            assert False, "unknown action"

        if self.step_count >= self.max_steps:
            done = True

        obs = self.gen_obs()

        return obs, reward, done, {}
    

class Sparse_Env(MyMG_Env):
    def __init__(self):
        super().__init__(size=6)

    def step(self, action):

        # Get names of end goal item and supporter
        

        self.step_count += 1
        reward = 0
        done = False

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
            print(self.put_goals)
            if fwd_cell == None or fwd_cell.can_overlap():
                self.agent_pos = fwd_pos  
            if fwd_cell != None and fwd_cell.type == 'lava':
                done = True

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
                    done = True
                    reward = self._reward()


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
            done = True

        obs = self.gen_obs()

        return obs, reward, done, {}
    

register(
    id='MiniGrid-Dense_Env-v0',
    entry_point='gym_minigrid.envs.MyEnvs:Dense_Env'
)

register(
    id='MiniGrid-Sparse_Env-v0',
    entry_point='gym_minigrid.envs.MyEnvs:Sparse_Env'
)