(* file: automaton.ml *)

module type LetterType =
  sig
    type t
    val to_string: t -> string
    val compare: t -> t -> int
  end

module type StateType = LetterType (* Currently they have the same requirements *)


module Make(Letter: LetterType) (State: StateType) =
  struct
    type l = Letter.t
    type s = State.t

    module LSet = ExtendedSet.Make(Letter)
    module SSet = ExtendedSet.Make(State)

    module Transition = struct
      type t = s * l * s
      let compare (s, l, t) (s1, l1, t1) =
	let c = State.compare s s1 in
	if c <> 0 then c else
	  let c = Letter.compare l l1 in
	  if c <> 0 then c else
	    State.compare t t1
      let (=) a b = compare a b = 0
    end

    module TSet = ExtendedSet.Make(Transition)
      
    type t = {
      letters     : LSet.t;
      states      : SSet.t;
      initial     : s;
      accepting   : SSet.t;
      transitions : TSet.t;
    }

    (* Create a new automaton from flat representation *)
    let from_states letters states initial accepting transitions =
      {letters = LSet.of_list letters; states = SSet.of_list states;
       initial = initial; accepting = SSet.of_list accepting;
       transitions = TSet.of_list transitions}

    (* Construct an automaton from functional representation *)
    let from_functions letters initial final move =
      let letters = LSet.of_list letters in
      let move a b = move (a,b) in (* Allow curring in construction *)
      let rec explore unvis vis trans =
	match SSet.pop unvis with
	  | None -> (vis, trans)
	  | Some(elt, rest) ->
	    if SSet.mem elt vis then explore rest vis trans (* We've already seen this *)
	    else explore
	      (List.fold_left (fun set elt -> SSet.add elt set) unvis
		 (List.concat (LSet.map_list (move elt) letters)))
	      (SSet.add elt vis)
	      (List.fold_left (fun set elt -> TSet.add elt set) trans
		 (LSet.fold (fun a lst -> 
		   (List.map (fun x -> (elt,a,x)) (move elt a)) @ lst) letters []))


      in
      let (states, transitions) = explore (SSet.singleton initial) SSet.empty TSet.empty in
      let accepting = SSet.filter final states in
      {letters = letters; states = states;
       initial = initial; accepting = accepting;
       transitions = transitions}

    let (=) a1 a2 =
      a1.letters = a2.letters &&
      a1.states = a2.states &&
      a1.initial = a2.initial &&
      a1.accepting = a2.accepting &&
      a1.transitions = a2.transitions

	

    (* Check if this automata accepts any infinite words *)
    let is_empty {letters = letters; states = states;
		   initial = initial; accepting = accepting;
		   transitions = transitions} =
      false
	


    let transition_to_string (start, letter, finish) =
      Printf.sprintf "(%s --%s-> %s)"
	(State.to_string start)
	(Letter.to_string letter)
	(State.to_string finish)
      

    let to_string {letters = letters; states = states;
		   initial = initial; accepting = accepting;
		   transitions = transitions} =
      let result = [
	"Automaton over: " ^ (String.concat ", " (LSet.map_list Letter.to_string letters));
	" + states: " ^ (String.concat ", " (SSet.map_list State.to_string states));
	" + initial: " ^ State.to_string initial;
	" + transitions: " ^ (String.concat ", " (TSet.map_list transition_to_string transitions));
	" + accepting: " ^ (String.concat ", " (SSet.map_list State.to_string accepting))
      ] in
      String.concat "\n" result
  end
