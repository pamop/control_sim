# -*- coding: utf-8 -*-
"""
Controllability simulation
pamop @nyu.edu
march 2017
"""

import numpy as np

# Task parameters
nactions = 5
noutcomes = nactions
L = nactions # variable name in paper
M = np.zeros([L,L])
numM = 3 # |M|
M[:numM,:numM] = np.identity(numM)
R = [0,0.2,0.23,0.27,0.3] # Sum to 1 (why?)
c = 0.5

ntrials = 15;

cbar = (1-c)/(L-1)
C = cbar * np.ones([L,L])
for idx in range(0,L):
    if sum(M[:,idx]) == 0:
        C[:,idx] = 1/L

Mbool = M.astype(bool)
C[Mbool] = c

# Simulated subject parameters
alpha = 0.2
beta = 0.3
    

class simsubj(object):
    'Simulated subject'
    
    def __init__(self,L,alpha,beta):
        self.Q = np.ones(L) / L
        self.alpha = alpha;
        self.beta = beta;
    
    def choose_action(self,trial):
        probs = np.zeros(L)
        # Softmax action selection policy
        for x in range(0,L):
            probs[x] = np.exp(self.Q[x]/self.beta)/np.sum(np.exp(np.delete(self.Q,x)/self.beta))
        
        # Normalize (?)
        probs = probs / np.sum(probs)        
        
        # Choose action a with probability p = probs
        a = np.random.choice(np.arange(L),p=probs) 
        a = a.astype(int)
        return a

    def updateQ(self,action,trial_rwd):
        self.Q[action] = self.Q[action] + alpha * trial_rwd
        
        
# Run simulated experiment    
subj1 = simsubj(L,alpha,beta)

# Preallocate storage
actions = np.zeros(ntrials)
outcomes = np.zeros(ntrials)

for trial in range(0,ntrials):
    # Subject makes choice    
    a = subj1.choose_action(trial)
    
    # One of L outcomes occurs
    outcome = np.random.choice(np.arange(L),p=C[:,a])
    trial_rwd = R[outcome]
    
    subj1.updateQ(a,trial_rwd)

    # Save what the subject did    
    actions[trial] = a
    outcomes[trial] = outcome
    
