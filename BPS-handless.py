# * Bot Paper Scissors
# * Shiva Nathan (15-112 G)
# * 4 May 2017

#Incorporates code for hand detection and finger tracking by Zane Lee
#taken on 26 April 2017
#https://github.com/lzane/Fingers-Detection-using-OpenCV-and-Python/blob/master/new.py

#Does not use bionic hand for gameplay
import random
import cv2
import numpy as np
import math
import string
import time
import copy
import decimal


## begin all functions written exclusively by Shiva Nathan
def init(data):
    data.difficulty = "e" # e for easy, i for impossible
    data.waitTime = 10 #milliseconds for waitKey to process image
    data.loop = False 
    data.roundCount = 1
    data.timer = 0 #time elapsed in each round
    data.roundTimer = 20
    data.numRounds = 5 #best of 5
    data.displayMoves = ["Rock...","Paper...","Scissors...","Shoot!"]
    data.font = cv2.FONT_HERSHEY_SIMPLEX #font for OpenCV GUI
    data.fontSize = 1 #font size for OpenCV GUI
    data.offset = 50 #offset value for adjusting text position
    data.fingerCount = 0 #number of fingers detected by OpenCV
    data.playerMove = ""
    data.bionicMove = ""
    data.roundWinner = ""
    data.finalWinner = "" #overall game winner
    data.playerScore = 0
    data.bionicScore = 0
    data.startColor = (0,0,255) #red, color of text
    data.fieldColor = (255, 255, 0) #black, color of game field
    data.endColor = data.startColor
        
def startScreen(cv2,data):
    #splash screen, prompt users to start game or learn how to play
    offset = data.offset
    print('showing startScreen')
    cv2.putText(data.img,'BOT PAPER SCISSORS',(int(data.width//2),int(data.height//4)),
                   data.font, data.fontSize,data.startColor,2,2)
    cv2.putText(data.img,'Press B to begin new game on Easy',(int(data.width//2),int(data.height//2)),
                   data.font, data.fontSize,data.startColor,2,2)
    cv2.putText(data.img,'Press H to learn how to play',(int(data.width//2),int(2*data.height//3)),
                   data.font, data.fontSize,data.startColor,2,2)
    cv2.putText(data.img,'Press Z to begin new game on IMPOSSIBLE',(int(data.width//2),int(5*data.height//6)),
                   data.font, data.fontSize,data.startColor,2,2)
    cv2.waitKey(data.waitTime)
    cv2.imshow('data.img',data.img)
    
def endScreen(cv2,data):
    #end screen, show final scores and winner
    offset = data.offset
    print('showing endScreen')
    yourScore = "Your Score: %s" % data.playerScore
    theirScore = "Bionic Score: %s" % data.bionicScore
    cv2.putText(data.img,yourScore,(int(data.width//3),int(2*data.height//3)),
                   data.font, data.fontSize,data.endColor,2,2)
    cv2.putText(data.img,theirScore,(int(5*data.width//6),int(2*data.height//3)),
                   data.font, data.fontSize,data.endColor,2,2)
    cv2.waitKey(data.waitTime)
                   
    finalVictor = "The victor is %s! Congratulations!" % data.finalWinner
    print(finalVictor)
    cv2.putText(data.img,finalVictor, (int(data.width//2),int(data.height//4)),
                                        data.font, data.fontSize,data.endColor,2,2)
    text = 'Press R to return to the starting screen!'
    print(text)
    cv2.putText(data.img,text, (int(data.width//2),int(data.height//4)+2*data.offset),
                                        data.font, data.fontSize,data.endColor,2,2)
    cv2.imshow('data.img',data.img)
    
def helpScreen(cv2,data):
    #help screen, explains how to play
    offset = data.offset
    print('showing helpScreen')
    
    prompt1 = "Welcome to Bot Paper Scissors!"
    prompt2 = "Be sure to read all the instructions before starting!"
    prompt3 = "The cyan rectangle is the game field."
    prompt3a = "Step 0: Make sure your hand or body isn't in the game field."
    prompt3b = "Otherwise the game won't be able to detect your moves properly."
    prompt4 = "Step 1: Press B to calibrate the game field."
    prompt5 = "Step 2: You will be prompted to put your hand into the game field."
    prompt6 = "When you do so, the game will begin."
    prompt7 = "You can take your hand out of the game field to pause the game."
    prompt7a = "To continue, just put your hand back into the game field."
    prompt8 = "Step 3: Play the game! Make sure your move is inside the game field."
    prompt9 = "The game goes to best of %d. Good luck!" % data.numRounds
    prompt10 = "Press R to return to the starting screen. Press B to start the game."
    
    promptList = [prompt1,prompt2,prompt3,prompt3a,prompt3b,prompt4,
                   prompt5,prompt6,prompt7,prompt7a,prompt8,prompt9,prompt10]
    
    #display each prompt in sequence of promptList
    for i in range(len(promptList)):
        cv2.putText(data.img,promptList[i],
                    (int(data.width//2)-4*offset,int(i*data.height//9)+offset),
                    data.font, 0.75*data.fontSize,data.endColor,2,2)
    cv2.imshow('data.img',data.img)
    
    
def pauseScreen(cv2,data):
    #prompt user to continue playing if hand leaves frame
    offset = data.offset
    prompt = "Game paused. Put your hand back in the frame to continue!"
    cv2.putText(data.img,prompt,(int(data.width//2)-2*data.offset,int(data.height//2)),
    data.font, data.fontSize,data.endColor,2,2)
    
def fakeBionic(cv2,data):
    #simulate movement of bionic hand without needing hand
    move = ""
    #randomly choose rock,paper,scissors, or gun
    i = random.randint(0,100)
    if (i < 32): move = "r"
    elif (i < 64): move = "p"
    elif (i < 96): move = "s"
    elif (i < 100): move = "g"
    return move

def cheatFakeBionic(cv2,data):
    #make move that will beat player's move 
    #simulate movement of bionic hand without needing hand
    move = ""
    #make move that beats player
    if data.playerMove == 's': move = "r"
    elif data.playerMove == 'r': move = "p"
    elif data.playerMove == 'p': move = "s"
    return move

def fakePlayer(cv2,data):
    #test function to simulate human movement without camera
    i = random.randint(0,100)
    if (i < 34): move = "r"
    elif (i < 67): move = "p"
    elif (i < 100): move = "s"
    return move
    
def determineWinner(cv2,data):
    #determines winner of round
    winner = ""
    bionicMove = data.bionicMove
    playerMove = data.playerMove
    print("bionic: %s, player: %s") % (bionicMove, playerMove)
    
    #if bionic move is gun, it wins by default
    if (bionicMove == "g"): winner = "bionic"
    #otherwise, compare rock vs paper vs scissors
    elif (bionicMove == "r"):
        if (playerMove == "r"): winner = "tie"
        elif (playerMove == "p"): winner = "player"
        elif (playerMove == "s"): winner = "bionic"
    elif (bionicMove == "p"):
        if (playerMove == "r"): winner = "bionic"
        elif (playerMove == "p"): winner = "tie"
        elif (playerMove == "s"): winner = "player"
    elif (bionicMove == "s"):
        if (playerMove == "r"): winner = "player"
        elif (playerMove == "p"): winner = "bionic"
        elif (playerMove == "s"): winner = "tie"

    return winner
    
            
def displayCountdown(cv2,data): #display RPS countdown
    offset = data.offset
    #because time.sleep pauses camera, have to rely on passes through main loop to count time
    i = data.timer//2
    
    #Display round number
    round = "Round %d" % data.roundCount
    cv2.putText(data.img,round,(int(data.width//2-0.25*offset),int(data.height//4+0.5*data.offset)),
                data.font, data.fontSize,data.endColor,2,2)
    
    #Increment through displayMoves list to show rock-paper-scissors-shoot countdown
    if i < len(data.displayMoves):
        print(data.displayMoves[i])
        cv2.putText(data.img,data.displayMoves[i],
                (int(data.width//2)-offset,int(data.height//2+i*data.height//6)),
                data.font, data.fontSize,data.endColor,2,2)
    
    
def playRound(cv2,data): #determine moves and winner, increment their score, increment round

    #how many round wins to be declared victor
    bestOf = data.numRounds - data.numRounds // 2
    print("count:",data.fingerCount)
        
    #determine player move    
    if data.fingerCount == 0: data.playerMove = 'r'
    elif data.fingerCount < 3: data.playerMove = 's'
    else: data.playerMove = 'p'
    
    #make bionic move depending on difficulty
    if data.difficulty == 'i': data.bionicMove = cheatFakeBionic(cv2,data)
    elif data.difficulty == 'e': data.bionicMove = fakeBionic(cv2,data)
    
    #determine winner and increment their score
    data.roundWinner = determineWinner(cv2,data)
    if (data.roundWinner == "bionic"): data.bionicScore += 1
    elif (data.roundWinner == "player"): data.playerScore += 1
    
    #debugging print statements
    print("playerMove:",data.playerMove)        
    print("bionicMove:",data.bionicMove)
    print("the winner is:",data.roundWinner)
    
    #if a player has reached best of numRounds, end the game
    if data.bionicScore >= (bestOf):
        data.finalWinner = "the bionic hand!"
        data.isBgCaptured = -1
    elif data.playerScore >= (bestOf):
        data.finalWinner = "you!"
        data.isBgCaptured = -1
    
    
def displayWinner(cv2,data): #show text for winner
    offset = data.offset
    winningText = "Winner: %s" % data.roundWinner
    print (winningText)
    cv2.putText(data.img,winningText,(int(data.width//2)-offset,int(data.height//2)),
                data.font, data.fontSize,data.endColor,2,2)


def displayGameData(cv2,data): #display round number, players' moves, and players' scores
    offset = data.offset
    if data.playerMove == "r": yourMove = "rock"
    elif data.playerMove == "p": yourMove = "paper"
    elif data.playerMove == "s": yourMove = "scissors"
    
    if data.bionicMove == "r": theirMove = "rock"
    elif data.bionicMove == "p": theirMove = "paper"
    elif data.bionicMove == "s": theirMove = "scissors"
    elif data.bionicMove == "g": theirMove = "GUN! BANG!"
    
    #display round
    round = "Round %d" % data.roundCount
    cv2.putText(data.img,round,(int(data.width//2-0.25*offset),int(data.height//4+0.5*data.offset)),
                data.font, data.fontSize,data.endColor,2,2)
    
    #display moves
    yourMove = "Your Move: %s" % yourMove
    cv2.putText(data.img,yourMove,(int(data.width//4 - data.offset),int(3*data.height//4)),
                data.font, data.fontSize,data.endColor,2,2)
    theirMove = "Their Move: %s" % theirMove
    cv2.putText(data.img,theirMove,(int(data.width//4 - data.offset),int(5*data.height//6)),
                data.font, data.fontSize,data.endColor,2,2)
             
    #display scores
    yourScore = "Your Score: %s" % data.playerScore
    cv2.putText(data.img,yourScore,(int(data.width//6 - 0.5*data.offset),int(data.height//6)),
                   data.font, data.fontSize,data.endColor,2,2)
    theirScore = "Bionic Score: %s" % data.bionicScore
    cv2.putText(data.img,theirScore,(int(3*data.width//6 + data.offset),int(data.height//6)),
                   data.font, data.fontSize,data.endColor,2,2)


## end all functions written exclusively by Shiva Nathan


##begin code written by Zane Lee and Shiva Nathan

def run():
    #create and initialize data structure
    class Struct(object): pass
    data = Struct()
    init(data)
    
    ## begin parameters and functions exclusively by Zane Lee
    cap_region_x_begin=0.5  # start point/total width
    cap_region_y_end=0.8  # start point/total width
    data.threshold = 60  #  BINARY threshold
    blurValue = 41  # GaussianBlur parameter
    bgSubThreshold = 50
    # variables by Zane Lee
    data.isBgCaptured = 0   # checks mode and if the background was captured
    triggerSwitch = False  # if true, keyborad simulator works


    def printThreshold(thr): #written by Zane Lee
        print("! Changed threshold to "+str(thr))
    
    def removeBG(frame): 
        fgmask = bgModel.apply(frame)
        # kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        # res = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
    
        kernel = np.ones((3, 3), np.uint8)
        fgmask = cv2.erode(fgmask, kernel, iterations=1)
        res = cv2.bitwise_and(frame, frame, mask=fgmask)
        return res
    
    def calculateFingers(res,drawing):  # -> finished bool, data.fingerCount: finger count
        #  convexity defect
        hull = cv2.convexHull(res, returnPoints=False)
        if len(hull) > 3:
            defects = cv2.convexityDefects(res, hull)
            if type(defects) != type(None):  # avoid crashing.   (BUG not found)
    
                data.fingerCount = 0
                for i in range(defects.shape[0]):  # calculate the angle
                    s, e, f, d = defects[i][0]
                    start = tuple(res[s][0])
                    end = tuple(res[e][0])
                    far = tuple(res[f][0])
                    a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
                    b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
                    c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
                    angle = math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c))  # cosine theorem
                    if angle <= math.pi / 2:  # angle less than 90 degree, treat as fingers
                        data.fingerCount += 1
                        cv2.circle(drawing, far, 8, [211, 84, 0], -1)
                return True, data.fingerCount
        return False, 0
    ## end parameters and functions exclusively by Zane Lee
    
    cap = cv2.VideoCapture(0)
    ## window and trackbar by Zane Lee, 
    cap.set(10,200)
    cv2.namedWindow('trackbar')
    cv2.createTrackbar('trh1', 'trackbar', data.threshold, 100, printThreshold)
    
    while cap.isOpened():
        data.ret, data.img = cap.read()
        data.width = 640 #cap.get(3)
        data.height = 480 #cap.get(4)
        data.threshold = cv2.getTrackbarPos('trh1', 'trackbar')
        data.img = cv2.bilateralFilter(data.img, 5, 50, 100)  # smoothing filter
        data.img = cv2.flip(data.img, 1)  # flip the frame horizontally
        #show game field
        cv2.rectangle(data.img, (int(cap_region_x_begin * data.img.shape[1]), 0),
                    (data.img.shape[1], int(cap_region_y_end * data.img.shape[0])),data.fieldColor, 2)
        #cv2.imshow('data.img', data.img) 
        ## end window and trackbar by Zane Lee
    
        ## Keyboard commands originally by Zane Lee and modified by Shiva Nathan
        k = cv2.waitKey(data.waitTime)
        if k == 27:  # press ESC to exit
            break

        elif k == ord('b'):  # press 'b' to start round and capture the background
            #displayCountdown(cv2,data)
            data.difficulty = 'e'
            bgModel = cv2.BackgroundSubtractorMOG2(0, bgSubThreshold)
            data.isBgCaptured = 1
            print '!!!Background Captured!!!'
            
        elif k == ord('z'):  # press 'b' to start round and capture the background
            #displayCountdown(cv2,data)
            data.difficulty = 'i'
            bgModel = cv2.BackgroundSubtractorMOG2(0, bgSubThreshold)
            data.isBgCaptured = 1
            print '!!!Background Captured!!!'
            
        elif k == ord('r'):  # press 'r' to restart game from start screen
            bgModel = None
            triggerSwitch = False
            data.isBgCaptured = 0
            init(data)
            
        elif k == ord('h'):  # press 'h' to view the help screen
            bgModel = None
            triggerSwitch = False
            data.isBgCaptured = -2
            init(data)
        
        ## Begin main hand capture operation written by Zane Lee
        if data.isBgCaptured == 1:  # this part wont run until background captured
            img = removeBG(data.img)
            img = img[0:int(cap_region_y_end * data.img.shape[0]),
                        int(cap_region_x_begin * data.img.shape[1]):data.img.shape[1]]  # clip the ROI
            cv2.imshow('mask', img)
    
            # convert the image into binary image
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (blurValue, blurValue), 0)
            cv2.imshow('blur', blur)
            data.ret, thresh = cv2.threshold(blur, data.threshold, 255, cv2.THRESH_BINARY)
            cv2.imshow('ori', thresh)
    
    
            # get the contours
            thresh1 = copy.deepcopy(thresh)
            contours, hierarchy = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            length = len(contours)
            maxArea = -1
            #if the hand is in the frame
            if length > 0:
                # find the biggest contour (according to area)
                for i in range(length):  
                    temp = contours[i]
                    area = cv2.contourArea(temp)
                    if area > maxArea:
                        maxArea = area
                        ci = i
    
                res = contours[ci]
                hull = cv2.convexHull(res)
                drawing = np.zeros(img.shape, np.uint8)
                cv2.drawContours(drawing, [res], 0, (0, 255, 0), 2)
                cv2.drawContours(drawing, [hull], 0, (0, 0, 255), 3)
    
        ##end main hand capture operation by Zane Lee
    
                
                ##modified for data structure by Shiva Nathan
                #calculate number of fingers
                isFinishCal,data.fingerCount = calculateFingers(res,drawing)
                
                ##gameplay by Shiva Nathan
                
                #display the countdown. 
                displayCountdown(cv2,data)
                #when the countdown is finished, use data.loop to ensure game only plays once per round
                if data.timer == 0.45*data.roundTimer:
                    data.loop = True
                if (data.timer > 0.45*data.roundTimer) and (data.timer < data.roundTimer):
                    if data.loop == True:
                        #play the game once
                        playRound(cv2,data)
                        data.loop = False
                    #display moves made, winner, and scores
                    displayWinner(cv2,data)
                    displayGameData(cv2,data)
                data.timer += 1
                #when round finishes, increment round count
                if (data.timer == data.roundTimer): data.roundCount += 1
                data.timer %= data.roundTimer
                
                cv2.imshow('data.img', data.img)
                
            else:#when hand is not in frame
                pauseScreen(cv2,data) 
                
            cv2.imshow('output', drawing)
        
        elif data.isBgCaptured == 0: #while background is not captured prompt user to start game
            startScreen(cv2,data)
        
        elif data.isBgCaptured == -1: #when game is over
            endScreen(cv2,data)
            
        elif data.isBgCaptured == -2: #go to help screen
            helpScreen(cv2,data)
        
        cv2.imshow('data.img', data.img) 
    ## end gameplay by Shiva Nathan

##end code written by Zane Lee and Shiva Nathan

run()
