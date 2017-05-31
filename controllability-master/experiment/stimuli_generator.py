import random
from math import floor

def create_stimuli(condition, counterbalance, dims=3, options=4, nblocks=7, trialsperblock=20):
    exp_definition = []
    for i in range(nblocks):
        outcomepairs = [-1] * dims
        proportions = [-1] * dims
        if i < nblocks - 1:
            outcomepairs[counterbalance] = random.randint(0, options-1)
        else:
            seconddim = random.choice([x for x in range(dims) if x != counterbalance])
            outcomes = random.sample(range(options), 2)
            outcomepairs[counterbalance] = outcomes[0]
            outcomepairs[seconddim] = outcomes[1]
        actionmeans = []
        for o in range(options):
            actionmeans.append([])
        for d in range(dims):
            if outcomepairs[d] == -1:
                proportions[d] = random.random()
            for o in range(options):
                if outcomepairs[d] == o:
                    actionmeans[o].append(1)
                elif outcomepairs[d] == -1:
                    actionmeans[o].append(proportions[d])
                else:
                    actionmeans[o].append(0)

        exp_definition.append(
            {"outcomepairs": outcomepairs,
             "proportions": proportions,
             "trials": trialsperblock,
             "actionmeans": actionmeans,
             "block": i,
            }
        )

    return exp_definition
