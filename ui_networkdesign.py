from tkinter import *
from path_tool import *
from generate_lpsolve import *

class SideDashBoard(Frame):
    def __init__(self, parent):
        super().__init__(parent)
  
        self.WIDTH = 200
        self.HEIGHT = 900
        self.LINK_ROW = 0
        self.DEMAND_ROW = 1
        objective = IntVar()
        self.config(width=self.WIDTH, height=self.HEIGHT)
        self.pack(side="left", anchor="n")
        self.pack_propagate(0)
        self.ProblemFormulation = {
            "Nodes":[],
            "LinkCosts":[],
            "LinkCapacities":[],
            "NetworkPaths":[],
            "NetworkDemands":[],
            "Min_Flow_Vol":0,
            "Min_#_Paths/Demand":0, 
            "Obj_Func":"none"
        }
        
        self.demand_entries = []
        self.cost_entries = []
        self.capacity_entries = []

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        
        ## Link costs
        self.l_frame = Frame(self)
        self.l_frame.grid(row=0, column=0)
        Label(self.l_frame, text="Link Costs",font=('Helvetica','12','bold')).grid(row=self.LINK_ROW, column=0, columnspan=2)
        ## Link capacities
        self.r_frame = Frame(self)
        self.r_frame.grid(row=0, column=1)
        Label(self.r_frame, text="Link Capacities",font=('Helvetica','12','bold')).grid(row=self.LINK_ROW, column=0, columnspan=2)
        ## Objective Function
        self.obj_frame = Frame(self)
        self.obj_frame.grid(row=1, column=0, columnspan=2)
        Label(self.obj_frame, text="Objective function", font=('Helvetica', 12, 'bold')).grid(row=0, column=0, columnspan=3)
        Radiobutton(self.obj_frame, text="Min hops", variable=objective, command=lambda:self.set_obj_func(objective), value=1).grid(row=1, column=0)
        Radiobutton(self.obj_frame, text="Min routing cost", variable=objective, command=lambda:self.set_obj_func(objective), value=2).grid(row=1, column=1)
        Radiobutton(self.obj_frame, text="None", variable=objective, command=lambda:self.set_obj_func(objective), value=3).grid(row=1, column=2)
        ## Path/Flow Constraints
        self.rules_frame = Frame(self)
        self.rules_frame.grid(row=2, column=0, columnspan=2)
        Label(self.rules_frame, text="Path/Flow constraints", font=('Helvetica', 12, 'bold')).grid(row=0, column=0, columnspan=3)
        Label(self.rules_frame, text="Max. Path length =").grid(row=1, column=0)
        self.ProblemFormulation["Max_Path_Length"] = Entry(self.rules_frame)
        self.ProblemFormulation["Max_Path_Length"].grid(row=1, column=1)
        Label(self.rules_frame, text="Min. Flow volume =").grid(row=2, column=0)
        self.ProblemFormulation["Min_Flow_vol"] = Entry(self.rules_frame)
        self.ProblemFormulation["Min_Flow_vol"].grid(row=2, column=1)
        Label(self.rules_frame, text="Min. # Paths/Demand =").grid(row=3, column=0)
        self.ProblemFormulation["Min_#_Paths/Demand"] = Entry(self.rules_frame)
        self.ProblemFormulation["Min_#_Paths/Demand"].grid(row=3, column=1)
        ## Demands
        self.demand_frame = Frame(self)
        self.demand_frame.grid(row=3, column=0, columnspan=2)
        Label(self.demand_frame, text="Demands",font=('Helvetica','12','bold')).grid(row=self.DEMAND_ROW, column=0, columnspan=3)
        self.DEMAND_ROW += 1
        Label(self.demand_frame, text="Node A").grid(row=self.DEMAND_ROW, column=0)
        Label(self.demand_frame, text="Node B").grid(row=self.DEMAND_ROW, column=1)
        Label(self.demand_frame, text="DVUs").grid(row=self.DEMAND_ROW, column=2)
        self.create_demand_entry()
        ## Buttons
        self.button_frame = Frame(self, pady=10)
        self.button_frame.grid(row=4, column=0, columnspan=2)
        self.b1 = Button(self.button_frame, text="Create demand", command=lambda:self.create_demand_entry())
        self.b1.grid(row=0, column=0,  sticky="nsew")
        self.b2 = Button(self.button_frame, text="Remove demand", command=lambda:self.remove_demand_entry())
        self.b2.grid(row=0, column=1, sticky="nsew")
        self.b3 = Button(self.button_frame, text="Solve", command=lambda:self.get_entries())
        self.b3.grid(row=1, column=0, columnspan=2)
        self.b3["state"] = DISABLED
        
    def get_entries(self):
        ProblemFormulation = {}
        ProblemFormulation["NetworkDemands"] = []
        ProblemFormulation["NetworkPaths"]   = []
        ProblemFormulation["LinkCosts"] = []
        ProblemFormulation["LinkCapacities"] = []
        ProblemFormulation["Obj_Func"] = self.ProblemFormulation["Obj_Func"]
        
        print("\n")
        links = self.ProblemFormulation["Links"]
        # TMPLINKS = [(1, 2), (2, 3), (1, 3)]
        print("Node Types: ", self.ProblemFormulation["node_types"])
        try:
            Nodes = self.ProblemFormulation["Nodes"]
            for i in range(0, len(self.demand_entries), 3):
                node_a = int(self.demand_entries[i].get())
                node_b = int(self.demand_entries[i+1].get())
                print(node_a, node_b)
                print(Nodes)
                if node_a not in Nodes:
                    print("Node %d does not exist." % (node_a))
                    return None
                elif node_b not in Nodes:
                    print("Node %d does not exist." % (node_b))
                    return None
                demand_vol = float(self.demand_entries[i+2].get())

                node_paths = path_finder(links, node_a, node_b)
                node_paths = remove_source_sink(node_paths, node_a, node_b, self.ProblemFormulation["node_types"])
                print("node_paths: ",node_paths)
                demand_paths = node_paths_to_demand_paths(links, node_paths)
                ProblemFormulation["NetworkPaths"].append(demand_paths)
                ProblemFormulation["NetworkDemands"].append(demand_vol)
        except:
            print("Missing demand")
            return None
   

        try:
            ProblemFormulation["Max_Path_Length"] = int(self.ProblemFormulation["Max_Path_Length"].get()) 
        except:
            ProblemFormulation["Max_Path_Length"] = "empty"
        try:
            ProblemFormulation["Min_#_Paths/Demand"] = int(self.ProblemFormulation["Min_#_Paths/Demand"].get()) 
        except:
            ProblemFormulation["Min_#_Paths/Demand"] = "empty"
        try:
            ProblemFormulation["Min_Flow_vol"] = float(self.ProblemFormulation["Min_Flow_vol"].get())
        except:
            ProblemFormulation["Min_Flow_vol"] = "empty"
            
        for i, j in zip(self.cost_entries, self.capacity_entries):
            try:
                ProblemFormulation["LinkCosts"].append(float(i.get()))
            except:
                ProblemFormulation["LinkCosts"].append('empty')
            try:
                ProblemFormulation["LinkCapacities"].append(float(j.get()))
            except:
                ProblemFormulation["LinkCapacities"].append('empty')

        print("Costs:", ProblemFormulation["LinkCosts"])
        print("Capacities:",ProblemFormulation["LinkCapacities"])
        print("Demands:", ProblemFormulation["NetworkDemands"])
        print("Paths:", ProblemFormulation["NetworkPaths"])
        print("MinFLowVol:", ProblemFormulation["Min_Flow_vol"])
        print("MaxPathLength:", ProblemFormulation["Max_Path_Length"])
        print("Min # Paths/Demand:", ProblemFormulation["Min_#_Paths/Demand"])

        viable = self.check_entries(ProblemFormulation)
        if viable != None:
            solve(ProblemFormulation)

    def check_entries(self, ProblemFormulation):
        ## Check if objective functions is viable
        missing_costs = []
        for i, cost in enumerate(ProblemFormulation["LinkCosts"]):
            if cost == "empty" and ProblemFormulation["Obj_Func"] == "min_routing_cost":
                missing_costs.append(i+1)
        if len(missing_costs) > 0:
            text = ""
            for i in missing_costs:
                text += "e%d, " % i
            print("Cannot minimise routing cost. Missing: ", text[:-2])
            return None
        return 1
                    

    def update_link_entries(self):
        self.LINK_ROW += 1
        l1 = Label(self.l_frame, text="e%d" % self.LINK_ROW, width=4)
        l1.grid(row=self.LINK_ROW, column=0)
        self.cost_entries.append(Entry(self.l_frame, width=10))
        self.cost_entries[-1].grid(row=self.LINK_ROW, column=1)
        
        l2 = Label(self.r_frame, text="c%d" % self.LINK_ROW, width=4)
        l2.grid(row=self.LINK_ROW, column=0)
        self.capacity_entries.append(Entry(self.r_frame, width=10))
        self.capacity_entries[-1].grid(row=self.LINK_ROW, column=1)
        
    def create_demand_entry(self):
        self.DEMAND_ROW += 1
        for i in range(3):
            self.demand_entries.append(Entry(self.demand_frame, width=10))
            self.demand_entries[-1].grid(row=self.DEMAND_ROW, column=i)
            
    def remove_demand_entry(self):
        print("REMOVED")
        if self.DEMAND_ROW >= 3:
            self.DEMAND_ROW -= 1
        try:
            for i in range(3):
                self.demand_entries[-1].destroy()
                self.demand_entries.pop()
        except:
            Exception   
            
    def set_obj_func(self, objective):
        match int(objective.get()):
            case 1:
                self.ProblemFormulation["Obj_Func"] = "min_hops"
            case 2:
                self.ProblemFormulation["Obj_Func"] = "min_routing_cost"
            case 3:
                self.ProblemFormulation["Obj_Func"] = "none"
            

class NetworkDesignTool(Frame):
    def __init__(self, parent, config):
        super().__init__(parent)
        self.BLOCKSIZE = config['BLOCKSIZE']
        self.HEIGHT = config['SCREEN_HEIGHT']
        self.WIDTH = config['SCREEN_WIDTH']
        self.TOOLBAR_HEIGHT = 240
        self.TOOLBAR_WIDTH = 90
        self.delete_icon = PhotoImage(file="icon/delete.png").subsample(4)
        
        self.RADIUS  = 20
        self.config(width=self.WIDTH, height=self.HEIGHT)
        self.pack(side="right", fill="both", expand=True)
        self.delete_mode = False
        
        self.network_design = {
            'circles':[],
            'lines':[],
            'links':[],
            'draw_circles':[],
            'draw_lines':[],
            'node_labels':[],
            'link_labels':[],
            'node_types':[]
        }
        
        self.node_count = 1
        self.link_count = 1
        self.drag_line = False
        self.drag_node = False
        self.idx       = None
        self.drag_lines_idx = []
        self.enable_create = True
        
        self.draw_grid()
        self.nodebar = self.canvas.create_rectangle(0, 0, self.TOOLBAR_WIDTH, self.TOOLBAR_HEIGHT, fill="#edc277")
        self.canvas.create_text(45, 10, text="Full/Transit")
        self.create_circle(45, 50, "green")
        self.canvas.create_text(45, 80, text="Source/Sink")
        self.create_circle(45, 120, "red")
        self.canvas.create_text(45, 150, text="Delete Node")
        self.canvas.create_image(45, 200, image=self.delete_icon)
        self.delete_node = self.canvas.create_image(45, 200, image=self.delete_icon)
        self.canvas.bind("<B1-Motion>", self.drag)
        self.canvas.bind("<ButtonRelease-1>", self.drop)
        self.canvas.bind("<B3-Motion>", self.dragline)
        self.canvas.bind("<ButtonRelease-3>", self.dropline)

    def draw_grid(self):
        self.canvas = Canvas(self, bg="white", width=self.WIDTH, height=self.HEIGHT)
        self.canvas.pack(fill="both", expand=True)
        for x in range(0, self.WIDTH, self.BLOCKSIZE):
            for y in range(0, self.HEIGHT, self.BLOCKSIZE):
                self.canvas.create_rectangle(x, y, x + self.BLOCKSIZE, y + self.BLOCKSIZE, fill="white", outline="#f6f6f6")
            
    def create_circle(self, x, y, c):
        r = self.RADIUS
        return self.canvas.create_oval((x-r, y-r), (x+r, y+r), fill=c, outline="black", width=2)
    
    def set_new_node(self, e, colour):
        self.delete_mode = False
        self.network_design["draw_circles"].append(self.create_circle(e.x, e.y, colour))
        self.network_design["circles"].append((e.x, e.y))
        self.create_node_label(e)
        self.drag_node = True
        self.enable_create = False
        self.idx = len(self.network_design["circles"]) - 1
        self.drag_lines_idx = []
        if colour == "red":
            self.network_design["node_types"].append("sourcesink")
        elif colour == "green":
            self.network_design["node_types"].append("full")
        self.master.sidedashboard.ProblemFormulation["Nodes"].append(self.node_count)
        self.node_count += 1  
    
    def create_node_label(self, e):
        self.network_design["node_labels"].append(self.canvas.create_text((e.x, e.y), 
                                                                          text=str(self.node_count), 
                                                                          font=('Helvetica','14','bold'), 
                                                                          fill="black"))
        
        
    def create_link_label(self, x, y):
        self.network_design["link_labels"].append(
                    self.canvas.create_text((x+2, y+2), text="e=%d"%(self.link_count),
                                            font=('Helvetica','12'), 
                                            fill="black"))
    
    def is_mouse_in_circle_region(self, x, y, e):
        return (x-e.x)**2 + (y-e.y)**2 <= self.RADIUS**2
    
    def circle_idx_at_mouse(self, e):
        for i, coords in enumerate(self.network_design["circles"]):
            x, y = coords
            if self.is_mouse_in_circle_region(x, y, e):
                return i
    
    def drag(self, e):
        if self.is_mouse_in_circle_region(45, 50, e) and self.enable_create == True:
            self.set_new_node(e, "green")
        if self.is_mouse_in_circle_region(45, 120, e) and self.enable_create == True:
            self.set_new_node(e, "red")

        if self.drag_node == False:
            self.idx = self.circle_idx_at_mouse(e)
            if self.idx is not None:
                self.drag_node = True
                if len(self.network_design["lines"]) > 0:
                    self.get_connected_lines(self.network_design["circles"][self.idx])
                    
        if self.drag_node == True:
            self.canvas.moveto(self.network_design["draw_circles"][self.idx], e.x-self.RADIUS, e.y-self.RADIUS)
            self.canvas.moveto(self.network_design["node_labels"][self.idx], e.x, e.y)
            self.network_design["circles"][self.idx] = e.x, e.y
            self.move_connected_lines(e.x, e.y)
            
    def drop(self, e):
        if self.drag_node == True:
            x, y = self.snap_grid(e)
            self.network_design["circles"][self.idx] = x+self.RADIUS, y+self.RADIUS
            self.canvas.moveto(self.network_design["draw_circles"][self.idx], x, y)
            self.canvas.moveto(self.network_design["node_labels"][self.idx], x+self.RADIUS, y+self.RADIUS)
            self.move_connected_lines(x+self.RADIUS, y+self.RADIUS)
        self.master.sidedashboard.ProblemFormulation["node_types"] = self.network_design["node_types"]
        self.drag_node = False
        self.enable_create = True
        self.idx = None
        
    def get_connected_lines(self, circle):
        x, y = circle 
        self.drag_lines_idx = []
        for i, coords in enumerate(self.network_design["lines"]):
            coords = self.canvas.coords(coords)
            for j in range(0, len(coords), 2):
                if x == coords[j] and y == coords[j+1]:
                    self.drag_lines_idx.append([i,j])
    
    def move_connected_lines(self, x, y):
        for i in self.drag_lines_idx:
            x1, y1, x2, y2 = self.canvas.coords(self.network_design["lines"][i[0]])
            if i[1] == 0:
                self.canvas.coords(self.network_design["lines"][i[0]], x, y, x2, y2)
                self.canvas.moveto(self.network_design["link_labels"][i[0]], (x+x2)/2, (y+y2)/2)
            elif i[1] == 2:
                self.canvas.coords(self.network_design["lines"][i[0]], x1, y1, x, y)
                self.canvas.moveto(self.network_design["link_labels"][i[0]], (x+x1)/2, (y+y1)/2)
        
    def dragline(self, e):
        if self.drag_line == False:
            self.idx = self.circle_idx_at_mouse(e)
            if self.idx is not None:
                x, y = self.network_design["circles"][self.idx]
                self.network_design["lines"].append(self.canvas.create_line(x, y, x+4, x+4))
                # self.network_design["node_labels"].append(self.canvas.create_text((e.x, e.y), text=str(self.node_count), fill="black"))
                self.network_design["link_labels"].append(
                    self.canvas.create_text((x+2, y+2), text="e=%d"%(self.link_count),font=('Helvetica','14','bold'), fill="black"))
                self.drag_line = True
        if self.drag_line == True:
            x, y = self.network_design["circles"][self.idx]
            self.canvas.coords(self.network_design["lines"][-1], x, y, e.x, e.y)
            self.canvas.moveto(self.network_design["link_labels"][-1], (x+e.x)/2, (y+e.y)/2)
    
    def dropline(self, e):
        self.idx = self.circle_idx_at_mouse(e)
        if self.idx is not None and self.drag_line == True:
            x1, y1 = self.canvas.coords(self.network_design["lines"][-1])[0], self.canvas.coords(self.network_design["lines"][-1])[1]
            x2, y2 = self.network_design["circles"][self.idx]
            self.idx = None  
            if x1!=x2 and y1!=y2:
                self.canvas.coords(self.network_design["lines"][-1], x1, y1, x2, y2)
                self.master.sidedashboard.update_link_entries()
                self.link_count += 1
                self.create_link(self.network_design["lines"][-1])
                print(self.network_design["links"])
                self.master.sidedashboard.ProblemFormulation["Links"] = self.network_design["links"] 
            else:
                self.reset_line()

        elif self.drag_line == True:
            self.reset_line()

        self.idx = None
        self.drag_line = False     
        
    def snap_grid(self, e):
        x,y = e.x, e.y
        x_off = x % self.BLOCKSIZE
        y_off = y % self.BLOCKSIZE
        if x_off < self.BLOCKSIZE/2:
            x -= x_off
        if x_off >= self.BLOCKSIZE/2:
            x += self.BLOCKSIZE - x_off
        if y_off < self.BLOCKSIZE/2:
            y -= y_off
        if y_off >= self.BLOCKSIZE/2:
            y += self.BLOCKSIZE - y_off
        return (x-self.RADIUS, y-self.RADIUS)
    
    def get_node_for_link(self, line):
        for i,circle in enumerate(self.network_design["circles"]):
            x, y = circle
            if line[0] == x and line[1] == y:
                node_1 = i+1
            elif line[2] == x and line[3] == y:
                node_2 = i+1
        return node_1, node_2
    
    def reset_line(self):
        self.canvas.delete(self.network_design["lines"][-1])#
        self.canvas.delete(self.network_design["link_labels"][-1])
        self.network_design["lines"].pop()
        self.network_design["link_labels"].pop()
        
    def create_link(self, line):
        self.network_design["links"].append(self.get_node_for_link(
                    self.canvas.coords(line)))
        self.master.sidedashboard.b3["state"] = ACTIVE
                
           