# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 11:55:48 2017

@author: pamop
"""

import numpy as np
import matplotlib.pyplot as plt

# Task parameters
nactions = 5
noutcomes = nactions
L = nactions # variable name in paper
M = np.zeros([L,L])
numM = 1 # |M|
M[:numM,:numM] = np.identity(numM)
R = [0.3,0,0,0,0.7] #[0,0.2,0.23,0.27,0.3] # Sum to 1
c = 0.8

ntrials = 200
nsubj = 50

cbar = (1-c)/(L-1)
C = cbar * np.ones([L,L])
for idx in range(0,L):
    if sum(M[:,idx]) == 0:
        C[:,idx] = 1/L

Mbool = M.astype(bool)
C[Mbool] = c


    

class simsubj(object):
    'Simulated subject'
    
    def __init__(self,L,alpha,beta):
        self.Q = np.ones(L) / L
        self.alpha = alpha
        self.beta = beta
    
    def choose_action(self,trial):
        probs = np.zeros(L)
        # Softmax action selection policy
        for x in range(0,L):
            probs[x] = np.exp(self.Q[x]/self.beta)/np.sum(np.exp(self.Q/self.beta))       
        
        # Choose action a with probability p = probs
        a = np.random.choice(np.arange(L),p=probs) 
        a = a.astype(int)
        return a

    def updateQ(self,action,trial_rwd):
        self.Q[action] = self.Q[action] + alpha * (trial_rwd - self.Q[action])
        
        
# Run simulated experiment
nLRcases = 3
avgrwd = np.zeros(nLRcases,ntrials) 
 
for LRcase in range(0,nLRcases):  
    
    
    actions = np.zeros(nsubj,ntrials)
    outcomes = np.zeros(nsubj,ntrials)
    trial_rwds = np.zeros(nsubj,ntrials)
    
    for subject in range(0,nsubj):
        # Simulated subject parameters
        alpha = 0.01 * 10**LRcase
        beta = 0.01 * 10**LRcase
        subj = simsubj(L,alpha,beta)
    
    
        for trial in range(0,ntrials):
            # Subject makes choice    
            a = subj.choose_action(trial)
            
            # One of L outcomes occurs
            outcome = np.random.choice(np.arange(L),p=C[:,a])
            trial_rwd = R[outcome]
            
            subj.updateQ(a,trial_rwd)
        
            # Save what the subject did    
            actions[subject,trial] = a
            outcomes[subject,trial] = outcome
            trial_rwds[subject,trial] = trial_rwd
            
        avgrwd[LRcase,:] = np.mean(trial_rwds,axis=0)
        
# Visualize
plt.plot(avgrwd[])