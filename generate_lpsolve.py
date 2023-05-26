# path_flow_vars = [[[1], [3, 2], [3, 5, 4]], [[2],[1, 3], [4, 5]]]
# link_capacities = [1,2,3,4,5]
def gen_lp_solve_code(path_flow_vars, path_flow_DV, link_capacities):
    print(path_flow_vars)
    print(path_flow_DV)
    f = open("lp_solve.txt", "w+")
    f.write("// DEMAND CONSTRAINTS\n")
    for i, flows in enumerate(path_flow_vars):
        demand_constraint = ""
        ## DEMAND CONSTRAINTS
        for x in range(len(flows)):
            demand_constraint += "x%d%d+" % (i+1, x+1)

        demand_constraint = demand_constraint[:-1] + "=" +str(path_flow_DV[i]) + ";\n"

        f.write(demand_constraint)


    f.write("\n// CAPACITY CONSTRAINTS\n")
    ## CAPACITY CONSTRAINTS
    for x in range(1,len(link_capacities)+1):
        link_inequality = ""
        # print(x, end=" ")
        for i, demand_path in enumerate(path_flow_vars):
            for j, flow in enumerate(demand_path):
                # print(j, flow, len(demand_path))
            
                if x in flow:
                    link_inequality += "x%d%d+" % (i+1,j+1)

        link_inequality = link_inequality[:-1] + "<=" + str(link_capacities[x-1]) + ";\n"
        f.write(link_inequality)

# gen_lp_solve_code(path_flow_vars, path_flow_DV)