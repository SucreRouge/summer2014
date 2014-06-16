(* Usage message *)
let usage = "Usage: ltl2ba [LTL EXPRESSION] [OUTPUT FILE]\n" ^
  "See `ltl2ba --help' for more information.\n"

let help = "This is an unhelpful help message.\n"

let file path =
  open_out_gen [Open_wronly; Open_creat; Open_trunc; Open_text] 0o666 path

let main formula path =
  let formula = (Parser.main Lexer.token (Lexing.from_string formula)) in
  print_endline ("Interpreted: " ^ (Ltl.to_string formula) ^ ".");
  print_endline "Converting LTL formula to negative normal form.";
  let formula_set = (Ltl.LtlSet.singleton (Ltl.nnf formula)) in
  print_endline "Constructing automaton from formula.";
  let a = Automaton.construct_gba_from formula_set in
  print_endline "Printing automaton to graph.";
  let g = Automaton.to_graph a in
  let out = file path in
  Graph.print_graph out g;
  close_out out;
  print_endline ("Graph output saved to " ^ path)
		    

(* Main function, produces graph from string ltl input *)
let () =
  if Array.length Sys.argv >= 2 && Sys.argv.(1) = "--help"
  then print_string help else
    if Array.length Sys.argv <> 3 then print_string usage
    else
      (* Run the main program on the input arguements *)
      main Sys.argv.(1) Sys.argv.(2)
