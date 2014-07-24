(* file test_automaton.ml *)
(* Test suite for automaton.ml *)

open Automaton

(* Make integers stringable for printable output *)
module StringableInt =
  struct
    type t = int
    let to_string = string_of_int
    let compare = Pervasives.compare
  end

module StringableString =
  struct
    type t = string
    let to_string x = String.copy x
    let compare = Pervasives.compare
  end

module A = Make (StringableString) (StringableInt)

let from_functions_tests = [
  ("Empty automaton", [], 0,
   (function _ -> false),
   (function _ -> [0]),
   (A.from_states [] [0] 0 [] []));
  ("Blinking", ["a"], 0,
   (function _ -> false),
   (function (0,_) -> [1] | _ -> [0]),
   (A.from_states ["a"] [0;1] 0 [] 
      [(0,"a",1);(1,"a",0)]));
  ("Three b's", ["a";"b"], 0,
   (function 3 -> true | _ -> false),
   (function (3,"b") -> [3] | (x,"b") -> [x+1] | (_,_) -> [0]),
   (A.from_states ["a";"b"] [3;2;1;0] 0 [3] 
     [(0,"a",0);(1,"a",0);(2,"a",0);(3,"a",0);(0,"b",1);(1,"b",2);
      (2,"b",3);(3,"b",3)]))
]
    
let from_functions_test =
  print_endline "== Testing Automaton.from_functions ==";
  List.for_all (fun (name,letters,initial,final,move,check) -> 
    let result = A.from_functions letters initial final move in
    let pass = A.(=) result check in
    print_endline (name ^ ": " ^ (string_of_bool pass));
    pass
  ) from_functions_tests

(* Now define some automata for future tests *)
let simple = A.from_functions
     ["a"] 0 
     (function 0 -> true | _ -> false)
     (function _ -> [0])
let blinking = A.from_functions
    ["a"] 0
    (function 0 -> true | _ -> false)
    (function (0,_) -> [1] | _ -> [0])
let abab = A.from_functions
    ["a";"b"] 0
    (function 0 -> true | _ -> false)
    (function (0,"a") -> [1] | (1,"b") -> [0] | (1,"a") -> [1] | _ -> [0])

let infinite_word_tests = [
  ("String of a's", simple, Some([],["a"]));
  ("Blinking", blinking, Some(["a"],["a";"a"]));
  ("Alternating a and b", abab, Some(["a"],["a";"b"]))
]

let infinite_word_test =
  print_endline "== Testing Automaton.infinite_word ==";
  List.for_all (fun (name, automaton, check) ->
    let result = A.infinite_word automaton in
    let pass = (result = check) in
    print_endline (name ^ ": " ^ (string_of_bool pass));
    pass
  ) infinite_word_tests

let test =
  let pass = from_functions_test &&
    infinite_word_test in
  print_endline ("=== Automaton summary: " ^ (string_of_bool pass))
