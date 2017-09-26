# A simple demo of the math found in
# http://www.redblobgames.com/grids/hexagons/

import pygame
from pygame.locals import *
import math

size = 24
width = size * 2
height = math.sqrt(3.0)/2.0 * width
screensize = (1280,720)

class Cube():
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z

class Hex():
    def __init__(self,q,r):
        self.q = q
        self.r = r
    def __str__(self):
        return "<{0:2d},{1:2d}>".format(self.q, self.r)

def cubeToHex(cube):
    return Hex(cube.x, cube.z)

def hexToCube(ax):
    x = ax.q
    z = ax.r
    y = -x-z
    return Cube(x,y,z)

def cubeAdd(cube1, cube2):
    return Cube(cube1.x+cube2.x, cube1.y+cube2.y, cube1.z+cube2.z)

def cubeDirection(direction):    
    cubeDirections = [Cube(+1,-1,0), Cube(+1,0,-1), Cube(0,+1,-1),
                      Cube(-1,+1,0), Cube(-1,0,+1), Cube(0,-1,+1)]
    return cubeDirections[direction]

def cubeNeighbor(direction):
    return cubeAdd(cube, cubeDirection(direction))

def hexAdd(hex1, hex2):
    return Hex(hex1.q + hex2.q, hex1.r+hex2.r)

def hexDirection(direction):
    hexDirections = [Hex(+1,0), Hex(+1,-1), Hex(0,-1),
                     Hex(-1,0), Hex(-1,+1), Hex(0,+1)]
    return hexDirections[direction]

def hexNeighbor(ax, direction):
    return hexAdd(ax, hexDirection(direction))

def cubeDistance(a,b):
    return (abs(a.x-b.x) + abs(a.y-b.y) + abs(a.z-b.z))/2

def hexDistance(a,b):
    return cubeDistance(hexToCube(a),hexToCube(b))

def hexToPixel(ax):
    x = size * 1.5 * ax.q
    y = size * math.sqrt(3.0) * (ax.r + ax.q/2.0)
    return (x,y)

def cubeRound(cube):
    rx = int(round(cube.x))
    ry = int(round(cube.y))
    rz = int(round(cube.z))
    xdiff = abs(rx - cube.x)
    ydiff = abs(ry - cube.y)
    zdiff = abs(rz - cube.z)
    if xdiff > ydiff and xdiff > zdiff:
        rx = -ry-rz
    elif ydiff > zdiff:
        ry = -rx-rz
    else:
        rz = -rx-ry
    return Cube(rx, ry, rz)
    
def pixelToCube(pixel):
    x,y = pixel
    q = x * 0.66667 / float(size)
    r = (-x * 0.333333 + math.sqrt(3.0)/3.0 * y)/ float(size)
    return cubeRound(hexToCube(Hex(q, r)))

def hexCorner(x, y, size, i):
    angle = (math.pi/180.0) * 60.0 * i
    return (x + size*math.cos(angle), y + size*math.sin(angle))

def hexCorners(x, y, size):
    return [hexCorner(x,y,size,i) for i in range(6)]
    
def drawCube(surf, cube, color=(0,128,0)):
    x,y = hexToPixel(cubeToHex(cube))
    points = hexCorners(x,y,size)
    pygame.draw.polygon(surf, color, points, 0)
    pygame.draw.polygon(surf, (0,0,0), points, 2)
    
    
def main():
    pygame.init()
    screen = pygame.display.set_mode(screensize)

    N = 7
    center = Cube (+19,-18,0)
    cubes = []
    redcubes = []
    bluecubes = []
    for dx in range(-N, N+1, 1):
        for dy in range(max(-N, -dx-N), min(N+1, -dx+N+1), 1):
            dz = -dx-dy
            cubes.append( cubeAdd(center, Cube(dx,dy,dz)))
    red = True
    while 1:
        screen.fill((200, 200, 255))
        for cube in cubes:
            drawCube(screen, cube)
        for cube in bluecubes:
            drawCube(screen, cube, (0,0,255))
        for cube in redcubes:
            drawCube(screen, cube, (255,0,0))
    
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return
                elif event.key == K_SPACE:
                    redcubes = []
                    bluecubes = []
            elif event.type == MOUSEBUTTONDOWN:
                red = not red
                if red:
                    redcubes.append(pixelToCube(event.pos))
                else:
                    bluecubes.append(pixelToCube(event.pos))
                
            
if __name__ == '__main__':
    try:
        main()
    finally:
        pygame.quit()
        
