import pygame
from random import SystemRandom

#region Variables and Constants

#region display and fps
screenWidth = 1500
screenHeight = 850
displaySurface = pygame.display.set_mode((screenWidth,screenHeight))
pygame.display.set_caption("Life Project")
clock = pygame.time.Clock()
run = True
fps = 30
correctionOffRandomConstant = fps//6
#endregion

#region import sprites
backgroundSprite = pygame.image.load('Sprite/background.jpg')
#endregion

#region counters
creatureNumber = 0
numberOfCreaturesThatDied = 0
#endregion

#region sizes and positions
creatureInfoXOffset = 20
creatureInfoYOffset = -30

foodInfoXOffset = 10
foodInfoYOffset = -15

infoBarWidth = 50
infoBarHeight = 5
infoBarVerticalOffset = 30
infoBarHorizontalOffset = infoBarWidth//2

offsetInfoTextPosition1 = 20
infoRectangleWidth = 150
infoRectangleHeight = 220
infoTextSize = 20
#endregion

#region colours
red = [255,0,0]
yellow = [255,255,0]
green = [50,255,50]
darkGreen = [0,130,50]
blue = [0,0,255]
white = [255,255,255]
black = [0,0,0]
water = [200,255,255]
pink = [255,20,147]
grey = [170,170,170]
backgroundColor = water
#endregion

#region foods and drinks
foodNames = ["Pain","Pomme de terre","Haricots","Riz","Cassoulet","Nuggets","Pizza","Hamburger","Tomate","Epinards","Tacos"]
drinkNames = ["Eau","Coca-Cola","Pepsi","Sinalco","Jus d'Orange","Jus de Pomme","Bière","Jus de Tomate","Rivela","Sirop","Jus de pomme"]
#endregion

#region object lists
creatureList = []
foodList = []
drinkList = []
#endregion

#region creatures
chancesOfMovingMax = 4
chancesOfMoving = 1
baseCreatureSpeed = 22

pregnantMinutesCountDown = 10

animationCreature = [0,1,2,1]
animationCreatureCount = 0

genders = ['male','female']
maleNames = ["Manuel","Terrence","Valentin","Léo","William","Carlos","Guillaume","Max","François","Anthony","Jack","Diego","Lucas","David","Xavier","Jacob","Carl","Jean","Yannick","Nicolas","Giordano","Beza","Mario","Brayan","Florient","Alexandre","Bartolomé"]
femaleNames = ["Paloma","Josefa","Jaqueline","Elisabeth","Isabel","Sandrine","Stéphanie","Suzane","Mercedes","Madeleine","Balbina","Olivia","Sara","Léontine","Valentine","Loredana","Catherine","Salomé","Vanessa","Cynthia","Aurora","Mélodie","Justine"]
lastNames = ["Martin","Robert-Charrue","Masnaghetti","Garcia","Marques de Matos","Kenny","Guillet","Comé","Shore","Nunes","Langenbach","Marti","Micheli","Archier","Canales","Padin","Lacroix","Oliveira","Gonzales","Carvalho","Lannister","Calvin","Fioriti","Schregler","Savary","Sudan"]
#endregion

#region initial number of things or things given/taken per minute
StartingNumberOfCreatures = 50
StartingNumberOfFoods = StartingNumberOfCreatures // 2
StartingNumberOfDrinks = StartingNumberOfCreatures // 2

creatureLifepointsPerMinuteWithHunger = 10
creatureLifepointsPerMinuteWithThirst = 10
agressivityGivenPerMinuteWithHunger = 5
agressivityGivenPerMinuteWithThirst = 5
creatureHungerPerMinute = 10
creatureThirstPerMinute = 10
creatureLibidoPerMinute = 4

foodGivenPerMinute = 20
drinkGivenPerMinute = 20
#endregion

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
mouseX , mouseY = pygame.mouse.get_pos()
pygame.font.init()

#endregion

#region Classes

class creature (object):
    
    def __init__(self, number):
        self.number = number
        self.lifePoints = 100
        self.gender = SystemRandom().choice(genders)
        self.color = [SystemRandom().randrange(0,255),SystemRandom().randrange(0,255),SystemRandom().randrange(0,255)]
        self.hunger = SystemRandom().randrange(0,30)
        self.thirst = SystemRandom().randrange(0,30)
        self.agressivity = 0
        self.libido = SystemRandom().randrange(0,30)
        self.pregnant = False
        self.pregnantCounter = 0
        self.foundfood = False
        self.founddrink = False
        self.foundpartner = False
        if self.gender == "male":
            self.name = SystemRandom().choice(maleNames)
        else:
            self.name = SystemRandom().choice(femaleNames)
        self.LastName = SystemRandom().choice(lastNames)

        self.birthDate = [day,month,year]
        self.counterMinutesAlive = 0

        self.height = SystemRandom().randrange(10,20)
        self.muscularMass = SystemRandom().randrange(0,100)
        self.bodyFat = SystemRandom().randrange(0,100)
        self.weight = ((self.height * self.muscularMass)/100) + self.bodyFat

        self.x = SystemRandom().randrange(0,screenWidth)
        self.y = SystemRandom().randrange(0,screenHeight)
        self.moveX = 0
        self.moveY = 0
        self.sightRadius = SystemRandom().randrange(self.height*2,self.height*4)
        self.speed = baseCreatureSpeed // self.height

        self.GeneTransmissionLastName = ""
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

        #creature itself
        if SystemRandom().randrange(0,100) > 30:
            animationCreatureCount += 1
        else:
            animationCreatureCount == 0
        if animationCreatureCount > 399 :
            animationCreatureCount = 0
        pygame.draw.circle(displaySurface,black,(self.x,self.y),self.height + 1 + animationCreature[animationCreatureCount//100])      
        pygame.draw.circle(displaySurface,self.color,(self.x,self.y),self.height + animationCreature[animationCreatureCount//100])      
        
        #pregnant pink dot
        if self.pregnant:
            pygame.draw.circle(displaySurface,pink,(self.x,self.y),self.height//2)                

        # show info only when the mouse is over the creature
        if (abs(self.x - mouseX) < self.height and abs(self.y - mouseY) < self.height) or (pygame.key.get_pressed()[pygame.K_SPACE]) : 
            #sight radius
            pygame.draw.circle(displaySurface,grey,(self.x,self.y),self.sightRadius,1)

            #Agressivity
            pygame.draw.rect(displaySurface,black,(self.x-infoBarHorizontalOffset-1,self.y-(self.height+infoBarVerticalOffset+(infoBarHeight*4)-1),infoBarWidth+2,infoBarHeight+2))
            pygame.draw.rect(displaySurface,grey,(self.x-infoBarHorizontalOffset,self.y-(self.height+infoBarVerticalOffset+(infoBarHeight*4)),infoBarWidth,infoBarHeight))
            
            pygame.draw.rect(displaySurface,black,(self.x-infoBarHorizontalOffset-1,self.y-(self.height+infoBarVerticalOffset+(infoBarHeight*4)-1),(infoBarWidth*self.agressivity)//100+2,infoBarHeight+2))
            pygame.draw.rect(displaySurface,yellow,(self.x-infoBarHorizontalOffset,self.y-(self.height+infoBarVerticalOffset+(infoBarHeight*4)),(infoBarWidth*self.agressivity)//100,infoBarHeight))

            #libidoBar
            pygame.draw.rect(displaySurface,black,(self.x-infoBarHorizontalOffset-1,self.y-(self.height+infoBarVerticalOffset+(infoBarHeight*3)-1),infoBarWidth+2,infoBarHeight+2))
            pygame.draw.rect(displaySurface,grey,(self.x-infoBarHorizontalOffset,self.y-(self.height+infoBarVerticalOffset+(infoBarHeight*3)),infoBarWidth,infoBarHeight))
            
            pygame.draw.rect(displaySurface,black,(self.x-infoBarHorizontalOffset-1,self.y-(self.height+infoBarVerticalOffset+(infoBarHeight*3)-1),(infoBarWidth*self.libido)//100+2,infoBarHeight+2))
            pygame.draw.rect(displaySurface,pink,(self.x-infoBarHorizontalOffset,self.y-(self.height+infoBarVerticalOffset+(infoBarHeight*3)),(infoBarWidth*self.libido)//100,infoBarHeight))

            #thirstBar
            pygame.draw.rect(displaySurface,black,(self.x-infoBarHorizontalOffset-1,self.y-(self.height+infoBarVerticalOffset+(infoBarHeight*2)-1),infoBarWidth+2,infoBarHeight+2))
            pygame.draw.rect(displaySurface,grey,(self.x-infoBarHorizontalOffset,self.y-(self.height+infoBarVerticalOffset+(infoBarHeight*2)),infoBarWidth,infoBarHeight))
            
            pygame.draw.rect(displaySurface,black,(self.x-infoBarHorizontalOffset-1,self.y-(self.height+infoBarVerticalOffset+(infoBarHeight*2)-1),(infoBarWidth - (infoBarWidth*self.thirst)//100+2),infoBarHeight+2))
            pygame.draw.rect(displaySurface,blue,(self.x-infoBarHorizontalOffset,self.y-(self.height+infoBarVerticalOffset+(infoBarHeight*2)),(infoBarWidth - (infoBarWidth*self.thirst)//100),infoBarHeight))

            #hungerBar
            pygame.draw.rect(displaySurface,black,(self.x-infoBarHorizontalOffset-1,self.y-(self.height+infoBarVerticalOffset+infoBarHeight-1),infoBarWidth+2,infoBarHeight+2))
            pygame.draw.rect(displaySurface,grey,(self.x-infoBarHorizontalOffset,self.y-(self.height+infoBarVerticalOffset+infoBarHeight),infoBarWidth,infoBarHeight))

            pygame.draw.rect(displaySurface,black,(self.x-infoBarHorizontalOffset-1,self.y-(self.height+infoBarVerticalOffset+infoBarHeight-1),((infoBarWidth) - (infoBarWidth*self.hunger)//100 +2),infoBarHeight+2))
            pygame.draw.rect(displaySurface,green,(self.x-infoBarHorizontalOffset,self.y-(self.height+infoBarVerticalOffset+infoBarHeight),(infoBarWidth - (infoBarWidth*self.hunger)//100),infoBarHeight))

            #lifeBar
            pygame.draw.rect(displaySurface,black,(self.x-infoBarHorizontalOffset-1,self.y-(self.height+infoBarVerticalOffset)-1,infoBarWidth+2,infoBarHeight+2))
            pygame.draw.rect(displaySurface,grey,(self.x-infoBarHorizontalOffset,self.y-(self.height+infoBarVerticalOffset),infoBarWidth,infoBarHeight))
            
            pygame.draw.rect(displaySurface,black,(self.x-infoBarHorizontalOffset-1,self.y-(self.height+infoBarVerticalOffset)-1,(infoBarWidth*self.lifePoints)//100+2,infoBarHeight+2))
            pygame.draw.rect(displaySurface,red,(self.x-infoBarHorizontalOffset,self.y-(self.height+infoBarVerticalOffset),(infoBarWidth*self.lifePoints)//100,infoBarHeight))
            
            #info creature
            myfont = pygame.font.SysFont('Comic Sans MS', 10)

            textsurface = myfont.render(str(self.name)+ " " + str(self.LastName), False, (0, 0, 0))
            displaySurface.blit(textsurface,(creatureInfoXOffset + self.x + self.height, creatureInfoYOffset + self.y + (self.height//2)))

            textsurface = myfont.render(str(self.birthDate[0]) + "/" + str(self.birthDate[1]) + "/" + str(self.birthDate[2]), False, (0, 0, 0))
            displaySurface.blit(textsurface,(creatureInfoXOffset + self.x + self.height, creatureInfoYOffset + self.y + (self.height//2)+10))

            textsurface = myfont.render(str(self.counterMinutesAlive) + " minutes", False, (0, 0, 0))
            displaySurface.blit(textsurface,(creatureInfoXOffset + self.x + self.height, creatureInfoYOffset + self.y + (self.height//2)+20))
            
            if self.pregnant:# show pregnancy counter only if pregnant
                textsurface = myfont.render(str(self.pregnantCounter), False, (0, 0, 0))
                displaySurface.blit(textsurface,(self.x-3,self.y-3))
    
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
                    self.moveX = SystemRandom().randrange(-self.sightRadius,self.sightRadius + correctionOffRandomConstant)//fps 

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
                    self.moveY = SystemRandom().randrange(-self.sightRadius,self.sightRadius + correctionOffRandomConstant)//fps 
        else:
            self.moveX -= self.moveX//fps
            self.moveY -= self.moveY//fps   

class food (object):
    
    def __init__(self):
        self.name = SystemRandom().choice(foodNames)
        self.nutrition = SystemRandom().randrange(1,30)
        self.height = self.nutrition//3
        self.weight = self.nutrition
        self.x = SystemRandom().randrange(0,screenWidth)
        self.y = SystemRandom().randrange(0,screenHeight)
        self.color = [SystemRandom().randrange(0,100),160 + (self.nutrition * 3),SystemRandom().randrange(0,100)]

    def draw(self):
        pygame.draw.circle(displaySurface,black,(self.x,self.y),self.height + 1)
        pygame.draw.circle(displaySurface,self.color,(self.x,self.y),(self.height))

        if abs(self.x - mouseX) < self.height and abs(self.y - mouseY) < self.height: # show info only when the mouse is over the creature
            #info food
            myfont = pygame.font.SysFont('Comic Sans MS', 10)

            textsurface = myfont.render(self.name, False, (0, 0, 0))
            displaySurface.blit(textsurface,(foodInfoXOffset + self.x + self.height, foodInfoYOffset + self.y ))

            textsurface = myfont.render("nutrition value = " + str(self.nutrition), False, (0, 0, 0))
            displaySurface.blit(textsurface,(foodInfoXOffset + self.x + self.height, foodInfoYOffset + self.y + 10))

class drink (object):
    
    def __init__(self):
        self.name = SystemRandom().choice(drinkNames)
        self.hydratation = SystemRandom().randrange(1,30)
        self.height = self.hydratation//3
        self.weight = self.hydratation
        self.x = SystemRandom().randrange(0,screenWidth)
        self.y = SystemRandom().randrange(0,screenHeight)
        self.color = [SystemRandom().randrange(0,100),0,150 + (self.hydratation * 2)]
    
    def draw(self):
        pygame.draw.circle(displaySurface,black,(self.x,self.y),self.height + 1)
        pygame.draw.circle(displaySurface,self.color,(self.x,self.y),(self.height))
        
        if abs(self.x - mouseX) < self.height and abs(self.y - mouseY) < self.height: # show info only when the mouse is over the creature
            #info drinks
            myfont = pygame.font.SysFont('Comic Sans MS', 10)

            textsurface = myfont.render(self.name, False, (0, 0, 0))
            displaySurface.blit(textsurface,(foodInfoXOffset + self.x + self.height, foodInfoYOffset + self.y ))

            textsurface = myfont.render("hydratation value = " + str(self.hydratation), False, (0, 0, 0))
            displaySurface.blit(textsurface,(foodInfoXOffset + self.x + self.height, foodInfoYOffset + self.y + 10))

#endregion

#region definitions

#region make objects apear (initialisation and updates)

def LifeProjectInitialisation():
    #region creatures creation
    global creatureNumber
    
    i = 0
    while i < StartingNumberOfCreatures:
        i += 1
        creatureList.append(creature(creatureNumber))
        creatureNumber +=1
    
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

def GivenSuppliesPerMinute():
    i = 0
    while i < foodGivenPerMinute:
        foodList.append(food()) # creates a food item
        i += 1
    i = 0
    while i < drinkGivenPerMinute:
        drinkList.append(drink()) # creates a drink item
        i += 1

#endregion

#region automatic actions performed on creatures

def CheckPregnancyAndGiveBirth():# counts time left to birth and does the birth
    global creatureNumber
    for creatures in creatureList:
        if creatures.pregnant:
            creatures.pregnantCounter -= 1
            if creatures.pregnantCounter <= 0:
                creatures.pregnantCounter = 0
                creatureList.append(creature(creatureNumber))
                creatureNumber += 1
                creatures.pregnant = False
                creatures.pregnantCounter = 0
                creatureList[-1].LastName = creatures.LastName
                creatureList[-1].number = creatureNumber
                creatureList[-1].x = creatures.x
                creatureList[-1].y = creatures.y
                creatureList[-1].libido = 0
                creatureList[-1].hunger = 0
                creatureList[-1].thirst = 0
                if SystemRandom().randrange(0,3) >= 1: # each gene has a 1/4 chance of beeing random
                    creatureList[-1].color = creatures.color
                if SystemRandom().randrange(0,3) >= 1:
                    creatureList[-1].height = creatures.GeneTransmissionHeight 
                if SystemRandom().randrange(0,3) >= 1:
                    creatureList[-1].sightRadius = creatures.GeneTransmissionSightRadius 
                if SystemRandom().randrange(0,3) >= 1:
                    creatureList[-1].agressivity = creatures.GeneTransmissionAgressivity 
                if SystemRandom().randrange(0,3) >= 1:
                    creatureList[-1].muscularMass = creatures.GeneTransmissionMuscularMass 
                if SystemRandom().randrange(0,3) >= 1:
                    creatureList[-1].bodyFat = creatures.GeneTransmissionBodyFat 
                if SystemRandom().randrange(0,3) >= 1:
                    creatureList[-1].weight = creatures.GeneTransmissionWeight 
                if SystemRandom().randrange(0,3) >= 1:
                    creatureList[-1].speed = creatures.GeneTransmissionSpeed 
                    
def CreatureStatsFpsUpdate(): # creature stats that need to be updated each frame
    global numberOfCreaturesThatDied
    for creatures in creatureList:
        if creatures.lifePoints <= 0: # kill them if they don't have any life points left
            creatureList.remove(creatures)
            numberOfCreaturesThatDied += 1

def CreatureStatsMinuteUpdate(): # stats that change automatically each minute
    for creatures in creatureList: 
        creatures.counterMinutesAlive += 1
        if creatures.hunger < 100 :
            creatures.hunger += creatureHungerPerMinute
        else:
            creatures.hunger = 100
            creatures.agressivity += agressivityGivenPerMinuteWithHunger
            creatures.lifePoints -= creatureLifepointsPerMinuteWithHunger
        if creatures.thirst < 100 :
            creatures.thirst += creatureThirstPerMinute
        else:
            creatures.agressivity += agressivityGivenPerMinuteWithThirst
            creatures.lifePoints -= creatureLifepointsPerMinuteWithThirst
            creatures.thirst = 100
        if creatures.libido < 100 :
            creatures.libido += creatureLibidoPerMinute

def InterractionsFPS(): #interraction between a creature and something else (that need to be tested each frame)
    for creatures in creatureList:
        for creaturesB in creatureList:
            # make baby
            if ((abs(creatures.x - creaturesB.x) < creatures.sightRadius) and (abs(creatures.y - creaturesB.y) < creatures.sightRadius)) and ((creatures.gender == "male" and creaturesB.gender == "female") or (creatures.gender == "female" and creaturesB.gender == "male")) and (creatures.libido>50 and creaturesB.libido>50) and not(creaturesB.pregnant):#make babies
                creatures.moveX = (creaturesB.x - creatures.x)//(fps//3)
                creatures.moveY = (creaturesB.y - creatures.y)//(fps//3)
                if ((creaturesB.x - creatures.x) == 0) and ((creaturesB.y - creatures.y) == 0) and (creatures.gender == "male" and creaturesB.gender == "female"):
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
                    creatures.moveX = 0
                    creatures.moveY = 0
                elif (creatures.moveX < 1 and creatures.moveX > -1) and (creatures.moveY < 1 and creatures.moveY > -1):
                    creatures.x += (creaturesB.x-creatures.x)
                    creatures.y += (creaturesB.y-creatures.y)      
            # fight
            if (((abs(creatures.x - creaturesB.x) < creatures.sightRadius) and (abs(creatures.y - creaturesB.y) < creatures.sightRadius)) and creatures.agressivity > 1 and creatures.number != creaturesB.number) and (creatures.LastName != creaturesB.LastName):
                creatures.moveX = (creaturesB.x - creatures.x)//(fps//3)
                creatures.moveY = (creaturesB.y - creatures.y)//(fps//3)
                if (creatures.moveX == 0 and creaturesB.moveX == 0) and (creatures.moveY == 0 and creaturesB.moveY == 0):
                    creatures.x = creaturesB.x
                    creatures.y = creaturesB.y
                    creaturesB.lifePoints -= (creatures.muscularMass + creatures.agressivity)//fps
                    creatures.agressivity -= 1     
        for foods in foodList: # eat
            if ((((foods.x - creatures.x) > -creatures.sightRadius) and ((foods.x - creatures.x) < creatures.sightRadius)) and (((foods.y - creatures.y) > -creatures.sightRadius) and ((foods.y - creatures.y) < creatures.sightRadius))) and creatures.hunger > 0:
                creatures.moveX = (foods.x - creatures.x)//(fps//3)
                creatures.moveY = (foods.y - creatures.y)//(fps//3)
               
                if ((foods.x - creatures.x) < creatures.height) and ((foods.y - creatures.y) < creatures.height):
                    creatures.eat(foods.weight, foods.nutrition)
                    foodList.remove(foods)
                    creatures.moveX = 0
                    creatures.moveY = 0
                elif (creatures.moveX < 1 and creatures.moveX > -1) and (creatures.moveY < 1 and creatures.moveY > -1):
                    creatures.x += (foods.x-creatures.x)
                    creatures.y += (foods.y-creatures.y)      
        for drinks in drinkList: # drink
            if ((((drinks.x - creatures.x) > -creatures.sightRadius) and ((drinks.x - creatures.x) < creatures.sightRadius)) and (((drinks.y - creatures.y) > -creatures.sightRadius) and ((drinks.y - creatures.y) < creatures.sightRadius))) and creatures.thirst > 0:
                creatures.moveX = (drinks.x - creatures.x)//(fps//3)
                creatures.moveY = (drinks.y - creatures.y)//(fps//3)
                if ((drinks.x - creatures.x) < creatures.height) and ((drinks.y - creatures.y) < creatures.height):
                    creatures.drink(drinks.weight, drinks.hydratation)
                    drinkList.remove(drinks)
                    creatures.moveX = 0
                    creatures.moveY = 0
                elif (creatures.moveX < 1 and creatures.moveX > -1) and (creatures.moveY < 1 and creatures.moveY > -1):
                    creatures.x += (drinks.x-creatures.x)
                    creatures.y += (drinks.y-creatures.y)       

def ActionsSECOND(): #actions that creatures do each second
    for creatures in creatureList:
        creatures.moveRandomly()

#endregion

#region TimeUpdates

def TimePasses():
    global CountFpsToASecond
    global second
    global minute
    global hour
    global day
    global month
    global year
    if CountFpsToASecond < fps: # counter from fps to a years ( calls timexUpdates )
        CountFpsToASecond += 1
    else:
        CountFpsToASecond = 0
        secondUpdate()
        if second < numberOfSecondsInAMinute :
            second += 1
        else:
            second = 0
            minuteUpdate()
            if minute < numberOfMinutesInAnHour :
                minute += 1
            else:
                minute = 0
                hourUpdate()
                if hour < numberOfHoursInADay :
                    hour += 1
                else:
                    hour = 0
                    dayUpdate()
                    if day <= numberOfDayInAMonth :
                        day += 1
                    else:
                        day = 1
                        monthUpdate()
                        if month <= numberOfMonthsInAYear:
                            month += 1
                        else:
                            month = 1
                            year += 1
                            yearUpdate()

def fpsUpdate():
    InterractionsFPS()
    for creatures in creatureList:
        creatures.move()
    CreatureStatsFpsUpdate() 
    redrawGameWindow()
    MouseGeneralFunctions()
    TimePasses()

def secondUpdate():
    ActionsSECOND()

def minuteUpdate():
    GivenSuppliesPerMinute()
    CreatureStatsMinuteUpdate()
    CheckPregnancyAndGiveBirth()

def hourUpdate():
    pass

def dayUpdate():
    pass

def monthUpdate():
    pass

def yearUpdate():
    pass

#endregion

#region window drawings

def redrawGameWindow():
    displaySurface.blit(backgroundSprite, (0,0)) #refill the image with desired background color in order to erase everything
    drawObjects()
    if mouseX < 100 and mouseY < 200:
        drawInfo()
    pygame.display.update()

def drawObjects():
    for foods in foodList:
        foods.draw()
    for drinks in drinkList:
        drinks.draw()
    for creatures in creatureList: # draws each creature
        creatures.draw()

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

    pygame.draw.rect(displaySurface,black,(0,0,infoRectangleWidth+1,infoRectangleHeight+1))
    pygame.draw.rect(displaySurface,white,(0,0,infoRectangleWidth,infoRectangleHeight))


    myfont = pygame.font.SysFont('Comic Sans MS', infoTextSize)

    textsurface = myfont.render("males = " + str(numberOfMale), False, black)
    displaySurface.blit(textsurface,(10,0))

    textsurface = myfont.render("females = " + str(numberOfFemale), False, black)
    displaySurface.blit(textsurface,(10,offsetInfoTextPosition1))

    textsurface = myfont.render("pregnant = " + str(numberOfPregnantCreatures), False, black)
    displaySurface.blit(textsurface,(10,offsetInfoTextPosition1*2))

    textsurface = myfont.render("deaths = " + str(numberOfCreaturesThatDied), False, black)
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

def MouseGeneralFunctions():
    global mouseX
    global mouseY
    mouseX , mouseY = pygame.mouse.get_pos()
    # if pygame.mouse.get_pressed()[2]:
    #     foodList.append(food())
    #     foodList[-1].x = mouseX
    #     foodList[-1].y = mouseY
    # if pygame.mouse.get_pressed()[0]:
    #     drinkList.append(drink())
    #     drinkList[-1].x = mouseX
    #     drinkList[-1].y = mouseY

#endregion

LifeProjectInitialisation()

while run:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:#closing the window makes the simulation quit
            run = False 
      
    fpsUpdate()     
    clock.tick(fps)

quit()