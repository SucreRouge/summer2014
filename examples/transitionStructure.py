import pydot
from PIL import Image
import StringIO

#Transition structure representation of the world
class TransitionStructure(dict):
    def __init__(self, data=dict()):
        #data : dict<(state, action, state), prob>
        for key in data: # Make sure we got the kind of data we want
            assert isinstance(key, tuple) and len(key) == 3

        for state, action in {(st, act) for (st, act, sprime) in data}:
            assert sum([prob for (st, act, sp), prob in data.items() 
                        if st == state and act == action]) == 1

        #Valid data, so keep track of it
        super(TransitionStructure, self).__init__(data)
        
    #Add a transition to the structure
    def addAction(self, state, action, results):
        #results : dict<state, prob>
        for (sprime, prob) in results.items():
            self[(state, action, sprime)] = prob

        #Make sure the probabilities are still valid
        assert sum([prob for (st, act, sp), prob in self.items()
                    if st == state and act == action]) == 1

    #Return all of the states in the transition structure
    def getStates(self):
        starts = {state for (state, action, sprime) in self}
        ends = {sprime for (state, action, sprime) in self}
        return starts | ends #return the union of states

    #Return all actions valid from a state
    def getActions(self, state):
        actions = {action for (st, action, sprime) in self
                   if st == state}
        return actions

    #Display structure using graphviz
    def display(self):
        graph = pydot.Dot(graph_type='digraph')
        for (start, action, dest), prob in self.items():
            if prob: #Only display non-zero transitions
                if prob < 1:
                    label = "%0.1f%s" % (prob, str(action))
                else:
                    label = str(action)
                edge = pydot.Edge(start, dest, label=label)
                graph.add_edge(edge)

        #Display the graph to the screen
        png_str = graph.create_png(prog='dot')
        data = StringIO.StringIO(png_str)
        img = Image.open(data)
        img.show()


if __name__ == "__main__":
    ts_sto_graph = TransitionStructure({
        (0,'a',1): 1,
        (1,'a',2): .8, (1,'a',1): .2,
        (2,'a',2): .3, (2,'a',3): .5, (2,'a',4): .2,
        (3,'a',1): .7, (3,'a',2): .3, (3,'b',5): .8, (3,'b',3): .2,
        (3,'c',3): 1,
        (4,'a',5): .8, (4,'a',6): .2,
        (5,'a',4): .1, (5,'a',3): .9,
        (5,'b',4): 1,
        (6,'a',4): .6, (6,'a',6): .4})

    ts_sto_graph.display()

