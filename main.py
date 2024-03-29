import pygame
import blocks

class Settings:
    grid_size  = (11, 19)
    block_size = 32
    canvas_size = (11*32, 19*32)
    background = (20, 20, 20)
    
def main():
    settings = Settings()
    
    pygame.init()
    pygame.display.set_caption("Falling Blocks")
     
    screen = pygame.display.set_mode(settings.canvas_size)
     
    running = True
    
    
    falling_block = blocks.Block(6, 0, settings.block_size)
    
    
    while running:    
        screen.fill(settings.background)
        falling_block.draw(screen)    
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    falling_block.move(-1, 0)
                    if falling_block.check_collision(settings)<0:
                        falling_block.move(1, 0)
                elif event.key == pygame.K_RIGHT:
                    falling_block.move(1, 0)
                    if falling_block.check_collision(settings)<0:
                        falling_block.move(-1, 0)
                elif event.key == pygame.K_DOWN:
                    falling_block.move(0, 1)
                    if falling_block.check_collision(settings)<0:
                        falling_block.move(0, -1)
                elif event.key == pygame.K_q:
                    falling_block.rotate(1)
                    if falling_block.check_collision(settings)<0:
                        falling_block.rotate(-1)
                elif event.key == pygame.K_e:
                    falling_block.rotate(-1)
                    if falling_block.check_collision(settings)<0:
                        falling_block.rotate(1)
        falling_block.update_graphics()
        
     
     
# run the main function only if this module is executed as the main script
if __name__=="__main__":
    main()
