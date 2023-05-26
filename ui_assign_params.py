from tkinter import *
from path_tool import path_finder, node_paths_to_demand_paths
from generate_lpsolve import gen_lp_solve_code
link_cost_entries = []
link_capacity_entries = []
demand_entries = []
row = 1

## Globals are a mess, fix later

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
    global link_cost_entries, link_capacity_entries, demand_entries
    path_flow_vars = []
    path_flow_DV = []
    link_capacities = []
    print
    idx = 0
    for i in range(0, len(demand_entries), 3):
        idx+=1
        node_a = int(demand_entries[i].get())
        node_b = int(demand_entries[i+1].get())
        node_paths = path_finder(links, node_a, node_b)
        demand_paths = node_paths_to_demand_paths(links, node_paths)
        # print("d{0} paths -> {1}".format(idx, demand_paths))
        
        path_flow_vars.append(demand_paths)
        path_flow_DV.append(float(demand_entries[i+2].get()))
    for i in range(len(link_capacity_entries)):
        link_capacities.append(float(link_capacity_entries[i].get()))
    # print(link_capacities)

    gen_lp_solve_code(path_flow_vars, path_flow_DV, link_capacities)
    win.destroy()
    link_cost_entries = []
    link_capacity_entries = []
    demand_entries = []


def assign_params(links):
    global row, win, demand_entries
    link_cost_entries = []
    demand_entries = []

    win = Tk()

    win.geometry("300x670")
    win.title("")
    
    
    Label(win, text="Link costs", font=('Helvetica', 12, 'bold')).grid(row=row, column=0, columnspan=6)
    Label(win, text="Link Capacities", font=('Helvetica', 12, 'bold')).grid(row=row, column=6, columnspan=6)
    for i in range(len(links)):
        row +=1
        link_cost_entries.append(Entry(win, width= 8))
        Label(win, text="e%d" % (i+1)).grid(row=row, column=0, columnspan=1)
        link_cost_entries[i].grid(row=row, column=1, columnspan=5)
 
        link_capacity_entries.append(Entry(win, width= 8))
        Label(win, text="c%d" % (i+1)).grid(row=row, column=6, columnspan=1)
        link_capacity_entries[i].grid(row=row, column=7, columnspan=4)
    row+=1
    # DEMANDS
    Label(win, text="Demands", font=('Helvetica', 12, 'bold')).grid(row=row, column=0, columnspan=12)
    row+=1
    Label(win, text="Node A").grid(row=row, column=0, columnspan=4)
    Label(win, text="Node B").grid(row=row, column=4, columnspan=4)
    Label(win, text="DVUs").grid(row=row, column=8, columnspan=4)
    create_demand()


    
    Button(win, text="Create demand",font=('Helvetica', 12, 'bold'), command=create_demand).grid(row=100, column=0, columnspan=3)
    Button(win, text="Remove demand",font=('Helvetica', 12, 'bold'), command=remove_demand).grid(row=100, column=6, columnspan=3)
    Button(win, text="LP_SOLVE", font=('Helvetica', 12, 'bold'), command=lambda: print_demand(links, win)).grid(row=102, column=0, columnspan=12)

    win.mainloop()