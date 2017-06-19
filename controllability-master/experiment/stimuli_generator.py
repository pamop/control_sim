#import random
from math import floor
import numpy as np
import json

def create_stimuli(condition, counterbalance, nactions=6, std_bw='[0,1,2,3]', std_wi='[0,1,2,3]', rwdmean=20, nblocks=16, trialsperblock=20):
    exp_definition = []
    # t_bw = np.arange(std_bw + 1)
    # t_wi = np.arange(std_wi + 1)
    std_bw = json.loads(std_bw)
    std_wi = json.loads(std_wi)
    std_bw[std_bw==0] = 1e-9
    std_wi[std_wi==0] = 1e-6
    stdperm = np.array(np.meshgrid(t_bw,t_wi)).T.reshape(-1,2)
    while len(stdperm) < nblocks:
        stdperm = np.concatenate((stdperm,stdperm))

    # random block order
    np.random.shuffle(stdperm)

    # maybe change rwd mean based on sbw and swi?

    for i in range(nblocks):
        sbw, swi = stdperm[i,0], stdperm[i,1]
        x = np.random.normal(0,1,nactions)
        x = x * round(sbw) / np.std(x)
        x = x - np.mean(x) + rwdmean
        R = np.round(x)
        V = swi**2 * np.ones(nactions) # Variance 

        exp_definition.append(
            {"R": R.tolist(),
             "V": V.tolist(),
             "sbw": sbw.tolist(),
             "swi": swi.tolist(),
             "rwdmean":rwdmean,
             "trials": trialsperblock,
             "block": i,
            }
        )

    return exp_definition
