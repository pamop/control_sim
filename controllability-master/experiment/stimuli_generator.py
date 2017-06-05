import random
from math import floor
import numpy as np

def create_stimuli(condition, counterbalance, nactions=6, std_bw = [0,1,2,3], std_wi = [0,1,2,3], rwdmean=20, nblocks=16, trialsperblock=20):
    exp_definition = []
    std_bw[std_bw==0] = 1e-9
    std_wi[std_wi==0] = 1e-9
    stdperm = np.array(np.meshgrid(std_bw,std_wi)).T.reshape(-1,2)
    if len(stdperm) > nblocks:
        console.log('fewer blocks than std bw/wi permutations')
    else:
        while len(stdperm) < nblocks:
            stdperm = np.concatenate((stdperm,stdperm))

    # random block order
    np.random.shuffle(stdperm)

    # maybe change rwd mean based on sbw and swi?

    for i in range(nblocks):
        sbw, swi = stdperm[i,0], stdperm[i,1]
        R = R * round(sbw) / np.std(np.random.normal(0,1,nactions)
        R = np.round(R - np.mean(R) + rwdmean)
        V = swi**2 * np.ones(nactions) # Variance 

        exp_definition.append(
            {"R": R,
             "V": V,
             "sbw": sbw,
             "swi": swi,
             "rwdmean":rwdmean,
             "trials": trialsperblock,
             "block": i,
            }
        )

    return exp_definition
