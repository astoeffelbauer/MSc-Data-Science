import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ------------------------------ update functions ------------------------------ #

def sarsa_update(qsa, next_qsa, r, alpha=0.1, gamma=1.0):
    "Perform sarsa update step."
    return qsa + alpha * (r + gamma * next_qsa - qsa)

def q_learning_update(qsa, next_qs, r, alpha=0.1, gamma=1.0):
    "Perform q-learning update step."
    return qsa + alpha * (r + gamma * np.max(next_qs) - qsa)


# ------------------------------ helper functions ------------------------------ #

def print_policy(env, Q, with_start=False):
    policy = np.argmax(Q, axis=-1)
    policy[env.GOAL_STATES[0]] = 6
    if with_start: 
        policy[env.START_STATE] = 7
    for i in env.obstacles:
        policy[i] = 8
    policy_string = np.array2string(policy).replace('0', '^').replace('3', '>').replace('1', 'v').replace('2', '<')
    policy_string = policy_string.replace('6', 'G').replace('7', 'S').replace('8', '|')
    print(policy_string)
    
    
def plot_episode_len(df):
    fig, ax = plt.subplots(figsize=(10,5))
    plt.plot(df['episode_length'])
    plt.title('Epside vs Episode Length')
    plt.xlabel('Epsiode')
    plt.ylabel('Episode Length')
    # plt.show()
    

def plot_episode_len_std(dfs):
    fig, ax = plt.subplots(figsize=(10,5)) 
    df = pd.concat(dfs).groupby(level=0)
    
    mean = df['episode_length'].mean()    
    plt.plot(mean)
    
    std = df['episode_length'].std()
    plt.fill_between(range(50), mean-std, mean+std, color='b', alpha=.1)

    plt.title('Epside vs Episode Length')
    plt.xlabel('Epsiode')
    plt.ylabel('Episode Length')
    # plt.show()
    