# -*- coding: utf-8 -*-
"""
Created 2018

"""

import pygame, time, random
from pygame.locals import *
pygame.init()
from math import sqrt

# set the width and height of the screen
WIDTH = 1000 #dimension of the area in which the birds move
HEIGHT = 1000

#center of the screen
CENTREX = WIDTH / 2
CENTREY = HEIGHT / 2

NUMBEROFBIRDS = 150 #number of birds we want in the flock
Number_of_neighbours = 7 #number of neighbours followed by each birds

# positions of the trees
barriers = [[50, 50], [50, 850], [100, 100], [450, 50], [450, 850], [500, 200], [550, 950], [600, 100], [600, 700], [650, 50], [650, 150], [700, 300], [800, 500], [850, 150], [850, 850], [900, 100], [950, 950]]
BARRIERRADIUS = 25

POSITIONSPREAD = 10000 
SPEEDSPREAD = 5 
MAXSPEED = 15 #maximum speed of the birds

BORDER = 100 #define the area where the birds sould remain
LEADERBORDER = 200 
BORDERSPEEDCHANGE = 0.2 #birds changes their speed when they are too close to 
#the border

MINDIST = 15.0 #minimum distance between two birds


LEADERBIRDRANDOMSPEEDCHANGE = 0.2 
LEADERMAXSPEED = 5.0 #maximum speed of the leader


size = [WIDTH, HEIGHT] #dimensions of the screen
screen = pygame.display.set_mode(size) #create the area where the birds move

birdlist = [] #initial list of birds, will be completed

# Generate leader bird, initial position and speed
leaderbirdx = 300.0
leaderbirdy = 300.0
leaderbirdvx = 5.0
leaderbirdvy = 0.0



# Generate birds
for i in range(NUMBEROFBIRDS): 
	x = random.uniform(CENTREX - POSITIONSPREAD, CENTREX + POSITIONSPREAD)
	y = random.uniform(CENTREY - POSITIONSPREAD, CENTREY + POSITIONSPREAD)
	vx = random.uniform(-SPEEDSPREAD, SPEEDSPREAD)
	vy = random.uniform(-SPEEDSPREAD, SPEEDSPREAD)
	
	newbird = [x, y, vx, vy]

	birdlist.append(newbird)
 # each bird is defined by 4 characteristics

for m in range(10000): #number of iterations
    screen.fill((118, 190, 228)) #the screen filled with the colour of the sky
    #generate the movement of the leader
    if (leaderbirdx < LEADERBORDER) : #the leader should remain in the area defined
        leaderbirdvx += BORDERSPEEDCHANGE
    if (leaderbirdy  < LEADERBORDER):
        leaderbirdvy += BORDERSPEEDCHANGE
    if (leaderbirdx > WIDTH - LEADERBORDER):
        leaderbirdvx -= BORDERSPEEDCHANGE
    if (leaderbirdy > HEIGHT - LEADERBORDER):
        leaderbirdvy -= BORDERSPEEDCHANGE
     
    #we draw the leader 
    pygame.draw.circle(screen, (255, 255, 255), (int(leaderbirdx), int(leaderbirdy)), 5, 0) 
    #the leader is a white circle of diameter 5, with a defined initial position
    #the argument 0 means that the circle is filled
    leaderbirdvx += random.uniform(-LEADERBIRDRANDOMSPEEDCHANGE, LEADERBIRDRANDOMSPEEDCHANGE) 
    #random move of the leader
    leaderbirdvy += random.uniform(-LEADERBIRDRANDOMSPEEDCHANGE, LEADERBIRDRANDOMSPEEDCHANGE)
   
    # Cap maximum speed
    speed = sqrt(leaderbirdvx*leaderbirdvx + leaderbirdvy*leaderbirdvy) 
    #norm of the leader's speed
    if (speed > LEADERMAXSPEED): 
        leaderbirdvx = leaderbirdvx * LEADERMAXSPEED/speed #we reduce the speed by 
        #multiplying it by aa number lower than 1
        leaderbirdvy = leaderbirdvy * LEADERMAXSPEED/speed

    
    leaderbirdx += leaderbirdvx #update the position of the leader
    leaderbirdy += leaderbirdvy 

    # Draw birds, positions and speeds 
    for i in range(NUMBEROFBIRDS):
        # Make copies for clarity
        x = birdlist[i][0]
        y = birdlist[i][1]
        vx = birdlist[i][2]
        vy = birdlist[i][3]  
        
        colr = int(float(i) * 200.0/NUMBEROFBIRDS) #define the birds' coulours, 
        #choosen for having shades of brown
        colg = int((NUMBEROFBIRDS-float(i)) * 90.0/NUMBEROFBIRDS)
        colb = 0
        
		#we draw the birds
        pygame.draw.circle(screen, (colr,colg,colb), (int(x), int(y)), 2, 0) 
        # Birds move away from border
        if (x < BORDER):
            vx += BORDERSPEEDCHANGE
        if (y < BORDER):
            vy += BORDERSPEEDCHANGE
        if (x > WIDTH - BORDER):
            vx -= BORDERSPEEDCHANGE
        if (y > HEIGHT - BORDER):
            vy -= BORDERSPEEDCHANGE 

        #Determination of the neighbourhood and cohesion property   
        v = [[1000, 100, 100] for k in range(Number_of_neighbours)]
        # list of neighbours, [distance to the bird i, x of the neighbour, y of the neighbour]
        #len(v) is the number of birds we want to follow
        isobarx = 0 #barycenter of x
        isobary = 0 #barycenter of y
        b = birdlist 	
        maximum = 0
        indice = 0
        for l in range (NUMBEROFBIRDS) :
            if (l != i) : #we take into account all of birds different from the bird i
                dx = b[l][0] - x 
                dy = b[l][1] - y 
                dist = sqrt(dx*dx + dy*dy) # distance between the bird i and the bird we study
                for p in range(len(v)) : # we find the bird in the list of neighbours which 
                #is the furthest from the bird i
                    if maximum < v[p][0]:
                        maximum = v[p][0]
                        indice = p 
                if dist < maximum :#if the bird studies is closer, we replace it
                        v[indice][1] = b[l][0]
                        v[indice][2] = b[l][1]
                        v[indice][0] = dist 
        for l in range (len(v)) : 
            if v[l][0] < 200 : #we don't take into account the birds which are to far from 
            #the bird i, even if we should follow fewer birds than expected
                isobarx = (isobarx + v[l][1])/(l+1) #we calculate the barycenter in x
                isobary = (isobary + v[l][2])/(l+1) #we calculate the barycenter in y 
        vx += 0.02*(isobarx-x) 
        vy += 0.02*(isobary-y)
        
        #alignment property
        v = [[1000,100,100,100,100] for i in range (Number_of_neighbours)]        
        # list of neighbours, [distance to the bird i, x of the neighbour, 
        #y of the neighbour, len(v) is the number of birds we want to follow
        isobarvx = 0
        isobarvy = 0
        b = birdlist
        maximum = 0
        indice = 0
        for l in range (NUMBEROFBIRDS) :
            if (l != i) : 
                dvx = b[l][2] - vx
                dvy = b[l][3] - vy
                dist = sqrt(dvx*dvx + dvy*dvy)
                for p in range(len(v)) :
                    if maximum < v[p][0]:
                        maximum = v[p][0]
                        indice = p
                if dist < maximum : 
                        v[indice][1] = b[l][0]
                        v[indice][2] = b[l][1]
                        v[indice][0] = dist
                        v[indice][3] = b[l][2]
                        v[indice][4] = b[l][3]
        for l in range (len(v)) : 
            if v[l][0] < 200 : 
                isobarvx = (isobarvx + v[l][3])/(l+1)
                isobarvy = (isobarvy + v[l][4])/(l+1)
        vx += 0.02*(isobarvx-vx)
        vy += 0.02*(isobarvy-vy)        
        

		 # Birds move towards leader bird
        leaderdiffx = leaderbirdx - x  
        leaderdiffy = leaderbirdy - y  
        vx += 0.01 * leaderdiffx  
        vy += 0.01 * leaderdiffy


        #Stay away from other birds, separation property 
        for j in range(NUMBEROFBIRDS):
            if (j != i): 
                dx = birdlist[j][0] - x 
                dy = birdlist[j][1] - y 
                dist = sqrt(dx*dx + dy*dy)  
            if (dist < MINDIST): #two birds should not be too close
                vx -= dx * 0.2  
                vy -= dy * 0.2  
                
            
        for barrier in barriers: # barrier is a list with the positions in x and y of 
        #the obstacle
            dx = barrier[0]-x
            dy = barrier[1]-y
            dist = sqrt(dx*dx + dy*dy)
            if (dist < BARRIERRADIUS + 15): #the birds can't be too close to the obstacle ; 
            #the choice of 15 is arbitrary
                vx -= dx * 0.5
                vx *= 0.6
                vy -= dy * 0.5 
                vy *= 0.6
		
		
		# Cap maximum speed, to limit the birds speed
        speed = sqrt(vx*vx + vy*vy)
        if (speed > MAXSPEED):
            vx = vx * MAXSPEED/speed 
            vy = vy * MAXSPEED/speed
			

		# Update positions according to speeds 
        birdlist[i][0] += vx 
        birdlist[i][1] += vy
        birdlist[i][2] = vx
        birdlist[i][3] = vy
    
    #we draw the obstacles
    for barrier in barriers:
        pygame.draw.circle(screen, (0,155,0), (int(barrier[0]), int(barrier[1])), BARRIERRADIUS, 0)

    time.sleep(0.002) #let a time between two iterations
    pygame.display.flip()

