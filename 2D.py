#OPENPOSE: TEXT TO SIGN LANGUAGE ANIMATION

#--Imports--
import sys, os, json, time, math, string
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame

#--Initialise Pygame--
pygame.init()


#--Miscellaneous Variable Definitions--\

#Window Size
width = 320
height = 224
#Used when skipping every 3rd value
count = 1
max = 3
#List of x,y co-ords of each keypoint
subList = []
#Current frame / current JSON file
curFrame = 3
#Digits within the current frame number
digits=1
#The json extension (example: hello_jsonExt.json)
jsonExt=""
#The current word in the sentence being processed
curWord = 0
#Size of text display
textSize = 20
#Initialises list of all available words
availableWordList = []
#Directory of raw jsons
jsonDirectory = 'GPUBinaries/openpose/raw_jsons'
#Defining colours
background = (0,0,60)
faceBase = (225,198,153)
eyeBase= (255,255,255)
red = (255,50,50)
green = (0,255,0)
blue = (0,0,255)
white = (255,255,255)
black = (0,0,0)
lipsBase = (100,0,0)
mouthInside = (50,0,0)
iris = (0,50,50)
baseBody = (200,150,120)
brow = (64,13,0)

#--Configure Size--

#Takes user input for screen size
while True:
    multiplierStr = input("Please enter a value between 1-4:\n1 = 320x224\n2 = 640x448\n3 = 960x672 (RECOMMENDED)\n4 = 1280x896\n")
    try:
        multiplier=int(multiplierStr)
        break
    except ValueError:
        pass

#--Generates sentenceList--

#Takes user input
sentence = input("\nEnter sentence for translation:\n")
#Remove Punctuation
sentence = sentence.translate(str.maketrans('', '', string.punctuation))
#Splits by whitespace into list
sentenceList=sentence.lower().split(" ")

#--Updated availableWordList usage--
for i in sentenceList:
    for fileName in os.listdir(jsonDirectory):
        if fileName == (i+"_000000000001_keypoints.json"):
            availableWordList.append(i)

#For every word in sentenceList
for i in sentenceList:
    #If it's an available word
    if i in availableWordList:
        #Do nothing
        pass
    #If not
    else:
        #Generate the missing word in letters for fingerspelling
        insert = list(i.upper())
        idx = sentenceList.index(i)
        #Replace in the sentenceList
        sentenceList = sentenceList[0:idx:] + insert + sentenceList[idx+1:len(sentenceList):]

#The length of words to sign
wordsInt = len(sentenceList)

width=width*multiplier
height=height*multiplier
textSize = textSize*multiplier

size = width, height

#Initialise pygame screen
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Kyro: "+' '.join(sentenceList))







#--Miscellaneous Function Definitions--

def DrawEllipse(coordList: list, index: int, col: tuple, weight: int, width: int, height: int):
    try:
        #Filters out untracked keypoints (if the keypoints are successfully tracked)
        if coordList[index][0] > 10*multiplier:
            #Defines a rectangle PyGame object within which the ellipse will be drawn
            r = pygame.Rect(0,0,width,height)
            #Centres the rectangle
            r.center = (coordList[index][0],coordList[index][1])
            #Draws ellipse
            pygame.draw.ellipse(screen,col,r,weight)
    except IndexError:
        pass

def DrawPoint(coordList: list,index: int,col: tuple,weight: int,xMod: int,yMod: int):
    #Converts weight parameter from diameter to radius
    weight = math.ceil(weight/2)
    try:
        #Filters out untracked keypoints (if the keypoints are successfully tracked)
        if coordList[index][0] > 10*multiplier:
            #Applies x and y modifiers
            coordList[index][0] = coordList[index][0]+xMod
            coordList[index][1] = coordList[index][1]+yMod
            #Draws circle
            pygame.draw.circle(screen,col,coordList[index],weight)
    except IndexError:
        pass

#Draws a misc. polygon
def DrawPoly(coordList: list, pointsList: list, col: tuple, weight: int):
    #Initialises list of all x,y points to be drawn
    drawList=[]
    try:
        for i in pointsList:
            #Filters out untracked keypoints (if the keypoints are successfully tracked)
            if coordList[i][0] > 10*multiplier:
                drawList.append(coordList[i])
        #Draws polygon connecting all the vertices in drawList
        pygame.draw.polygon(screen,col,drawList,weight)
    except IndexError:
        pass
    except ValueError:
        pass

#Draws a misc line
def DrawLine(coordList:list, pointsList: list, col: tuple, weight: int):
    #Initialises list of all x,y points to be drawn
    drawList=[]
    try:
        for i in pointsList:
            if coordList[i][0] > 10*multiplier:
                #Filters out untracked keypoints (if the keypoints are successfully tracked)
                drawList.append(coordList[i])
        #Draws a line connecting all the vertices in drawList
        pygame.draw.lines(screen,col,False,drawList,weight)
    except IndexError:
        pass
    except ValueError:
        pass


def DrawClothes():
    #--Display Body--
    try:
        lHip = (((width/2) + bodyKeypointList[2][0])/2,height)
        rHip = (((width/2) + bodyKeypointList[5][0])/2,height)
        lBicep = CalcMidpoint(bodyKeypointList[2],bodyKeypointList[3])
        rBicep = CalcMidpoint(bodyKeypointList[5],bodyKeypointList[6])
        lHigh = CalcMidpoint(bodyKeypointList[2],lBicep)
        rHigh = CalcMidpoint(bodyKeypointList[5],rBicep)
        mCore = CalcMidpoint(bodyKeypointList[1],(width/2,height))
        mFloor = (bodyKeypointList[1][0],height)
        mStomach = CalcMidpoint(mCore,mFloor)
        mNeck = CalcMidpoint(bodyKeypointList[0],bodyKeypointList[1])
        mNeckLower = CalcMidpoint(mNeck,bodyKeypointList[1])
        #See diagram
        clothingKeypointList=[bodyKeypointList[2],lHigh,lBicep,bodyKeypointList[5],rHigh,rBicep,mCore,mStomach,mFloor,lHip,rHip,mNeck,mNeckLower]
        DrawPoly(clothingKeypointList,[0,9,10,3],black,2*multiplier)
        DrawPoly(clothingKeypointList,[0,1,7,4,3],black,2*multiplier)
        DrawPoly(clothingKeypointList,[0,2,3],black,2*multiplier)
        DrawPoly(clothingKeypointList,[0,5,3],black,2*multiplier)
        DrawLine(clothingKeypointList,[0,3],black,22*multiplier)
        for i in range(2,7):
            DrawPoint(bodyKeypointList,i,black,22*multiplier,0,0)

        DrawPoly(clothingKeypointList,[0,9,10,3],red,0)
        DrawPoly(clothingKeypointList,[0,1,7,4,3],red,0)
        DrawPoly(clothingKeypointList,[0,2,3],red,0)
        DrawPoly(clothingKeypointList,[0,5,3],red,0)
        DrawLine(clothingKeypointList,[0,3],red,20*multiplier)
        for i in range(2,7):
            DrawPoint(bodyKeypointList,i,red,20*multiplier,0,0)
    except IndexError:
        pass

#Multiplies every point by the multiplier value
def Expand(pointsList):
    for i in range(len(pointsList)):
        pointsList[i][0]=pointsList[i][0]*multiplier
        pointsList[i][1]=pointsList[i][1]*multiplier
    return(pointsList)

#Returns the distance between two points
def CalcDistance(p1: tuple, p2: tuple):
    #d=√((x2 – x1)² + (y2 – y1)²)
    return math.ceil(math.sqrt(((p2[0] - p1[0])**2)+(p2[1]-p1[1])**2))

#Returns midppoint between two points
def CalcMidpoint(p1: tuple, p2: tuple):
    #(x₁ + x₂)/2, (y₁ + y₂)/2
    return ((math.ceil((p1[0]+p2[0])/2),math.ceil((p1[1]+p2[1])/2)))


#Displays entire avatar
def DisplayAvatar():
    
    #--Display Neck Outline--
    DrawLine(bodyKeypointList,[0,1],black,22*multiplier)
    #--Display Neck--
    DrawLine(bodyKeypointList,[0,1],baseBody,20*multiplier)
    
    DrawClothes()

    #--Display Arms Outlines--
    DrawLine(bodyKeypointList,[2,3,4],black,22*multiplier)
    DrawLine(bodyKeypointList,[5,6,7],black,22*multiplier)

    #--Display Arms--
    DrawLine(bodyKeypointList,[2,3,4],red,20*multiplier)
    DrawLine(bodyKeypointList,[5,6,7],red,20*multiplier)

    #--Display Ears--
    #Left Outline
    DrawEllipse(faceKeypointList,2,black,0,11*multiplier,16*multiplier)
    #Right Outline
    DrawEllipse(faceKeypointList,14,black,0,11*multiplier,16*multiplier)
    #Left
    DrawEllipse(faceKeypointList,2,faceBase,0,10*multiplier,15*multiplier)
    #Right
    DrawEllipse(faceKeypointList,14,faceBase,0,10*multiplier,15*multiplier)

    #--Display Head Outline--
    #Jaw
    DrawPoly(faceKeypointList,[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],black,2*multiplier)
    #Top of head
    try:
        headWidth = CalcDistance(faceKeypointList[16],faceKeypointList[0])
        headMidpoint = CalcMidpoint(faceKeypointList[16],faceKeypointList[0])
        r = pygame.Rect(0,0,headWidth+(1*multiplier),57*(multiplier)+(1*multiplier))
        r.center = (headMidpoint)
        pygame.draw.ellipse(screen,black,r,5*multiplier)
    except IndexError:
        pass

    #--Display Head--
    #Jaw
    DrawPoly(faceKeypointList,[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],faceBase,0)
    #Top of head
    try:
        headWidth = CalcDistance(faceKeypointList[16],faceKeypointList[0])
        headMidpoint = CalcMidpoint(faceKeypointList[16],faceKeypointList[0])
        r = pygame.Rect(0,0,headWidth,57*multiplier)
        r.center = (headMidpoint)
        pygame.draw.ellipse(screen,faceBase,r,0)
    except IndexError:
        pass

    #--Display Whites of Eyes--
    DrawPoly(faceKeypointList,[36,37,38,39,40,41],eyeBase,5*multiplier)
    DrawPoly(faceKeypointList,[42,43,44,45,46,47],eyeBase,5*multiplier)
    DrawPoint(faceKeypointList,36,eyeBase,4*multiplier,0,0)
    DrawPoint(faceKeypointList,39,eyeBase,4*multiplier,0,0)
    DrawPoint(faceKeypointList,42,eyeBase,4*multiplier,0,0)
    DrawPoint(faceKeypointList,45,eyeBase,4*multiplier,0,0)
    DrawPoly(faceKeypointList,[36,37,38,39,40,41],eyeBase,0)
    DrawPoly(faceKeypointList,[42,43,44,45,46,47],eyeBase,0)

    #--Display Pupils--
    DrawPoint(faceKeypointList,68,iris,5*multiplier,0,0)
    DrawPoint(faceKeypointList,69,iris,5*multiplier,0,0)
    DrawPoint(faceKeypointList,68,black,3*multiplier,0,0)
    DrawPoint(faceKeypointList,69,black,3*multiplier,0,0)
    DrawPoint(faceKeypointList,68,white,1*multiplier,+1,-1)
    DrawPoint(faceKeypointList,69,white,1*multiplier,+1,-1)

    #--Display Mouth--
    DrawPoly(faceKeypointList,[48,49,50,51,52,53,54,55,56,57,58,59],black,1*multiplier)
    DrawPoly(faceKeypointList,[48,49,50,51,52,53,54,55,56,57,58,59],lipsBase,0)
    DrawPoly(faceKeypointList,[60,61,62,63,64,65,66,67],mouthInside,0)

    #--Display Nose--
    DrawPoly(faceKeypointList,[27,28,29,30,31,32,33,34,35],baseBody,0)

    #--Display Eyebrows--
    DrawLine(faceKeypointList,[17,18,19,20,21],brow,1*multiplier)
    DrawLine(faceKeypointList,[22,23,24,25,26],brow,1*multiplier)

    #--Display Hands Outline --
    #Thumb
    DrawLine(lHandKeypointList,[0,1,2,3,4],black,5*multiplier)
    DrawLine(rHandKeypointList,[0,1,2,3,4],black,5*multiplier)
    #Index
    DrawLine(lHandKeypointList,[0,5,6,7,8],black,4*multiplier)
    DrawLine(rHandKeypointList,[0,5,6,7,8],black,4*multiplier)
    #Middle
    DrawLine(lHandKeypointList,[0,9,10,11,12],black,4*multiplier)
    DrawLine(rHandKeypointList,[0,9,10,11,12],black,4*multiplier)
    #Ring
    DrawLine(lHandKeypointList,[0,13,14,15,16],black,4*multiplier)
    DrawLine(rHandKeypointList,[0,13,14,15,16],black,4*multiplier)
    #Pinky
    DrawLine(lHandKeypointList,[0,17,18,19,20],black,4*multiplier)
    DrawLine(rHandKeypointList,[0,17,18,19,20],black,4*multiplier)
    #Palm
    DrawPoly(lHandKeypointList,[0,1,2,5,9,13,17],black,1)
    DrawPoly(rHandKeypointList,[0,1,2,5,9,13,17],black,1)
    #Joints
    for i in range(20):
        DrawPoint(lHandKeypointList,i,black,4*multiplier,0,0)
        DrawPoint(rHandKeypointList,i,black,4*multiplier,0,0)

    #--Display Hands--
    #Thumb
    DrawLine(lHandKeypointList,[0,1,2,3,4],faceBase,4*multiplier)
    DrawLine(rHandKeypointList,[0,1,2,3,4],faceBase,4*multiplier)
    #Index
    DrawLine(lHandKeypointList,[0,5,6,7,8],faceBase,3*multiplier)
    DrawLine(rHandKeypointList,[0,5,6,7,8],faceBase,3*multiplier)
    #Middle
    DrawLine(lHandKeypointList,[0,9,10,11,12],faceBase,3*multiplier)
    DrawLine(rHandKeypointList,[0,9,10,11,12],faceBase,3*multiplier)
    #Ring
    DrawLine(lHandKeypointList,[0,13,14,15,16],faceBase,3*multiplier)
    DrawLine(rHandKeypointList,[0,13,14,15,16],faceBase,3*multiplier)
    #Pinky
    DrawLine(lHandKeypointList,[0,17,18,19,20],faceBase,3*multiplier)
    DrawLine(rHandKeypointList,[0,17,18,19,20],faceBase,3*multiplier)
    #Palm
    DrawPoly(lHandKeypointList,[0,1,2,5,9,13,17],faceBase,0)
    DrawPoly(rHandKeypointList,[0,1,2,5,9,13,17],faceBase,0)
    #Joints
    for i in range(20):
        DrawPoint(lHandKeypointList,i,faceBase,3*multiplier,0,0)
        DrawPoint(rHandKeypointList,i,faceBase,3*multiplier,0,0)









#--PyGame Game Loop--
#Runs every frame
startTime=time.time()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    #--Reset a few variables after every frame--
    jsonExt=""
    bodyKeypointList=[]
    faceKeypointList=[]
    lHandKeypointList=[]
    rHandKeypointList=[]

    #--Calculate the current filename--
    for i in range(12-digits):
        jsonExt=jsonExt+"0"
    jsonExt=jsonExt+str(curFrame)
    jsonDir = "GPUBinaries/openpose/raw_jsons/" + sentenceList[curWord] + "_" + jsonExt +"_keypoints.json"

    #--Initialise Text Display--
    font = pygame.font.Font('freesansbold.ttf', textSize)
    text = font.render(sentenceList[curWord], True, white, None)
    textRect = text.get_rect()
    textRect.center = (width/2, height - textSize)

    #load into program as json in read mode
    try:
        with open(jsonDir,'r') as openfile:
            jsonObject = json.load(openfile)

            #--Collect Keypoints for Each Section--
            #Main Body Keypoints
            for i in jsonObject['people'][0]['pose_keypoints_2d']:
                #Skips every third value, in OpenPose every third value is the confidence level
                if (count < max):
                    subList.append(i)
                    count +=1
                else:
                    count = 1
                    bodyKeypointList.append(subList)
                    subList = []
            bodyKeypointList = Expand(bodyKeypointList)
            #Face Keypoints
            for i in jsonObject['people'][0]['face_keypoints_2d']:
                if (count < max):
                    subList.append(i)
                    count +=1
                else:
                    count = 1
                    faceKeypointList.append(subList)
                    subList = []
            faceKeypointList = Expand(faceKeypointList)
            #Right Hand Keypoints
            for i in jsonObject['people'][0]['hand_right_keypoints_2d']:
                if (count < max):
                    subList.append(i)
                    count +=1
                else:
                    count = 1
                    rHandKeypointList.append(subList)
                    subList = []
            rHandKeypointList = Expand(rHandKeypointList)
            #Left Hand Keypoints
            for i in jsonObject['people'][0]['hand_left_keypoints_2d']:
                if (count < max):
                    subList.append(i)
                    count +=1
                else:
                    count = 1
                    lHandKeypointList.append(subList)
                    subList = []
            lHandKeypointList = Expand(lHandKeypointList)

    #If we have reached the final frame
    except FileNotFoundError:
        #Increment the current word
        curWord+=1
        #If the last word was the final word, quit
        if curWord == wordsInt:
            endTime=time.time()
            print(endTime-startTime)
            quit()
        #Current frame / current JSON file reset
        curFrame = 3
        #Digits within the current frame number reset
        digits=1

    #Fill background colour before rendering on top
    screen.fill(background)

    #Display the avatar
    DisplayAvatar()

    screen.blit(text,textRect)
    pygame.display.flip()
    curFrame+=1
    digits = len(str(curFrame))
    time.sleep(0.03)