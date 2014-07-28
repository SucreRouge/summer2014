#file: valueIterator.py

from collections import defaultdict


class ValueIterator:
    
    runs = 100 #Number of iterations to use
    
    #Run value iteration on a transition structure
    def __init__(self, ts, rfs, worth):
        #ts : TransitionStructure
        #rfs : Tuple of reward functions
        #worth : tuple of reward values -> tuple in ordering
        self.ts = ts
        self.rfs = rfs
        self.ids = len(rfs) #how many identifiers do we have
        self.worth = worth #evaluate the worth of a tuple
        
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
        for val in values: #go through comparing each value
            if all(worth(val) == worth(elem) for elem in best):
                best.add(val) #Equal to other best elements
            elif all(worth(val) > worth(elem) for elem in best):
                best = {val} #Better than previous guess
        
        return best
        
    #Display the resulting policy on the transition structure
    def displayPolicy(self):
        pass


if __name__ == '__main__':
    pass
