from directkeys import *
import cv2
import numpy as np 
from time import sleep
import math
from vjoy import look_left,look_right, ultimate_release,throttle


def get_center(mask):

    contours,_ = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    max_area=0
    try:
        for cnt in contours:
            if cv2.contourArea(cnt)>max_area:
                max_area = cv2.contourArea(cnt)
                M = cv2.moments(cnt)
                center = (int(M["m10"]/M["m00"]),int(M["m01"]/M["m00"]))
        return center
                    
    except Exception as e:
        return None


def calc_angle(point,center):

    third_point = (center[0],center[1]+1)

    a = np.array(point)
    b = np.array(center)
    c = np.array(third_point)


    ba = a-b
    bc = c-b

    vec1 = ba/np.linalg.norm(ba)
    vec2 = bc/np.linalg.norm(bc)
    dot = np.dot(vec1,vec2)
    angle = np.arccos(dot)

    if ba[0]<0:
        angle = -angle

    return np.degrees(angle)

def PressKeyPWM(char,angle):
    time_down = (np.abs(angle)/90)

    if angle >10:    
        look_right(time_down)

    if angle <-10:    
        look_left(time_down)
    


#print(calc_angle((1,1),(0,0)))

if __name__=="__main__":
    
    for i in range(100000):
        pass
    print("out")
    cap=cv2.VideoCapture(0)

    while cap.isOpened():

        _,img=cap.read()
        img = cv2.GaussianBlur(img,(7,7),0)
        imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        yellow_mask = cv2.inRange(imgHSV,(42,84,0),(86,255,255))

        pink_mask = cv2.inRange(imgHSV,(140,84,107),(180,193,255))

        yellow_center = get_center(yellow_mask)
        pink_center = get_center(pink_mask)
        throttle()
        if yellow_center is not None and pink_center is not None:
            angle = calc_angle(pink_center,yellow_center)
            
            if angle>0:
                ultimate_release()
                PressKeyPWM(D,angle)
                print("Right")
            
            elif angle<0:
                ultimate_release()
                PressKeyPWM(A,angle)
                print("Left")
            
            else:
                ultimate_release()

        yellow_mask = cv2.resize(yellow_mask,(int(yellow_mask.shape[1]/2),int(yellow_mask.shape[0]/2)))
        pink_mask = cv2.resize(pink_mask,(int(pink_mask.shape[1]/2),int(pink_mask.shape[0]/2)))        
        cv2.imshow("yellow_mask",yellow_mask)
        cv2.imshow("pink_mask",pink_mask)
        cv2.imshow("frame",img)

        k = cv2.waitKey(10)
        if k==27:
            break
    cv2.destroyAllWindows()
    cap.release()

