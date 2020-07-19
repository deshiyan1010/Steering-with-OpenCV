import cv2
import numpy as np 

def nothing(x):
    pass
#img = cv2.imread("messi5.jpg",-1)
cap=cv2.VideoCapture(0)
cv2.namedWindow("img")
cv2.createTrackbar("Hmin","img",0,180,nothing)
cv2.createTrackbar("Hmax","img",0,180,nothing)
cv2.createTrackbar("Smin","img",0,255,nothing)
cv2.createTrackbar("Smax","img",0,255,nothing)
cv2.createTrackbar("Vmin","img",0,255,nothing)
cv2.createTrackbar("Vmax","img",0,255,nothing)

while cap.isOpened():

    _,img=cap.read()
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    Hmin = cv2.getTrackbarPos("Hmin","img")
    Hmax = cv2.getTrackbarPos("Hmax","img")
    Smin = cv2.getTrackbarPos("Smin","img")
    Smax = cv2.getTrackbarPos("Smax","img")
    Vmin = cv2.getTrackbarPos("Vmin","img")
    Vmax = cv2.getTrackbarPos("Vmax","img")

    mask = cv2.inRange(imgHSV,(Hmin,Smin,Vmin),(Hmax,Smax,Vmax))
    final=cv2.bitwise_and(img,img,mask=mask)

    cv2.imshow("Final",final)

    k = cv2.waitKey(10)
    if k==27:
        break
cv2.destroyAllWindows()
cap.release()

