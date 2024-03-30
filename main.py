import blocks
import pygame
from engine import Engine

def main():
    engine = Engine()
     
    running = True
    user_input = 0
    engine.screen.fill(engine.settings.background)
    while running:    
                
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                user_input = event.key
        engine.advance(user_input)
        user_input = 0

        
     
     
# run the main function only if this module is executed as the main script
if __name__=="__main__":
    main()
