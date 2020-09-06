import numpy as np
import pygame 

pygame.init()
win = pygame.display.set_mode((600,600))
pygame.display.set_caption("Sudoku")
img_board = pygame.image.load('sudoku_board.png')
font = pygame.font.SysFont("colibri", 72)   
run = True

class tile:
    def __init__(self,x,y,block):
        self.val = 0
        self.x = x
        self.y = y
        self.block = block
        self.av = []
        self.core = True

    def draw(self,win):
        text = font.render(str(self.val), True, (0, 0, 0))
        win.blit(text,
        (self.x*67 + 32 - text.get_width() // 2, self.y*67+32 - text.get_height() // 2))

    def __repr__(self):
        st = 'tile:(x='+str(self.x)+', y='+str(self.y)+', b='+str(self.block)+', val='+str(self.val) + ')'
        return st

def update_av(grid,n,x,y):
    for t in grid:
        if t.x == x or t.y == y:
            if n not in t.av:
                t.av.append(n)

def printg(grid):
    st = ''
    for t in grid:
        st += str(t.val) + ' '
        if t.y in [2,5]:
            st += '| '
        if t.y == 8:
            if t.x in [3,6]:
                print('---------------------')
            print(st)
            st = ''

def build():
    #build grid of 0s
    grid = []
    blocks = [[],[],[],[],[],[],[],[],[]]
    for i in range(0,9): 
        for j in range(0,9): 
            block = (i//3)*3+(j//3)
            t = tile(i,j,block)
            grid.append(t)
            blocks[block].append(t)

    #shuffling tiles in blocks
    for block in blocks:
        np.random.shuffle(block)

    #filling diagonal blocks
    for block in [blocks[0],blocks[4],blocks[8]]:
        n=1
        for t in block:
            t.val = n
            update_av(grid,n,t.x,t.y)
            n += 1

    for i in [1,2,3,5,6,7]:
        block = blocks[i]
        for n in range(1,10):
            for t in block:
                if n not in t.av and t.val == 0:
                    t.val = n
                    update_av(grid,n,t.x,t.y)
                    break
            if t.val == 0:
                # t.val=99
                return grid
    return grid

def test(grid):
    for t in grid:
        if t.val==0:
            return False
    return True

def get_grid(k):
    correct_grid = False
    while not correct_grid:
        grid = build()
        correct_grid = test(grid)

    gridk = grid[:]
    np.random.shuffle(gridk)
    for t in range(0,k):
        gridk[t].val=' '
    return grid

def redrawGameWindow(grid):
    win.blit(img_board, (0,0))
    for t in grid:
        t.draw(win)
    pygame.display.update()

grid = np.load("grid.npy",allow_pickle=True)

while run:
    pygame.time.Clock().tick(60)

    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or keys[pygame.K_t]:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.mouse.get_pos()

    redrawGameWindow(grid)
pygame.quit()