import unittest
from transitionStructure import *

class TransitionStructureTests(unittest.TestCase):
    def setUp(self):
        #Set up some sample transition structures for testing
        #ts_empty : Empty transition structure
        ts_empty = TransitonStructure()
        #ts_singleton : Single transition
        ts_singleton = TransitionStructure({(0,'a',1):1})
        #ts_tree : Tree transition structure
        
        #ts_dag : DAG transition structure
        
        #ts_graph : Cyclic transition structure
        

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
        self.assertEqual(ts0, TransitionStructure({(1,'a',2): .5, (1,'a',3): .5}))
        self.assertEqual(ts1, TransitionStructure({(0, 'a', 1): 1, (1, 'b', 2): 1}))

        #Invalid action added
        self.assertRaises(AssertionError, ts0.addAction, 0, 'a', {1: .6, 2: .7})
        #Added action makes total probability invalid
        self.assertRaises(AssertionError, ts1.addAction, 0, 'a', {2: 1})


if __name__ == '__main__':
    unittest.main()
