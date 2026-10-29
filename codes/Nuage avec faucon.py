
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

POSITIONSPREAD = 10000
SPEEDSPREAD = 5
MAXSPEED = 15 #maximum speed of the birds

BORDER = 100 #define the area where the birds sould remain
LEADERBORDER = 200
BORDERSPEEDCHANGE = 0.2 #birds changes their speed when they are too close to the border

MINDIST = 15.0 #minimum distance between two birds

LEADERBIRDRANDOMSPEEDCHANGE = 0.2
LEADERMAXSPEED = 5.0

MINDISTFALCON = 75.0
FALCONRANDOMSPEEDCHANGE = 0.3
FALCONMAXSPEED = 6.0


size = [WIDTH, HEIGHT] #dimensions of the screen
screen = pygame.display.set_mode(size) #create the area where the birds move

birdlist = [] #initial list of birds, will be completed


# Generate leader bird
leaderbirdx = 300.0
leaderbirdy = 300.0
leaderbirdvx = 5.0
leaderbirdvy = 0.0

#Generate falcon
falconx = 400.0
falcony = 400.0
falconvx = 6.5
falconvy = 0.0


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
    #generate the movement of the leader and the falcon
    if (leaderbirdx < LEADERBORDER) : #the leader should remain in the area defined
        leaderbirdvx += BORDERSPEEDCHANGE
    if (leaderbirdy  < LEADERBORDER):
        leaderbirdvy += BORDERSPEEDCHANGE
    if (leaderbirdx > WIDTH - LEADERBORDER):
        leaderbirdvx -= BORDERSPEEDCHANGE
    if (leaderbirdy > HEIGHT - LEADERBORDER):
        leaderbirdvy -= BORDERSPEEDCHANGE
    if (falconx < LEADERBORDER) : 
        falconvx += BORDERSPEEDCHANGE 
    if (falcony < LEADERBORDER) : 
        falconvy += BORDERSPEEDCHANGE 
    if falconx > (WIDTH - LEADERBORDER) : 
        falconvx -= BORDERSPEEDCHANGE 
    if falcony > (HEIGHT - LEADERBORDER) : 
        falconvy -= BORDERSPEEDCHANGE
    
    pygame.draw.circle(screen, (255, 255, 255), (int(leaderbirdx), int(leaderbirdy)), 5, 0)
    #the leader is a white circle of diameter 5, with a defined initial position
    #the argument 0 means that the circle is filled
    leaderbirdvx += random.uniform(-LEADERBIRDRANDOMSPEEDCHANGE, LEADERBIRDRANDOMSPEEDCHANGE)
    leaderbirdvy += random.uniform(-LEADERBIRDRANDOMSPEEDCHANGE, LEADERBIRDRANDOMSPEEDCHANGE)
    
    #Draw falcon and update
    pygame.draw.circle(screen, (97, 97, 97), (int(falconx), int(falcony)), 5, 0)
    gapleaderx = leaderbirdx - falconx
    gapleadery = leaderbirdy - falcony
    falconvx += gapleaderx * 0.008 # the falcon follow the leader
    falconvy += gapleadery * 0.008
    
    # Cap maximum speed
    speed = sqrt(leaderbirdvx*leaderbirdvx + leaderbirdvy*leaderbirdvy) 
    #norm of the leader's speed
    if (speed > LEADERMAXSPEED):
        leaderbirdvx = leaderbirdvx * LEADERMAXSPEED/speed #we reduce the speed by 
        #multiplying it by aa number lower than 1
        leaderbirdvy = leaderbirdvy * LEADERMAXSPEED/speed

    speedf = sqrt(falconvx*falconvx + falconvy*falconvy) #norm of falcon's speed
    if (speed > FALCONMAXSPEED):
        falconvx = falconvx * FALCONMAXSPEED/speedf
        falconvy = falconvy * FALCONMAXSPEED/speedf
    
    leaderbirdx += leaderbirdvx #update the position of the leader
    leaderbirdy += leaderbirdvy

    falconx += falconvx #upate the position of the falcon
    falcony += falconvy
    
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
        indice = 20
        for l in range (NUMBEROFBIRDS) :
            if (l != i) :#we take into account all of birds different from the bird i
                dx = b[l][0] - x
                dy = b[l][1] - y
                dist = sqrt(dx*dx + dy*dy) # distance between the bird i and the bird we study
                for p in range(len(v)) : # we find the bird in the list of neighbours which 
                #is the furthest from the bird i
                    if maximum < v[p][0]:
                        maximum = v[p][0]
                        indice = p
                if dist < maximum : #if the bird studies is closer, we replace it
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
			
        #Escape the falcon
        falcondiffx = falconx - x
        falcondiffy = falcony - y
        distfalcon = sqrt(falcondiffx*falcondiffx + falcondiffy*falcondiffy)
        if (distfalcon < MINDISTFALCON):
            vx -= falcondiffx * 0.4 # ?
            vx *= 0.6
            vy -= falcondiffy * 0.4
            vy *= 0.6
		
		# Cap maximum speed
        speed = sqrt(vx*vx + vy*vy)
        if (speed > MAXSPEED):
            vx = vx * MAXSPEED/speed
            vy = vy * MAXSPEED/speed
			

		# Update positions according to speeds
        birdlist[i][0] += vx
        birdlist[i][1] += vy
        birdlist[i][2] = vx
        birdlist[i][3] = vy
    
    time.sleep(0.002) #let a time between two iterations
    pygame.display.flip()
    
