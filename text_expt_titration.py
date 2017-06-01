# -*- coding: utf-8 -*-
"""
Created on Thu May 18 11:27:55 2017

@author: pamop
"""

import numpy as np
#import matplotlib.pyplot as plt
from datetime import datetime
#import time
import sys
import scipy.io as sio

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
        while True:
            try:
                a = int(input('choice: ')) - 1
                break
            except ValueError:
                print("Invalid number, please try again")
        a_subj[trial] = a
        
        trial_rwd = np.round(np.random.normal(R[a],np.sqrt(V[a])))
        rwd_subj[trial] = trial_rwd
        E += trial_rwd
        
        print('\nYou received {} points!\n\n'.format(trial_rwd))
        
    # Visualize
    print('TOTAL REWARD EARNED: {}'.format(E))
    
    return rwd_subj, a_subj
   
#    x = np.arange(1,ntrials + 1)
#    plt.plot(x,rwd_subj,'ko--')
#    #plt.plot(avgrwd[0,:],'ro',avgrwd[1,:],'bo',avgrwd[2,:],'go')
#    plt.xlabel('trial number')
#    plt.ylabel('reward received')
#    plt.show()
#    
#    plt.plot(x,a_subj+1,'ko-')
#    plt.xlabel('trial number')
#    plt.ylabel('action chosen')
#    plt.show()
    
    
#mu, sigma, n = 0, 4, 100
#s = np.random.normal(mu,sigma,n)
#np.mean(s)
#np.std(s, ddof=1)
#
#x = np.random.normal(mu,sigma, 10)
#x = x - np.mean(x)
#x = x/np.std(x)



#RUN EXPERIMENT!
ntrials = 20
n = 6
pointmean = 15
# initialize
resparr = np.zeros([5,5])
allRV = np.zeros([2,n,25])
allrwd = np.zeros([25, ntrials])
allact = np.zeros([25, ntrials])
allsig = np.zeros([25,2])

for i in range(0,25):
#    swin, sbw= np.random.choice([1e-15,1,2,3,4]), np.random.choice([1e-15,1,2,3,4])
#    while resparr[int(sbw),int(swin)] != 0:
#        swin, sbw= np.random.choice([1e-15,1,2,3,4]), np.random.choice([1e-15,1,2,3,4])
#    
    stdperm = np.array(np.meshgrid([1e-15,1,2,3,4],[1e-15,1,2,3,4])).T.reshape(-1,2)
    if len(stdperm) > nblocks:
        print('fewer blocks than std bw/wi permutations')
    else:
        while len(stdperm) < nblocks:
            stdperm = np.concatenate((stdperm,stdperm))

    x = np.random.normal(0,1,n)
    x = x * round(sbw) / np.std(x)
    x = x - np.mean(x) + pointmean
    R = np.round(x)
    V = swin**2 * np.ones(n)

    allsig[i,:] = [sbw,swin] 
    
    allRV[0,:,i] = R
    allRV[1,:,i] = V
    
    allrwd[i,:], allact[i,:] = practice_expt(R,V,ntrials)
    
    while True:
        try:
            envguess = int(input("What environment? High (1) or low (2) control? "))
            if envguess == 0:
                print("user input indicated exit")
                sys.exit()  
            break
        except ValueError:
            print("Invalid number, please try again")
    resparr[int(sbw),int(swin)] = envguess

filename = "titration_" + datetime.now().strftime("%m%d%y-%H%M%S")
np.savez(filename + ".npz",resparr=resparr, allRV=allRV, allrwd=allrwd, allact=allact, allsig=allsig, pointmean=pointmean)


alldatadict = {'resparr':resparr, 
               'allRV':allRV, 
               'allrwd':allrwd, 
               'allact':allact, 
               'allsig':allsig,
               'pointmean':pointmean,
               'ntrials':ntrials,
               'n':n
               }
sio.savemat(filename + ".mat", alldatadict)

a=0
for i in range(1,21):
    a += 8*i