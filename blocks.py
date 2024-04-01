'''
Copyright (c) 2024, Alessandro Lupo
All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree. '''

import pygame
import engine
import math

class Block():
    """
    Class defining a falling block
            - self.color: The (r,g,b) color of the block
            - self.locations: List of squares composing the block, recorded as [x_position, y_position, is_visible].
              A square with is_visible == false does not appear on screen, does not collide with anything, and is used
              only to facilitate the rotation algorithm.
            - self.graphics: List of pygame.rect objects composing the block.
    """
    
    # 
    COLLISION_NONE  = 0
    COLLISION_WALL  = -1
    COLLISION_BLOCK = -2
    
    color      = (0, 0, 0)
    locations  = []
    graphics   = []
    square_size = []
    
    def __init__(self, engine, blocktype, startx, color=-1, locations=0):   
        
        self.engine = engine
        
        if locations==0:
            if blocktype==0:
                # 'L' block
                self.locations = [[startx, 0, True], [startx, 1, True], [startx, 2, True], [startx+1, 2, True], [startx-1, 2, False]]
                self.color     = 0
            elif blocktype==1:
                # reversed 'L' block
                self.locations = [[startx+1, 0, True], [startx+1, 1, True], [startx+1, 2, True], [startx, 2, True], [startx-1, 2, False]]
                self.color     = 1
            elif blocktype==2:
                # square block
                self.locations = [[startx, 0, True], [startx, 1, True], [startx+1, 0, True], [startx+1, 1, True]]
                self.color     = 2
            elif blocktype==3:
                # I block
                self.locations = [[startx, 0, True], [startx, 1, True], [startx, 2, True], [startx, 3, True], [startx, 4, False]]
                self.color     = 3
            elif blocktype==4:
                # S block
                self.locations = [[startx, 0, True], [startx+1, 0, True], [startx+1, 1, True], [startx+2, 1, True]]
                self.color     = 4
            elif blocktype==5:
                # Z block
                self.locations = [[startx, 0, True], [startx+1, 0, True], [startx, 1, True], [startx-1, 1, True]]
                self.color     = 5
            elif blocktype==6:
                # reversed T block
                self.locations = [[startx, 1, True], [startx+1, 1, True], [startx+2, 1, True], [startx+1, 0, True],[startx+1, 2, False]]
                self.color     = 6
            else:
                raise Exception("Unknown blocktype")
        else:
            self.locations = locations
        
        self.update_graphics()
        
        if color!=-1:
            self.color = color
    
    def move(self, deltax, deltay):
        for i in range(len(self.locations)):
            self.locations[i] = [self.locations[i][0]+deltax, self.locations[i][1]+deltay, self.locations[i][2]]
    
    def rotate(self, direction):
        # Rotate counterclockwise: first transpose, then reverse columns
        # Rotate clockwise: first transpose, then reverse rows
        
        center_y = (max(self.locations, key=lambda x: x[1])[1]+min(self.locations, key=lambda x: x[1])[1])/2
        center_x = (max(self.locations, key=lambda x: x[0])[0]+min(self.locations, key=lambda x: x[0])[0])/2
        
        for i in range(len(self.locations)):
            self.locations[i] = [self.locations[i][0]-math.floor(center_x), self.locations[i][1]-math.floor(center_y), self.locations[i][2]]
        for i in range(len(self.locations)):
            self.locations[i] = [self.locations[i][1], self.locations[i][0], self.locations[i][2]]
        for i in range(len(self.locations)):
            self.locations[i] = [self.locations[i][0]+math.floor(center_x), self.locations[i][1]+math.floor(center_y), self.locations[i][2]]
        if direction == 1:
            for i in range(len(self.locations)):
                self.locations[i] = [self.locations[i][0], 2*center_y - self.locations[i][1], self.locations[i][2]]
        elif direction == -1:
            for i in range(len(self.locations)):
                self.locations[i] = [2*center_x - self.locations[i][0], self.locations[i][1], self.locations[i][2]]
        else:
            raise Exception("Unknown rotation")
        for i in range(len(self.locations)):
            self.locations[i][0] = int(self.locations[i][0])
            self.locations[i][1] = int(self.locations[i][1])
        
    def check_collision(self):
        for x,y,is_visible in self.locations:
            if is_visible == False:
                continue
            if x<0 or x>=self.engine.settings.grid_size[0]:
                return self.COLLISION_WALL
            if y == self.engine.settings.grid_size[1] or self.engine.old_blocks[y][x]>-1:
                return self.COLLISION_BLOCK
        return self.COLLISION_NONE
    
    def update_graphics(self):
        self.graphics = []
        for x,y,is_visible in self.locations:
            if is_visible:
                self.graphics.append(pygame.Rect(x*self.engine.settings.block_size, y*self.engine.settings.block_size, self.engine.settings.block_size, self.engine.settings.block_size))
    
    def draw(self):
        for rect in self.graphics:
            self.engine.screen.fill(self.engine.colors.COLORS[self.color], rect=rect)
    
    def clear(self):
        for rect in self.graphics:
            self.engine.screen.fill(self.engine.settings.background, rect=rect)
