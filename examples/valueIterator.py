#file: valueIterator.py

from collections import defaultdict

#Add sets through their components
def setAdd(setx, sety):
    return {x + y for x in setx for y in sety}

#Sum a list of sets in the way above
def setSum(sets):
    # sets: a list of sets
    if not sets:
        return {} #Nullary sum
    else:
        current = sets[0]
        for x in sets[1:]:
            current = setAdd(current, x)
        return current

#Multiply a tuple by a scalar as if it were a vector
def vecMult(scalar, tup):
    return tuple(scalar * x for x in tup)

#Multiply the contents of a set by a scalar
def setMult(scalar, setx):
    return {vecMult(scalar,x) for x in setx}

#Union a list of sets
def union(sets):
    current = set([])
    for x in sets:
        current = current | x
    return current

class ValueIterator:
    
    runs = 100 #Number of iterations to use
    gamma = 1
    
    #Run value iteration on a transition structure
    def __init__(self, ts, rfs, worth):
        #ts : TransitionStructure
        #rfs : Vector valued reward function
        #worth : tuple of reward values -> tuple in ordering
        self.ts = ts
        self.rfs = rfs
        self.ids = len(rfs(0)) #how many identifiers do we have
        self.worth = worth #evaluate the worth of a tuple
        
        #Q : dict<(state, action), (val, val, ...)>
        self.Q = defaultdict(lambda: {(0,) * self.ids})

        for run in range(self.runs):
            for st in ts.getStates():
                for act in ts.getActions(st):
                    self.update(st,act)

    #Update Q[st, act] using value iteration                
    def update(self, st, act):
        #Calculate future reward estimate
        fut = setSum([setMult(self.ts[(st,act,sp)], 
                             self.max(union(self.Q[(sp,ap)] 
                                            for ap in self.ts.getActions(sp))))
                      for sp in self.ts.getStates()])
        self.Q[(st, act)] = setAdd({self.rfs(st)}, setMult(self.gamma, fut))

    #Find the max of a set of values using the new ordering
    #Returns the set of maximal elements
    def max(self, values):
        best = set([])
        for val in values: #go through comparing each value
            if all(self.worth(val) == self.worth(elem) for elem in best):
                best.add(val) #Equal to other best elements
            elif all(self.worth(val) > self.worth(elem) for elem in best):
                best = {val} #Better than previous guess
        
        return best
        
    #Display the resulting policy on the transition structure
    def displayPolicy(self):
        pass


if __name__ == '__main__':
    pass
