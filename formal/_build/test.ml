(* Testing under construction files *)

module SInt =
  struct
    type t = int
    let to_string = string_of_int
  end

module IntAutomaton = Automaton.Make (SInt) (SInt)

let () =
  let a = (IntAutomaton.from_functions [5] 5
	     (fun s -> false) 
	     (fun s l -> [5])) in
  print_endline (IntAutomaton.to_string a)
    
