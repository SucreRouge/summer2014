#file: valueIterator.py
import pydot
from PIL import Image
import StringIO
import copy

from collections import defaultdict

#Add tuples as if they were vectors
#warning: if tuples have different lengths then only the shortest length will be used
def vecAdd(tupx, tupy):
    return tuple(x + y for x,y in zip(tupx, tupy))

#Add sets through their components
def setAdd(setx, sety):
    return {vecAdd(x, y) for x in setx for y in sety}

#Sum a list of sets in the way above
def setSum(sets):
    # sets: a list of sets
    if not sets:
        return set([]) #Nullary sum
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
    gamma = .9
    
    #Run value iteration on a transition structure
    def __init__(self, ts, rfs, worth):
        #ts : TransitionStructure
        #rfs : Vector valued reward function
        #worth : tuple of reward values -> tuple in ordering
        self.ts = ts

#        for state in ts.getStates(): #every state should have an action
#            assert ts.getActions(state)

        self.rfs = rfs
        self.worth = worth #evaluate the worth of a tuple
        
        #Q : dict<(state, action), (val, val, ...)>
        self.Q = defaultdict(lambda: {(0,) * len(self.rfs)})

        for run in range(self.runs):
            self.Qnext = copy.deepcopy(self.Q)
            for st in ts.getStates():
                for act in ts.getActions(st):
                    self.update(st,act)
            self.Q = self.Qnext

    #Update Q[st, act] using value iteration                
    def update(self, st, act):
        #Calculate future reward estimate
        fut = setSum([setMult(self.ts[(st,act,sp)], 
                             self.max(union(self.Q[(sp,ap)] 
                                            for ap in self.ts.getActions(sp))))
                      for sp in self.ts.getStates()])
        

        self.Qnext[(st, act)] = setAdd({self.rfs(st)}, setMult(self.gamma, fut))


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
        
    #Return the set of maximal actions from a state
    def policy(self, st):
        best = self.max(union(self.Q[(st, act)] # the maximal values
                              for act in self.ts.getActions(st)))
        #Inefficiently find the corresponding actions
        return {act for act in self.ts.getActions(st)
                if self.Q[(st, act)] & best}

        
    #Display the resulting policy on the transition structure
    def displayPolicy(self):
        graph = pydot.Dot(graph_type='digraph')
        for (start, action, dest), prob in self.ts.items():
            if prob: #Only display transitions with prob > 0
                if prob < 1:
                    label = "%0.1f%s" % (prob, str(action))
                else:
                    label = str(action)
                color = "purple" if action in self.policy(start) else "black"
                edge = pydot.Edge(str(start), str(dest), label=label, color=color)
                graph.add_edge(edge)
        #Display the graph to the screen
        png_str = graph.create_png(prog='neato')
        data = StringIO.StringIO(png_str)
        img = Image.open(data)
        img.show()

if __name__ == '__main__':
    pass
