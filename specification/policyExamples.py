from specification import *
from transitionStructure import *
from policyIterator import *

def LittmanHallway(n, p):
    #n: length of hallway in the safe direction
    #p: probability of hitting wall

    #Set up transition structure
    ts = TransitionStructure()
    ts.addAction('start', 'sit', {'start': 1})
    ts.addAction('start','a',{'wall': 1})
    ts.addAction('wall','a',{'goal': 1})
    ts.addAction('goal','a',{'done': 1})
    ts.addAction('done','a',{'done': 1})
    ts.addAction('start','b',{0: 1})
    ts.addAction(0, 'a', {'wall': p, 1: 1-p})
    ts.addAction(n, 'a', {'goal': 1})
    for k in range(1, n):
        ts.addAction(k, 'a', {k+1: 1})

    return ts
    

def testExample():
    ts = LittmanHallway(5, .3)
    rfs = combineReward(
        lambda st: 1 if st == 'goal' else 0,
        lambda st: 1 if st == 'wall' else 0)
    G, W = ID(0), ID(1)
    worth = Lex(G > 0, -W)
    iterator = PolicyIterator(ts, rfs, worth)
    return iterator


if __name__ == '__main__':
    testExample().displayPolicy()
