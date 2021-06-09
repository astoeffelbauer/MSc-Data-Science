# this file includes the implementations of my RL agents

import numpy as np
import heapq

# rl
import acme
from acme.agents.tf.mcts import search
from acme.agents.tf.mcts.models.simulator import Simulator

# custom
from environments import Maze
from policies import epsilon_greedy
from models import Model, PrioritySweepModel
from utils import sarsa_update, q_learning_update


# ------------------------------ SARSA Agent ------------------------------ #

class SarsaAgent(acme.Actor):
    
    def __init__(self, env_specs=None, epsilon=0.1, step_size=0.1):
        
#         number_of_states = observation_spec.num_states
#         number_of_actions = action_spec.num_values
        
        self.Q = np.zeros((6,9,4))
        
        # epsilon for policy and step_size for TD learning
        self.epsilon = epsilon
        self.step_size = step_size
        self.gamma = 1.0
        
        # set policy and behavior policy
        self.policy = None
        self.behavior = lambda q_values: epsilon_greedy(q_values, self.epsilon)
        
        # store timestep, action, next_timestep
        self.timestep = None
        self.action = None
        self.next_timestep = None
    
    def select_action(self, observation):
        "Choose an action according to the behavior policy."
        return self.behavior(self.Q[observation])

    def observe_first(self, timestep):
        "Observe the first timestep of the trajectory."
        self.timestep = timestep

    def observe(self, action, next_timestep):
        "Observe the next timestep."
        self.action = action
        self.next_timestep = next_timestep
        
    def update(self):
        "Update the policy."
        
        # get variables for convenience
        state = self.timestep.observation
        _, reward, discount, next_state = self.next_timestep
        action = self.action
        
        # sample a next action
        next_action = self.behavior(self.Q[next_state])

        # compute and apply the TD error
        td_error = reward + discount * self.Q[next_state][next_action] - self.Q[state][action]
        self.Q[state][action] += self.step_size * td_error
        
        # finally, set timestep to next_timestep
        self.timestep = self.next_timestep
        

# ------------------------------ Q-Learning Agent ------------------------------ #

class QAgent(acme.Actor):
    
    def __init__(self, env_specs=None, epsilon=0.1, step_size=0.1):
        
#         number_of_states = observation_spec.num_states
#         number_of_actions = action_spec.num_values
        
        self.Q = np.zeros((6,9,4))
        
        # epsilon for policy and step_size for TD learning
        self.epsilon = epsilon
        self.step_size = step_size
        self.gamma = 1.0
        
        # set policy and behavior policy
        self.policy = None
        self.behavior = lambda q_values: epsilon_greedy(q_values, self.epsilon)
        
        # store timestep, action, next_timestep
        self.timestep = None
        self.action = None
        self.next_timestep = None
    
    def select_action(self, observation):
        return self.behavior(self.Q[observation])

    def observe_first(self, timestep):
        self.timestep = timestep

    def observe(self, action, next_timestep):
        self.action = action
        self.next_timestep = next_timestep
        
    def update(self):
        
        # get variables for convenience
        state = self.timestep.observation
        _, reward, discount, next_state = self.next_timestep
        action = self.action
        
        # Q-value update
        td_error = reward + discount * np.max(self.Q[next_state]) - self.Q[state][action]        
        self.Q[state][action] += self.step_size * td_error
        
        # finally, set timestep to next_timestep
        self.timestep = self.next_timestep
        
        

# ------------------------------ Dyna-Q Agent ------------------------------ #

class DynaQAgent(QAgent):
    
    def __init__(self, env_specs=None, epsilon=0.1, step_size=0.1, planning_steps=0):
        super().__init__(env_specs, epsilon, step_size)
        self.planning_steps = planning_steps
        self.alpha = step_size
        
        # init model for planning
        self.model = Model()
        
    def update(self):
        
        # get variables for convenience
        state = self.timestep.observation
        _, reward, discount, next_state = self.next_timestep
        action = self.action
        
        # compute and apply the TD error
        self.Q[state][action] = q_learning_update(self.Q[state][action], self.Q[next_state], 
                                                  reward, self.step_size, self.gamma)
        
        # apply planning update
        self.model.update(state, action, next_state, reward)
        
        for i in range(self.planning_steps):
            pstate, paction, pnext_state, preward = self.model.sample()
            self.Q[pstate][paction] = q_learning_update(self.Q[pstate][paction], self.Q[pnext_state], 
                                                        preward, self.alpha, self.gamma)
        
        # finally, set timestep to next_timestep
        self.timestep = self.next_timestep
     
    
# ------------------------------ Priority Sweeping Agent ------------------------------ #
        
class PrioirtySweepAgent(QAgent):
    
    def __init__(self, env_specs=None, epsilon=0.1, step_size=0.1, planning_steps=1):
        super().__init__(env_specs, epsilon, step_size)
        
        self.alpha = 0.1
        
        # number of planning steps
        self.planning_steps = planning_steps
        
        # init model and prioirty queue for planning
        self.model = PrioritySweepModel()
        self.priority_queue = []
        self.priority_thresh = 0. # set to 0, so all elements are added
        
        ### Minor comment: Perhaps it would be more practical to include the prioirty queue
        ### in the environment model and adapte the sampling method such that it always 
        ### returns the item with the highest prioirty. However, it is not a natural part 
        ### of the model but rather of the agent, which is why I implemented it here.
        
    def update(self):
        "Update the policy thorugh Q-learning and prioritized sweeping."
        
        # get variables for convenience
        state = self.timestep.observation
        _, reward, discount, next_state = self.next_timestep
        action = self.action
        
        # compute and apply the TD error
        self.Q[state][action] = q_learning_update(self.Q[state][action], self.Q[next_state], 
                                                  reward, self.alpha, self.gamma)
        
        # update the environment model
        self.model.update(state, action, next_state, reward)
        
        # compute prioirty and add to queue
        priority = abs( reward + self.gamma*np.max(self.Q[next_state]) - self.Q[state][action] )
        
        # only add to queue if min threshold
        if priority > self.priority_thresh:
            heapq.heappush(self.priority_queue, (-priority, (state, action)))
        
        # repeat sweep for each planning step
        for i in range(self.planning_steps):
                        
            if not self.priority_queue:
                break
            
            # get (s,a) with higest prioirty
            _, (pstate, paction) = heapq.heappop(self.priority_queue)
            pnext_state, preward = self.model.model[pstate][paction]
            
            self.Q[pstate][paction] = q_learning_update(self.Q[pstate][paction], self.Q[pnext_state], 
                                                        preward, self.alpha, self.gamma)
            
            # sweep
            predecessors = self.model.get_predecessors((pstate))
            for state_, action_, reward_ in predecessors:
                # _, reward_sweep = self.model.model[state_][action_]
                
                priority = abs( reward_ + self.gamma*np.max(self.Q[pstate]) - self.Q[state_][action_] )
        
                if priority > self.priority_thresh:
                    heapq.heappush(self.priority_queue, (-priority, (state_, action_)))
        
        # finally, set timestep to next_timestep
        self.timestep = self.next_timestep
        
        
# ------------------------------ MCTS Agent ------------------------------ #

class MCTSAgent(acme.Actor):
    
    def __init__(self, env_specs=None, epsilon=0.1, step_size=0.1):
        
        self.epsilon = epsilon
        self.step_size = step_size

        # state values
        self.V = np.zeros((6,9))

        # for mcts
        self.model = Simulator(Maze())
        self.search_policy = search.bfs
        self.num_actions = 4
        self.eval_fn = lambda state: (np.ones(self.num_actions) / self.num_actions, self.V[state])
        
        # store timestep, action, next_timestep
        self.timestep = None
        self.action = None
        self.next_timestep = None
    
    def select_action(self, observation):
        "Choose an action based on a Monte Carlo tree search."
        
        # At decision time, the MCTS agent expands a search tree, simulates experience from the model
        # and choses the best action. The estimated returns are not used to back up the action values.
        # In fact, this agent only learns state values using one-step temporal difference learning.
        # These state values are used when deciding where to expand the search tree.

        if self.model.needs_reset:
            self.model.reset(observation)
        
        # search tree
        root = search.mcts(
            observation=observation,
            model=self.model,
            search_policy=self.search_policy,
            evaluation=self.eval_fn,
            num_simulations=100,
            num_actions=self.num_actions)
        
        # choose best action
        values = np.array([c.value for c in root.children.values()])
        best_action = search.argmax(values)
        return best_action

        # probs = search.visit_count_policy(root)
        # action = np.int32(np.random.choice(self.num_actions, p=probs))
        # return action

    def observe_first(self, timestep):
        self.timestep = timestep

    def observe(self, action, next_timestep):
        self.next_timestep = next_timestep
        
        # update the model
        self.model.update(self.timestep, action, next_timestep)

    def update(self):
        "Update the state values using one-step temporal difference learning."

        # get variables for convenience
        state = self.timestep.observation
        _, reward, discount, next_state = self.next_timestep

        # compute and apply td error
        td_error = reward + discount * self.V[next_state] - self.V[state]
        self.V[state] += self.step_size * td_error

        # finally, set timestep to next_timestep
        self.timestep = self.next_timestep
        