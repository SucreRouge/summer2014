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
  end

module Make(Letter: StringableType) (State: StringableType) =
  struct
    type l = Letter.t
    type s = State.t

    type transition = {
      link : l;
      s : s;
      t : s;
    }
      
    type t = {
      initial     : s;
      final       : s -> bool;
      transitions : transition list;
    }

    let transition_to_string {link: link; s: start; t: finish} =
      Printf.sprintf "%s --%s--> %s" 
	(State.to_string s)
	(Letter.to_string link)
	(state.to_string s)
      

    let to_string {initial: initial; final: final; transitions: transitions} =
      List.concat ", " (List.map transition_to_string transitions)
	
  end
