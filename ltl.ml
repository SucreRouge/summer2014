(* Linear temporal logic expressions *)
type ltl =
  | Top | Bottom
  | Atom     of string
  | Not      of ltl
  | And      of ltl * ltl
  | Or       of ltl * ltl
  | Next     of ltl
  | Finally  of ltl
  | Globally of ltl
  | Until    of ltl * ltl
  | Release  of ltl * ltl

(* Print a string representation of an ltl expression *)
let rec to_string exp =
  let print_paren exp =
    match exp with
      | Top | Bottom | Atom(_) | Not(_) | Next(_) | Finally(_) | Globally(_)
	  -> to_string exp (* No parens needed *)
      | _ -> "(" ^ (to_string exp) ^ ")"
  in
  match exp with
    | Top        -> "⊤"
    | Bottom     -> "⊥"
    | Atom(p)    -> p
    | Not(exp)   -> "¬" ^ (print_paren exp)
    | And(l, r)  -> (print_paren l) ^ " ∧ " ^ (print_paren r)
    | Or(l, r)       -> (print_paren l) ^ " ∨ " ^ (print_paren r)
    | Next(exp)      -> "X " ^ (print_paren exp)
    | Finally(exp)   -> "F " ^ (print_paren exp)
    | Globally(exp)  -> "G " ^ (print_paren exp)
    | Until(l, r)    -> (print_paren l) ^ " U " ^ (print_paren r)
    | Release(l, r)  -> (print_paren l) ^ " R " ^ (print_paren r)

(* Determine the size of an expression consistent with subformula ordering *)
let rec size_of exp =
  match exp with
    | Top | Bottom | Atom(_) -> 1
    | Not(exp) | Next(exp) | Finally(exp) | Globally(exp) -> 1 + size_of exp
    | And(l, r) | Or(l, r) | Until(l, r) | Release(l, r) ->
      1 + max (size_of l) (size_of r)

module LtlSet = 
  struct
    module S_ = Set.Make(
      struct
	type t = ltl
	let compare = compare
      end)
    include S_

    let of_list l = List.fold_left (fun s e -> add e s) empty l

    let compare a b = Pervasives.compare (elements a) (elements b)
    let (=) a b     = compare a b = 0

    let to_string set =
      let exps = List.map to_string (elements set) in
      "{" ^ (String.concat ", " exps) ^ "}"
	
    (* Return a tuple containing the largest formula in the set and the remaining elements *)
    let pop_largest set =
      let (_, largest) = List.fold_left (fun (size, value) formula ->
	let cur_size = size_of formula in
	if size < cur_size then
	  (cur_size, formula)
	else
	  (size, value)
      ) (0, Bottom) (elements set) in
      (largest, remove largest set)

end


(* Convert an expression into negative normal form. 
   Note that this does not increase the size of exp *)
let rec nnf exp = match exp with
  | Top | Bottom | Atom(_) -> exp
  | And(l, r)     -> And(nnf l, nnf r)
  | Or(l, r)      -> Or(nnf l, nnf r)
  | Next(p)       -> Next(nnf p)
  | Finally(p)    -> Finally(nnf p)
  | Globally(p)   -> Globally(nnf p)
  | Until(l, r)   -> Until(nnf l, nnf r)
  | Release(l, r) -> Release(nnf l, nnf r)
  | Not(exp) -> match exp with
      | Top           -> Bottom
      | Bottom        -> Top
      | Atom(_)       -> Not(exp)
      | Not(p)        -> nnf p
      | And(l,r)      -> Or(nnf (Not l), nnf (Not r))
      | Or(l,r)       -> And(nnf (Not l), nnf (Not r))
      | Next(p)       -> Next(nnf (Not p))
      | Finally(p)    -> Globally(nnf (Not p))
      | Globally(p)   -> Finally(nnf (Not p))
      | Until(l, r)   -> Release(nnf (Not l), nnf (Not r))
      | Release(l, r) -> Until(nnf (Not l), nnf (Not r))

(* Partially rewrite an expression in nnf to reduce the number of symbols 
   (X a) /\ (X b)     -> X (a /\ b)
   (X a) U (X b)      -> X (a U b)
   (a R x) /\ (a R y) -> a R (x /\ y)
   (a R x) \/ (b R x) -> (a \/ b) R x
   (G a) /\ (G b)     -> G(a /\ b)
   (GF a) \/ (GF b)   -> GF (a \/ b)
*)
let rec simplify exp = match exp with
  | And(Next l, Next r) -> Next(And(simplify l, simplify r))
  | Until(Next l, Next r) -> Next(Until(simplify l, simplify r))
  | And(Release(a, x), Release(b,y)) when a = b -> Release(a, And(x, y))
  | Or(Release(a, x), Release(b, y)) when x = y -> Release(Or(a, b), x)
  | And(Globally l, Globally r) -> Globally(And(simplify l, simplify r))
  | Or(Globally(Finally l), Globally(Finally r)) -> 
    Globally(Finally(Or(simplify l, simplify r)))
  | _ -> exp

(* An expression is reduced if it is either a literal or has next as the outermost connective *)
let is_reduced = function
  | Top | Bottom | Atom(_) | Not(Atom(_)) | Next(_) -> true
  | _ -> false

(* Conjunction concatenation of a ltl list *)
let and_concat = function
    | [] -> Top
    | (e::exps) -> List.fold_left (fun a b -> And(a, b)) e exps

(* Apply epsilon reduction rules on a formula set to produce valid transitions to more reduced sets *)
let epsilon_transform set =
  (* Single rule application, keeping track of !transitions *)
  let apply_rule exp = match exp with
    | And(l, r) -> [(LtlSet.of_list [l; r], None)]
    | Or(l, r) -> [(LtlSet.singleton l, None);
		   (LtlSet.singleton r, None)]
    | Release(l, r) -> [(LtlSet.of_list [l ; r], None);
			(LtlSet.of_list [r ; Next(exp)], None)]
    | Globally(p) -> [(LtlSet.of_list [p; Next(exp)], None)]
    | Until(l, r) -> [(LtlSet.singleton r, None);
		      (LtlSet.of_list [l;Next(exp)], Some(exp))]
    | Finally(p) -> [(LtlSet.singleton p, None);
		     (LtlSet.singleton (Next exp), Some(exp))]
    | _ -> failwith "reduced form given"
  in
  let (reduced, complex) = LtlSet.partition is_reduced set in
  if LtlSet.is_empty complex then
    None
  else
    let (exp, complex) = LtlSet.pop_largest complex in
    let rest = LtlSet.union reduced complex in
    let transformed = apply_rule exp in (* Reduce the largest non-reduced formula *)
    Some(List.map (fun (set, cond) -> (LtlSet.union set rest, cond)) transformed)

(* Calculate sigma transform condition and result set,
   input should be reduced and consistent *)
let sigma_transform set =
  List.fold_left (fun (conds, next) -> function
    | Top -> (conds, next)
    | Bottom -> failwith "inconsistent Bottom"
    | Atom(p) -> (Atom(p) :: conds, next)
    | Not(Atom(p)) -> (Not(Atom(p)) :: conds, next)
    | Next(x) -> (conds, LtlSet.add x next)
    | other -> failwith ("not reduced " ^ to_string other))
    ([], LtlSet.empty)(LtlSet.elements set)
    
  
