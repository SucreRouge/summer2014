#file: policyIterator.py
import pydot
from PIL import Image
import StringIO
import copy

from collections import defaultdict
import random

from vector import *
from numpy import mat, eye

class PolicyIterator:
    gamma = .8

    #Run policy iteration on a transition structure
    def __init__(self, ts, rfs, worth):
        #ts: TransitionStructure
        #    (Every state should have an action)
        #rfs: Vector valued reward function
        #worth: Translation from rewards to ordering
        self.ts = ts
        self.rfs = rfs
        self.worth = worth
        
        #Choose an arbitrary reference policy
        self.pi2 = dict()
        for state in self.ts.getStates():
            self.pi2[state] = random.choice(list(self.ts.getActions(state)))
        
        self.pi = dict() # Working policy

        self.V = dict() # Value function

        while not self.pi == self.pi2:
            self.pi = copy.deepcopy(self.pi2)
            self.pi2 = dict()

            states = list(self.ts.getStates())
            #Compute the value of policy pi
            #Solve V(s) = R(s) + gamma*sum over s' T(s, pi(s), s')*V(s')
            # Can be rewritten as V = R*(I - gamma*X)^-1 with:
            X = mat([[self.ts[(stx, self.pi[stx], sty)] for sty in states]
                 for stx in states])
            R = mat([[self.rfs(st)] for st in states])
            V = (((eye(len(states)) - self.gamma*X).I)*R).A1

            for i in range(len(states)):
                self.V[states[i]] = V[i]
            print self.V

            
            #Improve the policy at each state
            for st in self.ts.getStates():
                value = lambda act: self.worth(self.rfs(st) +
                    self.gamma*sum([self.ts[(st, act, sp)]*self.V[sp]
                                    for sp in states], 
                                   Vector([0]*len(self.rfs))))

                self.pi2[st] = max((value(act), act) 
                                   for act in self.ts.getActions(st))[1]

    def policy(self, st):
        return self.pi[st]

    def displayPolicy(self):
        graph = pydot.Dot(graph_type='digraph')
        for (start, action, dest), prob in self.ts.items():
            if prob: #only display transitions with non-zero prob
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
