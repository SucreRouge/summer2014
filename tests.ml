open Ltl
open Automata

(* Test suite for ltl2ba *)
(* tests in the form (ltl expression, matching automaton *)
let tests =
  let a = (Atom "a"), b = (Atom "b"), c = (Atom "c") in
  let empty = LtlSet.empty in 

  [(Atom "a",
    {starts: [LtlSet.of_list [a]];
     finals: [LtlSet.of_list [a];
	      empty];
     transitions:
       (TransitionSet.of_list
	  [{link: Sigma([a], []);
	    s: LtlSet.of_list [a];
	    t: empty}])});

   (Globally(Atom "a"),
    {starts: [LtlSet.of_list [Globally(a)]];
     finals: [LtlSet.of_list [Globally(a)]];
     transitions:
       (TransitionSet.of_list
	  [{link: Sigma([a], []);
	    s: LtlSet.of_list [Globally(a)];
	    t: LtlSet.of_list [Globally(a)]}])})]
	    
let () = print_endline "Testing..."
