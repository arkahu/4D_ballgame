# -*- coding: utf-8 -*-
"""
4D Ballgame

Created by: Arttu Huttunen, 2025
License: MIT. Do what you want with this software at your own risk.

Made with Python 3.12.7 and pygame 2.6.1.

The ball is a point in 2D or 3D or 4D space. Paddles are spheres that can bounce
the ball into goals in the end of the fields. Ball and paddle coordinates are
calculated as floats and then displayed approximately in pygame coordinates as 
two dimensional plane projections.

"""

import pygame, math


class Ball():
    def __init__(self, init_speed=4):
        self.start_speed = init_speed
        self.reset()

    def reset(self):
        """Reset ball position and speed. """
        self.x = 300
        self.y = 150
        self.z = 150
        self.w = 150
        
        self.sx = 0
        self.sy = self.start_speed
        self.sz = 0
        self.sw = 0
    
    def move(self):
        self.x += self.sx
        self.y += self.sy
        self.z += self.sz
        self.w += self.sw
        self.wall_check()
        
        #Bounce from walls, field is 600x300x300x300
        if self.x >= 600 or self.x <= 0:
            self.sx = -self.sx
        if self.y >= 300 or self.y <= 0:
            self.sy = -self.sy
        if self.z >= 300 or self.z <= 0:
            self.sz = -self.sz
        if self.w >= 300 or self.w <= 0:
            self.sw = -self.sw
 
    def wall_check(self):   
        """If ball in wall, move to edge. Otherwise the paddles can drive the 
        ball of the field. Sudden warps in ball position can be attributed to
        quantum fluctuations. """
        if self.x >= 600:   self.x = 600
        if self.x <= 0:     self.x = 0
        if self.y >= 300:   self.y = 300
        if self.y <= 0:     self.y = 0
        if self.z >= 300:   self.z = 300
        if self.z <= 0:     self.z = 0
        if self.w >= 300:   self.w = 300
        if self.w <= 0:     self.w = 0
 
    def bounce(self, padx, pady, padz, padw, dist, paddle_radius):
        """Calculate new speed for the ball based on paddle coordinates (padx, pady..)
        and distance the ball is inside the paddle. Speed is calculated by finding the
        surface normal vector at the point of contact, calculating the reclection
        with dot product of of normal vector and speed vector. If ball is inside the
        paddle, move it to the edge."""
        
        dx = self.x - padx
        dy = self.y - pady
        dz = self.z - padz
        dw = self.w - padw
        
        """
        #Reflection vector w of incoming vector v.
        #w=v-2(v*n)n  , * means dot product, n is normal vector.
        #circle center to collision point is in direction of surface normal 'n'
        
        Calculate normal vector (nx,ny,nz). (dx,dy,dz) points in same
        direction as n, from paddle center to point of contact, which is
        ball location. Scale d with circle radius adjusted by distance the 
        ball traveled inside, so that the lenght is 1, so it is unit vector.
        """

        nx = dx / (paddle_radius - dist)
        ny = dy / (paddle_radius - dist)
        nz = dz / (paddle_radius - dist)
        nw = dw / (paddle_radius - dist)
        
        v_dot_n = self.sx*nx + self.sy*ny + self.sz*nz + self.sw*nw
        self.sx = self.sx - 2*v_dot_n*nx
        self.sy = self.sy - 2*v_dot_n*ny
        self.sz = self.sz - 2*v_dot_n*nz
        self.sw = self.sw - 2*v_dot_n*nw
        
        #OPTION A
        #move ball to edge ; a simple hack to keep ball out of paddle        
        self.x += dist*nx
        self.y += dist*ny
        self.z += dist*nz
        self.w += dist*nw
        self.wall_check()
        
        #OPTION B: if ball inside paddle, accerelate towards surface normal
        #m = 0.1        #acceleratin multiplier
        #self.sx = self.sx - m*dist*nx
        #self.sy = self.sy - m*dist*ny


class Paddle():
    def __init__(self, x_start, y_start, z_start, w_start, size, pColor): 
        self.x = x_start 
        self.y = y_start
        self.z = z_start
        self.w = w_start
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
        if direction == 'wp':
            self.w += 1
        if direction == 'wn':
            self.w -= 1
        
        #BORDERS for paddle movement
        if self.x <= -50:
            self.x = -50
        if self.x >= 650:
            self.x = 650
            
        if self.y <= -50:         
            self.y = -50
        if self.y >= 350:
            self.y = 350

        if self.z <= -50:         
            self.z = -50
        if self.z >= 350:
            self.z = 350

        if self.w <= -50:         
            self.w = -50
        if self.w >= 350:
            self.w = 350
    
    def collision(self, ballx, bally, ballz, ballw):
        """Test if paddle collides with ball. Calculate Pythagorean distance 
        from paddle center to ball location. Return distance from paddle edge
        to ball, if positive, ball is inside the paddle. """
        dx = self.x - ballx
        dy = self.y - bally
        dz = self.z - ballz
        dw = self.w - ballw
        d = math.sqrt(math.pow(dx,2) + math.pow(dy, 2) + math.pow(dz,2) + math.pow(dw,2))
        return self.radius - d


#**********************************************

def start_screen(speedx10):
    """Defines the start and setup sceen. """
    
    title_font = pygame.font.SysFont('arial', 60)
    title_surf = title_font.render('4 DIMENSIONAL BALL GAME', False, 'magenta4')
    
    menu_font = pygame.font.SysFont('arial', 30)
    menu_4d_surf = menu_font.render('4D GAME', False, 'black') # mode 0
    menu_3d_surf = menu_font.render('3D GAME', False, 'black') # mode 1
    menu_2d_surf = menu_font.render('2D GAME', False, 'black') # mode 2
    menu_quit_surf = menu_font.render('QUIT', False, 'black')  # mode 3
    
    heading_font = pygame.font.SysFont('arial', 25)
    heading_font.set_underline(True)  
    info_font = pygame.font.SysFont('arial', 25)
    
    heading_surf = heading_font.render('Controls', False, 'black')
    info1_surf = info_font.render('Menu: UP/DOWN, select with ENTER/SPACE', False, 'black')
    info2_surf = info_font.render('           LEFT/RIGHT to change ball speed', False, 'black')
    info3_surf = info_font.render('Player1: w,a,s,d,q,e,r,f', False, 'black')
    info4_surf = info_font.render('Player2: Arrow keys and numpad 4,1,5,2', False, 'black')
    info5_surf = info_font.render('Back to menu: ESC', False, 'black')
    info6_surf = info_font.render('Playing field is 600x300x300x300, (x,y,z,w).', False, 'black')
    info7_surf = info_font.render('Created by: Arttu Huttunen, 2025', False, 'black')
    
    game_mode = 0
    
    running = True
    while running:
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game_mode = 3
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    running = False
                
                if event.key == pygame.K_UP:
                    game_mode -=1
                if event.key ==pygame.K_DOWN:
                    game_mode +=1
                if game_mode < 0:
                    game_mode = 0
                if game_mode > 3:
                    game_mode = 3

                if event.key == pygame.K_RIGHT:
                    speedx10 +=1
                if event.key ==pygame.K_LEFT:
                    speedx10 -=1
                if speedx10 < 0:
                    speedx10 = 0
                
        speed_surf = menu_font.render(f'SPEED: {speedx10/10}', False, 'black')
        
        screen.fill('darkgoldenrod1')
        screen.blit(title_surf,(400,150))
        
        sel_pos = 355 + game_mode*50
        pygame.draw.rect(screen, 'blue', (550, sel_pos, 20,20))
        
        screen.blit(menu_4d_surf, (600,350))
        screen.blit(menu_3d_surf, (600,400))
        screen.blit(menu_2d_surf, (600,450))
        screen.blit(menu_quit_surf, (600,500))
        screen.blit(speed_surf, (600,600))
        
        screen.blit(heading_surf, (1200,340))
        screen.blit(info1_surf, (1100,375))
        screen.blit(info2_surf, (1100,400))
        screen.blit(info3_surf, (1100,425))
        screen.blit(info4_surf, (1100,450))
        screen.blit(info5_surf, (1100,475))
        screen.blit(info6_surf, (1100,500))
        screen.blit(info7_surf, (1100,550))
        
        pygame.display.flip()
    else:
        return game_mode, speedx10


#***********************************************  

def run_game(game_mode, speed, mode_3d, mode_4d):
    """Actual game. In 2D mode, w and z values are locked. In 3D w is locked. """

    back_to_start = False #ESC returns to start menu, closing window shuts down
    
    
    
    ball1 = Ball(speed)
    
    paddle_radius = 40
    #paddle start x,y,z,w; paddle radius, colour
    paddle1 = Paddle(100, 150, 150, 150, paddle_radius, 'red')
    paddle2 = Paddle(500, 150, 150, 150, paddle_radius, 'yellow')
    
    score_font = pygame.font.SysFont('arial', 30)
    P1_points = 0
    P2_points = 0
    
    coord_font = pygame.font.SysFont('arial', 14) #for display of coordinates
    
    #initialize helper variables for displaying
    ball_coord_x = 300
    ball_coord_y = 150
    ball_coord_z = 150
    ball_coord_w = 150

    ball_speed_x = 0
    ball_speed_y = speed
    ball_speed_z = 0
    ball_speed_w = 0

    disp_counter = 0 #for display update rate
    
    #pre-render static dimension labels
    xy_X_surf = coord_font.render('x', False, 'black')
    xy_Y_surf = coord_font.render('y', False, 'black')
    xz_X_surf = coord_font.render('x', False, 'black')
    xz_Z_surf = coord_font.render('z', False, 'black')
    yz_Y_surf = coord_font.render('y', False, 'black')
    yz_Z_surf = coord_font.render('z', False, 'black')
    
    xw_X_surf = coord_font.render('x', False, 'black')
    xw_W_surf = coord_font.render('w', False, 'black')
    yw_Y_surf = coord_font.render('y', False, 'black')
    yw_W_surf = coord_font.render('w', False, 'black')
    zw_Z_surf = coord_font.render('z', False, 'black')
    zw_W_surf = coord_font.render('w', False, 'black')
    
    running = True
    while running:
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            running = False
            back_to_start = True
        
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
        if keys[pygame.K_r]:
            paddle1.move('wp')
        if keys[pygame.K_f]:
            paddle1.move('wn')
        
        if keys[pygame.K_UP]:
            paddle2.move('yp')
        if keys[pygame.K_LEFT]:
            paddle2.move('xn')
        if keys[pygame.K_DOWN]:
            paddle2.move('yn')
        if keys[pygame.K_RIGHT]:
            paddle2.move('xp')
        if keys[pygame.K_KP1]:
            paddle2.move('zn')
        if keys[pygame.K_KP4]:
            paddle2.move('zp')
        if keys[pygame.K_KP2]:
            paddle2.move('wn')
        if keys[pygame.K_KP5]:
            paddle2.move('wp')
    
        ball1.move()

        # In 3D or 2D mode, lock extra coordinates to center.
        if not mode_4d:
            ball1.w, paddle1.w, paddle2.w = 150,150,150        
        if not mode_3d:
            ball1.z, paddle1.z, paddle2.z = 150,150,150
            
        col_dist1 = paddle1.collision(ball1.x, ball1.y, ball1.z, ball1.w) 
        #how deep in paddle is ball, negative means outside
        if col_dist1 >= 0:
            ball1.bounce(paddle1.x, paddle1.y, paddle1.z, paddle1.w, col_dist1, paddle1.radius)
     
        col_dist2 = paddle2.collision(ball1.x, ball1.y, ball1.z, ball1.w)
        if col_dist2 >= 0:
            ball1.bounce(paddle2.x, paddle2.y, paddle2.z, paddle2.w, col_dist2, paddle2.radius)
    
    
        #Transform "normal" game coordinates to pygame coordinates, in pygame top corner is origin

        #plane xy, b=ball, p1=paddle1, p2=paddle2
        #px = nx+50 , "p=pygame, n=normal"; py = max(py) - ny
        xy_bx = 50 + ball1.x
        xy_by = 350 - ball1.y
        xy_p1x = 50 + paddle1.x
        xy_p1y = 350 - paddle1.y
        xy_p2x = 50 + paddle2.x
        xy_p2y = 350 - paddle2.y
    
        xz_bx = 750 + ball1.x
        xz_bz = 350 - ball1.z
        xz_p1x = 750 + paddle1.x
        xz_p1z = 350 - paddle1.z
        xz_p2x = 750 + paddle2.x
        xz_p2z = 350 - paddle2.z
    
        yz_by = 1450 + ball1.y
        yz_bz = 350 - ball1.z
        yz_p1y = 1450 + paddle1.y
        yz_p1z = 350 - paddle1.z
        yz_p2y = 1450 + paddle2.y
        yz_p2z = 350 - paddle2.z
    
        #second row in display
        xw_bx = 50 + ball1.x
        xw_bw = 750 - ball1.w
        xw_p1x = 50 + paddle1.x 
        xw_p1w = 750 - paddle1.w
        xw_p2x = 50 + paddle2.x
        xw_p2w = 750 - paddle2.w
        
        yw_by = 750 + ball1.y
        yw_bw = 750 - ball1.w
        yw_p1y = 750 + paddle1.y
        yw_p1w = 750 - paddle1.w
        yw_p2y = 750 + paddle2.y
        yw_p2w = 750 - paddle2.w
    
        zw_bz = 1450 + ball1.z
        zw_bw = 750 - ball1.w
        zw_p1z = 1450 + paddle1.z
        zw_p1w = 750 - paddle1.w
        zw_p2z = 1450 + paddle2.z
        zw_p2w =  750 - paddle2.w
    
        #check if goal, blink when goal
        if  ball1.x <= 0 and 100 < ball1.y < 200 and 100 < ball1.z < 200 and 100 < ball1.w < 200:
            P2_points += 1
            ball1.reset()
            screen.fill("white")
        elif  ball1.x >= 600 and 100 < ball1.y < 200 and 100 < ball1.z < 200 and 100 < ball1.w < 200:
            P1_points += 1
            ball1.reset()
            screen.fill("white")
        else:
            # fill the screen with a color to wipe away anything from last frame
            screen.fill("grey") 
        
        #update ball coordinate display only part of time to make it readable
        if disp_counter == 10:
            ball_coord_x, ball_coord_y, ball_coord_z, ball_coord_w = int (ball1.x), int (ball1.y), int(ball1.z), int(ball1.w)
            ball_speed_x, ball_speed_y, ball_speed_z, ball_speed_w = ball1.sx, ball1.sy, ball1.sz, ball1.sw
            disp_counter = 0
        else:
            disp_counter +=1
        
        
        #Draw projections
        # XY
        pygame.draw.circle(screen, paddle1.color, (xy_p1x, xy_p1y), paddle1.radius)
        pygame.draw.circle(screen, paddle2.color, (xy_p2x, xy_p2y), paddle2.radius)
        pygame.draw.circle(screen, 'blue' , (xy_bx, xy_by), 3) #ball, size 3 to make it visible
        
        pygame.draw.rect(screen, 'black', (50,50,600,300), width=1) #borders (topcorner x,y, length, width)
        pygame.draw.rect(screen, 'pink', (25,150,25,100))     #goal1
        pygame.draw.rect(screen, 'orange', (650,150,25,100))     #goal2

        if mode_3d:    
            # XZ
            pygame.draw.circle(screen, paddle1.color, (xz_p1x, xz_p1z), paddle1.radius)
            pygame.draw.circle(screen, paddle2.color, (xz_p2x, xz_p2z), paddle2.radius)
            pygame.draw.circle(screen, 'blue', (xz_bx,xz_bz), 3)
        
            pygame.draw.rect(screen, 'black', (750,50,600,300), width=1) #borders
            pygame.draw.rect(screen, 'pink', (725,150,25,100))     #goal1
            pygame.draw.rect(screen, 'orange', (1350,150,25,100))     #goal2
            
            # YZ
            pygame.draw.circle(screen, paddle1.color, (yz_p1y, yz_p1z), paddle1.radius)
            pygame.draw.circle(screen, paddle2.color, (yz_p2y, yz_p2z), paddle2.radius)
            pygame.draw.circle(screen, 'blue', (yz_by, yz_bz), 3)
            
            pygame.draw.rect(screen, 'black', (1450,50,300,300), width=1) #borders
            pygame.draw.rect(screen, 'brown', (1550,150,100,100), width=1)
        
            if mode_4d:
                # XW
                pygame.draw.circle(screen, paddle1.color, (xw_p1x, xw_p1w), paddle1.radius)
                pygame.draw.circle(screen, paddle2.color, (xw_p2x, xw_p2w), paddle2.radius)
                pygame.draw.circle(screen, 'blue' , (xw_bx, xw_bw), 3)
                
                pygame.draw.rect(screen, 'black', (50,450,600,300), width=1) #borders
                pygame.draw.rect(screen, 'pink', (25,550,25,100))     #goal1
                pygame.draw.rect(screen, 'orange', (650,550,25,100))     #goal2
            
                # YW
                pygame.draw.circle(screen, paddle1.color, (yw_p1y, yw_p1w), paddle1.radius)
                pygame.draw.circle(screen, paddle2.color, (yw_p2y, yw_p2w), paddle2.radius)
                pygame.draw.circle(screen, 'blue', (yw_by, yw_bw), 3)
            
                pygame.draw.rect(screen, 'black', (750,450,300,300), width=1)
                pygame.draw.rect(screen, 'brown', (850,550,100,100), width=1)
            
                # ZW
                pygame.draw.circle(screen, paddle1.color, (zw_p1z, zw_p1w), paddle1.radius)
                pygame.draw.circle(screen, paddle2.color, (zw_p2z, zw_p2w), paddle2.radius)
                pygame.draw.circle(screen, 'blue', (zw_bz, zw_bw), 3)
            
                pygame.draw.rect(screen, 'black', (1450,450,300,300), width=1)
                pygame.draw.rect(screen, 'brown', (1550,550,100,100), width=1)   
    
    
        # SCORES
        score_P1_surf = score_font.render(f'P1: {P1_points}', False, 'red')
        score_P2_surf = score_font.render(f'P2: {P2_points}', False, 'yellow')    
        screen.blit(score_P1_surf, (1200,500))
        screen.blit(score_P2_surf, (1200,550))
    
        # COORDINATE DISPLAY
        coord_P1_surf = coord_font.render(f'{paddle1.x}, {paddle1.y}, {paddle1.z}, {paddle1.w}', False, 'red')
        coord_P2_surf = coord_font.render(f'{paddle2.x}, {paddle2.y}, {paddle2.z}, {paddle2.w}', False, 'yellow')  
        coord_ball_surf = coord_font.render(f'{ball_coord_x}, {ball_coord_y}, {ball_coord_z}, {ball_coord_w}', False, 'blue') 
        speed_ball_surf = coord_font.render(f'{ball_speed_x:.2f}, {ball_speed_y:.2f}, {ball_speed_z:.2f}, {ball_speed_w:.2f}', False, 'green') 
        screen.blit(coord_P1_surf, (1200,660))
        screen.blit(coord_P2_surf, (1200,680))
        screen.blit(coord_ball_surf, (1200,700))
        screen.blit(speed_ball_surf, (1200,720))
    
        #dimension labels
        screen.blit(xy_X_surf, (60,350))
        screen.blit(xy_Y_surf, (40,330))
        screen.blit(xz_X_surf, (760,350))
        screen.blit(xz_Z_surf, (740,330))
        screen.blit(yz_Y_surf, (1460,350))
        screen.blit(yz_Z_surf, (1440,330))
    
        screen.blit(xw_X_surf, (60,750))
        screen.blit(xw_W_surf, (40,730))
        screen.blit(yw_Y_surf, (760,750))
        screen.blit(yw_W_surf, (740,730))
        screen.blit(zw_Z_surf, (1460,750))
        screen.blit(zw_W_surf, (1440,730))
    
    
        # flip() the display to put your work on screen
        pygame.display.flip()
        clock.tick(60)  # limits FPS to 60
    
    else:
        return back_to_start


#*********************************************

#Setup and start the game.
pygame.init()
screen = pygame.display.set_mode((1800, 800))
clock = pygame.time.Clock()
pygame.display.set_caption("4D ballgame")

#4d Set 1900x100 screen and 600x300x300x300 field, goal 100x100x100

speedx10 = 40 #ball speed x10 to avoid floats

running = True
while running:
    game_mode, speedx10 = start_screen(speedx10)
    
    if game_mode == 0:
        mode_3d = True
        mode_4d = True
    if game_mode == 1:
        mode_3d = True
        mode_4d = False
    elif game_mode == 2:
        mode_3d = False
        mode_4d = False
    
    if game_mode != 3 : # 3 is quit
        running = run_game(game_mode, speedx10/10, mode_3d, mode_4d)
    else:
        running = False

pygame.quit()
