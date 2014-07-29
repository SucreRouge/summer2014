import unittest
import random
import math
from transitionStructure import *
from specification import *
from valueIterator import *

class TransitionStructureTests(unittest.TestCase):
    def testConstructor_Functionality(self):
        valid_data0 = {(0, 'a', 1): 1, (0, 'b', 2): .5, (0, 'b', 3): .5}
        valid_data1 = {('a', 'x', 'b'): 1}
        valid_data2 = {}
        
        self.assertEqual(TransitionStructure(valid_data0), valid_data0)
        self.assertEqual(TransitionStructure(valid_data1), valid_data1)
        self.assertEqual(TransitionStructure(valid_data2), valid_data2)
        self.assertEqual(TransitionStructure(), {})

    def testConstructor_Correctness(self):
        #Probabilities sum to more than one
        invalid_probs = {(0, 'a', 1): 1, (0, 'b', 2): .6, (0, 'b', 3): .6}
        #Probability greater than one
        invalid_prob = {(0, 'a', 1): 1.2}
        #Invalid key format (tuple length)
        invalid_key = {(0, 'a'): 1}

        self.assertRaises(AssertionError, TransitionStructure, invalid_probs)
        self.assertRaises(AssertionError, TransitionStructure, invalid_prob)
        self.assertRaises(AssertionError, TransitionStructure, invalid_key)

    def testAddAction(self):
        ts0 = TransitionStructure()
        ts1 = TransitionStructure({(0, 'a', 1): 1})

        ts0.addAction(1, 'a', {2: .5, 3: .5})
        ts1.addAction(1, 'b', {2: 1}),
        self.assertEqual(ts0, TransitionStructure({(1,'a',2): .5,
                                                   (1,'a',3): .5}))
        self.assertEqual(ts1, TransitionStructure({(0, 'a', 1): 1,
                                                   (1, 'b', 2): 1}))

        #Invalid action added
        self.assertRaises(AssertionError, ts0.addAction, 0, 'a', {1: .6, 2: .7})
        #Added action makes total probability invalid
        self.assertRaises(AssertionError, ts1.addAction, 0, 'a', {2: 1})

    def setUp(self):
        #Set up some sample transition structures for testing
        #ts_empty : Empty transition structure
        self.ts_empty = TransitionStructure()
        #ts_singleton : Single transition
        self.ts_singleton = TransitionStructure({(0,'a',1):1})
        #ts_det_tree : Deterministic tree structure
        self.ts_det_tree = TransitionStructure({
            (0,'a',1): 1, (0,'b',2): 1,
            (1,'a',3): 1, (1,'b',4): 1,
            (2,'a',5): 1, (2,'b',6): 1})
        #ts_sto_tree : Stochastic tree structure
        self.ts_sto_tree = TransitionStructure({
            (0,'a',1): .3, (0,'a',2): .7,
            (1,'a',3): .6, (1,'a',4): .4,
            (2,'a',5): .2, (2,'a',6): .8})
        #ts_det_dag : Deterministic DAG structure
        self.ts_det_dag = TransitionStructure({
            (0,'a',1): 1, (0, 'b', 2): 1,
            (1,'a',3): 1,
            (2,'a',4): 1, (2, 'b', 5): 1,
            (3,'a',6): 1, (4, 'a', 6): 1, (5, 'b', 6): 1})
        #ts_sto_dag : Stochastic DAG structure
        self.ts_sto_dag = TransitionStructure({
            (0,'a',1): .3, (0, 'a', 2): .7,
            (1,'a',5): 1,
            (2,'a',3): .4, (2,'a',4): .6,
            (2,'b',1): .5, (2,'b',5): .5,
            (3,'a',5): 1, (4,'a',5): 1})
        #ts_det_graph : Deterministic cyclic structure (planar)
        self.ts_det_graph = TransitionStructure({
            (0,'a',1): 1, (0, 'b', 2): 1,
            (1,'a',2): 1,
            (2,'a',3): 1,
            (3,'a',4): 1, (3,'b',3): 1,
            (4,'a',1): 1, (4,'b',5): 1,
            (5,'a',6): 1, (6,'a',7): 1,
            (7,'a',4): 1,
            (8,'a',2): 1})
        #ts_sto_graph : Stochastic cyclic structure (planar)
        self.ts_sto_graph = TransitionStructure({
            (0,'a',1): 1,
            (1,'a',2): .8, (1,'a',1): .2,
            (2,'a',2): .3, (2,'a',3): .5, (2,'a',4): .2,
            (3,'a',1): .7, (3,'a',2): .3, (3,'b',5): .8, (3,'b',3): .2,
            (3,'c',3): 1,
            (4,'a',5): .8, (4,'a',6): .2,
            (5,'a',4): .1, (5,'a',3): .9,
            (5,'b',4): 1,
            (6,'a',4): .6, (6,'a',6): .4})
            

    def testGetStates(self):
        self.assertEqual(self.ts_empty.getStates(), set([]))
        self.assertEqual(self.ts_singleton.getStates(), {0, 1})
        self.assertEqual(self.ts_det_tree.getStates(), {0,1,2,3,4,5,6})
        self.assertEqual(self.ts_sto_tree.getStates(), {0,1,2,3,4,5,6})
        self.assertEqual(self.ts_det_dag.getStates(), {0,1,2,3,4,5,6})
        self.assertEqual(self.ts_sto_dag.getStates(), {0,1,2,3,4,5})
        self.assertEqual(self.ts_det_graph.getStates(), {0,1,2,3,4,5,6,7,8})
        self.assertEqual(self.ts_sto_graph.getStates(), {0,1,2,3,4,5,6})

    def testGetActions(self):
        self.assertEqual(self.ts_empty.getActions('anything'), set([]))
        self.assertEqual(self.ts_singleton.getActions(0), {'a'})
        self.assertEqual(self.ts_det_tree.getActions(4), set([]))
        self.assertEqual(self.ts_sto_tree.getActions(2), {'a'})
        self.assertEqual(self.ts_det_dag.getActions(4), {'a'})
        self.assertEqual(self.ts_sto_dag.getActions(2), {'a','b'})
        self.assertEqual(self.ts_det_graph.getActions(4), {'a','b'})
        self.assertEqual(self.ts_sto_graph.getActions(3), {'a','b','c'})


class SpecificationTests(unittest.TestCase):
    def testNumber(self):
        for n in random.sample(range(100), 20):
            self.assertEqual(Number(n).worth(0), n)
    def testID(self):
        vec = (1,8,-5,3,2,-18,6,7,19)
        for k in range(len(vec)):
            self.assertEqual(ID(k).worth(vec), vec[k])
    def testNegate(self):
        vec = (0,0)
        for i in range(-10,30):
            self.assertEqual(Negate(Number(i)).worth(vec), -i)
        self.assertEqual(Negate(Number(math.pi)).worth(vec), -math.pi)
        self.assertEqual(Negate(Number(math.sqrt(2))).worth(vec), -math.sqrt(2))
    def testAdd(self):
        vec = (0,-1,.73,29,-81)
        for k in range(len(vec)):
            self.assertEqual(Add(ID(k), ID(k)).worth(vec), vec[k] + vec[k])
        for n in random.sample(range(100), 20):
            self.assertEqual(Add(Number(n),Number(0)).worth(vec), n)
    def testMult(self):
        vec = (0,-1,.73,29,-81)
        for k in range(len(vec)):
            self.assertEqual(Mult(ID(k), ID(k)).worth(vec), vec[k] * vec[k])
        for n in random.sample(range(100), 20):
            self.assertEqual(Mult(Number(n),Number(1)).worth(vec), n)
    def testGte(self):
        vec = (0, 0)
        self.assertEqual(Gte(Number(0),Number(0)).worth(vec), 0)
        self.assertEqual(Gte(Number(10),Number(8)).worth(vec), 0)
        self.assertAlmostEqual(Gte(Number(-2),Number(0)).worth(vec), -math.sqrt(2))
    def testGt(self):
        vec = (0, 0)
        self.assertEqual(Gt(Number(0),Number(0)).worth(vec), -.1)
        self.assertEqual(Gt(Number(10),Number(8)).worth(vec), 0)
        self.assertEqual(Gt(Number(10.00001),Number(10)).worth(vec), 0)
        self.assertAlmostEqual(Gt(Number(-2),Number(0)).worth(vec), -math.sqrt(2)-.1)

class ValueIteratorTests(unittest.TestCase):
    def testSetAdd(self):
        self.assertEqual(setAdd({1,2,3},{1,2,3}), {2,3,4,5,6})
        self.assertEqual(setAdd({'h'}, {'ello','ow','ope'}), 
                         {'hello','how','hope'})
        self.assertEqual(setAdd({5,.6,32,-27.5},{0}), {5,.6,32,-27.5})
    def testSetSum(self):
        self.assertEqual(setSum({0},{1}), {1})
        self.assertEqual(setSum({x} for x in range(10)), {45})
        self.assertEqual(setSum(set(range(2)) for x in range(5)), 
                         set(range(6)))
    def testVecMult(self):
        self.assertEqual(vecMult(3,(1,2,3)), (3,6,9))
        self.assertEqual(vecMult(-.5,(4,3,2)), (-2,-1.5,-1))
        self.assertEqual(vecMult(0,(math.pi, 6.8123,-27)), (0,0,0))
        
    
        
    

if __name__ == '__main__':
    unittest.main()
