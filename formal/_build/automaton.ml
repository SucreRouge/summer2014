(* file: automaton.ml *)

module type StringableType =
  sig
    type t
    val to_string: t -> string
  end

module type S =
  sig
    type l (* letter type *)
    type s (* state type *)
      
    type t
      
    val to_string: t -> string
    val from_start: s -> t
  end

module Make(Letter: StringableType) (State: StringableType) =
  struct
    type l = Letter.t
    type s = State.t

    type transition = s * l * (s list)
      
    type t = {
      letters     : l list;
      states      : s list;
      initial     : s;
      accepting   : s list;
      transitions : transition list;
    }

    (* Create a new automaton from flat representation *)
    let from_states letters states initial accepting transitions =
      {letters = letters; states = states;
       initial = initial; accepting = accepting;
       transitions = transitions}

    (* Construct an automaton from functional representation *)
    let from_functions letters initial final move =
      let rec explore unvis vis trans =
	match unvis with
	  | [] -> (vis, trans)
	  | hd::tl ->
	    if List.mem hd vis then explore tl vis trans (* We've already seen this *)
	    else explore
	      ((List.concat (List.map (move hd) letters)) @ unvis)
	      (hd :: vis)
	      ((List.map (fun a -> (hd, a, move hd a)) letters) @ trans)
      in
      let (states, transitions) = explore [initial] [] [] in
      let accepting = List.filter final states in
      {letters = letters; states = states;
       initial = initial; accepting = accepting;
       transitions = transitions}


    let transition_to_string (start, letter, finish) =
      Printf.sprintf "%s --%s--> %s"
	(State.to_string start)
	(Letter.to_string letter)
	(State.to_string finish)
      

    let to_string {letters = letters; states = states;
		   initial = initial; accepting = accepting;
		   transitions = transitions} =
      "There should be an automata around here somewhere..."
	
  end
