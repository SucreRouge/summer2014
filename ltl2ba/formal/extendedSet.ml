module Make(Ord:Set.OrderedType) = struct
  module S =
    Set.Make(Ord)
  include S

  let of_list l = List.fold_left (fun s e -> add e s) empty l
  let of_option = function
    | Some(i) -> singleton i
    | None -> empty
  let unions = List.fold_left union empty

  let pop s =
    if is_empty s then None else
      let item = choose s in
      Some (item, remove item s)
      
  let map_list f s = List.map f (elements s)

  let map f s = of_list (map_list f s)

end
