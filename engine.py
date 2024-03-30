import random
import blocks
import pygame
import copy


        
class Engine():

    score = 0
    floor = []
    
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Falling Blocks")
        self.settings = Settings()
        self.screen = pygame.display.set_mode(self.settings.canvas_size)
        self.floor = [[0 for _ in range(self.settings.grid_size[1])] for _ in range(self.settings.grid_size[0])]
        self.falling_block = blocks.Block(self, random.randrange(6), 0, self.settings.block_size)
        print(self.floor)
    def advance(self, user_input):
        
        old_position = copy.copy(self.falling_block)
        
        collision_block = 0
        if user_input == pygame.K_LEFT:
            self.falling_block.move(-1, 0)
            collision_status = self.falling_block.check_collision()
            if collision_status<0:
                collision_block = (collision_status==self.falling_block.COLLISION_BLOCK)
                self.falling_block.move(1, 0)
        elif user_input == pygame.K_RIGHT:
            self.falling_block.move(1, 0)
            collision_status = self.falling_block.check_collision()
            if collision_status<0:
                collision_block = (collision_status==self.falling_block.COLLISION_BLOCK)
                self.falling_block.move(-1, 0)
        elif user_input == pygame.K_DOWN:
            self.falling_block.move(0, 1)
            collision_status = self.falling_block.check_collision()
            if collision_status<0:
                collision_block = (collision_status==self.falling_block.COLLISION_BLOCK)
                self.falling_block.move(0, -1)
        elif user_input == pygame.K_q:
            self.falling_block.rotate(-1)
            collision_status = self.falling_block.check_collision()
            if collision_status<0:
                collision_block = (collision_status==self.falling_block.COLLISION_BLOCK)
                self.falling_block.rotate(1)
        elif user_input == pygame.K_e:
            self.falling_block.rotate(1)
            collision_status = self.falling_block.check_collision()
            if collision_status<0:
                collision_block = (collision_status==self.falling_block.COLLISION_BLOCK)
                self.falling_block.rotate(-1)
        
        if collision_block:
            self.add_falling_block_to_floor()
            self.falling_block = blocks.Block(self, random.randrange(6), 0, self.settings.block_size)
        else:
            old_position.clear()
        
        self.falling_block.update_graphics()
        
        self.falling_block.draw()    
        pygame.display.flip()
    
    def add_falling_block_to_floor(self):
        for x, y, is_visible in self.falling_block.locations:
            if is_visible == 0:
                continue
            self.floor[x][y]=1
        print(self.floor)

class Settings():
    grid_size  = (11, 19)
    block_size = 32
    canvas_size = (11*32, 19*32)
    background = (20, 20, 20)