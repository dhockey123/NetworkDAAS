
from tkinter import *
from path_tool import *
from generate_lpsolve import solve
demand_rows = 4
# # links = [(1,2),(2,3),(1,3)]
# nodes =  [1, 2, 3, 4]
# links =   [(1, 2), (2, 3), (1, 4), (3, 4), (1, 3)]
# node_types = ["full", "full", "sourcesink", "full"]

def print_demand(links):
    demand_entries = vars["demand_entries"]
    for i in range(0, len(demand_entries), 3):
        node_a = int(demand_entries[i].get())
        node_b = int(demand_entries[i+1].get())
        node_paths = path_finder(links, node_a, node_b)
        node_paths = remove_source_sink(node_paths, node_a, node_b, vars["node_types"])
        demand_paths = node_paths_to_demand_paths(links, node_paths)
        vars["path_flow_vars"].append(demand_paths)
        vars["path_flow_DV"].append(float(demand_entries[i+2].get()))
    for i in range(len(vars["capacity_entries"])):
        try:
            vars["capacity_entries"][i] = float(vars["capacity_entries"][i].get())
        except:
            vars["capacity_entries"][i] = 0
        try: 
            vars["cost_entries"][i] = float(vars["cost_entries"][i].get())
        except:
            vars["cost_entries"][i] = 0
    
    if vars["max_path_length"].get():
        vars["max_path_length"] = float(vars["max_path_length"].get())
        vars["path_flow_vars"] = limit_path_hops(vars["max_path_length"],vars["path_flow_vars"])
    else:
        vars["max_path_length"] = 0
    if vars["min_flow_vol"].get():
        vars["min_flow_vol"] = float(vars["min_flow_vol"].get())
    else:
        vars["min_flow_vol"] = 0
    if vars["min_#_paths/demand"].get():
        vars["min_#_paths/demand"] = int(vars["min_#_paths/demand"].get())
    else:
        vars["min_#_paths/demand"] = 0
    print("Min flow vol: ", vars["min_flow_vol"])
    print("Max Paths/demand: ", vars["min_#_paths/demand"])
    print("Max path length: ", vars["max_path_length"])
    solve(vars)

    # win.destroy()

    
def create_demand(demand_frame):
    global demand_rows #, demand_frame,win
    for i in range(3):
        vars["demand_entries"].append(Entry(demand_frame, width=10))
        vars["demand_entries"][-1].grid(row=demand_rows, column=i)
    demand_rows+=1
    
def remove_demand():
    global demand_rows
    try:
        for i in range(3):
            vars["demand_entries"][-1].destroy()
            vars["demand_entries"].pop()
    except:
        Exception
    demand_rows-=1
    
def debug():
    print("test")
    for i in vars["demand_entries"]:
        print(i.get())
    for i in vars["cost_entries"]:
        print(i.get())
    for i in vars["capacity_entries"]:
        print(i.get())  
    print(vars["obj_func"])  
    print(vars["max_path_length"].get())
    print(vars["min_#_paths/demand"].get())
    print(vars["min_flow_vol"].get())
    
def set_obj_func(rb_var):
    match int(rb_var.get()):
        case 1:
            vars["obj_func"] = "min_hops"
        case 2:
            vars["obj_func"] = "min_routing_cost"
        case 3:
            vars["obj_func"] = "none"
    
vars= {}
vars["cost_entries"] = []
vars["capacity_entries"] = []
vars["demand_entries"] = []
vars["obj_func"] = 3
vars["path_flow_vars"] = []
vars["path_flow_DV"] = []



def assign_params(links, node_types):
    win = Tk()
    rb_var = IntVar()
    
    vars["node_types"] = node_types

    win.resizable(False,False)
    l_frame = Frame(win, width=150)
    l_frame.grid(row=0, column=0, sticky="nsew")
    r_frame = Frame(win, width=150)
    r_frame.grid(row=0, column=1, sticky="nsew")
    demand_frame = Frame(win, width=300)
    demand_frame.grid(row=1, column=0,  columnspan=2, sticky="nsew")

    win.columnconfigure(0, weight=1) 
    win.columnconfigure(1, weight=1) 
    win.rowconfigure(0, weight=1) 
    win.rowconfigure(1, weight=1) 

    ## LINK COSTS AND CAPACITIES
    Label(l_frame, text="Link Costs", font=('Helvetica', 12, 'bold')).grid(row=0, column=0, columnspan=2)
    Label(r_frame, text="Link Capacities", font=('Helvetica', 12, 'bold')).grid(row=0, column=1, columnspan=2)

    for i in range(1, len(links)+1):
        Label(l_frame, text="e%d" % (i) ).grid(row=i, column=0)
        vars["cost_entries"].append(Entry(l_frame, width=10))
        vars["cost_entries"][i-1].grid(row=i, column=1)
        Label(r_frame, text="c%d" % (i)).grid(row=i, column=0)
        vars["capacity_entries"].append(Entry(r_frame, width=10))
        vars["capacity_entries"][i-1].grid(row=i, column=1)
        
    ## DEMANDS
    demand_frame.columnconfigure(0, weight=1)
    demand_frame.columnconfigure(1, weight=1)
    demand_frame.columnconfigure(2, weight=1)

    Label(demand_frame, text="Demands", font=('Helvetica', 12, 'bold')).grid(row=0, column=0, columnspan=3)
    Label(demand_frame, text="Node A").grid(row=1, column=0)
    Label(demand_frame, text="Node B").grid(row=1, column=1)
    Label(demand_frame, text="DVUs").grid(row=1, column=2)
    create_demand(demand_frame)  

    ## OBJECTIVE FUNCTION
    obj_frame = Frame(win, width=300)
    obj_frame.grid(row=2, column=0, columnspan=2)
    Label(obj_frame, text="Objective function", font=('Helvetica', 12, 'bold')).grid(row=0, column=0, columnspan=3)
    Radiobutton(obj_frame, text="Min hops", variable=rb_var, command=lambda:set_obj_func(rb_var), value=1).grid(row=1, column=0)
    Radiobutton(obj_frame, text="Min routing cost", variable=rb_var, command=lambda:set_obj_func(rb_var), value=2).grid(row=1, column=1)
    Radiobutton(obj_frame, text="None", variable=rb_var, command=lambda:set_obj_func(rb_var), value=3).grid(row=1, column=2)

    ## PATH/FLOW CONSTRAINTS
    rules_frame = Frame(win, width=300)
    rules_frame.grid(row=3, column=0, columnspan=3)
    rules_frame.columnconfigure(0, weight=1)
    rules_frame.columnconfigure(1, weight=2)
    Label(rules_frame, text="Path/Flow constraints", font=('Helvetica', 12, 'bold')).grid(row=0, column=0, columnspan=3)
    Label(rules_frame, text="Max. path length").grid(row=1, column=0)
    vars["max_path_length"] = Entry(rules_frame, width=10)
    vars["max_path_length"].grid(row=1, column=1, columnspan=2)
    Label(rules_frame, text="Min. flow volume").grid(row=2, column=0)
    vars["min_flow_vol"] = Entry(rules_frame, width=10)
    vars["min_flow_vol"].grid(row=2, column=1, columnspan=2)
    Label(rules_frame, text="Min. # paths/demand").grid(row=3, column=0)
    vars["min_#_paths/demand"] = Entry(rules_frame, width=10)
    vars["min_#_paths/demand"].grid(row=3, column=1, columnspan=2)

    buttons_frame = Frame(win, width=300)
    buttons_frame.grid(row=4, column=0, columnspan=3)
    Button(buttons_frame, text="Create demand", command=lambda: create_demand(demand_frame)).grid(row=0, column=0)
    Button(buttons_frame, text="Remove demand", command=remove_demand).grid(row=0, column=1)
    Button(buttons_frame, text="DEBUG", command=lambda: print_demand(links)).grid(row=1, column=0, columnspan=3)
    win.mainloop()


# assign_params(links, node_types)