import cv2
import time
import os
import numpy as np
import mpsol as htm
import random
import ply
hem=0
wCam, hCam = 640, 480
list1 = [0,2,5]#[1,2,3,4,5,6,7,8,9,10,11,12]
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
import time
def winner(totalFingers,img,num):
    if totalFingers in list1:
        #if num!=0 and num!=0
        if num==0 and totalFingers==5:
            return "user"
        elif num==2 and totalFingers==0:
            return "user"
        elif num==5 and totalFingers==2:
            return "user"
        elif totalFingers==0 and num==5:
            return "computer"
        elif totalFingers==2 and num==0:
            return "computer"
        elif totalFingers==5 and num==2:
            return "computer"
        elif num==totalFingers:
            return "No winner"
        else:
            return "Invalid move"
    else:
        return "Invalid move"
def call(win):
        cv2.putText(img, f"Game Over - You {win}", (60,422), cv2.FONT_HERSHEY_PLAIN,
                            2, (255, 255, 255), 2)
        cv2.putText(img, "Press R to restart the game", (2,454), cv2.FONT_HERSHEY_PLAIN,
                            2, (255, 255, 255), 2)
def wins(resul,user,computer):
        cv2.rectangle(img,(510,0),(640,94),(0,0,0),-1)
        cv2.putText(img, f'User points: {user}', (10,422), cv2.FONT_HERSHEY_PLAIN,
                                2, (255, 255, 255), 2)
        cv2.putText(img, f'Computer points: {computer}', (8,454), cv2.FONT_HERSHEY_PLAIN,
                                2, (255, 250, 255), 2)
        if resul == "Invalid move":
            cv2.putText(img, f"That's an Invalid", (7,50), cv2.FONT_HERSHEY_PLAIN,
                                3, (0, 0, 0), 3)
            cv2.putText(img, f"move", (120,90), cv2.FONT_HERSHEY_PLAIN,
                                3, (0, 0, 0), 3)
        else:
            cv2.putText(img, f'Winner: {resul}', (7,50), cv2.FONT_HERSHEY_PLAIN,
                                3, (0, 0, 0), 3)
        cv2.putText(img, 'HELP', (539,27), cv2.FONT_HERSHEY_PLAIN,
                                2, (255, 250, 250), 2)
        cv2.putText(img, 'R - RESTART', (515,47), cv2.FONT_HERSHEY_PLAIN,
                                1, (255, 250, 250), 1)
        cv2.putText(img, 'U - UNDO', (515,67), cv2.FONT_HERSHEY_PLAIN,
                                1, (255, 250, 250), 1)
        cv2.putText(img, 'Q - QUIT', (515,87), cv2.FONT_HERSHEY_PLAIN,
                                1, (255, 250, 250), 1)
abcd=np.add(1,2)
resul = None
tipIds = [4, 8, 12, 16, 20,9]
preMove=None
user=0
def timerCount(no):
    cv2.line(img,(338,380),(338,480),(255,255,255),1)
    cv2.putText(img, f'{no}', (382,457), cv2.FONT_HERSHEY_PLAIN,
                                5, (250, 250, 250), 4)
computer=0
state=False
def comp(image,img):
    logo = cv2.imread(f'{image}.jpeg')
    logo = cv2.resize(logo, (147, 100))
    img[380:480, 493:640]=logo
intialtime=0
num=10
detector = htm.handDetector()
while True:
    startOver=0
    success, img = cap.read()
    img = detector.findHands(img)
    cv2.rectangle(img,(0,380),(500,480),(0,0,0),-1)
    
    lmList = detector.findPosition(img, draw=False)
    if state!=False:
        startOver=1
        if len(lmList) != 0:
            fingers = []
            for i in range(len(lmList)):
                if lmList[i][0]==9:
                        counter=int(time.time()-intialtime+1)
                        if counter==1:
                            timerCount("2")
                        elif counter==2:
                            timerCount("1")
                        #elif counter==3:
                            #timerCount("1")'''
                        else:
                            if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
                                fingers.append(1)
                            else:
                                fingers.append(0)
                            for id in range(1, 5):
                                if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                                    fingers.append(1)
                                else:
                                    fingers.append(0)
                            totalFingers = fingers.count(1)
                            num=random.choice(list1)
                            '''print(num1)
                            if num1 == 1 or num1==5 or num1==7  or num1==10:
                                num=0
                            elif num1==8 or num1==2 or num1==9 or num1==12:
                                num = 2
                            elif num1==3 or num1==4 or num1==6 or num1==11:
                                num = 5'''
                            print(totalFingers,num)
                            resul=winner(totalFingers,img,num)
                            hem=0
                            if resul=="user":
                                    user+=1
                            elif resul=="computer":
                                    
                                    computer+=1
                            else:
                                print(resul)
                            state=False
        else:
            state=False
            
    if startOver==0 and user<10 and computer<10:
        cv2.line(img,(338,380),(338,480),(255,255,255),1)
        if state==False and len(lmList) == 0:

            cv2.putText(img, 'Put your', (342,419), cv2.FONT_HERSHEY_PLAIN,
                                    2, (255, 250, 250), 1)
            cv2.putText(img, 'ryt hand ', (341,442), cv2.FONT_HERSHEY_PLAIN,
                                    2, (255, 250, 250), 1)
            cv2.putText(img, 'in view', (358,465), cv2.FONT_HERSHEY_PLAIN,
                                    2, (255, 250, 250), 1)
        
        else:
            cv2.putText(img, 'Press S', (342,419), cv2.FONT_HERSHEY_PLAIN,
                                2, (255, 250, 250), 1)
            cv2.putText(img, 'for your ', (341,442), cv2.FONT_HERSHEY_PLAIN,
                                    2, (255, 250, 250), 1)
            cv2.putText(img, 'turn', (358,465), cv2.FONT_HERSHEY_PLAIN,
                                    2, (255, 250, 250), 1)
   
    if num==0:
        comp("rockpapersc/rock",img)
    elif num==2:
        comp("rockpapersc/sci",img)
    elif num==5:
        comp("rockpapersc/paper",img)
    if user==11:
        with open("rockpapersc/won.wav"):
            ply.playsound("rockpapersc/won.wav")
            user+=1
    if computer==11:
        with open("rockpapersc/lost.wav"):
            ply.playsound("rockpapersc/lost.wav")
            computer+=1
    if user==10 or user>=12:
        call("won")
        user+=1
    elif computer==10 or computer>=12:
        call("lost")
        computer+=1
    else:
        startOver=1
        wins(resul,user,computer)
    cv2.imshow("Image", img)
    wq=cv2.waitKey(1)
    if wq==ord('1'):
        computer+=1
    if wq==ord('2'):
        user+=1
    if wq==ord('s'):
        intialtime=time.time()
        state=True
    if wq==ord('u'):
        if resul=="computer" and hem==0:
            hem=1
            computer=computer-1
        if resul=="user" and hem==0:
            hem=1
            user=user-1
    if wq==ord('r'):
        user=0
        computer=0
    if wq==ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
