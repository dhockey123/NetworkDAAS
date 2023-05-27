from tkinter import *
from path_tool import path_finder, node_paths_to_demand_paths
from generate_lpsolve import *
from objective_functions import *
link_cost_entries = []
link_capacity_entries = []
demand_entries = []
min_flow_volume = 0
min_num_paths_p_demand = 0
row = 1
obj_func_type = ""

## Globals are a mess, fix later
## Passing around too many different arrays. USE dictionaries!

def create_demand():
    global win, demand_entries
    win.title("")
    global row
    row+=1
    for i in range(3):
        demand_entries.append(Entry(win, width=8))
        demand_entries[-1].grid(row=row, column=i*4, columnspan=4)

def remove_demand():
    global win, demand_entries
    try:
        for i in range(3):
            demand_entries[-1].destroy()
            demand_entries.pop()

    except:
        win.title("No demands to remove..")

   
def print_demand(links, win):
    global link_cost_entries, link_capacity_entries, demand_entries, obj_func_type
    global min_num_paths_p_demand, min_flow_volume
    path_flow_vars = []
    path_flow_DV = []
    link_capacities = []
    link_costs = []
    print(min_flow_volume.get())
    print(min_num_paths_p_demand.get())
    idx = 0
    for i in range(0, len(demand_entries), 3):
        idx+=1
        node_a = int(demand_entries[i].get())
        node_b = int(demand_entries[i+1].get())
        node_paths = path_finder(links, node_a, node_b)
        demand_paths = node_paths_to_demand_paths(links, node_paths)
        
        path_flow_vars.append(demand_paths)
        path_flow_DV.append(float(demand_entries[i+2].get()))
    for i in range(len(link_capacity_entries)):
        try:
            link_capacities.append(float(link_capacity_entries[i].get()))
        except:
            link_capacities.append(0)
    for i in range(len(link_capacity_entries)):
        try:
            link_costs.append(float(link_cost_entries[i].get()))
        except:
            link_costs.append(0)

    obj_func = min_hops(path_flow_vars)
    # print("here->", obj_func)

    match obj_func_type:
        case "min_hops":
            obj_func = min_hops(path_flow_vars)
        case "min_routing_cost":
            obj_func = min_routing_cost(path_flow_vars, link_costs)

    solve_gen_dimen_alloc_prob(path_flow_vars, path_flow_DV, link_capacities, obj_func)
    # win.destroy()
    # link_cost_entries = []
    # link_capacity_entries = []
    # demand_entries = []

def set_obj_func(var):
    global obj_func_type
    # var = var.get()
    match int(var.get()):
        case 1:
            obj_func_type = "min_hops"
        case 2:
            obj_func_type = "min_routing_cost"

def assign_params(links):
    global row, win, demand_entries, obj_func_type, min_flow_volume, min_num_paths_p_demand
    demand_entries = []

    win = Tk()
    var = IntVar()

    win.geometry("300x670")
    win.title("")
    
    # LINK COSTS AND CAPACITIES
    Label(win, text="Link costs", font=('Helvetica', 12, 'bold')).grid(row=row, column=0, columnspan=6)
    Label(win, text="Link Capacities", font=('Helvetica', 12, 'bold')).grid(row=row, column=6, columnspan=6)
    for i in range(len(links)):
        row +=1
        link_cost_entries.append(Entry(win, width= 8))
        Label(win, text="e%d" % (i+1)).grid(row=row, column=0, columnspan=1)
        link_cost_entries[i].grid(row=row, column=1, columnspan=5)
 
        link_capacity_entries.append(Entry(win, width= 8, ))
        Label(win, text="c%d" % (i+1)).grid(row=row, column=6, columnspan=1)
        link_capacity_entries[i].grid(row=row, column=7, columnspan=4)
    row+=1
    # EXTRA PATH CONSTRAINTS
    Label(win, text="Min flow volume").grid(row=row, column=0)
    min_flow_volume = Entry(win, width=8)
    min_flow_volume.grid(row=row, column = 3)
    row+=1
    Label(win, text="Min # paths per demand").grid(row=row, column=0)
    min_num_paths_p_demand = Entry(win, width=8)
    min_num_paths_p_demand.grid(row=row, column = 3)
    row+=1
    # DEMANDS
    Label(win, text="Demands", font=('Helvetica', 12, 'bold')).grid(row=row, column=0, columnspan=12)
    row+=1
    Label(win, text="Node A").grid(row=row, column=0, columnspan=4)
    Label(win, text="Node B").grid(row=row, column=4, columnspan=4)
    Label(win, text="DVUs").grid(row=row, column=8, columnspan=4)
    create_demand()
    # RADIO BUTTONS
    row+=1
    n_row=100
    r = Radiobutton(win, text="Min Hops", variable=var, value=1, command=lambda: set_obj_func(var))
    r.grid(row=n_row, column=2, columnspan=4)
    n_row+=1
    r = Radiobutton(win, text="Min Routing Cost", variable=var, value=2, command=lambda: set_obj_func(var))
    r.grid(row=n_row, column=2, columnspan=4)
    ## BUTTONS
    n_row+=1
    Button(win, text="Create demand",font=('Helvetica', 12, 'bold'), command=create_demand).grid(row=n_row, column=0, columnspan=3)
    Button(win, text="Remove demand",font=('Helvetica', 12, 'bold'), command=remove_demand).grid(row=n_row, column=6, columnspan=3)
    n_row+=1
    Button(win, text="LP_SOLVE", font=('Helvetica', 12, 'bold'), command=lambda: print_demand(links, win)).grid(row=n_row, column=0, columnspan=12)
    n_row+=1
    win.mainloop()

# assign_params([(1,2),(2,3),(1,3)])