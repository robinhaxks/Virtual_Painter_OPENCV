import cv2
import numpy as np
import time
import os
import Handtracking as htm

mylist = os.listdir("Painter")

print(mylist)
brushthicknes = 15
drawcolor = (255,0,255)
xp , yp = 0,0
overlap = []

for impath in mylist:
    image = cv2.imread(f'{"Painter"}/{impath}')
    overlap.append(image)

header1 = overlap[0]   

print(len(overlap))    


cap=cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)


dector = htm.handDetector(detectionCon = 0.85)

imgcanvas = np.zeros((720,1280,3),np.uint8)

while True:
    sucess , img = cap.read()
    img = cv2.flip(img ,1)
    img[0:170,0:1280] = header1
    img = dector.findHands(img)

    lmlist = dector.findpositions(img ,draw = False)

    if len(lmlist)!=0 :

          
     
          x1,y1 = lmlist[8][1:]
          x2,y2 = lmlist[12][1:]
          fingers = dector.fingersup()

          if fingers[1] and fingers[2]:
              xp,yp = 0,0
              #print("selection mode")

              if y1 < 170:
                  if 0<x1<320:
                      #print("in blue")
                      drawcolor = (255,0,0)
                  elif 320<x1<640:
                       #print("in green")  
                       drawcolor = (0,255,0)
                  elif 640 <x1<960:
                       #print("in red")
                       drawcolor =(0,0,255)
                  elif 960 <x1<1280:
                       #print("in eraser")
                       drawcolor = (0,0,0)           
              cv2.rectangle(img,(x1,y1-25),(x2,y2+25),drawcolor,cv2.FILLED)       
                  
          if fingers[1] and fingers[2]==False:
              #print("drwaing mode")    
              cv2.circle(img,(x1,y1),15,drawcolor,cv2.FILLED)
              if xp ==0 and yp == 0:
                  xp,yp = x1,y1

              if drawcolor ==(0,0,0):
                  cv2.line(img , (xp,yp),(x1,y1),drawcolor,50)
                  cv2.line(imgcanvas,(xp,yp),(x1,y1),drawcolor,50)
              else:

                  cv2.line(img , (xp,yp),(x1,y1),drawcolor,brushthicknes)
                  cv2.line(imgcanvas,(xp,yp),(x1,y1),drawcolor,brushthicknes)
              xp,yp = x1,y1  

    imggray = cv2.cvtColor(imgcanvas,cv2.COLOR_BGR2GRAY)
    _ , imginv = cv2.threshold(imggray , 50,255,cv2.THRESH_BINARY_INV)
    imginv = cv2.cvtColor(imginv,cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img,imginv)
    img = cv2.bitwise_or(img,imgcanvas)            
    #img = cv2.addWeighted(img,0.5,imgcanvas,0.5,1)      
    cv2.imshow("VIPainter",img)
    #cv2.imshow("canvas",imgcanvas)
    cv2.waitKey(1)