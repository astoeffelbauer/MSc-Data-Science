### This file inlcudes some policies.

import numpy as np


# uniform random policy
def random_policy(q_values):
    return np.random.choice(len(q_values))

# greedy policy
def greedy(q_values):
    return np.argmax(q_values)

# epsilon greedy policy
def epsilon_greedy(q_values, epsilon):
    if np.random.random() > epsilon:
        return np.random.choice([action for action, value in enumerate(q_values) if value == np.max(q_values)])
    else:
        return np.random.choice(len(q_values))
    

