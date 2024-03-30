import blocks
import pygame
from engine import Engine

def main():
    MOVE_KEYS = {pygame.K_LEFT, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_q, pygame.K_e}
    engine = Engine()
     
    running = True
    user_input = 0
    engine.screen.fill(engine.settings.background)
    
    new_step = pygame.time.get_ticks()+engine.settings.time_step
    
    while running:    
                
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                user_input = event.key
        if user_input in MOVE_KEYS:
            if user_input == pygame.K_DOWN:
                new_step = pygame.time.get_ticks()+engine.settings.time_step
            running = engine.advance(user_input)
            user_input = 0
        
        if pygame.time.get_ticks()>new_step:
            running = engine.advance(0)
            new_step = pygame.time.get_ticks()+engine.settings.time_step
        
     
     
# run the main function only if this module is executed as the main script
if __name__=="__main__":
    main()
