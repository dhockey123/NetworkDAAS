from tkinter import *

class SideDashBoard(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        # self.parent = parent
        self.WIDTH = 200
        self.HEIGHT = 900
        self.LINK_ROW = 0
        self.DEMAND_ROW = 1
        # self.cost_entries = []
        self.config(width=self.WIDTH, height=self.HEIGHT)
        # self.grid_propagate(0)
        self.pack(side="left", anchor="n")
        self.ProblemFormulation = {
            "LinkCosts":[],
            "LinkCapacities":[],
            "NetworkPaths":[],
            "NetworkDemands":[],
            "Min_Flow_Vol":0,
            "Min_#_Paths/Demand":0, 
            "Obj_Func":"min: ;"
        }

        ## Link costs
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        self.l_frame = Frame(self, width=100)
        self.l_frame.grid(row=0, column=0)
        Label(self.l_frame, text="Link costs").grid(row=self.LINK_ROW, column=0, columnspan=2)
        ## Link capacities
        self.r_frame = Frame(self, width=100)
        self.r_frame.grid(row=0, column=1, sticky="nsew")
        Label(self.r_frame, text="Link Capacities").grid(row=self.LINK_ROW, column=0, columnspan=2)
        ## Demands
        self.demand_frame = Frame(self, width=200)
        self.demand_frame.grid(row=1, column=0, columnspan=2)
        Label(self.demand_frame, text="Demands").grid(row=self.DEMAND_ROW, column=0, columnspan=3)
        self.DEMAND_ROW += 1
        Label(self.demand_frame, text="Node A").grid(row=self.DEMAND_ROW, column=0)
        Label(self.demand_frame, text="Node B").grid(row=self.DEMAND_ROW, column=1)
        Label(self.demand_frame, text="DVUs").grid(row=self.DEMAND_ROW, column=2)
        self.create_demand_entry()
        

    def update_link_entries(self):
        self.LINK_ROW += 1
        Label(self.l_frame, text="e%d" % self.LINK_ROW, width=10).grid(row=self.LINK_ROW, column=0)
        tmp = Entry(self.l_frame, width=10)
        tmp.grid(row=self.LINK_ROW, column=1)
        
        Label(self.r_frame, text="c%d" % self.LINK_ROW, width=10).grid(row=self.LINK_ROW, column=0)
        tmp2 = Entry(self.r_frame, width=10)
        tmp2.grid(row=self.LINK_ROW, column=1)
        
    def create_demand_entry(self):
        self.DEMAND_ROW += 1
        for i in range(3):
            tmp = Entry(self.demand_frame, width=10)
            tmp.grid(row=self.DEMAND_ROW, column=i)

class NetworkDesignTool(Frame):
    def __init__(self, parent, config):
        super().__init__(parent)
        # self.parent = parent
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
            'draw_circles':[],
            'draw_lines':[],
            'node_labels':[],
            'link_labels':[]
        }
        
        self.node_count = 1
        self.link_count = 1
        self.drag_line = False
        self.drag_node = False
        self.idx       = None
        self.drag_lines_idx = []
        self.enable_create = True
        self.delete_mode = False
        
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
                
    # def click(self, e):
    #     bbox = self.canvas.bbox(self.thing)
    #     if bbox[0] <= e.x <= bbox[2] and bbox[1] <= e.y <= bbox[3]:
    #         self.master.sidedashboard.update_link_entries()
            
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
        # print(e.x, e.y)
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
            self.canvas.coords(self.network_design["lines"][-1], x1, y1, x2, y2)
            self.link_count += 1
            self.idx = None  
            self.master.sidedashboard.update_link_entries()
        elif self.drag_line == True:
            self.canvas.delete(self.network_design["lines"][-1])#
            self.canvas.delete(self.network_design["link_labels"][-1])
            self.network_design["lines"].pop()
            
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
           

class App(Tk):
    def __init__(self):
        super().__init__()
        self.config = {
            'SCREEN_HEIGHT': 900,
            'SCREEN_WIDTH': 1200,
            'BLOCKSIZE': 20
        }

        self.geometry("1200x900")
        self.sidedashboard = SideDashBoard(self)
        self.networkdesigntool = NetworkDesignTool(self, self.config)

if __name__ == "__main__":
    app = App()
    app.mainloop()
