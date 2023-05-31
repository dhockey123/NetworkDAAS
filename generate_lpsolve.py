import os

def min_hops(vars):
    obj_func = "min: "
    for i, demand in enumerate(vars["NetworkPaths"]):
        for j, flow in enumerate(demand):
            obj_func += "%dX%d%d+" % (len(flow), i+1, j+i)
    obj_func = obj_func[:-1]+";\n"
    return obj_func

def min_routing_cost(vars):
    obj_func = "min: "
    for i, demand in enumerate(vars["NetworkPaths"]):
        for j, flow in enumerate(demand):
            flow_cost = 0
            ## optimize later - dot product sliced arrays
            for link in flow:
                flow_cost += vars["LinkCosts"][link-1]
            obj_func += "%dX%d%d+" % (flow_cost, i+1, j+1)

    obj_func = obj_func[:-1] + ";\n"
    return obj_func

def get_obj_function(vars):
    match vars["Obj_Func"]:
        case "min_hops":
            vars["Obj_Func"] = min_hops(vars)
        case "min_routing_cost":
            vars["Obj_Func"] = min_routing_cost(vars)
        case "none":
            vars["Obj_Func"] = "min: ;"
    return vars["Obj_Func"]

def get_demand_constraints(NetworkPaths, NetworkDemands):
    all_demand_constraints = ""
    for i, demand in enumerate(NetworkPaths):
        demand_constraint = ""
        for x in range(len(demand)):
            demand_constraint += "X%d%d+" % (i+1, x+1)
        demand_constraint = demand_constraint[:-1] + "=" +str(NetworkDemands[i]) + ";\n"
        all_demand_constraints+=demand_constraint
    return all_demand_constraints

def get_capacity_constraints(NetworkPaths, LinkCapacities):
    all_capacity_constraints = ""
    print("NP: ", NetworkPaths)
    print("LC: ", LinkCapacities)
    for x in range(1,len(LinkCapacities)+1):
        link_inequality = ""
        for i, demand_path in enumerate(NetworkPaths):
            for j, flow in enumerate(demand_path):
                if x in flow:
                    link_inequality += "X%d%d+" % (i+1,j+1)
        if link_inequality != "":
            if LinkCapacities[x-1] != 'empty':
                link_inequality = link_inequality[:-1] + "<=" + str(LinkCapacities[x-1]) + ";\n"
            else:
                link_inequality = link_inequality[:-1] + "<=y" + str(x) + ";\n"
        all_capacity_constraints+=link_inequality
    return all_capacity_constraints

def get_enforced_path_constraints(NetworkPaths, NetworkDemands, min_paths):
    all_enf_path_constraints = ""
    for i, demand in enumerate(NetworkPaths):
        for j, flow in enumerate(demand):
            all_enf_path_constraints += ("X%d%d<=%.2f;\n" %(i+1, j+1, NetworkDemands[i]/min_paths))
    return all_enf_path_constraints

def get_flows_in_use(NetworkPaths, NetworkDemands):
    all_flows_in_use = ""
    for i, demand in enumerate(NetworkPaths):
        for j, flow in enumerate(demand):
            all_flows_in_use += "X%d%d<=%dU%d%d;\n" % (i+1, j+1, NetworkDemands[i], i+1, j+1)
    return all_flows_in_use

def get_lower_bound_flows(NetworkPaths, min_flow_vol):
    all_lower_bound_flows = ""
    for i, demand in enumerate(NetworkPaths):
        for j, flow in enumerate(demand):
            all_lower_bound_flows += "%dU%d%d<=X%d%d;\n" % (min_flow_vol,  i+1, j+1, i+1, j+1)
    return all_lower_bound_flows

def solve(vars):
    f = open("lp_solve.txt", "w+")
    ## OBJECTIVE FUNCTION
    f.write("// OBJECTIVE FUNCTION\n")
    f.write(get_obj_function(vars))

    # ## DEMAND CONSTRAINTS
    f.write("\n// DEMAND CONSTRAINTS\n")
    f.write(get_demand_constraints(vars["NetworkPaths"], vars["NetworkDemands"]))

    # ## CAPACITY CONSTRAINTS
    f.write("\n// CAPACITY CONSTRAINTS\n")
    f.write(get_capacity_constraints(vars["NetworkPaths"], vars["LinkCapacities"]))
    print("Test1", vars["Min_#_Paths/Demand"])
    
    if vars["Min_#_Paths/Demand"] != "empty" and vars["Min_#_Paths/Demand"] > 1:
        print("Test2", vars["Min_#_Paths/Demand"])
        f.write("\n// ENFORCE PATH DIVERSITY\n")
        f.write(get_enforced_path_constraints(vars["NetworkPaths"],
                                              vars["NetworkDemands"],
                                              vars["Min_#_Paths/Demand"]))
    if vars["Min_Flow_vol"] != "empty" and vars["Min_Flow_vol"] > 0:
        f.write("\n// FLOWS IN USE\n")
        f.write(get_flows_in_use(vars["NetworkPaths"], vars["NetworkDemands"]))
        f.write("\n// LOWER BOUND ON FLOWS\n")
        f.write(get_lower_bound_flows(vars["NetworkPaths"], vars["Min_Flow_vol"]))
        f.write("\n//VARIABLES\n")
        bin = "bin "
        for i, demand in enumerate(vars["NetworkPaths"]):
            for j, flow in enumerate(demand):
                bin += "U%d%d," % (i+1, j+1)
        f.write(bin[:-1]+";\n")
    f.close()
    return os.system("lp_solve "+os.getcwd()+"/lp_solve.txt")


