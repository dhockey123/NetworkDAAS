import pygame

SCREEN_WIDTH = 1020
SCREEN_HEIGHT = 480

DASH_WIDTH = 120
DASH_HEIGHT = SCREEN_HEIGHT
CIRCLE_RADIUS = 20
RED = (255, 0, 0)
GREEN = (82, 235, 52)
# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Network design")
pygame.init()

font = pygame.font.Font(None, 28)


paths = []

reset_image = pygame.image.load("icon/reset.svg")
reset_image = pygame.transform.smoothscale(reset_image, (55,55))
paper_image = pygame.image.load("icon/paper.svg")
paper_image = pygame.transform.smoothscale(paper_image, (55,55))
solve_image = pygame.image.load("icon/solve.svg")
solve_image = pygame.transform.smoothscale(solve_image, (55,55))


def create_line(line_start, line_end, lines):
    lines.append([line_start, line_end])

def draw_grid(SCREEN_WIDTH, SCREEN_HEIGHT, blocksize):
    for x in range(0, SCREEN_WIDTH, blocksize):
        for y in range(0, SCREEN_HEIGHT, blocksize):
            rect = pygame.Rect(x, y, blocksize, blocksize)
            pygame.draw.rect(screen, (246, 246, 246), rect, 1)

def snap_grid(pos, blocksize):
    x,y = pos[0], pos[1]
    x_off = pos[0] % blocksize
    y_off = pos[1] % blocksize
    if x_off < blocksize/2:
        x -= x_off
    if x_off >= blocksize/2:
        x += blocksize - x_off
    if y_off < blocksize/2:
        y -= y_off
    if y_off >= blocksize/2:
        y += blocksize - y_off
    return (x, y)

def is_mouse_in_circle(pos):
    return (pygame.mouse.get_pos()[0] - pos[0])**2 + (pygame.mouse.get_pos()[1] - pos[1])**2 <= CIRCLE_RADIUS**2

def is_mouse_in_fullnode(pos):
    ## FULL NODE
    x, y = 60, 60
    if (pygame.mouse.get_pos()[0]-x)**2 + (pygame.mouse.get_pos()[1]-y)**2 <= CIRCLE_RADIUS**2:
        return True
    
def is_mouse_in_transitnode(pos):
    ## FULL NODE
    x, y = 60, 120
    if (pygame.mouse.get_pos()[0]-x)**2 + (pygame.mouse.get_pos()[1]-y)**2 <= CIRCLE_RADIUS**2:
        return True
    
def is_mouse_in_deletemode(pos):
    ## FULL NODE
    x, y = 60, 180
    if (pygame.mouse.get_pos()[0]-x)**2 + (pygame.mouse.get_pos()[1]-y)**2 <= CIRCLE_RADIUS**2:
        return True
    
def is_mouse_in_paramfile(pos):
    x,y = 60, 270
    if (pygame.mouse.get_pos()[0]-x)**2 + (pygame.mouse.get_pos()[1]-y)**2 <= CIRCLE_RADIUS**2:
        return True

def get_lines_in_circle(lines, circle_pos, lines_idx):
     for x, line in enumerate(lines):
        for y, pos in enumerate(line):
            if pos == circle_pos:
                lines_idx.append([x,y])

def get_nodes_for_link(circles, line):
    for i,circle in enumerate(circles):
        if line[0] == circle:
            node_1 = i+1
        elif line[1] == circle:
            node_2 = i+1
    return node_1, node_2

def draw_circle(circles, node_types, label=True, color=RED):
    for i,circle_pos in enumerate(circles):
        # color = node_types[i]
        try:
            # print(node_types[0])
            color=node_types[i]
        except:
            Exception

        pygame.draw.circle(screen, (9,9,9), circle_pos, CIRCLE_RADIUS+2)
        pygame.draw.circle(screen, color, circle_pos, CIRCLE_RADIUS)
        if label == True:
            text = font.render(str(i+1), True, (0,0,0))
            screen.blit(text, (circle_pos))

def draw_line(lines):
    for i,line in enumerate(lines):
        x1, y1 = line[0]
        x2, y2 = line[1]
        text = font.render("e = "+str(i+1), True, (0,0,0))
        screen.blit(text, ((x1+x2)/2,(y1+y2)/2))
        pygame.draw.line(screen, (0,0,0), line[0], line[1])
        
def draw_cross(pos):
    x = pos[0]
    y = pos[1]
    radius=15
    pygame.draw.lines(screen, (0,0,0), True, [(x-radius,y-radius),(x+radius,y+radius)], 5)
    pygame.draw.lines(screen, (0,0,0), True, [(x-radius,y+radius),(x+radius,y-radius)], 5)
        

def draw_dash(DASH_WDITH, DASH_HEIGHT):
    global reset_image, paper_image
    font = pygame.font.SysFont('qtpristine', 14)
    pygame.draw.rect(screen, (237, 194, 119), pygame.Rect(0, 0, DASH_WIDTH, DASH_HEIGHT))
    # pygame.draw.rect(screen, (237, 194, 119), pygame.Rect(SCREEN_WIDTH-DASH_WIDTH,0, DASH_WIDTH, DASH_HEIGHT))
    
    ## SOURCE/SINK NODE
    label1 = font.render("Source/Sink node", True, (0, 0, 0))
    pos1 = label1.get_rect(center=(DASH_WIDTH/2, 30))
    screen.blit(label1, pos1)
    draw_circle([[60, 60]], 0, False)
    
    ## TRANSIT/FULL NODE
    label2 = font.render("Full node", True, (0, 0, 0))
    pos2 = label2.get_rect(center=(DASH_WIDTH/2, 90))
    screen.blit(label2, pos2)
    draw_circle([[60, 120]], 0, False, GREEN)
    # pygame.draw.circle(screen, (9,9,9), (40, 120), CIRCLE_RADIUS+2)
    # pygame.draw.circle(screen, (82, 235, 52), (40, 120), CIRCLE_RADIUS)
    
    ## DELETE TOOL
    text = font.render("Delete mode", True, (0,0,0))
    text_rect = text.get_rect(center=(DASH_WIDTH/2, 150))
    screen.blit(text, text_rect)
    # x,y=60, 180
    # radius=15
    draw_cross([60, 180])

    ## Generate param file
    text = font.render("Assign variables", True, (0,0,0))
    text_rect = text.get_rect(center=(DASH_WIDTH/2, 230))
    screen.blit(text, text_rect)
    screen.blit(paper_image, (35, 240))
    
    ## Solve button
    text = font.render("LP_SOLVE", True, (0,0,0))
    text_rect = text.get_rect(center=(DASH_WIDTH/2, 300))
    screen.blit(text, text_rect)
    screen.blit(solve_image, (35, 310))
    ## RESET TOOL
    text = font.render("Clear All", True, (0,0,0))
    text_rect = text.get_rect(center=(DASH_WIDTH/2, 400))
    screen.blit(text, text_rect)
    screen.blit(reset_image, (35, 405))


    ## TEXT INPUT 

    # pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(SCREEN_WIDTH-DASH_WIDTH+10, 10, DASH_WIDTH-20, 200))
    # # text = font.render("TEST\nTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTEST", True, (0,0,0))
    # # screen.blit(text, (200,200, 30, 30))
    # textbox = TextBox(screen, SCREEN_WIDTH-DASH_WIDTH+10, 10, DASH_WIDTH-20, 120, fontSize=14,
    #               borderColour=(0, 0, 0), textColour=(255, 255, 255), radius=10, borderThickness=1)
# def path_finder(links, a, b, path=[]):
#     path.append(a)
#     if a == b:
       
#         # print(path)
#         paths.append(list(set(path)))
#     for link in links:
#         if a in link:
#             if(a == link[0]):
#                 next_node = link[-1]
#             elif(a == link[1]):
#                 next_node = link[0]
#             if next_node not in path:
#                 new_path = list(path)
#                 path_finder(links, next_node, b, new_path)