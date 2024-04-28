'''
Copyright (c) 2024, Alessandro Lupo
All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree. '''

import pygame
from engine import Engine

def main():
    '''
    Main function'''

    MOVE_KEYS = {pygame.K_LEFT, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_q, pygame.K_e, pygame.K_UP}

    engine      = Engine()
    running     = True
    user_input  = -1
    
    time_of_next_step = pygame.time.get_ticks()+engine.settings.time_step
    
    while running:    
        # Main Loop in the game
                
        for event in pygame.event.get():
            # Check events in the queue
            if event.type == pygame.QUIT:
                # If received the QUIT event, leave the loop
                running = False
            elif event.type == pygame.KEYDOWN:
                # If received a KEYDOWN event, save the key in user_input to be processed
                user_input = event.key
        
        if user_input in MOVE_KEYS:
            # If the key is among MOVE_KEYS, process it. Otherwise ignore it
            running     = engine.advance(user_input)
            user_input  = -1
        
        if pygame.time.get_ticks()>time_of_next_step:
            # If it is time to advance the game (e.g. making the block move down)
            # Advance the game without input key (-1)
            # And set a new time_of_next_step
            running = engine.advance(-1)
            time_of_next_step = pygame.time.get_ticks()+engine.settings.time_step
     
# Run the main function only if this module is executed as the main script
if __name__=="__main__":
    main()
