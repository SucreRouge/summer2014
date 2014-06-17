(* file test_.ml *)
(* Complete test suite for folder *)

let test =
  Test_automaton.test

let () = print_endline (string_of_bool test)
