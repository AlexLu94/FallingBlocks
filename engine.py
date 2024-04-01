'''
Copyright (c) 2024, Alessandro Lupo
All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree. '''

import random
import blocks
import pygame
import copy
        
class Engine():

    score = 0
    
    def __init__(self):

        
        # Init variables
        self.settings = Settings()
        self.colors   = Colors()
        self.old_blocks = [[-1 for _ in range(self.settings.grid_size[0])] for _ in range(self.settings.grid_size[1])]
        
        # Init pygame library and screen
        pygame.init()
        pygame.display.set_caption("Falling Blocks")
        self.screen = pygame.display.set_mode(self.settings.canvas_size)
        self.screen.fill(self.settings.background)
        pygame.display.flip()
        
        self.falling_block = blocks.Block(self, random.randrange(7), 6)
        self.falling_block.update_graphics()
        self.falling_block.draw()
        self.score = 0
        

    def advance(self, user_input):
        
        # Save the old position of the block, to know where to clean the screen if we move it
        old_position = copy.copy(self.falling_block)
        
        # Perform movement, either because of user input or because of falling
        collision_block = False     # Flag: is the block colliding with one of the old_blocks?
        if user_input == pygame.K_LEFT:
            self.falling_block.move(-1, 0)
            collision_status = self.falling_block.check_collision()
            if collision_status<0:
                self.falling_block.move(1, 0)
        elif user_input == pygame.K_RIGHT:
            self.falling_block.move(1, 0)
            collision_status = self.falling_block.check_collision()
            if collision_status<0:
                self.falling_block.move(-1, 0)
        elif user_input == pygame.K_DOWN or user_input == 0:
            self.falling_block.move(0, 1)
            collision_status = self.falling_block.check_collision()
            if collision_status<0:
                collision_block = (collision_status==self.falling_block.COLLISION_BLOCK)
                self.falling_block.move(0, -1)
        elif user_input == pygame.K_q:
            self.falling_block.rotate(-1)
            collision_status = self.falling_block.check_collision()
            if collision_status<0:
                self.falling_block.rotate(1)
        elif user_input == pygame.K_e:
            self.falling_block.rotate(1)
            collision_status = self.falling_block.check_collision()
            if collision_status<0:
                self.falling_block.rotate(-1)
        
        # If falling_block hit any of the old_blocks
        if collision_block:
            self.add_falling_block_to_old_blocks()
            if random.randint(0, 100)<10:
                self.falling_block = blocks.Block(self, random.randrange(7), 6)
            else:
                optimal_block_shape = self.find_optimal_block_shape()
                if len(optimal_block_shape)>1:
                    self.falling_block = blocks.Block(self, 0, 6, locations = optimal_block_shape, color = 8)
                else:
                    self.falling_block = blocks.Block(self, random.randrange(7), 6)
                    
            
            full_lines = self.check_full_lines()        # Check if we have full lines
            if len(full_lines)>0:                       # If yes
                self.process_full_lines(full_lines)     # process them
                self.score += 1 if len(full_lines)==1 else 2 if len(full_lines) == 2 else 4 if len(full_lines) == 3 else 8
                print("New score:", self.score)
                self.settings.time_step = int(self.settings.time_step*0.95)
            if self.falling_block.check_collision()<0:  # If, even after processing the full lines, the falling_block
                self.game_over()                        # is still colliding, then it is game_over
                return False                            # Return False to signal that the loop can finish
        else:
            # If we have no collision, just clear the old position of the falling_block because we are going to move it
            old_position.clear()
        
        # Draw the new position of falling_block
        self.falling_block.update_graphics()
        self.falling_block.draw()
        
        # Advance the dispaly
        pygame.display.flip()
        
        # Return True to signal that the loop can continue
        return True
    
    def add_falling_block_to_old_blocks(self):
        for x, y, is_visible in self.falling_block.locations:
            if is_visible == 0:
                continue
            self.old_blocks[y][x]=self.falling_block.color
    
    def check_full_lines(self):
        retv = []
        for i in range(len(self.old_blocks)):
            for v in self.old_blocks[i]:
                if v == -1:
                    break
            else:
                retv.append(i)
        return retv
    
    def game_over(self):
        self.falling_block.color = 7
        self.falling_block.update_graphics()
        self.falling_block.draw()
        pygame.display.flip()
        print("GAME OVER")
        running = True
        pygame.event.clear()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                    running = False
                    
    def process_full_lines(self, full_lines):
        # Change the old_blocks
        for line in list(full_lines):
            for i in reversed(range(0, line)):
                temp = self.old_blocks[i].copy()
                self.old_blocks[i+1] = temp
            self.old_blocks[0] = [-1 for _ in range(self.settings.grid_size[0])]
        # Update graphics
        self.screen.fill(self.settings.background)
        for y in range(len(self.old_blocks)):
            for x in range(len(self.old_blocks[y])):
                if self.old_blocks[y][x]>-1:
                    self.screen.fill(self.colors.COLORS[self.old_blocks[y][x]], rect=pygame.Rect(x*self.settings.block_size, y*self.settings.block_size, self.settings.block_size, self.settings.block_size))

    def find_optimal_block_shape(self):
        # First, determine the correct row
        for y in range(self.settings.grid_size[1]):
            for x in range(self.settings.grid_size[0]):
                if self.old_blocks[y][x]>-1:
                    if (x>=1 and self.old_blocks[y][x-1]<0) or (x<len(self.old_blocks[y])-1 and self.old_blocks[y][x+1]<0):
                        break
            else:
                continue
            break
        print("Existing block in", x, y)
        # Randomly chose the side of an existing block
        if x==0:
            print("x was 0")
            x   += 1
            side = 1
        elif x == self.settings.grid_size[0]:
            print("x was max")
            x    -= 1
            side = -1
        elif random.randint(0, 1)==1:
            print("going right")
            x   += 1
            side = 1
        else:
            print("going left")
            x    -= 1
            side = -1
        
        # First fill the line
        locations=[[0, 0, True]]
        if side == 1:   # If going right
            while x<self.settings.grid_size[0]-1 and self.old_blocks[y][x]<0:
                x += 1
                new_location = locations[-1].copy()
                new_location[0] += 1
                locations.append(new_location)
        else:           # Elif going left
            while x>0 and self.old_blocks[y][x]<0:
                x -= 1
                new_location = locations[-1].copy()
                new_location[0] -= 1
                locations.append(new_location)
        # Need to correct for negative locations now
        min_x = min(locations, key = lambda x: x[0])[0]
        for i in range(len(locations)):
            locations[i][0] -= min_x
        print(locations)
        return locations
    
class Settings():
    grid_size  = (11, 19)
    block_size = 32
    canvas_size = (11*32, 19*32)
    background = (20, 20, 20)
    time_step = 200
    
class Colors():
    COLORS = [(0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255), (255, 0, 255), (192, 192, 192), (255, 255, 255), (255, 0, 0), (100, 255, 255)]