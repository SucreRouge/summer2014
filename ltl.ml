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

(* A set of formulae is reduced if all formulae are either literals or
   formulae with outermost connective X *)


(* Main function *)
let () =
  let exp = Not(And(Atom "p", Finally(Or(Bottom, Next(Atom "q"))))) in
  print_string ((to_string exp) ^ "\n" ^ (to_string (nnf exp)) ^ "\n")
