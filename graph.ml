(* Output files compatible with dot *)

type shape = DoubleCircle | Circle

type node = {
  name : string;
  shape : shape;
  start : bool;
}

type edge {
  label : string;
  s : node;
  t : node;
}

type graph = {
  title : string;
  settings : string list;
  nodes : node list;
  edges : edge list;
}

let new_graph title =
  { title = title; settings = []; nodes = []; edges = [] }

let find_node {nodes = nodes} name =
  List.find (fun n -> n.name = name) nodes

let add_node graph node =
  try begin
    ignore (find_node graph node.name);
    graph
  end with
    | Not_found -> { graph with nodes = node :: graph.nodes }

let link graph s_name t_name label =
  { graph with edges = 
      { label = label;
	s = find_node graph s_name; 
	t = find_node graph t_name;
      } :: graph.edges }

open Printf

let print_nodes out nodes =
  let print_node_list nodes =
    if not (List.is_empty nodes) then
      (List.iter (fun n -> fprintf out "\"%s\" " n.name) nodes;
       fprintf out ";\n")
  in
  let (circle, double) = List.partition (fun n -> n.shape = Circle) nodes in
  fprintf out "\tnode [shape = doublecircle]; ";
  print_node_list double;
  fprintf out "\tnode [shape = circle]; ";
  print_node_list circle;
  let starts = List.find_all (fun n -> n.start) nodes in
  List.iter (fun n -> 
    fprintf out "\t\"_nil_%s\" [style=\"invis\"];\n\t\"_nil_%s\" -> \"%s\";\n"
      n.name n.name n.name) starts

let print_edges out =
  List.iter (fun e ->
    fprintf out "\t\"%s\" -> \"%s\" [ label = \"%s\" ];\n" e.s.name e.t.name e.label)

let print_graph out { title = title; settings = settings; nodes = nodes; edges = edges } =
  fprintf out "digraph %s {\n" title;
  List.iter (fprintf out "\t%s\n").settings;
  print_nodes out nodes;
  print_edges out edges;
  fprintf out "}\n"
