#file: hallway.py
#Use our specification to solve Littman's hallway problem

from transitionStructure import *
from specification import *
from valueIterator import *


if __name__ == '__main__':
    p = .3 #Chance of stochastically hitting wall
    n = 5 # length of hallway

    #Set up the transition structure
    ts = TransitionStructure()
    ts.addAction('start','sit',{'start': 1})
    ts.addAction('start','a',{'wall': 1})
    ts.addAction('wall','a',{'goal': 1})
    ts.addAction('goal','a',{'goal': 1})
    ts.addAction('start','b',{0: 1})
    ts.addAction(0, 'a', {'wall': p, 1: 1-p})
    ts.addAction(n, 'a', {'goal': 1})
    for k in range(1, n):
        ts.addAction(k, 'a', {k+1: 1})
    
    #And the reward function
    G = lambda st: 1 if st == 'goal' else 0
    W = lambda st: 1 if st == 'wall' else 0
    rfs = combineReward(G, W)
    worth = Lexicographic(Gt(ID(0), Number(0)), Negate(ID(1))).worth
    
    vi = ValueIterator(ts, rfs, worth)

    vi.displayPolicy()
    
