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
      let compare = Pervasives.compare
      let (=) a b = compare a b = 0
      let to_string (start, letter, finish) =
	Printf.sprintf "(%s --%s-> %s)"
	  (State.to_string start)
	  (Letter.to_string letter)
	  (State.to_string finish)

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
      let (states, transitions) = 
	explore (SSet.singleton initial) SSet.empty TSet.empty in
      let accepting = SSet.filter final states in
      {letters = letters; states = states;
       initial = initial; accepting = accepting;
       transitions = transitions}

    let (=) a1 a2 =
      (LSet.compare a1.letters a2.letters = 0) &&
	(SSet.compare a1.states a2.states = 0) &&
	(State.compare a1.initial a2.initial = 0) &&
	(SSet.compare a1.accepting a2.accepting = 0) &&
	(compare (TSet.elements a1.transitions) (TSet.elements a2.transitions) = 0) 


	

    (* Check if this automata accepts any infinite words, returns None if empty*)
    let infinite_word a =
      (* First perform a depth first search from the start node looking for a final node *)
      let get_transitions node = (* Get the transitions from a node *)
	TSet.elements (TSet.filter (fun (x,_,_) -> State.compare node x == 0)
	  a.transitions) in

      (* find a path from cur to a state matching pred *)
      let rec reachable unvis goal vis path =
	match unvis with
	  | [] -> None (* We looked everywhere *)
	  | (_,act,st)::tl ->
	    if SSet.mem st vis then None else
	      let vis = SSet.add st vis in
	      let newpath = act::path in
	      if State.compare st goal == 0 then Some(List.rev newpath) else
		match reachable (get_transitions st) goal vis newpath with
		  | Some(path) -> Some(path) (* Goal down this branch *)
		  | None -> (* Look sideways *)
		    reachable tl goal vis newpath in

      let rec find_word unvis vis path =
	match unvis with
	  | [] -> None (* We looked everywhere *)
	  | (_,act,st)::tl ->
	    if SSet.mem st vis then None else
	      let vis = SSet.add st vis in
	      let newpath = act::path in
	      if SSet.mem st a.accepting then
	      (* Its possible, we have to check for a cylce *)
		match reachable (get_transitions st) st SSet.empty [] with
		  | Some(loop) -> Some(path, loop)
		  | None -> begin (* keep looking down *)
		    match find_word (get_transitions st) vis newpath with
		      | Some(path, loop) -> Some(path, loop)
		      | None -> (* look sideways *)
			find_word tl vis newpath
		  end
	      else (* Keep looking *)
		match find_word (get_transitions st) vis newpath with
		  | Some(path, loop) -> Some(path, loop)
		  | None -> (* look sideways *)
		    find_word tl vis newpath in
      find_word (get_transitions a.initial) SSet.empty []

    let word_to_string (path, loop) =
      let path = String.concat "" (List.map Letter.to_string path) in
      let loop = String.concat "" (List.map Letter.to_string loop) in
      path ^ "(" ^ loop ^ ")"

    let is_empty automaton = match infinite_word automaton with
      | None -> true
      | Some(_) -> false

      
    let to_string {letters = letters; states = states;
		   initial = initial; accepting = accepting;
		   transitions = transitions} =
      let result = [
	"Automaton over: " ^ (String.concat ", " (LSet.map_list Letter.to_string letters));
	" + states: " ^ (String.concat ", " (SSet.map_list State.to_string states));
	" + initial: " ^ State.to_string initial;
	" + transitions: " ^ (String.concat ", " (TSet.map_list Transition.to_string transitions));
	" + accepting: " ^ (String.concat ", " (SSet.map_list State.to_string accepting))
      ] in
      String.concat "\n" result
  end
