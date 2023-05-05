import time
from enum import Enum
from random import randint
import subprocess

# Requirements
try:
    import  cvzone
    from cvzone.HandTrackingModule import HandDetector
except:
    subprocess.run(['pip','install','cvzone'])
    import cvzone
    from cvzone.HandTrackingModule import HandDetector

try:
    import  cv2
except:
    subprocess.run(['pip','install','opencv-python'])
    import cv2

try:
    import  mediapipe
except:
    subprocess.run(['pip','install','mediapipe'])
    import mediapipe

# Global Functions
class RPS_Values(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

class RPS_Point(Enum):
    PLAYER1_WIN = 1
    PLAYER2_WIN = 2
    TIE = 3

def getMove(fingers):
    if fingers == [0,0,0,0,0]: return RPS_Values.ROCK
    if fingers == [1,1,1,1,1]: return RPS_Values.PAPER
    if fingers == [0,1,1,0,0]: return RPS_Values.SCISSORS

def getAIMove():
    RandVal = randint(1,3)
    return RandVal

def EvalGameWinner(move1, move2):
    if move1 == move2: return RPS_Point.TIE
    if move1 == RPS_Values.ROCK and move2 == RPS_Values.PAPER: return RPS_Point.PLAYER2_WIN
    if move1 == RPS_Values.ROCK and move2 == RPS_Values.SCISSORS: return RPS_Point.PLAYER1_WIN
    if move1 == RPS_Values.PAPER and move2 == RPS_Values.SCISSORS: return RPS_Point.PLAYER2_WIN
    else: return RPS_Point.PLAYER2_WIN if EvalGameWinner(move2, move1) == RPS_Point.PLAYER1_WIN else RPS_Point.PLAYER1_WIN

def getMoveName(move):
    if move == RPS_Values.ROCK: return "Rock"
    if move == RPS_Values.PAPER: return "Paper"
    if move == RPS_Values.SCISSORS: return  "Scissors"
    return "No Move"

# Global Variables
H,W = 3,4
cap = cv2.VideoCapture(0)
cap.set(H, 640)
cap.set(W, 480)
detector = HandDetector(maxHands=1)
timer = 0
stateResult = False
startGame = False
scores = [0,0]

while True:
    imgBG = cv2.imread("src/Background.png")
    success, img = cap.read()
    imgScaled = cv2.resize(img, (0,0), None, 0.875, 0.875)
    imgScaled = imgScaled[:,80:480]
    hands = detector.findHands(imgScaled,draw=False)
    if hands:
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        playerMove = getMove(fingers)
        cv2.rectangle(imgScaled, (hand["bbox"][0] - 20, hand["bbox"][1] - 20),
                      (hand["bbox"][0] + hand["bbox"][2] + 20, hand["bbox"][1] + hand["bbox"][3] + 20),
                      (255, 182, 56), 2)
        cv2.putText(imgScaled, getMoveName(playerMove), (hand["bbox"][0] - 30, hand["bbox"][1] - 30),
                    cv2.FONT_HERSHEY_PLAIN,
                    2, (255, 182, 56), 2)

    if startGame:
        if stateResult is False:
            timer = time.time() - intialTime
            cv2.putText(imgBG, str(int(timer)),(605,435), cv2.FONT_HERSHEY_PLAIN, 6, (255,182,56), 4)
        if timer > 3:
            stateResult = True
            timer = 0

            AIMove = getAIMove()
            imgAI = cv2.imread(f'src/{AIMove}.png', cv2.IMREAD_UNCHANGED)
            imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))

            if hands:
                if playerMove in [RPS_Values.PAPER, RPS_Values.ROCK, RPS_Values.SCISSORS]:
                    if EvalGameWinner(RPS_Values(AIMove), playerMove) == RPS_Point.PLAYER1_WIN: scores[0]+=1
                    elif EvalGameWinner(RPS_Values(AIMove), playerMove) == RPS_Point.PLAYER2_WIN: scores[1]+=1

            else:
                NoMove = True
                cv2.putText(imgBG, "NO MOVE",(530,420), cv2.FONT_HERSHEY_PLAIN, 6, (255,182,56), 4)


    imgBG[234:654,795:1195] = imgScaled

    if stateResult:
        imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))
        if NoMove: cv2.putText(imgBG, "NO MOVE", (530, 420), cv2.FONT_HERSHEY_PLAIN, 3, (255,182,56), 2)

    cv2.putText(imgBG, str(scores[0]), (410, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
    cv2.putText(imgBG, str(scores[1]), (1112, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)

    cv2.imshow("rock - paper - scissors", imgBG)
    key = cv2.waitKey(1)

    if key == ord(' '):
        NoMove = False
        startGame = True
        intialTime = time.time()
        stateResult = False
    if key == ord('q'):
        break

