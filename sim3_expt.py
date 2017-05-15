# -*- coding: utf-8 -*-
"""
New file

contact: pamop@nyu.edu
date: 5/3/2017
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import time

class RLagent(object):
    'Simulated RL subject'
    
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
        self.Q[action] = self.Q[action] + self.alpha * (trial_rwd - self.Q[action])
        
class robotagent(object):
    'Simulated robot agent'
    
    def __init__(self,L):
        self.L = L        
        
    def choose_action(self,trial):
        a = trial%L
        return a

class omniscientagent(object):
    'Simulated omniscient agent'
    def __init__(self,R):
        self.R = R
        
    def choose_action(self,trial):
        a = np.argmax(R)
        return a

def runexpt(R,V,ntrials):
    # Run simulated experiment
    L = len(R)
    alpha = 0.008
    beta = 0.1
    RLsubj = RLagent(L,alpha,beta)
    robot = robotagent(L)
    omniagent = omniscientagent(R)
    
    # Expected rewards
    E_RL,E_robot,E_omni = 0,0,0
    a_RL,a_robot,a_omni = np.zeros(ntrials),np.zeros(ntrials),np.zeros(ntrials)
    
    for trial in range(0,ntrials):
        #RL
        a = RLsubj.choose_action(trial)
        trial_rwd = np.round(np.random.normal(R[a],np.sqrt(V[a]))) #deterministic
        RLsubj.updateQ(a,trial_rwd)
        E_RL += trial_rwd
        a_RL[trial] = a
        
        #Robot
        a = robot.choose_action(trial)
        E_robot += np.round(np.random.normal(R[a],np.sqrt(V[a])))
        a_robot[trial] = a        
        
        #Omni
        a = omniagent.choose_action(trial)
        E_omni += np.round(np.random.normal(R[a],np.sqrt(V[a])))
        a_omni[trial] = a
    
    # Visualize
    plt.bar([1,2,3],[E_robot,E_RL,E_omni])
    #plt.plot(avgrwd[0,:],'ro',avgrwd[1,:],'bo',avgrwd[2,:],'go')
    plt.xlabel('robot, RL, omniscient agent')
    plt.ylabel('reward earned')
    plt.show()
    
    x = np.arange(1,ntrials + 1)
    plt.plot(x,a_RL+1,'bo-',x,a_robot+1,'go-',x,a_omni+1,'ro-')
    plt.legend(['RL','robot','omni'])
    plt.xlabel('trial number')
    plt.ylabel('action chosen')
    plt.show()

# Task parameters
nactions = 6
L = nactions # variable name in paper

# Environ 1: No w/in variance, all between
R = [3,7,6,4,3,1] #mean = 4, variance = 24
V = [0.0001,0.0001,0.0001,0.0001,0.0001,0.0001] #each action deterministically leads to that reward

ntrials = 20
#nsubj = 300

runexpt(R,V,ntrials)

# Environ 2: No w/in variance, all between
R = [9,9,9,9,9,9] #reward mean = 9, variance = 24 (std = 4.9)
V = [24,24,24,24,24,24] #variance

ntrials = 20
#nsubj = 300
runexpt(R,V,ntrials)

