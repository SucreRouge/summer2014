#file: valueIterator.py

from collections import defaultdict


class ValueIterator:
    
    runs = 100 #Number of iterations to use
    
    #Run value iteration on a transition structure
    def __init__(self, ts, rfs, compare):
        #ts : TransitionStructure
        #rfs : Tuple of reward functions
        #compare : ordering function on tuples
        self.ts = ts
        self.rfs = rfs
        self.ids = len(rfs) #how many identifiers do we have
        self.compare = compare
        
        #Q : dict<(state, action), (val, val, ...)>
        self.Q = defaultdict(lambda: (0,) * self.ids)

        for run in range(runs):
            for st in ts.getStates():
                for act in ts.getActions(st):
                    self.update(st,act)

    #Update Q[st, act] using value iteration                
    def update(self, st, act):
        pass

    #Find the max of a set of values using the new ordering
    #Returns the set of maximal elements
    def max(self, values):
        best = set([])
        
        
        
        
    #Display the resulting policy on the transition structure
    def displayPolicy(self):
        pass


if __name__ == '__main__':
    pass
