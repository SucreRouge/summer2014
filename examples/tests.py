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
    def testCombineReward(self):
        rf1 = lambda x: 3
        rf2 = lambda x: x
        rf3 = lambda x: x*x
        rf4 = lambda x: x + 2
        self.assertEqual(combineReward(rf1, rf2, rf3, rf4)(0), (3, 0, 0, 2))
        self.assertEqual(combineReward(rf2, rf3, rf1, rf4)(2), (2, 4, 3, 4))
        self.assertEqual(combineReward(rf1)(5), (3,))
    def testNum(self):
        for n in random.sample(range(100), 20):
            self.assertEqual(Num(n)(0), n)
    def testID(self):
        vec = (1,8,-5,3,2,-18,6,7,19)
        for k in range(len(vec)):
            self.assertEqual(ID(k)(vec), vec[k])
    def testNegate(self):
        vec = (0,0)
        for i in range(-10,30):
            self.assertEqual(Negate(Num(i))(vec), -i)
        self.assertEqual(Negate(Num(math.pi))(vec), -math.pi)
        self.assertEqual(Negate(Num(math.sqrt(2)))(vec), -math.sqrt(2))
    def testAdd(self):
        vec = (0,-1,.73,29,-81)
        for k in range(len(vec)):
            self.assertEqual(Add(ID(k), ID(k))(vec), vec[k] + vec[k])
        for n in random.sample(range(100), 20):
            self.assertEqual(Add(Num(n),Num(0))(vec), n)
    def testMult(self):
        vec = (0,-1,.73,29,-81)
        for k in range(len(vec)):
            self.assertEqual(Mult(ID(k), ID(k))(vec), vec[k] * vec[k])
        for n in random.sample(range(100), 20):
            self.assertEqual(Mult(Num(n),Num(1))(vec), n)
    def testGte(self):
        vec = (0, 0)
        self.assertEqual(Gte(Num(0),Num(0))(vec), 0)
        self.assertEqual(Gte(Num(10),Num(8))(vec), 0)
        self.assertAlmostEqual(Gte(Num(-2),Num(0))(vec), -math.sqrt(2))
    def testGt(self):
        vec = (0, 0)
        self.assertEqual(Gt(Num(0),Num(0))(vec), -.1)
        self.assertEqual(Gt(Num(10),Num(8))(vec), 0)
        self.assertEqual(Gt(Num(10.00001),Num(10))(vec), 0)
        self.assertAlmostEqual(Gt(Num(-2),Num(0))(vec), -math.sqrt(2)-.1)
    def testLexicographic(self):
        vec = (0, 1, 2, 3)
        self.assertEqual(Lex(ID(0),ID(1),ID(2),ID(3))(vec), vec)
        self.assertEqual(Lex(Num(5), ID(2), Add(Num(3),ID(0)))(vec),
            (5,2,3))
        self.assertEqual(Lex(Gt(ID(3), Num(0)), Negate(Mult(ID(1), Num(67.2))))(vec), (0, -67.2))

class ValueIteratorTests(unittest.TestCase):
    def testVecAdd(self):
        self.assertEqual(vecAdd((0,),(1,)), (1,))
        self.assertEqual(vecAdd((0,1),(1,0)), (1,1))
        self.assertEqual(vecAdd((-math.pi, 1),(math.pi, -1)), (0,0))
    def testSetAdd(self):
        self.assertEqual(setAdd({(1,),(2,),(3,)},{(1,),(2,),(3,)}), 
                         {(2,),(3,),(4,),(5,),(6,)})
        self.assertEqual(setAdd({('h',)}, {('ello',),('ow',),('ope',)}), 
                         {('hello',),('how',),('hope',)})
        self.assertEqual(setAdd({(5,),(.6,),(32,),(-27.5,)},{(0,)}), 
                         {(5,),(.6,),(32,),(-27.5,)})
    def testSetSum(self):
        self.assertEqual(setSum([{(0,)},{(1,)}]), {(1,)})
        self.assertEqual(setSum([{(x,)} for x in range(10)]), {(45,)})
        self.assertEqual(setSum([{(0,),(1,)} for x in range(5)]), 
                         set((x,) for x in range(6)))
    def testVecMult(self):
        self.assertEqual(vecMult(3,(1,2,3)), (3,6,9))
        self.assertEqual(vecMult(-.5,(4,3,2)), (-2,-1.5,-1))
        self.assertEqual(vecMult(0,(math.pi, 6.8123,-27)), (0,0,0))
    def testSetMult(self):
        self.assertEqual(setMult(3,{(0,),(1,),(2,)}),{(0,),(3,),(6,)})
        self.assertEqual(setMult(0,{(0,1,2),(0,0,0),(5,9,-3.14)}),{(0,0,0)})
        self.assertEqual(setMult(-2,{(5,3,1),(0,0,4),(.5,1,6)}),
                         {(-10,-6,-2),(0,0,-8),(-1,-2,-12)})
    def testUnion(self):
        self.assertEqual(union([]), set([]))
        self.assertEqual(union([{0},{0},{0}]), {0})
        self.assertEqual(union([{0},{1},{0,1},{0}]), {0,1})
        self.assertEqual(union([{'a','b'},{'a'},{'c'}]),{'a','b','c'})
    def testConstructorBasic(self):
        ts0 = TransitionStructure({(0, 'a', 1): 1})
        rfs0 = combineReward(lambda st: st)
        worth0 = ID(0)
        vi0 = ValueIterator(ts0, rfs0, worth0)
        #(maxing over an empty set)
        self.assertEqual(dict(vi0.Q), {(0,'a'): set([])})
        ts1 = TransitionStructure({(0, 'a', 1): 1, (1,'a',2): 1, (2,'a',2): 1})
        rfs1 = lambda st: (1,) if st == 1 else (0,)
        vi1 = ValueIterator(ts1, rfs1, worth0)
        self.assertEqual(dict(vi1.Q), {(0,'a'): {(vi1.gamma,)},
                                       (1,'a'): {(1,)},
                                       (2,'a'): {(0,)}})
        ts2 = TransitionStructure(
            {(0,'a',1): 1, (0,'b',2): 1,
             (1,'a',-1): 1, (2,'a',-1): 1,
             (-1,'a',-1): 1}) #-1 is terminal state
        rfs2 = combineReward(
            lambda st: 1 if st == 2 else 0,
            lambda st: 1 if st == 2 or st == 1 else 0)
        worth2 = Gt(ID(0), ID(1))
        vi2 = ValueIterator(ts2, rfs2, worth2)
        self.assertEqual(dict(vi2.Q), {(0,'a'): {(0,vi2.gamma)},
                                       (0,'b'): {(vi2.gamma,vi2.gamma)},
                                       (1,'a'): {(0,1)}, (2,'a'): {(1,1)},
                                       (-1,'a'): {(0,0)}})

    def testConstructorWorth(self):
        ts0 = TransitionStructure(
            {(0,'a',1): 1,
             (1,'a',2): 1, (1,'b',3): 1,
             (2,'a',-1): 1, (3,'a',-1): 1,
             (-1,'a',-1): 1}) #-1 is terminal state
        rfs0 = combineReward(
            lambda st: 1 if st == 3 else 0,
            lambda st: 1 if st == 2 or st == 3 else 0)
        worth0 = Gt(ID(1), ID(0))
        worth1 = Gte(ID(1), ID(0))
        worth2 = Add(Gte(ID(0), ID(1)), Gte(ID(1), ID(0)))
        vi0 = ValueIterator(ts0, rfs0, worth0)
        vi1 = ValueIterator(ts0, rfs0, worth1)
        vi2 = ValueIterator(ts0, rfs0, worth2)
        gam = vi0.gamma #brevity
        self.assertEqual(dict(vi0.Q), 
                         {(-1,'a'): {(0,0)}, 
                          (3, 'a'): {(1,1)},     (2, 'a'): {(0,1)},
                          (1, 'b'): {(gam,gam)}, (1, 'a'): {(0, gam)},
                          (0, 'a'): {(0, gam**2)}}) #the interesting bit
        self.assertEqual(dict(vi1.Q), 
                         {(-1,'a'): {(0,0)}, 
                          (3, 'a'): {(1,1)},     (2, 'a'): {(0,1)},
                          (1, 'b'): {(gam,gam)}, (1, 'a'): {(0, gam)},
                          (0, 'a'): {(0, gam**2), (gam**2, gam**2)}}) 
        self.assertEqual(dict(vi2.Q), 
                         {(-1,'a'): {(0,0)}, 
                          (3, 'a'): {(1,1)},     (2, 'a'): {(0,1)},
                          (1, 'b'): {(gam,gam)}, (1, 'a'): {(0, gam)},
                          (0, 'a'): {(gam**2, gam**2)}})
                                       
        
    

if __name__ == '__main__':
    unittest.main()
