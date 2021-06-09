### This file inlcudes all my implementations of the environment models used
### in my project.

import random


# ------------------------------ Simple Model ------------------------------ #

class Model():
    "Simple environment model for dyna-Q agent."
    
    def __init__(self):
        self.model = {}
        
    def update(self, state, action, next_state, reward):
        "Update the model with a new transition."
        if state not in self.model.keys():
            self.model[state] = {}
        self.model[state][action] = (next_state, reward)
    
    def sample(self):
        "Sample a transition uniformly at random."
        # randomly sample (s, a, s', r)
        state = random.sample(self.model.keys(), 1)[0]
        action = random.sample(self.model[state].keys(), 1)[0]
        next_state, reward = self.model[state][action]
        return state, action, next_state, reward
    
    
    
# ------------------------------ Prioirty Sweeping Model ------------------------------ #

class PrioritySweepModel(Model):
    "Environment model for priority sweeping agent."
    
    def __init__(self):
        # super().__init__()
        self.model = {}
        
    def update(self, state, action, next_state, reward):
        "Update the model with a new transition."
        if state not in self.model.keys():
            self.model[state] = {}
        self.model[state][action] = (next_state, reward)
    
    def sample(self):
        "Sample a transition uniformly at random." # actually not required for this agent
        # randomly sample (s, a, s', r)
        state = random.sample(self.model.keys(), 1)[0]
        action = random.sample(self.model[state].keys(), 1)[0]
        next_state, reward = self.model[state][action]
        return state, action, next_state, reward
    
    def get_predecessors(self, state):   
        "Get all possible predecessors of a state."
        
        # store list of predecessor states
        predecessors = []
        
        for state_, d in self.model.items():
            for action, (next_state, reward) in d.items():
                if next_state == state:
                    predecessors.append((state_, action, reward))
                    
        return predecessors