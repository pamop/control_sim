# -*- coding: utf-8 -*-
"""
Created on Wed May 24 12:41:12 2017

@author: pamop
"""

import numpy as np
import fnmatch
import os
import matplotlib.pyplot as plt


# Import data
for file in os.listdir('.'):
    if fnmatch.fnmatch(file, 'titration_0525*.npz'):
        np.load(file)
# resparr, allRV, allrwd, allact, allsig
#resparr = 5 x 5
#allRV = 2 x n=6 x 25
#allrwd = 25 x ntrials=20
#allact = 25 x ntrials=20
#allsig = 25 x 2 ([:,0]=sbw, [:,1]=swin)

ntrials = 20
n = 6

optpercent = np.zeros([5,5])

for block in range(0,25):
    
    R, V = allRV[0,:,block], allRV[1,:,block]
    optact = np.argmax(R)
#    optpercent[allsig[block,0],allsig[block,1]] = np.sum(allact[block,:]==optact)
    axisloc = round(allsig[block,0]*5 + allsig[block,1]+1)
    rwdofactchosen = np.zeros(ntrials)
    for i in range(0,n):
        rwdofactchosen[allact[block,:]==i] = R[i]
    
    # Visualize
    plt.subplot(5,5,axisloc)
#    plt.xlim((np.min(allRV[0,:,:]),np.max(allRV[0,:,:])))
    plt.ylim((0,ntrials))
#    plt.hist(rwdofactchosen,bins=16)
    plt.xlim((np.min(allrwd),np.max(allrwd)))
    plt.hist(allrwd[block,:])
    if axisloc != 21:
        plt.tick_params(axis='both', which='both', bottom='off', top='off', labelbottom='off', right='off', left='off', labelleft='off')
#    if block%4==0:
       
#    plt.subplot(5,5,axisloc)
#    plt.bar(1,np.sum(allact[block,:]==optact))
#    plt.ylim((0, 20))

#plt.bar()
    
#
## Visualize
#plt.bar([1,2,3],[E_robot,E_RL,E_omni])
##plt.plot(avgrwd[0,:],'ro',avgrwd[1,:],'bo',avgrwd[2,:],'go')
#plt.xlabel('robot, RL, omniscient agent')
#plt.ylabel('reward earned')
#plt.show()
#
#x = np.arange(1,ntrials + 1)
#plt.plot(x,a_RL+1,'bo-',x,a_robot+1,'go-',x,a_omni+1,'ro-')
#plt.legend(['RL','robot','omni'])
#plt.xlabel('trial number')
#plt.ylabel('action chosen')
#plt.show()