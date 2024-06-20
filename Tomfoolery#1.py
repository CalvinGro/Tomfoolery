import pygame
import random
import math

#initializing game
pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption('Bouncing')
gameActive = True
gravity = 0.4
Xvelocity = 0
Yvelocity = 0
#colors
BLUE = (65,150,245)
WHITE = (255,255,255)
CLEAR = (0,0,0,0)
BLACK = (0,0,0)

borderWidth = 5
class circleSprite(pygame.sprite.Sprite):
    #constructer for circles
    def __init__(self, color, radius, position, hollow):
        super().__init__()
        self.image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA)
        if hollow:
            pygame.draw.circle(self.image,color,(radius, radius), radius, borderWidth)
        else:
            pygame.draw.circle(self.image,color,(radius, radius), radius)
        self.rect = self.image.get_rect(center = position)
        self.radius = radius

#returns an array of all points around the circle
def getEdgePoints(center, radius, step=0.03):
    x_center, y_center = center
    points = []
    theta = 0
    while theta <= 2 * math.pi:
        x = radius * math.cos(theta)
        y = radius * math.sin(theta)
        points.append((round(x_center + x, 1), round(y_center + y, 1)))
        theta += step
    
    return points

def calcHypotenuse(pt1, pt2):

    lenY = abs(pt1[1] - pt2[1])
    lenX = abs(pt1[0] - pt2[0])
    hypt = math.sqrt(lenX**2 + lenY**2)
    return hypt

def angleBetweenLines(pt1, pt2, pt3, pt4):
    # Calculate the slopes of the lines formed by the pairs of points
    #line 1 pt1-2
    #line 2 pt3-4
    print(pt1,pt2,pt3,pt4)
    if pt1[0] != pt2[0] and pt1[1] != pt2[1]:
        slope1 = (pt1[1] - pt2[1]) / (pt1[0] - pt2[0])
    else: slope1 = 0


    if pt3[0] != pt4[0] and pt3[1] != pt4[1]:
        slope2 = (pt3[1] - pt4[1]) / (pt3[0] - pt4[0])
    else: slope2 = 0
    
    # Calculate the angle between the lines using arctan formula
    angleRadians = math.atan(abs((slope2 - slope1) / (1 + slope1 * slope2)))
    angleDegrees = math.degrees(angleRadians)
    
    return angleDegrees

center = (300, 300)
perimeterRadius = 200
ballRadius = 15
inboundsRadius = perimeterRadius - (ballRadius * 2) - borderWidth
lowestRand = center[0] - (inboundsRadius * math.sqrt(2))/2
highestRand = center[0] + (inboundsRadius * math.sqrt(2))/2
randomPosition = (random.uniform(lowestRand,highestRand), random.uniform(lowestRand,highestRand))

perimeterSprite = circleSprite(BLACK,perimeterRadius,center,True)
ballSprite = circleSprite(BLUE,ballRadius,randomPosition,False)
allSprites = pygame.sprite.Group(perimeterSprite, ballSprite)
edgePoints = getEdgePoints(center, perimeterRadius)
edgeCircles = pygame.sprite.Group()
for point in edgePoints:
    circleSprite(BLACK,1,point,False)
    edgeCircles.add(circleSprite(BLACK,1,point,False))

clock = pygame.time.Clock()

while gameActive:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
    screen.fill(WHITE)
    previousPt = (ballSprite.rect.center)
    ballSprite.rect.y += Yvelocity
    ballSprite.rect.x += Xvelocity
    
    #collision detection
    if pygame.sprite.spritecollideany(ballSprite, edgeCircles):
        collidedSprite = pygame.sprite.spritecollideany(ballSprite, edgeCircles)
        collisionPt = collidedSprite.rect.center
        #print(collisionPt)

        #pygame.draw.line(screen,BLACK,center,collisionPt)
        #pygame.draw.line(screen,BLACK,collisionPt,previousPt)
        angleAtImpact = angleBetweenLines(center,collisionPt,previousPt,collisionPt)

        #finds angle of the normal line counter_clockwise to the pos x-axis
        radAngle = math.atan2(collisionPt[1] - 300, collisionPt[0] - 300)
        BaseLineAngle = math.degrees(radAngle) % 360
        previousAngle = (math.degrees(math.atan2(previousPt[1] - collisionPt[1],previousPt[0] - collisionPt[1]))) % 360
        print(BaseLineAngle)

        #determine if angle of bounce is left or right
        if previousAngle > BaseLineAngle:
            angleAtImpact = -angleAtImpact
            print("left")
        else:
            print("right")
        print(previousAngle)
        print(BaseLineAngle)
        #temp calc for bounce
        tempAngleOfBounce = ((BaseLineAngle - 180) % 360) + angleAtImpact
        distance = calcHypotenuse(previousPt,collisionPt)
        
        Xvelocity = math.cos(math.radians(tempAngleOfBounce)) * distance * 0.4
        Yvelocity = math.sin(math.radians(tempAngleOfBounce)) * distance * 0.4

    
    allSprites.draw(screen)
    #pygame.draw.circle(screen,BLACK,previousPt,4)
    Yvelocity += gravity
    pygame.display.flip()

    clock.tick(10)