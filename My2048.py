import pygame
import pygame as pg
import sys,time  
import random  
from pygame.locals import * 
from random import randrange, choice 
from collections import defaultdict
SIZE=4      
COLORS=[(255,255,255),(135,220,32),(32,220,55),(220,180,32),(220,32,72),(32,135,220),(180,32,220),(220,32,197),(243,171,186),(165,24,54),(0xa2,0xcd,0x5a),(0x98,0xFB,0x98),(106, 90, 205)]
BLOCK_LEN=130

class Qipan:
    def __init__(self,size):
        self.size=size
        self.map=[[0 for i in range(self.size)] for j in range(self.size)]  
        self.is_move=False           
        self.score=0
        self.high_score=0
        self.spawn()
        self.spawn()
        
    def transpose(self):
        self.map=[list(row) for row in zip(*self.map)]
    def invert(self):
        self.map=[row[::-1] for row in self.map]        

    def spawn(self):
        new_element = 4 if randrange(100) > 89 else 2
        i,j = choice([(i,j) for i in range(self.size) for j in range(self.size) if self.map[i][j] == 0])
        self.map[i][j] = new_element

    def reset(self):
        if self.score > self.high_score:
            self.high_score = self.score
        self.score = 0
        self.is_move=False
        self.map=[[0 for i in range(self.size)] for j in range(self.size)]
        self.spawn()
        self.spawn()
        
    def move_to_left(self):
        new_map=[]
        for row in self.map:
            new_row=[]
            linshi=0
            for val in row:
                if val!=0:
                    if linshi!=val:
                        new_row.append(val)
                        linshi=val
                    else:
                        v_x=new_row.pop() * 2
                        new_row.append(v_x)    
                        self.score+=v_x
                        linshi=0 
            new_row+=[0]*(len(row)-len(new_row))
            if not row==new_row:
                self.is_move=True
            new_map.append(new_row)
        self.map=new_map
    
    def move_left(self):
        self.move_to_left()
        if self.is_move:
            self.spawn()
    def move_right(self):
        self.invert()
        self.move_to_left()
        if self.is_move:
            self.spawn()
        self.invert()
    def move_up(self):
        self.transpose()
        self.move_to_left()
        if self.is_move:
            self.spawn()
        self.transpose()
    def move_down(self):
        self.transpose()
        self.invert()
        self.move_to_left()
        if self.is_move:
            self.spawn()
        self.invert()
        self.transpose()
        
    def game_over(self):  
        for i in self.map:  
            for j in i:  
                if j==0:  
                    return False  
        for i in range(0,self.size):  
            for j in range(0,self.size):
                if i-1>=0 and self.map[i][j]==self.map[i-1][j] or j-1>=0 and self.map[i][j]==self.map[i][j-1] or i+1<self.size and self.map[i][j]==self.map[i+1][j] or j+1<self.size and self.map[i][j]==self.map[i][j+1]:  
                    return False  
        return True  
    
def getColor(n):  
    hh = 0  
    for i in range(1,12):  
        if n==0:
            return (255,255,255)
        if n/2 ==1:  
            hh = i 
        n=n/2
    return COLORS[hh]

def display(qipan,screen):
    qi_font=pg.font.Font(None,70)
    score_font=pg.font.Font(None,70)
    high_score_font=pg.font.Font(None,70)
    introduce_font=pg.font.Font(None,70)
    introduce2_font=pg.font.Font(None,50)
    screen.fill((255,255,255))
    for i in range(qipan.size):
        for j in range(qipan.size):
            block=pg.Surface((BLOCK_LEN,BLOCK_LEN))
            block.fill(getColor(qipan.map[i][j]))
            if qipan.map[i][j]!=0:
                font_surf = qi_font.render(str(qipan.map[i][j]),True,(0,0,0)) 
            else:
                font_surf = qi_font.render('',True,(106, 90, 205))
            sur_rect = font_surf.get_rect()
            sur_rect.center = (j*BLOCK_LEN+BLOCK_LEN/2,BLOCK_LEN*i+BLOCK_LEN/2)
            screen.blit(block,(j*BLOCK_LEN,i*BLOCK_LEN))                         
            screen.blit(font_surf,sur_rect)
    score_sur = score_font.render('score: '+str(qipan.score),True,(106, 90, 205))
    score_rect = score_sur.get_rect()
    score_rect.center = (BLOCK_LEN*qipan.size/2,BLOCK_LEN*qipan.size+35)
    screen.blit(score_sur,score_rect)
    high_score_sur = high_score_font.render('highest score: '+str(qipan.high_score),True,(106, 90, 205))
    score_rect = high_score_sur.get_rect()
    score_rect.center = (BLOCK_LEN*qipan.size/2,BLOCK_LEN*qipan.size+105)
    screen.blit(high_score_sur,score_rect)
    introduce_sur = introduce_font.render('Welcome to 2048',True,(106, 90, 205))
    introduce_rect = introduce_sur.get_rect()
    introduce_rect.center = (BLOCK_LEN*qipan.size/2,BLOCK_LEN*qipan.size+175)
    screen.blit(introduce_sur,introduce_rect)
    introduce2_sur = introduce2_font.render('W,Up  A,Left  S,Down  D,Right',True,(106, 90, 205))
    introduce2_rect = introduce2_sur.get_rect()
    introduce2_rect.center = (BLOCK_LEN*qipan.size/2,BLOCK_LEN*qipan.size+245)
    screen.blit(introduce2_sur,introduce2_rect)
    pygame.display.update()
def main():
    pg.init()
    qipan=Qipan(4)
    screen=pg.display.set_mode((BLOCK_LEN*qipan.size,800))
    screen.fill((255,255,255))
    pg.display.set_caption("2048")
    clock=pg.time.Clock()
    while True:
        while not qipan.game_over():
            keys = pygame.key.get_pressed()
            for event in pg.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            qipan.is_move=False
            if event.type == pygame.KEYUP:
                if keys[K_UP] or keys[K_w]:
                    qipan.move_up()
                elif keys[K_DOWN]or keys[K_s]:
                    qipan.move_down()
                elif keys[K_RIGHT]or keys[K_d]:
                    qipan.move_right()
                elif keys[K_LEFT]or keys[K_a]:
                    qipan.move_left()
            display(qipan,screen)
            if qipan.is_move==1:
                if qipan.high_score<qipan.score:
                    qipan.high_score=qipan.score
            time.sleep(0.05)
        result = "You Failed"
        screen.fill((255,255,255))
        map1_font = pygame.font.SysFont("arial",100)
        font_surf = map1_font.render(result,True,(255,0,0))
        font_rect = font_surf.get_rect()
        font_rect.center = (BLOCK_LEN*qipan.size/2,250) 
        screen.blit(font_surf,font_rect)
        map2_font = pygame.font.SysFont("arial",50)
        font_surf2 = map2_font.render('your score: '+str(qipan.score),True,(0,255,255))
        font_rect2 = font_surf2.get_rect()
        font_rect2.center = (BLOCK_LEN*qipan.size/2,340) 
        screen.blit(font_surf2,font_rect2)
        map3_font = pygame.font.SysFont("arial",50)
        font_surf3 = map3_font.render('highest score: '+str(qipan.high_score),True,(0,255,0))
        font_rect3 = font_surf3.get_rect()
        font_rect3.center = (BLOCK_LEN*qipan.size/2,420) 
        screen.blit(font_surf3,font_rect3)
        map4_font = pygame.font.SysFont("arial",60)
        font_surf4 = map4_font.render('Press any key to restart',True,(255,255,0))
        font_rect4 = font_surf4.get_rect()
        font_rect4.center = (BLOCK_LEN*qipan.size/2,500) 
        screen.blit(font_surf4,font_rect4)
        pg.display.update()
        reset=False
        clock.tick(5)  
        for event in pygame.event.get():    
            if event.type == QUIT:                 
                pygame.quit()  
                sys.exit() 
            if event.type == pygame.KEYUP:
                qipan.reset()
                break
        pygame.display.update()
main()