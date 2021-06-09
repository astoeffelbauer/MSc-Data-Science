import numpy as np


# actions
LOW = 0
HIGH = 1


######## Environment for the parts 1 and 2 of the assignment
class Game:

    def __init__(self):
        self.initial_state = 3
        self.win_state = 6
        self.loss_state = 0

        self.state = self.initial_state
        self.reward = 0.0
        self.is_terminal = False

    # return (next state, reward, is_done)
    def step(self, action):
        # i = self.state

        if action == HIGH:
            WIN_ROUND = np.random.rand() < 0.55
            self.state = self.state + 1 if WIN_ROUND else self.state - 1
            self.reward = -50

        elif action == LOW:
            WIN_ROUND = np.random.rand() < 0.45
            self.state = self.state + 1 if WIN_ROUND else self.state - 1
            self.reward = -10

        else:
            assert False, "Actions can only be LOW (0) and HIGH (1)."

        if self.state == self.win_state:
            self.reward += 1000
            self.is_terminal = True
            # print('WIN!!')

        elif self.state == self.loss_state:
            self.is_terminal = True
            # print('LOSS!!')

        return self.state, self.reward, self.is_terminal

    def reset(self):
        self.state = self.initial_state
        self.reward = 0.0
        self.is_terminal = False
        return self.state


######## Environment for part 3 of the assignment
class EnergyGame:
    
    def __init__(self):
        self.initial_state = (3,10)
        self.win_state = 6
        self.loss_state = 0
        
        self.state = self.initial_state
        self.reward = 0.0
        self.is_terminal = False
        
    def update_energy(self, energy, value):
        return max(min(10, energy+value), 0)

    def step(self, action):
        
        score, energy = self.state
        
        if action == HIGH:
            WIN_ROUND = np.random.rand() < 0.55
            score = score + 1 if WIN_ROUND else score - 1
            energy = self.update_energy(energy, -1)
            self.reward = 0
                
        elif action == LOW:
            WIN_ROUND = np.random.rand() < 0.45
            score = score + 1 if WIN_ROUND else score - 1
            self.reward = 0
                
        else:
            assert False, "Actions can only be LOW (0) and HIGH (1)."
            
        # add energy with prob b
        if np.random.rand() < 0.2:
            energy = self.update_energy(energy, 2)
            
        if score == self.win_state:
            self.reward += 1000
            self.is_terminal = True
            
        elif score == self.loss_state:
            self.is_terminal = True
            
        self.state = (score, energy)
        
        return self.state, self.reward, self.is_terminal

    def reset(self):
        self.state = self.initial_state
        self.reward = 0.0
        self.is_terminal = False
        return self.state