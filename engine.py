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
        self.colors   = Colors()
        self.screen = pygame.display.set_mode(self.settings.canvas_size)
        self.floor = [[-1 for _ in range(self.settings.grid_size[0])] for _ in range(self.settings.grid_size[1])]
        self.falling_block = blocks.Block(self, random.randrange(7), 6, self.settings.block_size)
        self.falling_block.update_graphics()
        self.falling_block.draw()    
        pygame.display.flip()
    
    def advance(self, user_input):
        
        old_position = copy.copy(self.falling_block)
        collision_block = 0
        if user_input == pygame.K_LEFT:
            self.falling_block.move(-1, 0)
            collision_status = self.falling_block.check_collision()
            if collision_status<0:
                #collision_block = (collision_status==self.falling_block.COLLISION_BLOCK)
                self.falling_block.move(1, 0)
        elif user_input == pygame.K_RIGHT:
            self.falling_block.move(1, 0)
            collision_status = self.falling_block.check_collision()
            if collision_status<0:
                #collision_block = (collision_status==self.falling_block.COLLISION_BLOCK)
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
                #collision_block = (collision_status==self.falling_block.COLLISION_BLOCK)
                self.falling_block.rotate(1)
        elif user_input == pygame.K_e:
            self.falling_block.rotate(1)
            collision_status = self.falling_block.check_collision()
            if collision_status<0:
                #collision_block = (collision_status==self.falling_block.COLLISION_BLOCK)
                self.falling_block.rotate(-1)
        
        if collision_block:
            self.add_falling_block_to_floor()
            self.falling_block = blocks.Block(self, random.randrange(7), 6, self.settings.block_size)
            
            full_lines = self.check_full_lines()
            if len(full_lines)>0:
                self.process_full_lines(full_lines)
                
            
            if self.falling_block.check_collision()<0:
                self.game_over()
                return False
        else:
            old_position.clear()
        
        self.falling_block.update_graphics()
        self.falling_block.draw()    
        pygame.display.flip()
        

        return True
    
    def add_falling_block_to_floor(self):
        for x, y, is_visible in self.falling_block.locations:
            if is_visible == 0:
                continue
            self.floor[y][x]=self.falling_block.color
    
    def check_full_lines(self):
        retv = []
        for i in range(len(self.floor)):
            for v in self.floor[i]:
                if v == -1:
                    break
            else:
                retv.append(i)
        return retv
    
    def game_over(self):
        self.falling_block.color = 6
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
        # Change the floor
        for line in list(full_lines):
            for i in reversed(range(0, line)):
                temp = self.floor[i].copy()
                self.floor[i+1] = temp
            self.floor[0] = [-1 for _ in range(self.settings.grid_size[0])]
        # Update graphics
        self.screen.fill(self.settings.background)
        for y in range(len(self.floor)):
            for x in range(len(self.floor[y])):
                if self.floor[y][x]>-1:
                    self.screen.fill(self.colors.COLORS[self.floor[y][x]], rect=pygame.Rect(x*self.settings.block_size, y*self.settings.block_size, self.settings.block_size, self.settings.block_size))

class Settings():
    grid_size  = (11, 19)
    block_size = 32
    canvas_size = (11*32, 19*32)
    background = (20, 20, 20)
    time_step = 100
    
class Colors():
    COLORS = [(220, 80, 15), (80, 220, 15), (15, 80, 220), (220, 15, 80), (80, 15, 220), (15, 220, 80), (255, 0, 0)]