# -*- coding: utf-8 -*-
"""
Created on Mon May 15 09:45:29 2017

@author: pamop
"""

import numpy as np
import matplotlib.pyplot as plt
import time

def practice_expt(R,V,ntrials):
    print('Welcome to the experiment!')
    
    L = len(R)
    E = 0
    a_subj = np.zeros(ntrials)  
    rwd_subj = np.zeros(ntrials)
    
    for trial in range(0,ntrials):
        print('TRIAL {}'.format(trial+1))
        print('Make a choice:')
        for i in range(1,L+1):
            print('[{}] '.format(i), end='')
        a = int(input('choice: ')) - 1
        a_subj[trial] = a
        
        trial_rwd = np.round(np.random.normal(R[a],np.sqrt(V[a])))
        rwd_subj[trial] = trial_rwd
        E += trial_rwd
        
        print('\nYou received {} points!\n\n'.format(trial_rwd))
        time.sleep(1)
        
    # Visualize
    print('TOTAL REWARD EARNED: {}'.format(E))
   
    x = np.arange(1,ntrials + 1)
    plt.plot(x,rwd_subj,'ko--')
    #plt.plot(avgrwd[0,:],'ro',avgrwd[1,:],'bo',avgrwd[2,:],'go')
    plt.xlabel('trial number')
    plt.ylabel('reward received')
    plt.show()
    
    plt.plot(x,a_subj+1,'ko-')
    plt.xlabel('trial number')
    plt.ylabel('action chosen')
    plt.show()
    
    
    
#RUN EXPERIMENT!
ntrials = int(input('Num trials: '))
print('Choose an environment: 1 (high controllability) or 2 (low control)')

env = int(input('Environment: '))
if env == 1:
    # Environ 1: No w/in variance, all between
    R = [3,7,6,4,3,1] #mean = 4, variance = 24
    V = [0.0001,0.0001,0.0001,0.0001,0.0001,0.0001]
elif env == 2:
    # Environ 2: No w/in variance, all between
    R = [9,9,9,9,9,9] #reward mean = 9, variance = 24 (std = 4.9)
    V = [24,24,24,24,24,24] #variance
else:
    print('start over and choose 1 or 2!!')
    
practice_expt(R,V,ntrials)