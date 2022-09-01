from cvzone.HandTrackingModule import HandDetector
import cv2
import socket
import math
import os
import time
import numpy as np

FPS = 4 # 1초를 4프레임으로 나누었을 때의 시간. 4는 1초를 4프레임으로 나눈다는 의미인 듯 https://deep-eye.tistory.com/10
prev_time = 0
prev_y = 0
start=False


def Angle2d(p0, p1, p2):
    p0 = [p0[1], p0[2]]
    p1 = [p1[1], p1[2]]
    p2 = [p2[1], p2[2]]
    v0 = np.array(p0) - np.array(p1)
    v1 = np.array(p2) - np.array(p1)
    angle = np.math.atan2(np.linalg.det([v0,v1]),np.dot(v0,v1))
    return angle

# x는 1280으로 나누기 y는 720으로 나누기

cap = cv2.VideoCapture(0)
# cap.set(3, 1280)
# cap.set(4, 720)
success, img = cap.read()
h, w, _ = img.shape
detector = HandDetector(detectionCon=0.8, maxHands=2)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverAddressPort = ("127.0.0.1", 5052)

tmp = []

updown = 0

while True:
    # Get image frame
    success, img = cap.read()
    # Find the hand and its landmarks
    hands, img = detector.findHands(img)  # with draw
    if len(hands) == 0: # hands == lmList len(lmList)는 21개. (디텍트를 했을 때만)
        if len(tmp) > 0:
            sock.sendto(str.encode(str(tmp)), serverAddressPort) # 디텍트를 못 햇어 근데 이전에 뭐 한 게 있다? 그러면 소켓으로 보냄.

    # hands = detector.findHands(img, draw=False)  # without draw
    data = []


    if hands:
        # Hand 1
        hand = hands[0]
        lmList = hand["lmList"]  # List of 21 Landmark points
        #x1, x2, y1, y2 = 0, 0, 0, 0

        print('0번의 값', lmList[0])
        if len(lmList) != 0:

            # 좌표 보내드리고
            x1, y1 = lmList[8][1:]  # 8번 # 두번째 좌표 ## 애초에 cx, cy만 저장하니까 id빼고 두 개를 받아옴
            x2, y2 = lmList[9][1:]  # 9번
            x3, y3 = lmList[12][1:]  # 12번 세번째 좌표
            # 맨 뒤에 updown붙이려면?

            ### 2. updown 상태 표시
            current_time = time.time() - prev_time
            if (success is True) and (current_time > 1. / FPS):
                y_tmp = lmList[0][1]
                if y_tmp<230: #jump
                    updown= 1
                elif y_tmp<400: # walk
                    updown = 0
                else: # 그 이상은 전부 slide
                    updown = -1
                print('0번의 y값: ', lmList[0][1])

            send_value = str(x1)+","+str(y1)+","+str(x2)+","+str(y2)+","+str(x3)+","+str(y3)+","+str(updown)

        # 보내기!!!!
        print(send_value)
        sock.sendto(str.encode(send_value), serverAddressPort)
        #time.sleep(0.1)


    # Display
    cv2.imshow("Image", img)
    cv2.waitKey(1)