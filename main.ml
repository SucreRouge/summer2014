(* Usage message *)
let usage = "Usage: ltl2ba [LTL EXPRESSION] [OUTPUT FILE]\n" ^
  "See `ltl2ba --help' for more information.\n"

let help = "This is an unhelpful help message.\n"

let main formula file =
  let formula = (Parser.main Lexer.token (Lexing.from_string formula)) in
  print_endline (Ltl.to_string formula)

(* Main function, produces graph from string ltl input *)
let () =
  if Array.length Sys.argv >= 2 && Sys.argv.(1) = "--help"
  then print_string help else
    if Array.length Sys.argv <> 3 then print_string usage
    else
      (* Run the main program on the input arguements *)
      main Sys.argv.(1) Sys.argv.(2)
