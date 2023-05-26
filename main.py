import pygame
from tkinter import *
from ui_networkdesign import *
from ui_assign_params import *

SCREEN_WIDTH = 1020
SCREEN_HEIGHT = 480
DASH_WIDTH = 120
DASH_HEIGHT = SCREEN_HEIGHT


#Define geometry of the window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Network design - Press 'space' key - R.Click between nodes")
pygame.init()

circles, lines, links, nodes, node_types, lines_idx, paths = [],[],[],[],[],[],[]
node, link = 0,0
drag_idx, drag_offset = None, None
delete_mode, drawing_line = False, False
blocksize = 20

# Initialize Pygame

def reset():
    global nodes, node_types, links, lines, circles
    nodes = []
    node_types = []
    links = []
    lines = []
    circles = []

# Used for repositioning existing circle
def create_drag_node():
    global node, drag_idx, drag_offset
    circles.append(event.pos)
    node+=1
    nodes.append(node)
    drag_idx = len(circles) - 1
    drag_offset = (0, 0)

font = pygame.font.Font(None, 28)
# Main game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        # Handle mouse events
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # Check if old circle is L.clicked
                for i, circle_pos in enumerate(circles):
                    if is_mouse_in_circle(circle_pos):
                        get_lines_in_circle(lines, circle_pos, lines_idx)
                        drag_idx = i
                        drag_offset = (circle_pos[0] - event.pos[0], circle_pos[1] - event.pos[1])
                        break
                # Create new circle at L.mouse click location
                else:
                    if is_mouse_in_fullnode(event.pos):
                        node_types.append(RED)
                        create_drag_node()
                    elif is_mouse_in_transitnode(event.pos):
                        node_types.append(GREEN)
                        create_drag_node()
                    elif is_mouse_in_deletemode(event.pos):
                        delete_mode = True
                    elif is_mouse_in_paramfile(event.pos):
                        # paramfile(links)
                        print("OBSOLETE")
                    elif is_mouse_in_circle((60, 420)):
                        reset()

            ## Create new link/line if R.mouse click location within circle 
            elif event.button == 3:
                for i, circle_pos in enumerate(circles):
                    if is_mouse_in_circle(circle_pos):
                        line_start = circle_pos
                        drawing_line = True
                        drag_offset_line = (circle_pos[0] - event.pos[0], circle_pos[1] - event.pos[1])
                        create_line(circle_pos, (event.pos[0]+10, event.pos[1]+10), lines)
                        break

        # Drop objects on mouse release
        elif event.type == pygame.MOUSEBUTTONUP:
            if delete_mode == True:
                ## IF mouserelease in circles, delete circle.
                for i, circle in enumerate(circles):
                    if is_mouse_in_circle(circle):
                        circles.pop(i)
                        node_types.pop(i)
                        nodes.pop(i)
                        lines_pop_idx = []
                        
                        ## Get IDX of unconnected lines
                        for j, link in enumerate(links):
                            if i+1 in link:
                                lines_pop_idx.append(j)

                        ## Delete removed lines and links
                        for idx in sorted(lines_pop_idx, reverse=True):
                            del links[idx]
                            del lines[idx]
                 
                        ## Decrement node values > value of deleted node
                        for j, link in enumerate(links):
                            a,b = link
                            if a>i+1 and b>i+1:
                                links[j] = (a-1, b-1)
                            elif b>i+1:
                                links[j] = (a, b-1)
                            elif a>i+1:
                                links[j] = (a-1, b)

            delete_mode = False 
            
            if event.button == 1:
                if drag_idx != None:
                    # Stop following the mouse
                    circles[drag_idx] = snap_grid(event.pos, blocksize)
                    drag_idx = None
                    drag_offset = None
                    for x,y in lines_idx:
                        lines[x][y] = snap_grid(event.pos, blocksize)
                    lines_idx = []
            # Complete line/link at R.mouse release location if within a circle
            elif event.button == 3:
                if drawing_line == True:
                    for i, circle_pos in enumerate(circles):
                        if is_mouse_in_circle(circle_pos):
                            ## Fixes possibility of single-point line errors
                            try:
                                drawing_line = False
                                lines[-1][1] = (circle_pos[0], circle_pos[1])
                                links.append(get_nodes_for_link(circles, lines[-1]))
                                if lines[-1][0] == lines[-1][1]:
                                    links.pop()
                                    link-=1
                                break
                            except:
                                lines.pop()
                                
                    if drawing_line == True:
                        drawing_line = False
                        lines.pop()

        # Objects follow mouse on hold
        elif event.type == pygame.MOUSEMOTION:
            # print(event.pos)
            if drag_idx != None:
                # Update the position of the circle (and lines) being dragged
                circles[drag_idx] = (event.pos[0] + drag_offset[0], event.pos[1] + drag_offset[1])
                for x,y in lines_idx:
                    lines[x][y] = circles[drag_idx]

            if drawing_line == True:
                lines[-1][1] = (event.pos[0] + drag_offset_line[0], event.pos[1] + drag_offset_line[1])

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # paramfile(links)
                assign_params(links)
                
                # lp_solve_it()
      
                print("\nNodes: ", nodes)
                print("Links: ", links)
                # node_paths =  path_finder(links, node_a, node_b)
                # print("Node paths: ", node_paths)
                # demand_paths = node_paths_to_demand_paths(links, node_paths)
                # # demand_paths = limit_path_hops(2, demand_paths)
                # print("Demand paths: ", demand_paths)
                
    # Clear the screen
    screen.fill((255, 255, 255))

    draw_grid(SCREEN_WIDTH, SCREEN_HEIGHT, blocksize)
    draw_dash(DASH_WIDTH, DASH_HEIGHT)
    draw_circle(circles, node_types)
    draw_line(lines)
    
    if(delete_mode == True):
        draw_cross(event.pos)
   
    pygame.display.update()