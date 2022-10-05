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

points = []
for _ in range(100):
    x = random.randint(0, width)
    y = random.randint(0, height)
    points.append((x,y))
old_points = points

new_points = []
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

    regions = []
    for indexed_region in vor_regions:
        if not indexed_region:
            continue
        region = [tuple(vor.vertices[vertex_index]) for vertex_index in indexed_region]
        regions.append(region)

    for _ in range(n_relax):
        regions, points = relax(regions)
    return regions, points


class Pop:
    x = None
    y = None

    dx = 0
    dy = 0

    def __init__(self, pos):
        self.x, self.y = pos

    def pos(self):
        return (self.x, self.y)

    def move(self):
        self.x += self.dx
        self.y += self.dy

    def random_walk(self):
        self.dx = random.uniform(-1, 1)
        self.dy = random.uniform(-1, 1)


regions, points = make_regions(points)

# Road Types
# Diagonal: 0-6, 9-3
# NS: 1-7, 2-8
# EW: 11-5, 10-4

point1 = random.choice(sector[1])
point2 = random.choice(sector[7])

surface.fill(blue)
for r in regions:
    pygame.draw.polygon(surface, random_color(), r)

pygame.draw.line(surface, BLACK, point1, point2, 3)

pops = []
for _ in range(100):
    # x = random.randint(0, width)
    # y = random.randint(0, height)
    x = random.randint(width*.25, width*.75)
    y = random.randint(height*.25, height*.75)

    pop = Pop((x,y))
    pop.random_walk()

    pops.append(pop)
    pygame.draw.circle(pop_surface, BLACK, (x, y), 2)

c = 0
# Scale of 1 indicates 1px = 10m
scale = 2
offset_x = 0
offset_y = 0

paused = False
while 1:
    c += 1
    for event in pygame.event.get():
        # print(event)
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP:
                scale *= 1.1
            elif event.key == pygame.K_DOWN:
                scale /= 1.1
            elif event.key == pygame.K_w:
                offset_y += 100
            elif event.key == pygame.K_a:
                offset_x += 100
            elif event.key == pygame.K_s:
                offset_y -= 100
            elif event.key == pygame.K_d:
                offset_x -= 100
            # else:
            #     paused = not paused

    if not paused:
        screen.fill(blue)
        pop_surface.fill(pygame.SRCALPHA)

        for pop in pops:
            # pop.random_walk()
            # pop.move()
            x, y = pop.pos()
            # print((x, y))
            pygame.draw.circle(pop_surface, BLACK, (x, y), 2)

        scaled_surface = pygame.transform.scale(surface, (width*scale, height*scale))
        scaled_pop_surface = pygame.transform.scale(pop_surface, (width*scale, height*scale))

        screen.blit(scaled_surface, (offset_x, offset_y))
        screen.blit(scaled_pop_surface, (offset_x, offset_y))
        pygame.display.flip()

    if c % 10000 == 0:
        c = 0