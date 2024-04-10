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
        
        pygame.key.set_repeat(200, 55)
        
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
        elif (user_input == pygame.K_q) or (user_input == pygame.K_UP):
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
            full_lines = self.check_full_lines()        # Check if we have full lines
            if len(full_lines)>0:                       # If yes
                self.process_full_lines(full_lines)     # process them
                self.score += 1 if len(full_lines)==1 else 3 if len(full_lines) == 2 else 9 if len(full_lines) == 3 else 27
                print("New score:", self.score)
                self.settings.time_step = int(self.settings.time_step*0.95)
            self.falling_block = self.get_new_block()
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
        print("GAME OVER. Score:", self.score)
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

    def get_new_block(self):
        if random.randint(0, 100)<=self.settings.probability_good_block:
            optimal_block_shape = self.find_optimal_block_shape()
            optimal_block_shape = self.resize_optimal_block(optimal_block_shape)
            if len(optimal_block_shape)>1:
                new_block = blocks.Block(self, 0, 6, locations = optimal_block_shape, color = 8)
            else:
                new_block = blocks.Block(self, random.randrange(7), 6)
        else:
            new_block = blocks.Block(self, random.randrange(7), 6)
        return new_block
    
    def resize_optimal_block(self, locations):
        '''
        Given an optimal block, resize it according to the game settings.
        This is to avoid spanning of huge blocks.'''
        bottom_line = max(locations, key = lambda x: x[1])[1]
        min_column  = min(locations, key = lambda x: x[0])[0]
        max_column  = max(locations, key = lambda x: x[0])[0]
        
        # Determine the index of the highest row to accept
        max_line_to_accept = bottom_line - max(1, round(random.gauss(self.settings.optimal_block_size_y_mean, self.settings.optimal_block_size_y_std)))
        # Determine the range of the columns to accept
        if random.randint(0, 1)==0:
            min_column_to_accept = min_column
            max_column_to_accept = max(min_column +1, max_column - max(0, round(random.gauss(self.settings.optimal_block_size_x_mean, self.settings.optimal_block_size_x_std))))
        else:
            min_column_to_accept = min(max_column -1, min_column + max(0, round(random.gauss(self.settings.optimal_block_size_x_mean, self.settings.optimal_block_size_x_std))))
            max_column_to_accept = max_column
        
        to_delete = []
        for i in range(len(locations)):
            if locations[i][0]<min_column_to_accept or locations[i][0]>max_column_to_accept or locations[i][1]<max_line_to_accept:
                to_delete.append(i)
        for i in reversed(to_delete):
            del locations[i]
        if len(locations) == 0:
            return locations
        min_line = min(locations, key = lambda x: x[1])[1]
        for i in range(len(locations)):
            locations[i][1]-=min_line
        return locations
        
    def find_optimal_block_shape(self):
        # First, determine the correct row
        for y in range(self.settings.grid_size[1]):
            for x in range(self.settings.grid_size[0]):
                if self.old_blocks[y][x]>-1 and ((x>=1 and self.old_blocks[y][x-1]<0) or (x<len(self.old_blocks[y])-1 and self.old_blocks[y][x+1]<0)):
                    break
            else:
                continue
            break
        # Randomly chose the side of an existing block
        if x==0:
            x   += 1
            side = 1
        elif x == self.settings.grid_size[0]:
            x    -= 1
            side = -1
        elif random.randint(0, 1)==1:
            x   += 1
            side = 1
        else:
            x    -= 1
            side = -1
        # Fill the first line
        locations=[[x, y, True]]
        if side == 1:   # If going right
            while x<self.settings.grid_size[0]-2 and self.old_blocks[y][x]<0:
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
        # Now go down each column
        if locations == []:
            return []
        to_add = []
        try:
            for x,_,_ in locations:
                yt = y+1
                while yt<self.settings.grid_size[1] and self.old_blocks[yt][x]<0:
                    to_add.append([x, yt, True])
                    yt += 1
        except IndexError:
            print("DEBUG")
            print("Location:")
            print(locations)
            return []
        locations += to_add

            
        
        
        return locations
    
class Settings():
    grid_size  = (11, 19)
    block_size = 32
    canvas_size = (11*32, 19*32)
    background = (20, 20, 20)
    time_step = 300
    probability_good_block = 50
    optimal_block_size_x_mean = 3
    optimal_block_size_x_std  = 2
    optimal_block_size_y_mean = 3
    optimal_block_size_y_std  = 2
    
class Colors():
    COLORS = [(0, 127,255), (0, 255, 127), (255, 127, 0), (255, 0, 127), (127, 255, 0), (127, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 0)]