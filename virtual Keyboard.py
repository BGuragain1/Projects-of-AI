#we are gonna make a virtual keyboard
import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep
from pynput.keyboard import Key,Controller

finalText = ""
#template for running web cam
cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

detector = HandDetector(detectionCon=1)
keyList = [["Q","W","E","R","T","Y","U","I","O","P"],
           ["A","S","D","F","G","H","J","K","L","L"],
           ["Z","X","C","V","B","N","M",",",".","/"]]

keyboard = Controller()

def drawAll(img,buttonList):

    for buttons in buttonList:
        x, y = buttons.pos
        w, h = buttons.size
        cv2.rectangle(img, buttons.pos, (x + w, y + h), (255, 0, 255), cv2.FILLED)
        cv2.putText(img, buttons.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

    return img
class Button:
    def __init__(self,pos,text,size=[85,85]):
        self.pos = pos
        self.text = text
        self.size = size

buttonList = []
for j in range(len(keyList)):
    for i, key in enumerate(keyList[j]):
        buttonList.append(Button([i * 100 + 50, 100 * j + 50], key))


while True:
    success,img = cap.read()
    img = cv2.flip(img, 1)
    # track our hand and it's landmark
    img = detector.findHands(img)
    lmList,bboxInfo = detector.findPosition(img)
    img = drawAll(img, buttonList)

    if lmList:
        for button in buttonList:
            x , y = button.pos
            w , h = button.size

            # get the value of finger tip since 8 is the value for finger tip in mediapipe
            if x<lmList[8][0]<x+w and y < lmList[8][1] < y + h:
                #change the color if the finger tip touches the key
                    cv2.rectangle(img, button.pos, (x + w, y + h), (175, 0, 175), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

                    l,_,_ = detector.findDistance(8,12,img,draw=False)
                    print(l)

                    if l<35:
                        keyboard.press(button.text)
                        cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                        cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                        finalText +=button.text
                        sleep(0.15)

    cv2.rectangle(img, (50, 350), (700, 450), (175, 0, 175), cv2.FILLED)
    cv2.putText(img, finalText,(60, 425), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)

    cv2.imshow("Image",img)
    cv2.waitKey(1)


