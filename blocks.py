import pygame

class Block:
    """A block"""
    
    COLLISION_NONE  = 0
    COLLISION_WALL  = -1
    COLLISION_FLOOR = -2
    
    color      = (0, 0, 0)
    locations  = []
    graphics   = []
    block_size = []
    def __init__(self, blocktype, startx, block_size, color=0):   
        
        self.block_size = block_size
        
        if blocktype==0:
            # 'L' block
            self.locations = [(startx, 0), (startx, 1), (startx, 2), (startx+1, 2)]
            self.color     = (220, 80, 15)
        elif blocktype==1:
            # reversed 'L' block
            self.locations = [(startx+1, 0), (startx+1, 1), (startx+1, 2), (startx, 2)]
            self.color     = (15, 80, 220)
        elif blocktype==2:
            # square block
            self.locations = [(startx, 0), (startx, 1), (startx+1, 0), (startx+1, 1)]
            self.color     = (220, 220, 80)
        elif blocktype==3:
            # I block
            self.locations = [(startx, 0), (startx, 1), (startx, 2), (startx, 3)]
            self.color     = (80, 220, 220)
        elif blocktype==4:
            # S block
            self.locations = [(startx, 0), (startx, 1), (startx+1, 1), (startx+2, 1), (startx+2, 2)]
            self.color     = (220, 80, 220)
        elif blocktype==5:
            # Z block
            self.locations = [(startx, 2), (startx, 1), (startx+1, 1), (startx+2, 1), (startx+2, 0)]
            self.color     = (220, 15, 80)
        elif blocktype==6:
            # reversed T block
            self.locations = [(startx, 1), (startx+1, 1), (startx+2, 1), (startx+1, 0)]
            self.color     = (80, 220, 15)
        else:
            raise Exception("Unknown blocktype")
        
        self.update_graphics()
        
        if color!=0:
            self.color = color
    
    def move(self, deltax, deltay):
        for i in range(len(self.locations)):
            self.locations[i] = (self.locations[i][0]+deltax, self.locations[i][1]+deltay)
 
    def check_collision(self, settings):
        print(self.locations)
        for (x,y) in self.locations:
            if x<0 or y<0 or x>=settings.grid_size[0] or y>=settings.grid_size[1]:
                return self.COLLISION_WALL
        return self.COLLISION_NONE
    
    def update_graphics(self):
        self.graphics = []
        for (x,y) in self.locations:
            self.graphics.append(pygame.Rect(x*self.block_size, y*self.block_size, self.block_size, self.block_size))
    
    def draw(self, surface):
        for rect in self.graphics:
            surface.fill(self.color, rect=rect)
