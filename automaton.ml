type link = Epsilon of Ltl.ltl list
	    | Sigma of Ltl.ltl list * Ltl.ltl list

type state = Ltl.LtlSet.t
type transition = {
  link : link;
  s : state;
  t : state;
}

(* Order transitions lexicographically *)
module OrderedTransition = struct
  type t = transition
  let compare a b =
    let c = compare a.link b.link in
    if c <> 0 then c else
      let c = Ltl.LtlSet.compare a.s b.s in
      if c <> 0 then c else
	Ltl.LtlSet.compare a.t b.t
  let (=) a b = 
    compare a b = 0
end

module TransitionSet = Set.Make(OrderedTransition)

(* Generalized Buchi Automaton *)
type automaton = {
  starts: state list;
  finals: state list;
  transitions: TransitionSet.t;
}

let link_to_string link =
  let format_conds conds =
    String.concat " ∧ " (List.map Ltl.to_string conds)
  in
  match link with
    | Epsilon(postpones) -> 
      "ε" ^ (String.concat "" (List.map (fun f -> ", !" ^ Ltl.to_string f) postpones))
    | Sigma(conds, postpones) -> 
      "Σ" ^ (format_conds conds) ^ (String.concat "" (List.map (fun f -> ", " ^ (Ltl.to_string f)) postpones))

let transition_to_string {link = link; s = s; t = t} =
  Printf.sprintf "%s -> %s (%s)" (Ltl.LtlSet.to_string s) (Ltl.LtlSet.to_string t) (link_to_string link)

(* Produce set of transitions while adding epsilon transitions and reducing
   the resulting graph *)
let rec reduction_graph transitions state =
  let is_known trans transitions =
    TransitionSet.exists (OrderedTransition.(=) trans) transitions
  in
  let add_transition trans transitions =
    if is_known trans transitions then transitions
    else reduction_graph (TransitionSet.add trans transitions) trans.t
  in
  let epsilon_from_option = function
    | None -> Epsilon([])
    | Some(p) -> Epsilon([p])
  in
  match Ltl.epsilon_transform state with
    | None ->
      let (conds, next) = Ltl.sigma_transform state in
      let trans = {link = Sigma(conds, []); s = state; t = next } in
      add_transition trans transitions
    | Some(conv_list) ->
      List.fold_left (fun transitions (next, cond) ->
	let trans = { link = epsilon_from_option cond;
		      s = state; t = next } in
	add_transition trans transitions
      )	transitions conv_list
      
(* Construct an automaton from a start state *)
let construct_from start_state =
  { starts = [start_state]; finals = []; transitions = reduction_graph TransitionSet.empty start_state }

(* Produce a graph from an automaton *)
let to_graph automaton =
  let set_to_s = Ltl.LtlSet.to_string in
  let g = (Graph.new_graph "Automaton") in
  let is_start s = List.exists ((=) s) automaton.starts in
  let add_node s = (if is_start s then Graph.add_start else Graph.add_node) in
  List.fold_left (fun g { link = link; s = s; t = t } ->
    let s_string = set_to_s s in
    let t_string = set_to_s t in
    let g = (add_node s) g s_string in
    let g = (add_node t) g t_string in
    Graph.link g s_string t_string (link_to_string link)
  ) g (TransitionSet.elements automaton.transitions)

