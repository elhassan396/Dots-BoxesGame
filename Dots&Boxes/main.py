import pygame
import sys
from random import choice
from pathlib import Path
#################### COLORS ###################

LIGHT_RED = (255,189,189)
RED = (255,0,0)
LIGHT_GREEN = (171,255,175)
GREEN = (0,255,0)

LIGHT_PURPLE = (245, 236 ,255)
PURPLE = (134, 71, 210)

PINK = (251, 0, 90)
BG_COLOR = (255,255,255)

########### Window Variables ##################
PAD = 100 # Top and left space from the Canva

CANVA_HEIGHT = 600 
CANVA_WIDTH = 800

SIZE = 100 #the size of a square , possible options : [20,25,40,50,100,200]

ROWS = CANVA_HEIGHT // SIZE # The number of squares along the y axis (of the canva ofc)
COLUMNS = CANVA_WIDTH // SIZE # The number of squares along the x axis

RIGHT_SPACE = 700 # the width of the space right to the canva
SW =  PAD + CANVA_WIDTH + RIGHT_SPACE
SH =  CANVA_HEIGHT + 2 * PAD
############## Selection Variables ######################
"""Here is how the selection process of a square works : 
-first we select a square (square = [COL,ROW])
-from that square we select a side using position variable (position= 3)   
"""
square = [0,0] #This tracks the selected square [COL,ROW]
position = 1 #This tracks the selected side of a square (there are 4 sides ofc)
index = 0 #An index used to change the position
####################   Scores   ########################
redScore = 0
greenScore = 0
########################################################
redToPlay = choice([True,False]) #if not red to play then ofc green 
FPS = 10 #We don't need a higher value for this kind of games
########################################################
"""Each time we confirm a valid selection we add it to the data map"""
data = {} #The data stored here like this {sq_1:[pos_1,pos_2,...],...}
#So we create a square which is a list , with max 4 elements
########################################################
"""when the four sides of a square are selected we add the color of the player and the square [color,sq_n]  """
completeSquares = []
################ dicts of images #################
"""These are used to store the images/sound objects"""
sounds = {}  
images = {}
numbers_img = {"r":{},"g":{}} # Used to draw the scores in the Gothic style ("r":"red","g":"green")
################################################
winner = "notYet" #the possible options : "RED" ,"GREEN" , "DRAW"
didAValidMove = False # go to updateCompleteSquares and updateData functions to understand this one 

helpMode = False #In this mode you can't select anything until it's quitted, used to show how the game should be played
revisionMode = False # In this mode you can't select anything as well ,just see what happened
music = True #used to turn music on/off
sound = True #used to turn sound on/off
#####################################################
screen = pygame.display.set_mode((SW,SH))
pygame.display.set_caption("Squary")
clock = pygame.time.Clock()
pygame.init()
#####################################################
"""
Convert2Str is a helper function, because lists are not hashbal in python, meaning a list connot be a key in a dict
,but because using a list as a key is for me a good decision , I created this together with Convert2List to be like 
an intermediate between str and list in the key, so in the data map , we store the square key like this
X-Y- instead of [X,Y], and then when we need to do some computations with the actuall int X and Y we extract from "X-Y-" the list [X,Y] using Convert2List
"""
###################################### Helper Functions ##################################################
def loadAssests():
    global sounds,images,numbers_img
    path = Path(__file__).resolve().parent
    #Load sounds
    sounds_ = ["invalid","buttonClick","squareCompleted","valid","victory","draw","sizeChanged"]
    for sound in sounds_:
        #Edge case
        if sound == "buttonClick":
            sounds[sound] = pygame.mixer.Sound(f"{path}/Sounds/{sound}.wav")
            continue
        sounds[sound] = pygame.mixer.Sound(f"{path}/Sounds/{sound}.mp3")
    
    #Load bg music
    pygame.mixer.music.load(f"{path}/Sounds/bg_music.mp3")

    #Load images
    images_ = ["bg","main","green","red","winDow_r","winDow_g","draw","helpLogo","help","music_on","music_off","sound_on","sound_off"]
    for image in images_:
        images[image] = pygame.image.load(f"{path}/Images/{image}.png")

    #Load images for the Score font
    numbers = ["zero","one","two","three","four","five","six","seven","eight","nine"]
    for color in ["r","g"]:
        for number in numbers:
            numbers_img[color][number] = pygame.image.load(f"{path}/Images/Numbers/{color}/{number}_{color}.png")
            
loadAssests()

def Convert2Str(l):
    return f"{l[0]}-{l[1]}-"

def Convert2List(s:str):
    result = []
    temp = []
    for letter in s:
        if letter == "-":
            result.append(int("".join(temp)))
            temp = []
        else:
            temp.append(letter)
    return result

"""Used to help drawing the selected side of a square"""
def convertSqPos2XY(square,position):    
    X = PAD + (square[0]) * SIZE
    Y = PAD + (square[1]) * SIZE
    mapP2XY = {
            0:[(X,Y),(X+SIZE,Y)], 
            1:[(X+SIZE,Y),(X+SIZE,Y+SIZE)],
            2:[(X,Y+SIZE),(X+SIZE,Y+SIZE)],
            3:[(X,Y),(X,Y+SIZE)]
            }
    return mapP2XY[position]
    
###############################################Update Functions################################################
def updateScores(color):
    global redScore,greenScore
    if color == "red":
        redScore +=1
    else:
        greenScore +=1
        
def updateData():
    global data,position,square,didAValidMove
     
    c = square[0] 
    r = square[1]
    map_1 = {
        0:(c,r-1),
        1:(c+1,r),
        2:(c,r+1),
        3:(c-1,r)
            }
    square_ = Convert2Str(square) 
    if not (position in data[square_]):#If it's not already selected
        data[square_].append(position)
        #don't forget to add the corresponding position to the square that shares that side
        directions = [(c,r-1),(c-1,r),(c,r+1),(c+1,r)]
        #f_direction are the directions that are inside the Canva
        f_directions = filter(lambda T:(T[0] >= 0 and T[1] >= 0) and (T[0] <= COLUMNS-1 and T[1] <= ROWS-1) ,directions)
        if map_1[position] in f_directions:
            map_2 = {1:3,3:1,2:0,0:2}#if two squares share a side, then that side definition depend on the square, it may be the left one for a square and the right one for the othre , so we use this map_2 to define this...   
            data[Convert2Str(map_1[position])].append(map_2[position])
        didAValidMove = True 
         
        if sound:
            #if the sound is on , play the valid move sound
            pygame.mixer.Sound.play(sounds["valid"])
    else: #if it's already selected
        if sound:
            pygame.mixer.Sound.play(sounds["invalid"])

def updateCompleteSquares():
    global data,completeSquares,redToPlay,didAValidMove
    #color of the player that played the last move (we didn't change redToPlay yet)
    color = "red" if redToPlay else "green"
    init_scores = [redScore,greenScore] #Those are the scores before any completeSquare is added
    for square_ in data.keys(): #square_ here is something like this : "X-Y-"
        #Remember this square variable here is not the global one just the local one
        square = Convert2List(square_)
        if not ( ([square,"red"] in completeSquares) or ([square,"green"] in completeSquares) ) :#first check if that square is already registered as complete
            #handle first the corners because they need only 2 positions to complete a square
            if square in [[0,0],[COLUMNS-1,0],[0,ROWS-1],[COLUMNS-1,ROWS-1]]:#check if that square is in the corner
                if len(data[square_]) == 2: #Check first if it's full
                    completeSquares.append([square,color])# add the square together with its color
                    updateScores(color)
                    if sound:
                        pygame.mixer.Sound.play(sounds["squareCompleted"])
                        
            #Now handle the squares that touch the edges but not in the corners , they need 3 positions
            #Pay attention here , this condition take care of the four edges including the corners, but because 
            #we already checked the corners in the first condition and we are using elif , this only take care of the edges without the corners
            
            elif ((square[0] in [0,COLUMNS-1]) or (square[1] in [0,ROWS-1])):
                if len(data[square_]) == 3:
                    completeSquares.append([square,color])
                    updateScores(color)
                    if sound:
                        pygame.mixer.Sound.play(sounds["squareCompleted"])
            #Here we are in the center of the grid
            else:
                if len(data[square_]) == 4:
                    completeSquares.append([square,color])
                    updateScores(color)
                    if sound:
                        pygame.mixer.Sound.play(sounds["squareCompleted"])
    #After updating the completeSquares check if there is any update  , if there is then we should allow him to play again
    if (init_scores == [redScore,greenScore]) and didAValidMove: #Nothing new
        redToPlay = not redToPlay
    #After we update the perfectSquares we should reset didAValidMove to False.
    didAValidMove = False    
            

        
"""
We use this initialize function to init some variables when we go back from the menu , everything should be init..
to avoid some problems
"""  
def initialize():
    global data,square,position,index,ROWS,COLUMNS,completeSquares,greenScore,redScore,redToPlay,winner,revisionMode

    greenScore = 0
    redScore = 0
    
    redToPlay = choice([True,False]) #random player to start
    
    square = [0,0]
    position = 1
    index = 0
    
    ROWS = CANVA_HEIGHT // SIZE
    COLUMNS = CANVA_WIDTH // SIZE
    
    winner = "notYet"
    revisionMode = False
    
    completeSquares.clear()
    #Init data with empty squares
    data.clear()
    for c in range(COLUMNS):
        for r in range(ROWS):
            data[Convert2Str([c,r])] = []

##########################################Drawing Functions##############################################
def drawScoreUsingImgsFromInt(x_1,x_2,height):
    #50x80px
    size = abs(x_2 - x_1)
    map = dict(enumerate(["zero","one","two","three","four","five","six","seven","eight","nine"]))

    for color in ["r","g"]:
        s_p = x_1 if color == "r" else x_2
        score = str(greenScore) if color == "g" else str(redScore)

        if len(score) == 1:
            offset = (size // 2) - (50 // 2)
            screen.blit(numbers_img[color][map[int(score)]],( s_p + offset , height ))

        elif len(score) == 2:
            offset = (size // 2) - 50
            screen.blit(numbers_img[color][map[int(score[0])]],( s_p + offset , height ))
            screen.blit(numbers_img[color][map[int(score[1])]],( s_p + offset + 50 , height ))

        elif len(score) == 3:
            offset = (size // 2) - 50 - (50 // 2)
            screen.blit(numbers_img[color][map[int(score[0])]],( s_p + offset , height ))
            screen.blit(numbers_img[color][map[int(score[1])]],( s_p + offset + 50 , height ))
            screen.blit(numbers_img[color][map[int(score[2])]],( s_p + offset + 50 + 50 , height ))

def drawScoreGUIDynamicParts():
    #draw the scores
    drawScoreUsingImgsFromInt(920,1250,210)
    #draw who to play next
    if redToPlay:
        screen.blit(images["red"],(PAD+CANVA_WIDTH+20+ (RIGHT_SPACE - 2 * 20) // 2 - 75,6*PAD//4 - 30))
    else:
        screen.blit(images["green"],(PAD+CANVA_WIDTH+20+ (RIGHT_SPACE - 2 * 20) // 2 -75,6*PAD//4 - 30))

def renderText(text,family,size,center,fg,bg):
    font = pygame.font.SysFont(family,size,bold=True)
    surf = font.render(text,True,fg,bg)
    rect = surf.get_rect(center=center)
    screen.blit(surf,rect)

def drawCompleteSquares():
    for completeSquare in completeSquares:
        X = PAD + (completeSquare[0][0]) * SIZE
        Y = PAD + (completeSquare[0][1]) * SIZE
        color = LIGHT_RED if completeSquare[1] == "red" else LIGHT_GREEN
        pygame.draw.rect(screen,color,pygame.Rect(X,Y,SIZE,SIZE),width=SIZE)
               
def drawGrid():
    v_lines = [[(PAD+i*SIZE,PAD),(PAD+i*SIZE,PAD+ CANVA_HEIGHT)] for i in range(1,COLUMNS)] #vertical lines
    h_lines = [[(PAD,PAD + i *SIZE),(PAD+CANVA_WIDTH,PAD+i*SIZE)] for i in range(1,ROWS)] #horizontal lines
    
    for line in v_lines + h_lines:
        pygame.draw.line(screen,"gray",line[0],line[1],1)


def drawData():
    """draw the selected lines"""
    for square in data.keys(): #again!! ,a square here is a string,we need to convert it
        for position in data[square]:
                coordinates = convertSqPos2XY(Convert2List(square),position)
                pygame.draw.line(screen,"PURPLE",coordinates[0],coordinates[1],width=3)
                
def drawCursor():
    coordinates = convertSqPos2XY(square,position)
    #use a line as the cursor (not recommended!!)
    # pygame.draw.line(screen,"pink",coordinates[0],coordinates[1],width=5)   
    color = "PURPLE"
    pygame.draw.circle(screen,color,((coordinates[0][0]+coordinates[1][0])//2,(coordinates[0][1]+coordinates[1][1])//2),5,width=5)
        
def animateExit(center):
    FPS = 60 
    i = 0
    while i < 35:
        #We may not need this here if the animation is fast 
        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         pygame.quit();sys.exit()
        
        pygame.draw.circle(screen,PINK,center,5 + i *50 ,5 + i *50)
        i+=1
        
        pygame.display.update()
        clock.tick(FPS)

def drawSelectedSquare():
    X = PAD + (square[0]) * SIZE
    Y = PAD + (square[1]) * SIZE
    pygame.draw.rect(screen,LIGHT_PURPLE,pygame.Rect(X,Y,SIZE,SIZE),width=SIZE)
    
def drawHelpLogo():
    #30x51
    screen.blit(images["helpLogo"],(1600 - 30 - 20, 5 ))
    
def drawMusicLogo():
    #30x35
    screen.blit(images["music_on"] if music else images["music_off"],(1600 - 30 * 2 - 20 - 30, 35 ))
    
def drawSoundLogo():
    #30x35
    screen.blit(images["sound_on"] if sound else images["sound_off"],(1600 - 30 * 3 - 20 - 50, 35 ))

################################################################################################################

def winDow():
    """This is the last window showen after a round is completed"""
    global goToMenu,revisionMode
    
    if winner == "GREEN":
        screen.blit(images["winDow_g"],(0,0))
        drawScoreUsingImgsFromInt(0,800,400)
        
    elif winner == "RED":
        screen.blit(images["winDow_r"],(0,0))
        drawScoreUsingImgsFromInt(0,800,400)
        
    else:#draw
        screen.blit(images["draw"],(0,0))
        
    running  = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit();sys.exit()
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                if pygame.Rect(640,580,321,96).collidepoint(pos[0],pos[1]): # clicking on "Go back to Menu" button
                    if sound:       
                        pygame.mixer.Sound.play(sounds["buttonClick"])
                    revisionMode = False #don't do revision , just go to the menu
                    animateExit(pos)
                    running = False
                    break
                    
                elif pygame.Rect(719,686,161,38).collidepoint(pos[0],pos[1]): #go to the game for revision
                    if sound:
                        pygame.mixer.Sound.play(sounds["buttonClick"])
                    revisionMode = True
                    screen.blit(images["main"],(0,0))
                    running = False
                    break
            
        pygame.display.update()
        clock.tick(FPS)
    
def menu():
    global SIZE
    SIZES = [20,25,40,50,100,200]
    pygame.mixer.music.play(-1,0,5000)
    pygame.mixer.music.set_volume(0.2)
    
    screen.blit(images["bg"],(0,0))
    renderText(f" {SIZE} ","monospace",32,(800,475),"white",PURPLE)
    
    size_index = SIZES.index(SIZE)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit();sys.exit()
                
            if event.type == pygame.KEYDOWN:#Change the size
                if event.key == pygame.K_LEFT:
                    size_index = (size_index - 1) % len(SIZES)
                    SIZE = SIZES[size_index]
                    renderText(f" {SIZE} ","monospace",32,(800,475),PINK,BG_COLOR)
                    pygame.mixer.Sound.play(sounds["sizeChanged"])
                    
                elif event.key == pygame.K_RIGHT:
                    size_index = (size_index + 1) % len(SIZES)
                    SIZE = SIZES[size_index]
                    renderText(f" {SIZE} ","monospace",32,(800,475),PINK,BG_COLOR)
                    pygame.mixer.Sound.play(sounds["sizeChanged"])
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                
                if pygame.Rect(700,550,200,100).collidepoint(pos[0],pos[1]):#CLick on start button
                    if sound:
                        pygame.mixer.Sound.play(sounds["buttonClick"])
                    animateExit(pos)
                    
                    initialize()

                    mainGame()

                    screen.blit(images["bg"],(0,0))
                    renderText(f" {SIZE} ","monospace",32,(800,475),"white",PURPLE)
                    
                elif pygame.Rect(700,450,50,50).collidepoint(pos[0],pos[1]):
                    size_index = (size_index - 1) % len(SIZES)
                    SIZE = SIZES[size_index]
                    renderText(f" {SIZE} ","monospace",32,(800,475),"white",PURPLE)
                    if sound:
                        pygame.mixer.Sound.play(sounds["sizeChanged"])
                    
                elif pygame.Rect(850,450,50,50).collidepoint(pos[0],pos[1]):
                    size_index = (size_index + 1) % len(SIZES)
                    SIZE = SIZES[size_index]
                    renderText(f" {SIZE} ","monospace",32,(800,475),"white",PURPLE)
                    if sound:
                        pygame.mixer.Sound.play(sounds["sizeChanged"])


        pygame.display.update()
        clock.tick(FPS)


def mainGame():
    
    global square,position,index,winner,revisionMode,helpMode,music,sound
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit();sys.exit()
                
            elif event.type == pygame.MOUSEBUTTONDOWN :
                pos = pygame.mouse.get_pos()
                
                if not (pygame.Rect(620,77,915,431).collidepoint(pos[0],pos[1])) and helpMode: #disable the helpMode if he clicked outside the help popUp box
                    helpMode = False
                    
                elif (pygame.Rect(1552,28,25,47).collidepoint(pos[0],pos[1])) and not helpMode: #enable the help mode (you can't with the help mode active)
                
                    if sound:
                        pygame.mixer.Sound.play(sounds["buttonClick"])
                    helpMode = True
                    
                elif (pygame.Rect(1600 - 30 * 2 - 20 - 30, 35 ,30,35).collidepoint(pos[0],pos[1])) and not helpMode:   #enable/disable music (you can't with the help mode active)
                
                    if sound:     
                        pygame.mixer.Sound.play(sounds["buttonClick"])
                        
                    if music:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
                        
                    music = not music
                    
                elif (pygame.Rect(1600 - 30 * 3 - 20 - 50, 35 ,30,35).collidepoint(pos[0],pos[1])) and not helpMode:  #enable/disable sound (you can't with the help mode active)
                    if sound :
                        pygame.mixer.Sound.play(sounds["buttonClick"]) 
                    sound = not sound

                elif pygame.Rect(15,15,120,70).collidepoint(pos[0],pos[1]) and not helpMode: #Go to the Menu (you can't with the help mode active)

                    if sound:
                        pygame.mixer.Sound.play(sounds["buttonClick"])
                    running =  False
                    break 
                #selection of a square in the canva
                elif pygame.Rect(PAD,PAD,CANVA_WIDTH,CANVA_HEIGHT).collidepoint(pos[0],pos[1]) and not (revisionMode or helpMode): #you can't select a square with the help/revision Mode active
                    
                    col = (pos[0] - PAD) // SIZE
                    row = (pos[1] - PAD) // SIZE
                    square = [col,row]
                    
                    if col == 0:
                        if row == 0 :#top_left corner
                            position = (2 if position == 0 else 1) if position in (0,3) else position
                        elif row == (ROWS-1):#bottom_left corner
                            position = (0 if position == 2 else 1) if position in (2,3) else position
                            
                        else:#first column without the corners
                            position = 1 if position == 3 else position
                            index = [0,1,2].index(position)
                          
                    elif col == (COLUMNS-1):
                        if row == 0 :#top_right corner
                            position = (2 if position == 0 else 3) if position in (0,1) else position
                            
                        elif row == (ROWS-1):#bottom_right corner
                            position = (3 if position == 1 else 0) if position in (1,2) else position
                        else:#last column without the corners
                            position = 3 if position == 1 else position
                            index = [0,2,3].index(position)
                            
                    elif row == 0:#top row without the corners
                        position = 2 if position == 0 else position
                        index = [1,2,3].index(position)
                        
                    elif row == (ROWS-1):#bottom row without the corners
                        position = 0 if position == 2 else position
                        index = [0,1,3].index(position) 
                        
                    # else:#In the middle we don't need to do this
                    #     pass         
            if (event.type == pygame.KEYDOWN) and not (revisionMode or helpMode):  #In help mode or revision mode we don't allow switching the position or confirmation os a selction
                if event.key == pygame.K_RETURN:          
                    updateData()
                    updateCompleteSquares()

                    if len(completeSquares) == ROWS * COLUMNS:#There is nothing else to select
                        if redScore < greenScore:

                            winner = "GREEN"
                            if sound:
                                pygame.mixer.Sound.play(sounds["victory"])
            
                        elif redScore > greenScore:

                            winner = "RED"
                            if sound:
                                pygame.mixer.Sound.play(sounds["victory"])
            
                        else:

                            winner = "DRAW"
                            if sound:
                                pygame.mixer.Sound.play(sounds["draw"])
                        #draw for the last time 
                        drawCompleteSquares()
                        drawData()
                        drawCursor()
                        drawScoreGUIDynamicParts()
                        pygame.display.update()
                        #wait a little bit for the players to see what just happened
                        pygame.time.delay(2000)
                        #Enter the Win-Dow 
                        winDow()
                        #Check now what the user choose , go to the menu or do revision
                        if not revisionMode: #if the player didn't select revision mode , just go to the menu
                            running  = False
                            break 

                elif event.key ==  pygame.K_m  :
                    if square[1] == 0:
                        if square[0] == 0 :
                            index = (index+1) % 2
                            position = [1,2][index if [1,2][index] != position else (index+1) % 2]
                        elif square[0] == (COLUMNS - 1):
                            index = (index+1) % 2
                            position = [2,3][index if [2,3][index] != position else (index+1) % 2]
                        else:
                            index = (index+1) % 3
                            position = [1,2,3][index if [1,2,3][index] != position else (index+1) % 3]
                    elif square[1] == (ROWS-1):  
                        if square[0] == 0 :
                            index = (index+1) % 2
                            position = [0,1][index if [0,1][index] != position else (index+1) % 2]
                        elif square[0] == (COLUMNS - 1):
                            index = (index+1) % 2
                            position = [0,3][index if [0,3][index] != position else (index+1) % 2]
                        else:
                            index = (index+1) % 3
                            position = [0,1,3][index if [0,1,3][index] != position else (index+1) % 3]
                    elif square[0] == 0 and (square[1] not in (0,ROWS-1)):  
                        index = (index+1) % 3
                        position = [0,1,2][index if [0,1,2][index] != position else (index+1) % 3]
                    elif square[0] == (COLUMNS -1) and (square[1] not in (0,ROWS-1)):  
                        index = (index+1) % 3
                        position = [0,2,3][index if [0,2,3][index] != position else (index+1) % 3]
                    else:
                        index = (index+1) % 4
                        position = [0,1,2,3][index if [0,1,2,3][index] != position else (index+1) % 4]
                        
        if not running : break 
            
         
        screen.blit(images["main"],(0,0))
        # clear for the canva part
        screen.fill(BG_COLOR,pygame.Rect(PAD,PAD,CANVA_WIDTH,CANVA_HEIGHT))
        drawSelectedSquare()
        drawGrid()
        drawCompleteSquares()
        drawData()
        drawCursor()
        drawScoreGUIDynamicParts()
        drawHelpLogo()
        drawMusicLogo()
        drawSoundLogo()
        if helpMode: #Only draw it when the help mode is active
            screen.blit(images["help"],(0,0))

        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    menu()

