import os

def min_hops(vars):
    obj_func = "min: "
    for i, demand in enumerate(vars["path_flow_vars"]):
        for j, flow in enumerate(demand):
            obj_func += "%dX%d%d+" % (len(flow), i+1, j+i)
    obj_func = obj_func[:-1]+";\n"
    return obj_func

def min_routing_cost(vars):
    obj_func = "min: "
    for i, demand in enumerate(vars["path_flow_vars"]):
        for j, flow in enumerate(demand):
            flow_cost = 0
            ## optimize later - dot product sliced arrays
            for link in flow:
                flow_cost += vars["cost_entries"][link-1]
            obj_func += "%dX%d%d+" % (flow_cost, i+1, j+1)

    obj_func = obj_func[:-1] + ";\n"
    return obj_func

def get_obj_function(vars):
    match vars["obj_func"]:
        case "min_hops":
            vars["obj_func"] = min_hops(vars)
        case "min_routing_cost":
            vars["obj_func"] = min_routing_cost(vars)
        case "none":
            vars["obj_func"] = "min: ;"
    return vars["obj_func"]

def get_demand_constraints(path_flow_vars, path_flow_DV):
    all_demand_constraints = ""
    for i, demand in enumerate(path_flow_vars):
        demand_constraint = ""
        for x in range(len(demand)):
            demand_constraint += "X%d%d+" % (i+1, x+1)
        demand_constraint = demand_constraint[:-1] + "=" +str(path_flow_DV[i]) + ";\n"
        all_demand_constraints+=demand_constraint
    return all_demand_constraints

def get_capacity_constraints(path_flow_vars, link_capacities):
    all_capacity_constraints = ""
    for x in range(1,len(link_capacities)+1):
        link_inequality = ""
        # print(x, end=" ")
        for i, demand_path in enumerate(path_flow_vars):
            for j, flow in enumerate(demand_path):
                if x in flow:
                    link_inequality += "X%d%d+" % (i+1,j+1)
        if link_inequality != "":
            if link_capacities[x-1] != 0:
                link_inequality = link_inequality[:-1] + "<=" + str(link_capacities[x-1]) + ";\n"
            else:
                link_inequality = link_inequality[:-1] + "<=y" + str(x) + ";\n"
        all_capacity_constraints+=link_inequality
    return all_capacity_constraints

def get_enforced_path_constraints(path_flow_vars, path_flow_DV, min_paths):
    all_enf_path_constraints = ""
    for i, demand in enumerate(path_flow_vars):
        for j, flow in enumerate(demand):
            all_enf_path_constraints += ("X%d%d<=%.2f;\n" %(i+1, j+1, path_flow_DV[i]/min_paths))
    return all_enf_path_constraints

def get_flows_in_use(path_flow_vars, path_flow_DV):
    all_flows_in_use = ""
    for i, demand in enumerate(path_flow_vars):
        for j, flow in enumerate(demand):
            all_flows_in_use += "X%d%d<=%dU%d%d;\n" % (i+1, j+1, path_flow_DV[i], i+1, j+1)
    return all_flows_in_use

def get_lower_bound_flows(path_flow_vars, min_flow_vol):
    all_lower_bound_flows = ""
    for i, demand in enumerate(path_flow_vars):
        for j, flow in enumerate(demand):
            all_lower_bound_flows += "%dU%d%d<=X%d%d;\n" % (min_flow_vol,  i+1, j+1, i+1, j+1)
    return all_lower_bound_flows

# def solve_gen_dimen_alloc_prob(path_flow_vars, path_flow_DV, link_capacities, obj_func):
#     f = open("lp_solve.txt", "w+")
#     ## OBJECTIVE FUNCTION
#     f.write("// OBJECTIVE FUNCTION\n")
#     f.write(obj_func)

#     ## DEMAND CONSTRAINTS
#     f.write("\n// DEMAND CONSTRAINTS\n")
#     f.write(get_demand_constraints(path_flow_vars, path_flow_DV))

#     ## CAPACITY CONSTRAINTS
#     f.write("\n// CAPACITY CONSTRAINTS\n")
#     f.write(get_capacity_constraints(path_flow_vars, link_capacities))

#     f.close()
#     os.system("lp_solve "+os.getcwd()+"/lp_solve.txt")
def solve_gen_dimen_alloc_prob(vars):
    f = open("lp_solve.txt", "w+")
    ## OBJECTIVE FUNCTION
    f.write("// OBJECTIVE FUNCTION\n")
    f.write(get_obj_function(vars))

    ## DEMAND CONSTRAINTS
    f.write("\n// DEMAND CONSTRAINTS\n")
    f.write(get_demand_constraints(vars["path_flow_vars"], vars["path_flow_DV"]))

    ## CAPACITY CONSTRAINTS
    f.write("\n// CAPACITY CONSTRAINTS\n")
    f.write(get_capacity_constraints(vars["path_flow_vars"], vars["capacity_entries"]))

    f.close()
    os.system("lp_solve "+os.getcwd()+"/lp_solve.txt")

def solve_enforced_path_diversity(vars):
    f = open("lp_solve.txt", "w+")
    ## OBJECTIVE FUNCTION
    f.write("// OBJECTIVE FUNCTION\n")
    f.write(get_obj_function(vars))

    ## DEMAND CONSTRAINTS
    f.write("\n// DEMAND CONSTRAINTS\n")
    f.write(get_demand_constraints(path_flow_vars, path_flow_DV))

    ## CAPACITY CONSTRAINTS
    f.write("\n// CAPACITY CONSTRAINTS\n")
    f.write(get_capacity_constraints(path_flow_vars, link_capacities))

    ## ENFORCED PATH DIVERSITY
    f.write("\n// ENFORCED PATH DIVERSITY\n")
    f.write(get_enforced_path_constraints(path_flow_vars, path_flow_DV, min_paths))

    f.close()
    os.system("lp_solve "+os.getcwd()+"/lp_solve.txt")

def solve_min_flow_vol(path_flow_vars, path_flow_DV, link_capacities, min_flow_vol, obj_func):
    f = open("lp_solve.txt", "w+")
    ## OBJECTIVE FUNCTION
    f.write("// OBJECTIVE FUNCTION\n")
    f.write(obj_func)
    
    ## DEMAND CONSTRAINTS
    f.write("\n// DEMAND CONSTRAINTS\n")
    f.write(get_demand_constraints(path_flow_vars, path_flow_DV))

    ## CAPACITY CONSTRAINTS
    f.write("\n// CAPACITY CONSTRAINTS\n")
    f.write(get_capacity_constraints(path_flow_vars, link_capacities))

    ## FLOWS IN USE
    f.write("\n// FLOWS IN USE\n")
    f.write(get_flows_in_use(path_flow_vars, path_flow_DV))

    ## MIN FLOW VOLUME
    f.write("\n// MIN FLOW VOLUME\n")
    f.write(get_lower_bound_flows(path_flow_vars, min_flow_vol))


    f.close()
    os.system("lp_solve "+os.getcwd()+"/lp_solve.txt")

## commit test