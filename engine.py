'''
Copyright (c) 2024, Alessandro Lupo
All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.
'''

import pygame, copy, random
import blocks
 
class Engine:
    '''
    The game engine class responsible for game mechanics and rendering.
    '''
    
    def __init__(self):
        '''
        Initialize the Engine class with game settings, colors, score,
        and setup the initial game screen and falling block.
        '''

        # Initialize variables and settings
        self.settings = Settings()
        self.colors = Colors()
        self.score = 0
        self.old_blocks = [[-1 for _ in range(self.settings.grid_size[0])] for _ in range(self.settings.grid_size[1])]
        
        # Initialize pygame library and game display
        pygame.init()
        pygame.display.set_caption("Falling Blocks")
        self.screen = pygame.display.set_mode(self.settings.canvas_size)
        self.screen.fill(self.settings.background)
        pygame.display.flip()
        pygame.key.set_repeat(200, 55)
        
        # Position the first falling block
        self.falling_block = blocks.Block(self, random.randrange(7), 6)
        self.falling_block.update_graphics()
        self.falling_block.draw()
        
    def advance(self, user_input):
        '''
        Advance the game by moving the falling block based on user input,
        checking for collisions, and updating the game state.
        '''

        # Save current block position for clearing if block moves
        old_position = copy.copy(self.falling_block)
        
        # Process movement and check for collisions
        collision_block = False  # Flag to indicate if block collides with existing blocks
        if user_input == pygame.K_LEFT:
            self.falling_block.move(-1, 0)
            if self.falling_block.check_collision() < 0:
                self.falling_block.move(1, 0)  # Undo move on collision
        elif user_input == pygame.K_RIGHT:
            self.falling_block.move(1, 0)
            if self.falling_block.check_collision() < 0:
                self.falling_block.move(-1, 0)  # Undo move on collision
        elif user_input == pygame.K_DOWN or user_input == -1:
            self.falling_block.move(0, 1)
            collision_status = self.falling_block.check_collision()
            if collision_status < 0:
                collision_block = (collision_status == self.falling_block.COLLISION_BLOCK)
                self.falling_block.move(0, -1)  # Undo move on collision
        elif user_input == pygame.K_q or user_input == pygame.K_UP:
            self.falling_block.rotate(-1)
            if self.falling_block.check_collision() < 0:
                self.falling_block.rotate(1)  # Undo rotation on collision
        elif user_input == pygame.K_e:
            self.falling_block.rotate(1)
            if self.falling_block.check_collision() < 0:
                self.falling_block.rotate(-1)  # Undo rotation on collision
        
        # Handle collision with old blocks
        if collision_block:
            self.add_falling_block_to_old_blocks()
            full_lines = self.check_full_lines()
            if full_lines:
                # Process full lines and update score
                self.process_full_lines(full_lines)
                self.score += 1 if len(full_lines) == 1 else 3 if len(full_lines) == 2 else 9 if len(full_lines) == 3 else 27
                print("New score:", self.score)
                pygame.display.set_caption(f"Falling Blocks - Score: {self.score}")
                self.settings.time_step = int(self.settings.time_step * 0.95)
            self.falling_block = self.get_new_block()
            if self.falling_block.check_collision() < 0:
                self.game_over()
                return False  # Signal to end game loop
        else:
            old_position.clear()  # Clear old position if no collision
        
        # Draw updated block position and refresh display
        self.falling_block.update_graphics()
        self.falling_block.draw()
        pygame.display.flip()
        
        return True  # Signal to continue game loop
    
    def add_falling_block_to_old_blocks(self):
        '''
        Add the falling block to the old_blocks grid, making it a fixed part
        of the game field.
        '''
        for x, y, is_visible in self.falling_block.locations:
            if is_visible:
                self.old_blocks[y][x] = self.falling_block.color
    
    def check_full_lines(self):
        '''
        Identify full lines in the old_blocks grid.
        '''
        retv = []
        for i, row in enumerate(self.old_blocks):
            if all(v != -1 for v in row):
                retv.append(i)
        return retv
    
    def game_over(self):
        '''
        End the game, display "Game Over" message, and wait for window closure.
        '''

        # Highlight last block in red
        self.falling_block.color = 9
        self.falling_block.update_graphics()
        self.falling_block.draw()

        # Display "GAME OVER" message
        font = pygame.font.Font(None, 64)
        text = font.render("GAME OVER :(", True, (255, 200, 200))
        textpos = text.get_rect(centerx=self.screen.get_width() / 2, y=300)
        self.screen.blit(text, textpos)
        text = font.render(f"SCORE: {self.score}", True, (255, 255, 255))
        textpos = text.get_rect(centerx=self.screen.get_width() / 2, y=380)
        self.screen.blit(text, textpos)

        pygame.display.flip()

        print("GAME OVER. Score:", self.score)
        print("Close the window to exit")
        
        running = True
        pygame.event.clear()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
    def process_full_lines(self, full_lines):
        '''
        Remove full lines from old_blocks, shift remaining blocks down,
        and update the display.
        '''
        for line in full_lines:
            for i in range(line, 0, -1):
                self.old_blocks[i] = self.old_blocks[i - 1].copy()
            self.old_blocks[0] = [-1] * self.settings.grid_size[0]
        
        # Update graphics after removing lines
        self.screen.fill(self.settings.background)
        for y, row in enumerate(self.old_blocks):
            for x, color_index in enumerate(row):
                if color_index > -1:
                    rect = pygame.Rect(x * self.settings.block_size, y * self.settings.block_size, self.settings.block_size, self.settings.block_size)
                    self.screen.fill(self.colors.COLORS[color_index], rect=rect)

    def get_new_block(self):
        '''
        Generate a new block.
        '''
        # Note: `probability_good_block` is currently set to zero, so the following condition is always skipped.
        if random.randint(0, 100) <= self.settings.probability_good_block:
            optimal_block_shape = self.find_optimal_block_shape()
            optimal_block_shape = self.resize_optimal_block(optimal_block_shape)
            if optimal_block_shape:
                return blocks.Block(self, 0, 6, locations=optimal_block_shape, color=8)
        return blocks.Block(self, random.randrange(7), 6)
    
    def resize_optimal_block(self, locations):
        '''
        Resize an optimal block shape to fit within the game grid,
        avoiding oversized blocks.
        [Currently not used]
        '''
        # Determine vertical and horizontal limits
        bottom_line = max(locations, key=lambda x: x[1])[1]
        min_column, max_column = min(locations, key=lambda x: x[0])[0], max(locations, key=lambda x: x[0])[0]
        
        max_line_to_accept = bottom_line - max(1, round(random.gauss(self.settings.optimal_block_size_y_mean, self.settings.optimal_block_size_y_std)))
        min_column_to_accept = min_column if random.choice([True, False]) else max(min_column, max_column - round(random.gauss(self.settings.optimal_block_size_x_mean, self.settings.optimal_block_size_x_std)))

        # Remove any parts of block exceeding limits
        locations = [loc for loc in locations if min_column_to_accept <= loc[0] <= max_column]
        
        if locations:
            min_line = min(locations, key=lambda x: x[1])[1]
            for loc in locations:
                loc[1] -= min_line

        return locations
    
    def find_optimal_block_shape(self):
        '''
        Create an optimal block that fills a gap within the old_blocks grid.
        [Currently not used]
        '''
        # Find first empty spot
        for y, row in enumerate(self.old_blocks):
            for x, cell in enumerate(row):
                if cell > -1 and (self.old_blocks[y][x - 1] < 0 or (x + 1 < len(row) and self.old_blocks[y][x + 1] < 0)):
                    break
            else:
                continue
            break

        # Randomly choose side to fill
        side = random.choice([-1, 1])
        x += side
        locations = [[x, y, True]]
        
        while 0 <= x < len(row) - 1 and self.old_blocks[y][x] < 0:
            x += side
            new_loc = [locations[-1][0] + side, y, True]
            locations.append(new_loc)

        # Add any empty cells below
        to_add = [[x, yt, True] for x, _, _ in locations for yt in range(y + 1, len(self.old_blocks)) if self.old_blocks[yt][x] < 0]
        
        return locations + to_add
    
class Settings:
    grid_size = (11, 19)
    block_size = 32
    canvas_size = (11 * 32, 19 * 32)
    background = (20, 20, 20)
    time_step = 300
    probability_good_block = 0
    optimal_block_size_x_mean = 3
    optimal_block_size_x_std = 2
    optimal_block_size_y_mean = 3
    optimal_block_size_y_std = 2
    
class Colors:
    COLORS = [(0, 127, 255), (0, 255, 127), (255, 127, 0), (255, 0, 127), (127, 255, 0), (127, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 0), (255, 0, 0)]
