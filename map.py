import random
import sys, pygame
from scipy.spatial import Voronoi
from pprint import pprint
pygame.init()

random.seed(1)

size = width, height = 800, 600
speed = [2, 2]
blue = 66, 135, 245
WHITE = 255, 255, 255
BLACK = 0, 0, 0

def random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return (r, g, b)

screen = pygame.display.set_mode(size)
surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
pop_surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)

# ball = pygame.image.load("intro_ball.gif")
# ballrect = ball.get_rect()

# vor_surface = pygame.Surface(screen.get_size())
# vor_surface.convert_alpha()
# vor_surface.set_colorkey(WHITE)
# vor_surface.fill(WHITE)

points = []
for _ in range(100):
    # x = random.randint(-width, width*2)
    # y = random.randint(-height, height*2)
    x = random.randint(0, width)
    y = random.randint(0, height)
    points.append((x,y))
old_points = points

new_points = []
# sector1 = []
# sector2 = []
# sector3 = []
# sector4 = []
# sector5 = []
# sector6 = []
# sector7 = []
# sector8 = []
# sector9 = []
for point in points:
    x, y = point

    new_points.append((x+width, y))
    new_points.append((x+width, y+height))
    new_points.append((x+width, y-height))
    new_points.append((x, y))
    new_points.append((x, y+height))
    new_points.append((x, y-height))
    new_points.append((x-width, y))
    new_points.append((x-width, y+height))
    new_points.append((x-width, y-height))
    # sector1.append((x-width, y-height))
    # sector2.append((x, y-height))
    # sector3.append((x+width, y-height))
    # sector4.append((x-width, y))
    # sector5.append((x, y))
    # sector6.append((x+width, y))
    # sector7.append((x-width, y+height))
    # sector8.append((x, y+height))
    # sector9.append((x+width, y+height))

points = new_points

sector = [[] for _ in range(12)]

for point in points:
    x, y = point
    if (-0.5*width) < x < 0 and (-0.5*height) < y < 0:
        sector[0] += [point]
    if 0 < x < (0.5*width) and (-0.5*height) < y < 0:
        sector[1] += [point]
    if (0.5*width) < x < width and (-0.5*height) < y < 0:
        sector[2] += [point]
    if width < x < (1.5*width) and (-0.5*height) < y < 0:
        sector[3] += [point]
    if width < x < (1.5*width) and 0 < y < (0.5*height):
        sector[4] += [point]
    if width < x < (1.5*width) and (0.5*height) < y < height:
        sector[5] += [point]
    if width < x < (1.5*width) and height < y < (1.5*height):
        sector[6] += [point]
    if (0.5*width) < x < width and height < y < (1.5*height):
        sector[7] += [point]
    if 0 < x < (0.5*width) and height < y < (1.5*height):
        sector[8] += [point]
    if (-0.5*width) < x < 0 and height < y < (1.5*height):
        sector[9] += [point]
    if (-0.5*width) < x < 0 and (0.5*height) < y < height:
        sector[10] += [point]
    if (-0.5*width) < x < 0 and 0 < y < (0.5*height):
        sector[11] += [point]

def get_midpoint(points):
    n = len(points)
    x_sum = y_sum = 0
    for x, y in points:
        x_sum += x
        y_sum += y
    return (x_sum / n, y_sum / n)


def make_regions(points, n_relax=0):
    # Todo: Make this find the midpoint between the old point and the new point
    def relax(regions):
        relaxed_points = []
        for n, region in enumerate(regions):
            centroid = get_midpoint(region)
            relaxed_points.append(centroid)
            # centroid = get_midpoint(region)
            # relaxed_points.append(get_midpoint([points[n], centroid]))
        return make_regions(relaxed_points)

    vor = Voronoi(points)
    vor_regions = [r for r in vor.regions if -1 not in r]

    # pprint(vor_regions)
    # exit()

    regions = []
    for indexed_region in vor_regions:
        if not indexed_region:
            continue
        region = [tuple(vor.vertices[vertex_index]) for vertex_index in indexed_region]
        regions.append(region)

    for _ in range(n_relax):
        regions, points = relax(regions)
    return regions, points

# vor = Voronoi(points)
# print(vor.regions)
# exit()
regions, points = make_regions(points)

pprint(len(points))
# pprint(regions)

# Road Types
# Diagonal: 0-6, 9-3
# NS: 1-7, 2-8
# EW: 11-5, 10-4


point1 = random.choice(sector[1])
point2 = random.choice(sector[7])

surface.fill(blue)
for r in regions:
    pygame.draw.polygon(surface, random_color(), r)
# for (x,y) in points:
#     pygame.draw.circle(surface, (0,0,0), (x, y), 2)

pygame.draw.line(surface, BLACK, point1, point2, 3)

pops = []
for _ in range(100):
    x = random.randint(0, width)
    y = random.randint(0, height)
    pops.append((x,y))
    pygame.draw.circle(pop_surface, BLACK, (x, y), 2)

# exit()

def move_pops(pops):
    new_pops = []
    for x, y in pops:
        pop = Pop((x, y))
        dx = random.choice([-1, 0, 1])
        dy = random.choice([-1, 0, 1])
        pop.v = (dx, dy)
        new_pops.append(pop)
    return new_pops

class Pop:
    def __init__(self, position):
        self.x, self.y = position

pops = move_pops(pops)

c = 0
while 1:
    c += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    if c % 100000 == 0:
        c = 0

        screen.fill(blue)
        pop_surface.fill(pygame.SRCALPHA)


        # print(pops[0])
        for pop in pops:
            x, y = pop
            pygame.draw.circle(pop_surface, BLACK, (x, y), 2)

        screen.blit(surface, (0,0))
        screen.blit(pop_surface, (0,0))
        pygame.display.flip()