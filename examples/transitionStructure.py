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

        #Return the graph for testing purposes

        
        #Display the graph to the screen
        png_str = graph.create_png(prog='dot')
        data = StringIO.StringIO(png_str)
        img = Image.open(data)
        img.show()

        return graph


def main():
    ts = TransitionStructure()
    ts.addAction(0, 'a', {1: 1})
    ts.display()

if __name__ == "__main__":
    main()
