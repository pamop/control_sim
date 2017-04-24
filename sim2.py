# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 11:55:48 2017

@author: pamop
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import time

# Task parameters
nactions = 5
noutcomes = nactions
L = nactions # variable name in paper
M = np.zeros([L,L])
numM = 5 # |M|
M[:numM,:numM] = np.identity(numM)
R = [0.3,0,0,0,0.7] #[0,0.2,0.23,0.27,0.3] # Sum to 1
c = 0.8

ntrials = 200
nsubj = 300

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
avgrwd = np.zeros([nLRcases,ntrials]) 
 
for LRcase in range(0,nLRcases):  
    
    
    actions = np.zeros([nsubj,ntrials])
    outcomes = np.zeros([nsubj,ntrials])
    trial_rwds = np.zeros([nsubj,ntrials])
    
    for subject in range(0,nsubj):
        # Simulated subject parameters
        alpha = 0.01 * 10**LRcase
        beta = 0.01
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
plt.plot(avgrwd[0,:],'ro',avgrwd[1,:],'bo',avgrwd[2,:],'go')
plt.xlabel('trial')
plt.ylabel('average reward')
plt.legend(('LR=0.01','LR=0.1','LR=1.0'),loc='lower right')

#plt.plot(actions[1,:],'o')
#plt.plot(np.mean(actions,axis=0),'o')

## hist
#observations = [range(10),range(20),range(50),range(200)]
#filenames = []
#for ii in range(0,4):
##    subjhist, edges = np.histogram(actions[:,ii*50:ii*50+49],bins=[0, 1, 2, 3, 4])
#    plt.hist(actions[1,observations[ii]],bins=5)
#    fname = 'hist' + str(ii)
#    filenames.append(fname)
#    plt.title('|M|=4,LR=1')
#    plt.savefig(fname)
#    plt.cla()
##    time.sleep(1)


#filenames = []
#for ii in range(0,4):
#    plt.hist(np.mean(actions[:,ii*50:ii*50 + 49],axis=0),bins=5)
#    fname = 'hist' + str(ii)
#    filenames.append(fname)
#    plt.savefig(fname)
#    plt.cla()
#
##stats.binned_statistic(np.ones(ntrials), np.mean(actions,axis=0), 'mean', bins=20)
#
#import imageio
#images = []
#for filename in filenames:
#    images.append(imageio.imread(filename))
#imageio.mimsave('/Users/pamop/Documents/gureckis lab/control_sim/test.gif', images)