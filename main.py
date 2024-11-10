'''
Copyright (c) 2024, Alessandro Lupo
All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.
'''

import pygame
from engine import Engine

def main():
    '''
    Main function for executing the game loop.
    '''

    # Define movement keys for game control
    MOVE_KEYS = {pygame.K_LEFT, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_q, pygame.K_e, pygame.K_UP}

    # Initialize game engine and variables
    engine = Engine()
    running = True
    user_input = -1
    time_of_next_step = pygame.time.get_ticks() + engine.settings.time_step

    # Main game loop
    while running:    
        
        # Process events from the event queue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Exit the loop if a quit event is detected
                running = False
            elif event.type == pygame.KEYDOWN:
                # Capture the key pressed by the user for processing
                user_input = event.key
        
        if user_input in MOVE_KEYS:
            # Process movement if key is in MOVE_KEYS; ignore otherwise
            running = engine.advance(user_input)
            user_input = -1
        
        if pygame.time.get_ticks() > time_of_next_step:
            # Automatically advance the game state if time has elapsed
            # Process without specific user input (-1) and set the next step time
            running = engine.advance(-1)
            time_of_next_step = pygame.time.get_ticks() + engine.settings.time_step
     
# Execute main function only when this script is run directly
if __name__ == "__main__":
    main()