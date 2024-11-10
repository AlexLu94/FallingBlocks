'''
Copyright (c) 2024, Alessandro Lupo
All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.
'''

import pygame
import engine
import math

class Block:
    """
    Class defining a falling block within the game.

    Attributes:
        color: The (r, g, b) color of the block.
        locations: A list of squares composing the block, each represented as [x_position, y_position, is_visible].
                   Squares with is_visible == False are not displayed or interactable, aiding in rotation logic.
        graphics: A list of pygame.Rect objects representing the block's graphical components.
    """
    
    COLLISION_NONE  = 0
    COLLISION_WALL  = -1
    COLLISION_BLOCK = -2
    
    color = (0, 0, 0)
    locations = []
    graphics = []
    square_size = []
    
    def __init__(self, engine, blocktype, startx, color=-1, locations=0):   
        """
        Initialize the block with a specific shape or given locations.

        Parameters:
            engine: Reference to the game engine for accessing settings and display.
            blocktype: The type of block (0-6), defining its shape.
            startx: Initial x-coordinate for the block.
            color: Optional parameter to set a specific color; defaults to block type color if not specified.
            locations: Optional preset locations for custom block shapes.
        """
        self.engine = engine
        
        if locations == 0:
            # Define block shapes based on blocktype
            if blocktype == 0:
                # 'L' block
                self.locations = [[startx, 0, True], [startx, 1, True], [startx, 2, True], [startx+1, 2, True], [startx-1, 2, False]]
                self.color = 0
            elif blocktype == 1:
                # Reversed 'L' block
                self.locations = [[startx+1, 0, True], [startx+1, 1, True], [startx+1, 2, True], [startx, 2, True], [startx-1, 2, False]]
                self.color = 1
            elif blocktype == 2:
                # Square block
                self.locations = [[startx, 0, True], [startx, 1, True], [startx+1, 0, True], [startx+1, 1, True]]
                self.color = 2
            elif blocktype == 3:
                # I block
                self.locations = [[startx, 0, True], [startx, 1, True], [startx, 2, True], [startx, 3, True], [startx, 4, False]]
                self.color = 3
            elif blocktype == 4:
                # S block
                self.locations = [[startx, 0, True], [startx+1, 0, True], [startx+1, 1, True], [startx+2, 1, True]]
                self.color = 4
            elif blocktype == 5:
                # Z block
                self.locations = [[startx, 0, True], [startx+1, 0, True], [startx, 1, True], [startx-1, 1, True]]
                self.color = 5
            elif blocktype == 6:
                # Reversed T block
                self.locations = [[startx, 1, True], [startx+1, 1, True], [startx+2, 1, True], [startx+1, 0, True],[startx+1, 2, False]]
                self.color = 6
            else:
                raise Exception("Unknown blocktype")
        else:
            self.locations = locations
        
        self.update_graphics()
        
        if color != -1:
            self.color = color
    
    def move(self, deltax, deltay):
        """Move the block by specified deltas."""
        for i in range(len(self.locations)):
            self.locations[i] = [self.locations[i][0] + deltax, self.locations[i][1] + deltay, self.locations[i][2]]
    
    def rotate(self, direction):
        """
        Rotate the block around its center.

        Parameters:
            direction: Rotation direction; -1 for counterclockwise, 1 for clockwise.
        """
        # Compute center of rotation
        center_y = (max(self.locations, key=lambda x: x[1])[1] + min(self.locations, key=lambda x: x[1])[1]) / 2
        center_x = (max(self.locations, key=lambda x: x[0])[0] + min(self.locations, key=lambda x: x[0])[0]) / 2
        
        # Translate block to origin, transpose, then apply rotation
        for i in range(len(self.locations)):
            self.locations[i] = [self.locations[i][0] - math.floor(center_x), self.locations[i][1] - math.floor(center_y), self.locations[i][2]]
        for i in range(len(self.locations)):
            self.locations[i] = [self.locations[i][1], self.locations[i][0], self.locations[i][2]]
        for i in range(len(self.locations)):
            self.locations[i] = [self.locations[i][0] + math.floor(center_x), self.locations[i][1] + math.floor(center_y), self.locations[i][2]]
        
        if direction == 1:
            for i in range(len(self.locations)):
                self.locations[i] = [self.locations[i][0], 2 * center_y - self.locations[i][1], self.locations[i][2]]
        elif direction == -1:
            for i in range(len(self.locations)):
                self.locations[i] = [2 * center_x - self.locations[i][0], self.locations[i][1], self.locations[i][2]]
        else:
            raise Exception("Unknown rotation direction")
        
        # Ensure positions are integers
        for i in range(len(self.locations)):
            self.locations[i][0] = int(self.locations[i][0])
            self.locations[i][1] = int(self.locations[i][1])
        
    def check_collision(self):
        """
        Check for collisions with the game boundaries or existing blocks.

        Returns:
            COLLISION_NONE if no collision, COLLISION_WALL if colliding with wall, or COLLISION_BLOCK if colliding with other blocks.
        """
        for x, y, is_visible in self.locations:
            if not is_visible:
                continue
            if x < 0 or x >= self.engine.settings.grid_size[0]:
                return self.COLLISION_WALL
            if y == self.engine.settings.grid_size[1] or self.engine.old_blocks[y][x] > -1:
                return self.COLLISION_BLOCK
        return self.COLLISION_NONE
    
    def update_graphics(self):
        """Update graphical representation of the block based on current locations."""
        self.graphics = []
        for x, y, is_visible in self.locations:
            if is_visible:
                rect = pygame.Rect(x * self.engine.settings.block_size, y * self.engine.settings.block_size, self.engine.settings.block_size, self.engine.settings.block_size)
                self.graphics.append(rect)
    
    def draw(self):
        """Draw the block on the game screen."""
        for rect in self.graphics:
            self.engine.screen.fill(self.engine.colors.COLORS[self.color], rect=rect)
    
    def clear(self):
        """Clear the block's graphical representation from the screen."""
        for rect in self.graphics:
            self.engine.screen.fill(self.engine.settings.background, rect=rect)