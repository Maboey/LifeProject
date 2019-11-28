import pygame
from random import SystemRandom

#region Variables and Constants
screenWidth = 1500
screenHeight = 900
displaySurface = pygame.display.set_mode((screenWidth,screenHeight))
pygame.display.set_caption("Life Project")
clock = pygame.time.Clock()
run = True
fps = 30
correctionOffRandomConstant = fps//6

red = [255,0,0]
green = [50,255,50]
darkGreen = [0,130,50]
blue = [0,0,255]
white = [255,255,255]
black = [0,0,0]
water = [50,255,255]
pink = [255,20,147]
grey = [170,170,170]
backgroundColor = white

pygame.font.init()

infoBarWidth = 50
infoBarHeight = 5
infoBarVerticalOffset = 10
infoBarHorizontalOffset = infoBarWidth//2

genders = ['male','female']
creatureList = []
foodList = []
drinkList = []

chancesOfMovingMax = 6
chancesOfMoving = 2
baseCreatureSpeed = 23

pregnantMinutesCountDown = 10

StartingNumberOfCreatures = 50
StartingNumberOfFoods = StartingNumberOfCreatures // 2
StartingNumberOfDrinks = StartingNumberOfCreatures // 2

foodGivenPerMinute = 3
drinkGivenPerMinute = 3

offsetInfoTextPosition1 = 20
infoRectangleWidth = 340
infoRectangleHeight = 220
infoTextSize = 20

numberOfCreaturesThatDied = 0

#region valeurs du temps (-1 pour les test de conditions dans la fonction sceondGeneralUpdate)
numberOfSecondsInAMinute = 59
numberOfMinutesInAnHour = 59
numberOfHoursInADay = 23
numberOfDayInAMonth = 29
numberOfMonthsInAYear = 11
second = 0
minute = 0
hour = 0
day = 1
month = 1
year = 0
CountFpsToASecond = 0
#endregion

firstTimeInWhileLoop = True

animationCreature = [0,1,2,1]
animationCreatureCount = 0

#endregion

#region Classes
class stuff(object):
    def __init__(self):
        self.weight = 0
        self.x = screenWidth//2
        self.y = screenHeight//2

class creature (stuff):
    def __init__(self,name):
        self.lifePoints = 100
        self.gender = SystemRandom().choice(genders)
        self.color = [SystemRandom().randrange(0,255),SystemRandom().randrange(0,255),SystemRandom().randrange(0,255)]
        self.hunger = SystemRandom().randrange(0,30)
        self.thirst = SystemRandom().randrange(0,30)
        self.agressivity = SystemRandom().randrange(0,30)
        self.libido = SystemRandom().randrange(0,30)
        self.pregnant = False
        self.pregnantCounter = 0
        self.foundfood = False
        self.founddrink = False
        self.foundpartner = False
        self.name = name
        self.birthDate = [day,month,year]

        self.height = SystemRandom().randrange(15,25)
        self.muscularMass = SystemRandom().randrange(0,100)
        self.bodyFat = SystemRandom().randrange(0,100)
        self.weight = ((self.height * self.muscularMass)/100) + self.bodyFat

        self.x = SystemRandom().randrange(0,screenWidth)
        self.y = SystemRandom().randrange(0,screenHeight)
        self.moveX = 0
        self.moveY = 0
        self.sightRadius = SystemRandom().randrange(self.height*2,self.height*4)
        self.speed = baseCreatureSpeed//self.height

        self.GeneTransmissionHeight = 0
        self.GeneTransmissionSightRadius = 0
        self.GeneTransmissionAgressivity = 0
        self.GeneTransmissionMuscularMass = 0
        self.GeneTransmissionBodyFat = 0
        self.GeneTransmissionWeight = 0
        self.GeneTransmissionSpeed = 0

    def eat(self,foodWeight,foodNutrition):
        self.weight += foodWeight
        self.lifePoints += foodNutrition
        self.hunger -= foodNutrition
        if self.lifePoints>100:
            self.lifePoints = 100
        if self.hunger<0:
            self.hunger = 0

    def drink(self,drinkWeight,drinkHydratationValue):
        self.thirst -= drinkHydratationValue
        self.lifePoints += drinkHydratationValue
        self.weight += drinkWeight
        if self.lifePoints>100:
            self.lifePoints = 100
        if self.thirst<0:
            self.thirst = 0

    def poop(self):
        self.weight -= SystemRandom().randrange(0,30)   
    
    def draw(self):
        global animationCreature
        global animationCreatureCount
        #sight radius
        pygame.draw.circle(displaySurface,grey,(self.x,self.y),self.sightRadius,1)      

        #libidoBar
        pygame.draw.rect(displaySurface,black,(self.x-infoBarHorizontalOffset-1,self.y-(self.height+infoBarVerticalOffset+(infoBarHeight*3)-1),infoBarWidth+2,infoBarHeight+2))
        pygame.draw.rect(displaySurface,grey,(self.x-infoBarHorizontalOffset,self.y-(self.height+infoBarVerticalOffset+(infoBarHeight*3)),infoBarWidth,infoBarHeight))
        
        pygame.draw.rect(displaySurface,black,(self.x-infoBarHorizontalOffset-1,self.y-(self.height+infoBarVerticalOffset+(infoBarHeight*3)-1),(infoBarWidth*self.libido)//100+2,infoBarHeight+2))
        pygame.draw.rect(displaySurface,pink,(self.x-infoBarHorizontalOffset,self.y-(self.height+infoBarVerticalOffset+(infoBarHeight*3)),(infoBarWidth*self.libido)//100,infoBarHeight))


        #thirstBar
        pygame.draw.rect(displaySurface,black,(self.x-infoBarHorizontalOffset-1,self.y-(self.height+infoBarVerticalOffset+(infoBarHeight*2)-1),infoBarWidth+2,infoBarHeight+2))
        pygame.draw.rect(displaySurface,grey,(self.x-infoBarHorizontalOffset,self.y-(self.height+infoBarVerticalOffset+(infoBarHeight*2)),infoBarWidth,infoBarHeight))
        
        pygame.draw.rect(displaySurface,black,(self.x-infoBarHorizontalOffset-1,self.y-(self.height+infoBarVerticalOffset+(infoBarHeight*2)-1),(infoBarWidth*self.thirst)//100+2,infoBarHeight+2))
        pygame.draw.rect(displaySurface,blue,(self.x-infoBarHorizontalOffset,self.y-(self.height+infoBarVerticalOffset+(infoBarHeight*2)),(infoBarWidth*self.thirst)//100,infoBarHeight))

        #hungerBar
        pygame.draw.rect(displaySurface,black,(self.x-infoBarHorizontalOffset-1,self.y-(self.height+infoBarVerticalOffset+infoBarHeight-1),infoBarWidth+2,infoBarHeight+2))
        pygame.draw.rect(displaySurface,grey,(self.x-infoBarHorizontalOffset,self.y-(self.height+infoBarVerticalOffset+infoBarHeight),infoBarWidth,infoBarHeight))

        pygame.draw.rect(displaySurface,black,(self.x-infoBarHorizontalOffset-1,self.y-(self.height+infoBarVerticalOffset+infoBarHeight-1),(infoBarWidth*self.hunger)//100 +2,infoBarHeight+2))
        pygame.draw.rect(displaySurface,green,(self.x-infoBarHorizontalOffset,self.y-(self.height+infoBarVerticalOffset+infoBarHeight),(infoBarWidth*self.hunger)//100,infoBarHeight))

        #lifeBar
        pygame.draw.rect(displaySurface,black,(self.x-infoBarHorizontalOffset-1,self.y-(self.height+infoBarVerticalOffset)-1,infoBarWidth+2,infoBarHeight+2))
        pygame.draw.rect(displaySurface,grey,(self.x-infoBarHorizontalOffset,self.y-(self.height+infoBarVerticalOffset),infoBarWidth,infoBarHeight))
        
        pygame.draw.rect(displaySurface,black,(self.x-infoBarHorizontalOffset-1,self.y-(self.height+infoBarVerticalOffset)-1,(infoBarWidth*self.lifePoints)//100+2,infoBarHeight+2))
        pygame.draw.rect(displaySurface,red,(self.x-infoBarHorizontalOffset,self.y-(self.height+infoBarVerticalOffset),(infoBarWidth*self.lifePoints)//100,infoBarHeight))

        #creature
        animationCreatureCount += 1
        if animationCreatureCount > 300 :
            animationCreatureCount = 0
        pygame.draw.circle(displaySurface,black,(self.x,self.y),self.height + 1 + animationCreature[animationCreatureCount//100])      
        pygame.draw.circle(displaySurface,self.color,(self.x,self.y),self.height + animationCreature[animationCreatureCount//100])      
        
        #pregnant pink dot and countdown
        if self.pregnant:
            pygame.draw.circle(displaySurface,pink,(self.x,self.y),self.height//2)

            myfont = pygame.font.SysFont('Comic Sans MS', 10)
            textsurface = myfont.render(str(self.pregnantCounter), False, (0, 0, 0))
            displaySurface.blit(textsurface,(self.x-3,self.y-6))
        
        #info creature
        myfont = pygame.font.SysFont('Comic Sans MS', 10)
        
        textsurface = myfont.render(self.gender, False, (0, 0, 0))
        displaySurface.blit(textsurface,(self.x-(self.height//2),self.y+self.height))

        textsurface = myfont.render(str(self.birthDate[0]) + "/" + str(self.birthDate[1]) + "/" + str(self.birthDate[2]), False, (0, 0, 0))
        displaySurface.blit(textsurface,(self.x - (self.height//2),self.y + self.height+10))
    
    def move(self):
        if not ((self.x + (4*self.moveX)) > screenWidth or (self.x + (4*self.moveX)) < 0):
            self.x += self.moveX * self.speed
        else:
            self.moveX = 0
        if not ((self.y + (4*self.moveY)) > screenHeight or (self.y + (4*self.moveY)) < 0):
            self.y += self.moveY*self.speed
        else:
            self.moveY = 0

    def moveRandomly(self):
        if SystemRandom().randrange(0,chancesOfMovingMax) > chancesOfMoving:
            if SystemRandom().randrange(0,chancesOfMovingMax) > chancesOfMoving:
                if (self.x + (2*self.sightRadius)) > screenWidth :
                    self.moveX = SystemRandom().randrange(-self.sightRadius,0)//fps
                    if self.moveX == 0:
                        self.moveX = -1
                elif (self.x - (2*self.sightRadius)) < self.sightRadius :
                    self.moveX = SystemRandom().randrange(0,self.sightRadius)//fps
                    if self.moveX == 0:
                        self.moveX = 1
                elif self.moveX < -1:
                    self.moveX = SystemRandom().randrange(0,self.sightRadius)//fps
                else :
                    self.moveX += SystemRandom().randrange(-self.sightRadius,self.sightRadius + correctionOffRandomConstant)//fps 

            if SystemRandom().randrange(0,chancesOfMovingMax) > chancesOfMoving:      
                if (self.y + (2*self.sightRadius)) > screenHeight :
                    self.moveY = SystemRandom().randrange(-self.sightRadius,0)//fps
                    if self.moveY == 0:
                        self.moveY = -1
                elif (self.y - (2*self.sightRadius)) < self.sightRadius :
                    self.moveY = SystemRandom().randrange(0,self.sightRadius)//fps
                    if self.moveY == 0:
                        self.moveY = 1
                elif self.moveY < -1:
                    self.moveY = SystemRandom().randrange(0,self.sightRadius)//fps
                else:
                    self.moveY += SystemRandom().randrange(-self.sightRadius,self.sightRadius + correctionOffRandomConstant)//fps 
        else:
            self.moveX -= self.moveX//fps
            self.moveY -= self.moveY//fps   

class food (stuff):
    def __init__(self):
        self.nutrition = SystemRandom().randrange(1,30)
        self.height = self.nutrition//3
        self.weight = self.nutrition
        self.x = SystemRandom().randrange(0,screenWidth)
        self.y = SystemRandom().randrange(0,screenHeight)
        self.color = [SystemRandom().randrange(0,100),150 + (self.nutrition * 3),SystemRandom().randrange(0,100)]

    def draw(self):
        pygame.draw.circle(displaySurface,black,(self.x,self.y),self.height + 1)
        pygame.draw.circle(displaySurface,self.color,(self.x,self.y),(self.height))
        pass

class drink (stuff):
    def __init__(self):
        self.hydratation = SystemRandom().randrange(1,30)
        self.height = self.hydratation//3
        self.weight = self.hydratation
        self.x = SystemRandom().randrange(0,screenWidth)
        self.y = SystemRandom().randrange(0,screenHeight)
        self.color = [SystemRandom().randrange(0,100),0,150 + (self.hydratation * 2)]
    def draw(self):
        pygame.draw.circle(displaySurface,black,(self.x,self.y),self.height + 1)
        pygame.draw.circle(displaySurface,self.color,(self.x,self.y),(self.height))
        pass

#endregion

#region definitions
def LifeProjectInitialisation():
    #region creatures creation
    i = 0
    while i < StartingNumberOfCreatures:
        i += 1
        creatureList.append(creature("creature"+str(i)))
    #endregion
    #region food creation
    i = 0
    while i < StartingNumberOfFoods:
        i += 1
        foodList.append(food())
    #endregion
    #region drink creation
    i = 0
    while i < StartingNumberOfDrinks:
        i += 1
        drinkList.append(drink())
    #endregion

#region Time Updates
def fpsUpdate():
    global numberOfCreaturesThatDied 
    #region secondUpdate
    global CountFpsToASecond
    if CountFpsToASecond < fps: # fps count to get to a second and call "sceondUpdate()"
        CountFpsToASecond += 1
    else:
        CountFpsToASecond = 0
        secondUpdate()
    #endregion
    #region update the position of each creature
    for obj in creatureList:
        obj.move()
        pass
    #endregion
    #region makes creature go towards foods, drinks or partners and eat, drink, or make a baby
    for creatures in creatureList:
        for creaturesB in creatureList: # make baby
            if ((((creaturesB.x - creatures.x) > -creatures.sightRadius) and ((creaturesB.x - creatures.x) < creatures.sightRadius)) and (((creaturesB.y - creatures.y) > -creatures.sightRadius) and ((creaturesB.y - creatures.y) < creatures.sightRadius))) and (creatures.gender == "male" and creaturesB.gender == "female") and (creatures.libido>50 and creaturesB.libido>50) and not(creaturesB.pregnant):
                creatures.moveX = (creaturesB.x - creatures.x)//(fps//3)
                creatures.moveY = (creaturesB.y - creatures.y)//(fps//3)
                creatures.foundpartner = True
                if ((creaturesB.x - creatures.x) == 0) and ((creaturesB.y - creatures.y) == 0):
                    creaturesB.pregnant = True
                    creaturesB.pregnantCounter = pregnantMinutesCountDown
                    creaturesB.libido = 0
                    creatures.libido = 0
                    creaturesB.GeneTransmissionHeight = (creaturesB.height + creatures.height)//2
                    creaturesB.GeneTransmissionSightRadius = (creaturesB.sightRadius + creatures.sightRadius)//2
                    creaturesB.GeneTransmissionAgressivity = (creaturesB.agressivity + creatures.agressivity)//2
                    creaturesB.GeneTransmissionMuscularMass = (creaturesB.muscularMass + creatures.muscularMass)//2
                    creaturesB.GeneTransmissionBodyFat = (creaturesB.bodyFat + creatures.bodyFat)//2
                    creaturesB.GeneTransmissionWeight = (creaturesB.weight + creatures.weight)//2
                    creaturesB.GeneTransmissionSpeed = (creaturesB.speed + creatures.speed)//2
                elif (creatures.moveX < 1 and creatures.moveX > -1) and (creatures.moveY < 1 and creatures.moveY > -1):
                    creatures.x += (creaturesB.x-creatures.x)
                    creatures.y += (creaturesB.y-creatures.y)      
            else:
                creatures.foundpartner = False
        for foods in foodList: # eat
            if ((((foods.x - creatures.x) > -creatures.sightRadius) and ((foods.x - creatures.x) < creatures.sightRadius)) and (((foods.y - creatures.y) > -creatures.sightRadius) and ((foods.y - creatures.y) < creatures.sightRadius))) and creatures.hunger > 0:
                creatures.moveX = (foods.x - creatures.x)//(fps//3)
                creatures.moveY = (foods.y - creatures.y)//(fps//3)
                creatures.foundfood = True
                if ((foods.x - creatures.x) == 0) and ((foods.y - creatures.y) == 0):
                    creatures.eat(foods.weight, foods.nutrition)
                    foodList.remove(foods)
                elif (creatures.moveX < 1 and creatures.moveX > -1) and (creatures.moveY < 1 and creatures.moveY > -1):
                    creatures.x += (foods.x-creatures.x)
                    creatures.y += (foods.y-creatures.y)
            else:
                creatures.foundfood = False
        for drinks in drinkList: # drink
            if ((((drinks.x - creatures.x) > -creatures.sightRadius) and ((drinks.x - creatures.x) < creatures.sightRadius)) and (((drinks.y - creatures.y) > -creatures.sightRadius) and ((drinks.y - creatures.y) < creatures.sightRadius))) and creatures.thirst > 0:
                creatures.moveX = (drinks.x - creatures.x)//(fps//3)
                creatures.moveY = (drinks.y - creatures.y)//(fps//3)
                creatures.founddrink = True
                if ((drinks.x - creatures.x) == 0) and ((drinks.y - creatures.y) == 0):
                    creatures.drink(drinks.weight, drinks.hydratation)
                    drinkList.remove(drinks)
                elif (creatures.moveX < 1 and creatures.moveX > -1) and (creatures.moveY < 1 and creatures.moveY > -1):
                    creatures.x += (drinks.x-creatures.x)
                    creatures.y += (drinks.y-creatures.y)      
            else:
                creatures.founddrink = False
    #endregion
    #region kill creatures if they don't have any life left
    for creatures in creatureList:
        if creatures.lifePoints <= 0:
            creatureList.remove(creatures)
            numberOfCreaturesThatDied += 1
    #endregion
    
    redrawGameWindow()

def secondUpdate():
    #region global variables
    global second
    global minute
    global hour
    global day
    global month
    global year
    #endregion
    #region updates the direction where each creature goes
    for creatures in creatureList:
        if not creatures.foundfood and not creatures.founddrink :
            creatures.moveRandomly()
    #endregion
    #region Time passes
    if second < numberOfSecondsInAMinute :
        second += 1
    else:
        second = 0
        if minute < numberOfMinutesInAnHour :
            minute += 1
            minuteUpdate()
        else:
            minute = 0
            if hour < numberOfHoursInADay :
                hour += 1
                hourUpdate()
            else:
                hour = 0
                if day <= numberOfDayInAMonth :
                    day += 1
                    dayUpdate()
                else:
                    day = 1
                    if month <= numberOfMonthsInAYear:
                        month += 1
                        monthUpdate()
                    else:
                        month = 1
                        year += 1
                        yearUpdate()
    #endregion

def minuteUpdate():
    i = 0
    while i < foodGivenPerMinute:
        foodList.append(food()) # creates a food item
        i += 1
    i = 0
    while i < drinkGivenPerMinute:
        drinkList.append(drink()) # creates a drink item
        i += 1
    for creatures in creatureList: # evolve creature stats
        if creatures.hunger < 100 :
            creatures.hunger += 5
        else:
            creatures.lifePoints -= 5
        if creatures.thirst < 100 :
            creatures.thirst += 5
        else:
            creatures.lifePoints -= 5
        if creatures.libido < 100 :
            creatures.libido += 5
        if creatures.pregnant:
            creatures.pregnantCounter -= 1
            if creatures.pregnantCounter <= 0:
                creatureList.append(creature("creature"+str(len(creatureList))))
                creatureList[-1].x = creatures.x
                creatureList[-1].y = creatures.y
                creatureList[-1].libido = 0
                creatureList[-1].hunger = 0
                creatureList[-1].thirst = 0
                creatureList[-1].color = creatures.color
                creatureList[-1].height = creatures.GeneTransmissionHeight 
                creatureList[-1].sightRadius = creatures.GeneTransmissionSightRadius 
                creatureList[-1].agressivity = creatures.GeneTransmissionAgressivity 
                creatureList[-1].muscularMass = creatures.GeneTransmissionMuscularMass 
                creatureList[-1].bodyFat = creatures.GeneTransmissionBodyFat 
                creatureList[-1].weight = creatures.GeneTransmissionWeight 
                creatureList[-1].speed = creatures.GeneTransmissionSpeed 
                creatures.pregnant = False
                creatures.pregnantCounter = 0

def hourUpdate():
    pass

def dayUpdate():
    pass

def monthUpdate():
    pass

def yearUpdate():
    pass
#endregion

def redrawGameWindow():
    displaySurface.fill(backgroundColor) #refill the image with desired background color in order to erase everything
    
    for obj in foodList:
        obj.draw()

    for obj in drinkList:
        obj.draw()
    
    for obj in creatureList: # draws each creature
        obj.draw()
        pass
    
    drawInfo()

    pygame.display.update()

def drawInfo():
    numberOfMale = 0
    numberOfFemale = 0
    numberOfPregnantCreatures = 0

    for creatures in creatureList:
        if creatures.gender == "male":
            numberOfMale += 1
        if creatures.gender == "female":
            numberOfFemale += 1
        if creatures.pregnant:
            numberOfPregnantCreatures += 1       

    myfont = pygame.font.SysFont('Comic Sans MS', infoTextSize)

    textsurface = myfont.render("number of males = " + str(numberOfMale), False, black)
    displaySurface.blit(textsurface,(10,0))

    textsurface = myfont.render("number of females = " + str(numberOfFemale), False, black)
    displaySurface.blit(textsurface,(10,offsetInfoTextPosition1))

    textsurface = myfont.render("number of pregnant creatures = " + str(numberOfPregnantCreatures), False, black)
    displaySurface.blit(textsurface,(10,offsetInfoTextPosition1*2))

    textsurface = myfont.render("number of creatures that died = " + str(numberOfCreaturesThatDied), False, black)
    displaySurface.blit(textsurface,(10,offsetInfoTextPosition1*3))

    textsurface = myfont.render("year = " + str(year), False, black)
    displaySurface.blit(textsurface,(10,offsetInfoTextPosition1*4))

    textsurface = myfont.render("month = " + str(month), False, black)
    displaySurface.blit(textsurface,(10,offsetInfoTextPosition1*5))

    textsurface = myfont.render("day = " + str(day), False, black)
    displaySurface.blit(textsurface,(10,offsetInfoTextPosition1*6))

    textsurface = myfont.render("hour = " + str(hour), False, black)
    displaySurface.blit(textsurface,(10,offsetInfoTextPosition1*7))

    textsurface = myfont.render("minute = " + str(minute), False, black)
    displaySurface.blit(textsurface,(10,offsetInfoTextPosition1*8))

    textsurface = myfont.render("second = " + str(second), False, black)
    displaySurface.blit(textsurface,(10,offsetInfoTextPosition1*9))
#endregion

while run:
    for event in pygame.event.get(): # event detection (like closing the window)
                 if event.type == pygame.QUIT:
                    run = False    
    if firstTimeInWhileLoop :
        firstTimeInWhileLoop = False
        LifeProjectInitialisation()    
    fpsUpdate()     
    clock.tick(fps)
quit()