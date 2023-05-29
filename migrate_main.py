from tkinter import *
demand_rows =4
main = Tk()
SCREEN_HEIGHT = 900
SCREEN_WIDTH = 1200
DASH_HEIGHT = 80
DASH_WIDTH = 200

CIRCLE_RADIUS = 20
BLOCKSIZE = 20
row =1
rb_var = IntVar()
def create_circle(x, y, r, c):
    r = CIRCLE_RADIUS
    return c.create_oval((x-r, y-r), (x+r, y+r), fill="red", outline="black", width=2)

def create_demand(demand_frame):
    global demand_rows #, demand_frame,win
    for i in range(3):
        vars["demand_entries"].append(Entry(demand_frame, width=10))
        vars["demand_entries"][-1].grid(row=demand_rows, column=i)
    demand_rows+=1
    
def create_cost_capacity():
    global row, l_frame, r_frame
    Label(l_frame, text="e%d" % (row) ).grid(row=row, column=0)
    vars["cost_entries"].append(Entry(l_frame, width=10))
    vars["cost_entries"][row-1].grid(row=row, column=1)
    Label(r_frame, text="c%d" % (row)).grid(row=row, column=0)
    vars["capacity_entries"].append(Entry(r_frame, width=10))
    vars["capacity_entries"][row-1].grid(row=row, column=1)
    row+=1
    
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


win = Frame(main)
win.pack(side=LEFT, anchor=N)
window = Frame(main)
window.pack(side=RIGHT)

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



c = Canvas(window, height=SCREEN_HEIGHT, width=SCREEN_WIDTH, bg="white")




c.pack(side=RIGHT)
circles = []

for x in range(0, SCREEN_WIDTH, BLOCKSIZE):
    for y in range(0, SCREEN_HEIGHT, BLOCKSIZE):
        c.create_rectangle(x, y, x+BLOCKSIZE, y+BLOCKSIZE, fill="white", outline="#f6f6f6")


c.create_rectangle(0,0, DASH_WIDTH, DASH_HEIGHT, fill="#edc277")

create_circle(30, DASH_HEIGHT/2, 10, c)
# test = [create_circle(50, 50, 10, c), create_circle(100, 150, 10, c), create_circle(150, 200, 10, c)]
test = []
# circles.append((50, 50))
# circles.append((100, 150))
# circles.append((150, 200))
# labels = [c.create_text(circles[0], text="1", fill="black")]#,
        # #   c.create_text(circles[1], text="2", fill="black"),
        #   c.create_text(circles[2], text="3", fill="black")]
labels = []
idx = []
drag_node = False
drag_line = False

print(c.children)
print(test)

def circle_idx_at_mouse(e):
    for i, coords in enumerate(circles):
        x, y = coords
        if (x-e.x)**2 + (y-e.y)**2 <= CIRCLE_RADIUS**2:
            return i

def is_mouse_in_circle_region(x, y, e):
    return (x-e.x)**2 + (y-e.y)**2 <= CIRCLE_RADIUS**2

def coords(e):
    global circles
    print(circles)
    print(e.x, e.y)
    
# def update_node_positions(e):
    
def snap_grid(e):
    x,y = e.x, e.y
    x_off = x % BLOCKSIZE
    y_off = y % BLOCKSIZE
    if x_off < BLOCKSIZE/2:
        x -= x_off
    if x_off >= BLOCKSIZE/2:
        x += BLOCKSIZE - x_off
    if y_off < BLOCKSIZE/2:
        y -= y_off
    if y_off >= BLOCKSIZE/2:
        y += BLOCKSIZE - y_off
    return (x-CIRCLE_RADIUS, y-CIRCLE_RADIUS)

def create(e):
    if len(c.find_overlapping(e.x, e.y, e.x+10, e.y+10)) == 0:
        test.append(create_circle(e.x, e.y, 10, c))
line = []
drag_lines_idx = []
links = []

def get_lines(circle):
    global line, drag_lines_idx
    x,y = circle
    drag_lines_idx = []
    print("DEBUG ", line)
    for i, coords in enumerate(line):
        coords = c.coords(coords)
        for j in range(0, len(coords), 2):
            if x == coords[j] and y == coords[j+1]:
                drag_lines_idx.append([i, j])
                
def move_lines(x, y):
    for i in drag_lines_idx:
        x1, y1, x2, y2 = c.coords(line[i[0]])
        if i[1] == 0:
            c.coords(line[i[0]], x, y, x2, y2)
        elif i[1] == 2:
            c.coords(line[i[0]], x1, y1, x, y)
node_num = 1
fresh_node = True
def drag(e):
    global drag_node, circles, idx, line, fresh_node, drag_lines_idx, labels, node_num
    if is_mouse_in_circle_region(30, 40, e) and fresh_node == True:
        test.append(create_circle(e.x, e.y, 10, c))
        labels.append(c.create_text((e.x, e.y), text=str(node_num), fill="black"))
        circles.append((e.x, e.y))
        drag_node = True
        fresh_node = False
        idx = len(circles)-1
        drag_lines_idx = []
        node_num += 1

    if drag_node == False:
        idx = circle_idx_at_mouse(e)
        if idx is not None:
            drag_node = True
            print(circles[idx])
            try:
                get_lines(circles[idx])
            except:
                Exception

    if drag_node == True:        
        c.moveto(test[idx], e.x-CIRCLE_RADIUS, e.y-CIRCLE_RADIUS)
        c.moveto(labels[idx], e.x-9, e.y-9)
        circles[idx] = e.x, e.y
        move_lines(e.x, e.y)

        
        
def drop(e):
    global drag_node, circles, idx, fresh_node
    # print("DROP: %d, DRAG_MODE: %s" % (idx, drag_node))
    if drag_node == True and fresh_node == True:
        x, y = snap_grid(e)
        circles[idx] = x+CIRCLE_RADIUS, y+CIRCLE_RADIUS
        c.moveto(test[idx], x, y)
        c.moveto(labels[idx], x+CIRCLE_RADIUS/2, y+CIRCLE_RADIUS/2)
        move_lines(x+CIRCLE_RADIUS, y+CIRCLE_RADIUS)
    drag_node = False 
    fresh_node = True
    idx = None
 
def get_nodes_for_link(line):
    for i,circle in enumerate(circles):
        x, y = circle
        if line[0] == x and line[1] == y:
            node_1 = i+1
        elif line[2] == x and line[3] == y:
            node_2 = i+1
    return node_1, node_2


def dragline(e):
    global drag_line, idx
    if drag_line == False: 
        idx = circle_idx_at_mouse(e)
        if idx is not None:       
            idx = circle_idx_at_mouse(e)
            x, y = circles[idx]
            line.append(c.create_line(x, y, x+4, y+4))
            c.tag_lower(line[-1], test[idx])
            drag_line = True
            
    if drag_line == True:
        x, y = circles[idx]
        c.coords(line[-1], x, y, e.x, e.y)
        c.tag_lower(line[-1], test[idx])
    # drag_line = False
        
def dropline(e):
    ## No handling of duplicate lines/links
    global drag_line, links
    idx = circle_idx_at_mouse(e)
    if idx is not None and drag_line==True:
        x1, y1 = c.coords(line[-1])[0], c.coords(line[-1])[1]
        x2, y2 = circles[idx]
        c.coords(line[-1], x1, y1, x2, y2)
        c.tag_lower(line[-1], test[idx])
        idx = None
        links.append(get_nodes_for_link(c.coords(line[-1])))
        create_cost_capacity()
        print(links)
    elif drag_line==True:
        c.delete(line[-1])
        # print(line)
        line.pop()
    drag_line = False
    
    # line = c.create_line()
# a = (230, 200)
# b = (101, 290)
# c.create_line(a, b)



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

main.bind("<B1-Motion>", drag)
main.bind("<ButtonRelease-1>", drop)
main.bind("<B3-Motion>", dragline)
main.bind("<ButtonRelease-3>", dropline)

main.mainloop()