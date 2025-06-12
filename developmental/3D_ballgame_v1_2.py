# -*- coding: utf-8 -*-
"""
3D ballgame, development version of 4D ballgame.

Created by: Arttu Huttunen, 2025
License: MIT. Do what you want with this software at your own risk.

Made with Python 3.12.7 and pygame 2.6.1.
"""

# 3D version 2. READY.

# new drawing order, paddles back. v1.1 messed up

import pygame, math


class Ball():
    def __init__(self):   
        self.reset()

    def reset(self):
        """Initialize position and speed. """
        self.x = 300
        self.y = 150
        self.z = 150
        self.sx = 0
        self.sy = 4
        self.sz = 0
    
    def move(self):
        self.x += self.sx
        self.y += self.sy
        self.z += self.sz
        
        #Bounce from walls
        if self.x >= 600 or self.x <= 0:
            self.sx = -self.sx
        if self.y >= 300 or self.y <= 0:
            self.sy = -self.sy
        if self.z >= 300 or self.z <= 0:
            self.sz = -self.sz
        
    def bounce(self, padx, pady, padz, dist, paddle_radius):
        """Calculate new speed for the ball based on paddle coordinates (padx, pady)
        and distance the ball is inside the paddle. Speed is calculated by finding the
        surface normal vector at the point of contact, calculating the reclection
        with dot product of of normal vector and speed vector. If ball is inside the
        paddle, move it to the edge."""
        
        dx = self.x - padx
        dy = self.y - pady
        dz = self.z - padz
        #w=v-2(v*n)n  , * means dot product
        #circle center to collision point is in direction of surface normal 'n'
        
        # Calculate normal vector (nx,ny,nz), (dx,dy,dz) points from in same
        # direction as n, from paddle center to point of contact. Scale d with
        # circle radius adjusted by distance the ball traveled inside, so that
        # the lenght is 1, so it is unit vector.
        #dist is negative
        nx = dx / (paddle_radius + dist)
        ny = dy / (paddle_radius + dist)
        nz = dz / (paddle_radius + dist)
        
        v_dot_n = self.sx*nx + self.sy*ny + self.sz*nz
        self.sx = self.sx - 2*v_dot_n*nx
        self.sy = self.sy - 2*v_dot_n*ny
        self.sz = self.sz - 2*v_dot_n*nz
        
        #OPTION A
        #move ball to edge ; a simple hack to keep ball out of paddle        
        self.x += -dist*nx
        self.y += -dist*ny
        self.z += -dist*nz
        #print (math.degrees(x_ang), nx, ny)
        
        #OPTION B: if ball inside paddle, accerelate towards surface normal
        #m = 0.1        #acceleratin multiplier
        #self.sx = self.sx - m*dist*nx
        #self.sy = self.sy - m*dist*ny



class Paddle():
    def __init__(self, x_start, y_start, z_start, pName, size, pColor): 
        self.x = x_start 
        self.y = y_start
        self.z = z_start
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
        if direction == 'zp':            
            self.z += 1
        if direction == 'zn':            
            self.z -= 1          
         
        if self.x <= -100:         #HARD CODED BORDERS
            self.x = -100
        if self.x >= 700:
            self.x = 700
            
        if self.y <= -100:         
            self.y = -100
        if self.y >= 400:
            self.y = 400

        if self.z <= -100:         
            self.z = -100
        if self.z >= 400:
            self.z = 400

    def collision(self, ballx, bally, ballz):
        dx = self.x - ballx
        dy = self.y - bally
        dz = self.z - ballz
        d = math.sqrt(math.pow(dx,2) + math.pow(dy, 2) + math.pow(dz,2))
        return d - self.radius


#***********************************************  

pygame.init()
screen = pygame.display.set_mode((1900, 500))
clock = pygame.time.Clock()
pygame.display.set_caption("3D ball game")

#Set 800x500 screen and 600x300 field
#Set 1900x500 screen and 600x300x300 field, goal 100x100

ball1 = Ball()

#paddle start x,y,z; player id, paddle radius, colour
paddle1 = Paddle(100, 150, 150, 'P1', 40, 'red')
paddle2 = Paddle(500, 150, 150, 'P2', 40, 'yellow')

score_font = pygame.font.SysFont('arial', 30)
P1_points = 0
P2_points = 0

coord_font = pygame.font.SysFont('arial', 14) #for display of coordinates

ball_coord_x = 300
ball_coord_y = 150
ball_coord_z = 150

counter = 0

#pre-render static dimension labels
xy_X_surf = coord_font.render('x', False, 'black')
xy_Y_surf = coord_font.render('y', False, 'black')
xz_X_surf = coord_font.render('x', False, 'black')
xz_Z_surf = coord_font.render('z', False, 'black')
yz_Y_surf = coord_font.render('y', False, 'black')
yz_Z_surf = coord_font.render('z', False, 'black')

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
    if keys[pygame.K_q]:
        paddle1.move('zp')
    if keys[pygame.K_e]:
        paddle1.move('zn')
   
    if keys[pygame.K_UP]:
        paddle2.move('yp')
    if keys[pygame.K_LEFT]:
        paddle2.move('xn')
    if keys[pygame.K_DOWN]:
        paddle2.move('yn')
    if keys[pygame.K_RIGHT]:
        paddle2.move('xp')
    if keys[pygame.K_KP0]:
        paddle2.move('zn')
    if keys[pygame.K_KP1]:
        paddle2.move('zp')

    ball1.move()
    
    col_dist1 = paddle1.collision(ball1.x, ball1.y, ball1.z) #how deep in paddle is ball
    #print (col_dist1)
    if col_dist1 <= 0:
        ball1.bounce(paddle1.x, paddle1.y, paddle1.z, col_dist1, paddle1.radius)
        #print (col_dist1)
 
    col_dist2 = paddle2.collision(ball1.x, ball1.y, ball1.z) #how deep in paddle is ball
    if col_dist2 <= 0:
        ball1.bounce(paddle2.x, paddle2.y, paddle2.z, col_dist2, paddle2.radius)

    #Transform x,y coordinates to pygame coordinates
    #px = nx+100 , pygame, normal; py = max(py) - ny
    #paddle and ball
    xy_bx = 100 + ball1.x
    xy_by = 400 - ball1.y
    xy_p1x = 100 + paddle1.x
    xy_p1y = 400 - paddle1.y
    xy_p2x = 100 + paddle2.x
    xy_p2y = 400 - paddle2.y


    xz_bx = 800 + ball1.x
    xz_bz = 400 - ball1.z
    xz_p1x = 800 + paddle1.x
    xz_p1z = 400 - paddle1.z
    xz_p2x = 800 + paddle2.x
    xz_p2z = 400 - paddle2.z

    yz_by = 1500 + ball1.y
    yz_bz = 400 - ball1.z
    yz_p1y = 1500 + paddle1.y
    yz_p1z = 400 - paddle1.z
    yz_p2y = 1500 + paddle2.y
    yz_p2z = 400 - paddle2.z

    #check if goal, blink when goal
    if  ball1.x <= 0 and 100 < ball1.y < 200 and 100 < ball1.z < 200:
        P2_points += 1
        ball1.reset()
        screen.fill("white")
    elif  ball1.x >= 600 and 100 < ball1.y < 200 and 100 < ball1.z < 200:
        P1_points += 1
        ball1.reset()
        screen.fill("white")
    else:
        # fill the screen with a color to wipe away anything from last frame
        screen.fill("grey") 
    
    #update ball coordinate display only part of time to make it readable
    if counter == 10:
        ball_coord_x, ball_coord_y, ball_coord_z = int (ball1.x), int (ball1.y), int(ball1.z)
        counter = 0
    else:
        counter +=1
    
    # XY
    pygame.draw.circle(screen, paddle1.color, (xy_p1x, xy_p1y), paddle1.radius)
    pygame.draw.circle(screen, paddle2.color, (xy_p2x, xy_p2y), paddle2.radius)
    pygame.draw.circle(screen, 'blue' , (xy_bx, xy_by), 3)
    
    pygame.draw.rect(screen, 'black', (100,100,600,300), width=1) #borders
    pygame.draw.rect(screen, 'pink', (75,200,25,100))     #goal1
    pygame.draw.rect(screen, 'orange', (700,200,25,100))     #goal2

    # XZ
    pygame.draw.circle(screen, paddle1.color, (xz_p1x, xz_p1z), paddle1.radius)
    pygame.draw.circle(screen, paddle2.color, (xz_p2x, xz_p2z), paddle2.radius)
    pygame.draw.circle(screen, 'blue', (xz_bx,xz_bz), 3)

    pygame.draw.rect(screen, 'black', (800,100,600,300), width=1) #borders
    pygame.draw.rect(screen, 'pink', (775,200,25,100))     #goal1
    pygame.draw.rect(screen, 'orange', (1400,200,25,100))     #goal2
    
    # YZ
    pygame.draw.circle(screen, paddle1.color, (yz_p1y,yz_p1z), paddle1.radius)
    pygame.draw.circle(screen, paddle2.color, (yz_p2y, yz_p2z), paddle2.radius)
    pygame.draw.circle(screen, 'blue', (yz_by, yz_bz), 3)
    
    pygame.draw.rect(screen, 'black', (1500,100,300,300), width=1) #borders
    #pygame.draw.rect(screen, 'pink', (1475,200,25,100))     #goal1
    #pygame.draw.rect(screen, 'orange', (1800,200,25,100))     #goal2
    pygame.draw.rect(screen, 'brown', (1600,200,100,100), width=1)


    # SCORES
    score_P1_surf = score_font.render(f'P1: {P1_points}', False, 'red')
    score_P2_surf = score_font.render(f'P2: {P2_points}', False, 'yellow')    
    screen.blit(score_P1_surf, (250,0))
    screen.blit(score_P2_surf, (450,0))

    # COORDINATES
    coord_P1_surf = coord_font.render(f'{paddle1.x}, {paddle1.y}, {paddle1.z}', False, 'red')
    coord_P2_surf = coord_font.render(f'{paddle2.x}, {paddle2.y}, {paddle2.z}', False, 'yellow')  
    coord_ball_surf = coord_font.render(f'{ball_coord_x}, {ball_coord_y}, {ball_coord_z}', False, 'blue') 
    screen.blit(coord_P1_surf, (10,480))
    screen.blit(coord_P2_surf, (720,480))
    screen.blit(coord_ball_surf, (400,480))

    #dimension labels
    screen.blit(xy_X_surf, (120,80))
    screen.blit(xy_Y_surf, (80,120))
    screen.blit(xz_X_surf, (820,80))
    screen.blit(xz_Z_surf, (780,120))
    screen.blit(yz_Y_surf, (1520,80))
    screen.blit(yz_Z_surf, (1480,120))

    # flip() the display to put your work on screen
    pygame.display.flip()
    clock.tick(60)  # limits FPS to 60

pygame.quit()