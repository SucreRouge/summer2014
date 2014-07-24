{
  open Parser
}

let space = [' ' '\t']
let digit = ['0'-'9']
let alpha = ['A'-'Z' 'a'-'z' '_']
let alnum = digit | alpha | '\''

let atom = ['a'-'z']

rule token = parse
  | space+ { token lexbuf }  (* skip spaces *)
  
  | '(' { LPAREN }
  | ')' { RPAREN }

  | atom { ATOM (Lexing.lexeme lexbuf) }
  | "top" { TOP }
  | "bottom" { BOTTOM }
  | "!"  { NOT }
  | "not" { NOT }
  | "&&" { AND }
  | "and" { AND }
  | "||" { OR }
  | "or" { OR }
  | "X" { NEXT }
  | "N" { NEXT }
  | "F" { FINALLY }
  | "G" { GLOBALLY }
  | "U" { UNTIL }
  | "R" { RELEASE }

  | eof { EOF }
