from zoo import *
from specification import *


#Ratio choice example, cannot be made with normal reward functions to choose x.
def ratioExample():
    A, B = ID(0), ID(1)
    worth = A | B
    ratioChoice(worth).displayPolicy()

def ratioSitExample():
    A, B = ID(0), ID(1)
    worth = (A | B) + (A > 0) + (B > 0)
    ratioChoiceSit(worth).displayPolicy()

#Littman's Hallway with limit problem
def hallwayExample():
    G, W, S = ID(0), ID(1), ID(2)
    worth = Lex(G > 0, -W)
    print "       n        p    policy('start')"
    print "------------------------------------------"
    for n in [2*x for x in range(1,5)]:
        for p in [.2*x + .1 for x in range(5)]:
            print "%8d %8.2f    %s" % (n, p, hallway(n, p, worth).policy('start'))

def hallwaystartExample():
    G, W, S = ID(0), ID(1), ID(2)
    worth = Trunc(Lex((G > 0), -W))
    vi = hallwaydoublestart(5, .3, worth)
    vi.displayPolicy()
    

def gridExample():
    X, Y = ID(0), ID(1)
    worth = Lex(X, Y)
    vi = tgrid(5,5,.8,worth)
    vi.displayPolicy()
    print vi.policy((0, 1))
    
    


if __name__ == '__main__':
    hallwaystartExample()
