# -*- coding: utf-8 -*-
"""
2D ballgame, development version of 4D ballgame.

Created by: Arttu Huttunen, 2025
License: MIT. Do what you want with this software at your own risk.

Made with Python 3.12.7 and pygame 2.6.1.
"""

# 2D ball game 1.1
# 2D version
# coordinate display, code cleanup, some tweaks in 1.1

import pygame, math


class Ball():
    def __init__(self):    
        self.reset()

    def reset(self):
        """Initialize position and speed. """
        self.x = 300
        self.y = 150
        self.sx = 0
        self.sy = 4
    
    def move(self):
        self.x += self.sx
        self.y += self.sy
        
        #Bounce from walls
        if self.x >= 600 or self.x <= 0:
            self.sx = -self.sx
        if self.y >= 300 or self.y <= 0:
            self.sy = -self.sy
        
    def bounce(self, padx, pady, dist):
        """Calculate new speed for the ball based on paddle coordinates (padx, pady)
        and distance the ball is inside the paddle. Speed is calculated by finding the
        surface normal vector at the point of contact, calculating the reflection
        with dot product of of normal vector and speed vector. If ball is inside the
        paddle, move it to the edge."""

        dx = self.x - padx
        dy = self.y - pady
        #w=v-2(v*n)n  , * means dot product
        #circle center to collision point is in direction of surface normal 'n'
        x_ang = math.atan2(dy, dx) #angle to x-axis
        #length of n is 1, so cos (x_ang) = nx/1
        nx = math.cos(x_ang) #normal vector
        ny = math.sin(x_ang)
        
        #easier way to calculate normal vector is to divide d with paddle radius
        #because d-vector points from circle center to collision point and has
        #length radius, compensate for ball being 'dist' inside of paddle.
        #nx = dx / (radius + dist)
        #ny = dy / (radius + dist)
        
        v_dot_n = self.sx*nx + self.sy*ny
        self.sx = self.sx - 2*v_dot_n*nx
        self.sy = self.sy - 2*v_dot_n*ny
        
        #move ball to edge ; a simple hack to keep ball out of paddle
        #dist is negative
        self.x += -dist*nx
        self.y += -dist*ny
        #print (math.degrees(x_ang), nx, ny)
        
        #OPTION B: if ball inside paddle, accerelate towards surface normal
        #m = 0.1        #acceleration multiplier
        #self.sx = self.sx - m*dist*nx
        #self.sy = self.sy - m*dist*ny


class Paddle():
    def __init__(self, x_start, y_start, pName, size, pColor): 
        self.x = x_start 
        self.y = y_start
        self.name = pName
        self.radius = size
        self.color = pColor

    def move(self, direction):
        if direction == 'xp':            
            self.x += 1
        if direction == 'xn':            
            self.x -= 1
        if direction == 'yp':            
            self.y += 1
        if direction == 'yn':            
            self.y -= 1               
         
        if self.x <= -100:         #HARD CODED BORDERS
            self.x = -100
        if self.x >= 700:
            self.x = 700
        if self.y <= -100:         
            self.y = -100
        if self.y >= 400:
            self.y = 400

    def collision(self, ballx, bally):
        dx = self.x - ballx
        dy = self.y - bally
        d = math.sqrt(math.pow(dx,2) + math.pow(dy, 2))
        return d - self.radius


#***********************************************  

pygame.init()
screen = pygame.display.set_mode((800, 500))
clock = pygame.time.Clock()
pygame.display.set_caption("2D ball game")

#Set 800x500 screen and 600x300 field

ball1 = Ball()

paddle1 = Paddle(100, 150, 'P1', 40, 'red')
paddle2 = Paddle(500, 150, 'P2', 40, 'yellow')


score_font = pygame.font.SysFont('arial', 30)
P1_points = 0
P2_points = 0

coord_font = pygame.font.SysFont('arial', 14) #for display of coordinates

ball_coord_x = 300
ball_coord_y = 150

counter = 0

running = True
while running:
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        paddle1.move('yp')
    if keys[pygame.K_a]:
        paddle1.move('xn')
    if keys[pygame.K_s]:
        paddle1.move('yn')
    if keys[pygame.K_d]:
        paddle1.move('xp')

    if keys[pygame.K_UP]:
        paddle2.move('yp')
    if keys[pygame.K_LEFT]:
        paddle2.move('xn')
    if keys[pygame.K_DOWN]:
        paddle2.move('yn')
    if keys[pygame.K_RIGHT]:
        paddle2.move('xp')

    ball1.move()
    
    col_dist1 = paddle1.collision(ball1.x, ball1.y) #how deep in paddle is ball
    if col_dist1 <= 0:
        ball1.bounce(paddle1.x, paddle1.y, col_dist1)
 
    col_dist2 = paddle2.collision(ball1.x, ball1.y) #how deep in paddle is ball
    if col_dist2 <= 0:
        ball1.bounce(paddle2.x, paddle2.y, col_dist2)
    

  
    #Transform x,y coordinates to pygame coordinates
    #px = nx+100 , pygame, normal; py = max(py) - ny
    #paddle and ball
    p1x = 100 + paddle1.x
    p1y = 400 - paddle1.y
    p2x = 100 + paddle2.x
    p2y = 400 - paddle2.y
    bx = 100 + ball1.x
    by = 400 - ball1.y

    #check if goal, blink when goal
    if  ball1.x <= 0 and 100 < ball1.y < 200:
        P2_points += 1
        ball1.reset()
        screen.fill("white")
    elif  ball1.x >= 600 and 100 < ball1.y < 200:
        P1_points += 1
        ball1.reset()
        screen.fill("white")
    else:
        # fill the screen with a color to wipe away anything from last frame
        screen.fill("grey") 
    
    #update ball coordinate display only part of time to make it readable
    if counter == 10:
        ball_coord_x, ball_coord_y = int (ball1.x), int (ball1.y)
        counter = 0
    else:
        counter +=1

    pygame.draw.rect(screen, 'black', (100,100,600,300), width=1) #borders
    pygame.draw.rect(screen, 'pink', (0,200,100,100))     #goal1
    pygame.draw.rect(screen, 'orange', (700,200,100,100))     #goal2

    pygame.draw.circle(screen, paddle1.color , (p1x, p1y),paddle1.radius)
    pygame.draw.circle(screen, paddle2.color , (p2x, p2y),paddle2.radius)
    pygame.draw.circle(screen, 'blue' , (bx, by), 3)

    score_P1_surf = score_font.render(f'P1: {P1_points}', False, 'red')
    score_P2_surf = score_font.render(f'P2: {P2_points}', False, 'yellow')    
    screen.blit(score_P1_surf, (250,0))
    screen.blit(score_P2_surf, (450,0))

    coord_P1_surf = coord_font.render(f'{paddle1.x}, {paddle1.y}', False, 'red')
    coord_P2_surf = coord_font.render(f'{paddle2.x}, {paddle2.y}', False, 'yellow')  
    coord_ball_surf = coord_font.render(f'{ball_coord_x}, {ball_coord_y}', False, 'blue') 
    screen.blit(coord_P1_surf, (10,480))
    screen.blit(coord_P2_surf, (720,480))
    screen.blit(coord_ball_surf, (400,480))

    # flip() the display to put your work on screen
    pygame.display.flip()
    clock.tick(60)  # limits FPS to 60

pygame.quit()