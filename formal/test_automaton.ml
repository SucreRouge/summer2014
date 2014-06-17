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
    let to_string x = x
    let compare = Pervasives.compare
  end

module A = Make (StringableString) (StringableInt)

let from_functions_tests = [
  ([], 0, (* Empty automata *)
   (function _ -> false),
   (function _ -> [0]),
   (A.from_states [] [0] 0 [] []));
  (["a";"b"], 0, (* Blinking *)
   (function _ -> false),
   (function (0,_) -> [1] | _ -> [0]),
   (A.from_states ["a";"b"] [0;1] 0 [] [(0,"a",1);(1,"a",0);(0,"b",0);(1,"b",0)]));
  (["a";"b"], 0, (* Consecuative bs *)
   (function 3 -> true | _ -> false),
   (function (3,"b") -> [3] | (x,"b") -> [x+1] | (_,_) -> [0]),
   (A.from_states ["a";"b"] [3;2;1;0] 0 [3] 
     [(0,"a",0);(1,"a",0);(2,"a",0);(3,"a",0);(0,"b",1);(1,"b",2);(2,"b",3);(3,"b",3)]))
]
    
let from_functions_test =
  List.for_all (fun (letters,initial,final,move,check) -> 
    let result = A.from_functions letters initial final move in
    print_endline (A.to_string result);
    print_endline (A.to_string check);
    A.(=) result check
  ) from_functions_tests

let test = 
  from_functions_test

let () = print_endline (string_of_bool test)
