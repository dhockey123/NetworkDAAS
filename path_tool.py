def path_finder(links, a, b, path=None, result=None):
    if path is None:
        path = []
    if result is None:
        result = []
    path.append(a)
    if a == b:
        if path not in result:
            result.append(path)
    for link in links:
        if a in link:
            if a == link[0]:
                next_node = link[-1]
            elif a == link[1]:
                next_node = link[0]
            if next_node not in path:
                new_path = list(path)
                path_finder(links, next_node, b, new_path, result)
    
    return result

def node_paths_to_demand_paths(links, paths):
    demand_paths = []
    
    for path in paths:
        tmp_path = []
        for i in range(len(path)-1):
            for idx, link in enumerate(links):
                if path[i] in link and path[i+1] in link:
                    tmp_path.append(idx+1)
        demand_paths.append(tmp_path)

    return sorted(demand_paths, key=len)

def limit_path_hops(length, paths):
    new_paths = []
    for demand in paths:
        new_path = []
        for path in demand:
            if len(path) <= length:
                print(path, len(path))
                new_path.append(path)
        new_paths.append(new_path)
        
    return(new_paths)


# links = [(1, 2), (2, 3), (3, 1), (2, 4), (4, 3)]

# print(path_finder(links, 2, 1))
# print(node_paths_to_demand_paths(links, path_finder(links,1 , 2)))
# paths = [[[1], [3, 2]],[[2],[1,3]]]
# print(limit_path_hops(1, paths))