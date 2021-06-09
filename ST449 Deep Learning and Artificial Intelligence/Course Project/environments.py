import dm_env
from dm_env import specs

# based on https://github.com/ShangtongZhang/reinforcement-learning-an-introduction/blob/master/chapter08/maze.py
# but adapted to work with Acme agents

# ------------------------------ maze environment ------------------------------ #

class Maze(dm_env.Environment):
    def __init__(self):
        
        # maze width and hight
        self.WORLD_WIDTH = 9
        self.WORLD_HEIGHT = 6

        # possible actions
        self.ACTION_UP = 0
        self.ACTION_DOWN = 1
        self.ACTION_LEFT = 2
        self.ACTION_RIGHT = 3
        self.actions = [self.ACTION_UP, self.ACTION_DOWN, self.ACTION_LEFT, self.ACTION_RIGHT]

        # start and goal state(s)
        self.START_STATE = (2, 0)
        self.GOAL_STATES = [(0, 8)]

        # obstacles
        self.obstacles = [(1, 2), (2, 2), (3, 2), (0, 7), (1, 7), (2, 7), (4, 5)]

        # the size of q value
        self.q_size = (self.WORLD_HEIGHT, self.WORLD_WIDTH, len(self.actions))

        # keep track of current state
        self.STATE = self.START_STATE
        
        # apparently neccessary
        self._reset_next_step = True

    def step(self, action):
        
        # reset if necessary
        if self._reset_next_step:
            return self.reset()
        
        # get x, y for convenience
        x, y = self.STATE
        
        if action == self.ACTION_UP:
            x = max(x - 1, 0)
        elif action == self.ACTION_DOWN:
            x = min(x + 1, self.WORLD_HEIGHT - 1)
        elif action == self.ACTION_LEFT:
            y = max(y - 1, 0)
        elif action == self.ACTION_RIGHT:
            y = min(y + 1, self.WORLD_WIDTH - 1)
        if (x, y) in self.obstacles:
            x, y = self.STATE
          
        # update state
        self.STATE = (x, y)
        
        # check for termination.
        if (x, y) in self.GOAL_STATES:
            reward = 1.0
            self._reset_next_step = True
            return dm_env.termination(reward=reward, observation=self.STATE)
        else:
            return dm_env.transition(reward=0., observation=self.STATE)
    
    def reset(self):
        self._reset_next_step = False
        self.STATE = self.START_STATE
        return dm_env.restart(self.STATE)
        
    def observation_spec(self):
        """Returns the observation spec."""
        pass
#         return specs.BoundedArray(shape=self._board.shape, dtype=self._board.dtype,
#                                   name="board", minimum=0, maximum=1)

    def action_spec(self):
        """Returns the action spec."""
        pass
#         return specs.DiscreteArray(
#             dtype=int, num_values=len(_ACTIONS), name="action")


# ------------------------------ small maze (not used)  ------------------------------ #

# class SmallMaze(Maze):
    
#     def __init__(self):
        
#         # maze width and hight
#         self.WORLD_WIDTH = 3
#         self.WORLD_HEIGHT = 4

#         # possible actions
#         self.ACTION_UP = 0
#         self.ACTION_DOWN = 1
#         self.ACTION_LEFT = 2
#         self.ACTION_RIGHT = 3
#         self.actions = [self.ACTION_UP, self.ACTION_DOWN, self.ACTION_LEFT, self.ACTION_RIGHT]

#         # start and goal state(s)
#         self.START_STATE = (2, 0)
#         self.GOAL_STATES = [(0, 2)]

#         # obstacles
#         self.obstacles = [(0, 1), (2, 1)]

#         # the size of q value
#         self.q_size = (self.WORLD_HEIGHT, self.WORLD_WIDTH, len(self.actions))

#         # keep track of current state
#         self.STATE = self.START_STATE
        
#         # apparently neccessary
#         self._reset_next_step = True
        