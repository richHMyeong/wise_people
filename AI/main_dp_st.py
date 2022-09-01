from cvzone.HandTrackingModule import HandDetector
import cv2
import socket
import math
import os

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
success, img = cap.read()
h, w, _ = img.shape
detector = HandDetector(detectionCon=0.8, maxHands=2)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverAddressPort = ("127.0.0.1", 5052)


tmp = []

while True:
    # Get image frame
    success, img = cap.read()
    # Find the hand and its landmarks
    hands, img = detector.findHands(img)  # with draw
    if len(hands) == 0:
        if len(tmp) > 0:
            sock.sendto(str.encode(str(tmp)), serverAddressPort)

    # hands = detector.findHands(img, draw=False)  # without draw
    data = []


    if hands:
        # Hand 1
        hand = hands[0]
        lmList = hand["lmList"]  # List of 21 Landmark points
        x1, x2, y1, y2 = 0, 0, 0, 0

        if len(lmList) != 0:
            x1, y1 = lmList[8][1:]  # 두번째 좌표
            x2, y2 = lmList[12][1:]  # 세번째 좌표

            # 3. Check which fingers are up
            fingers = detector.fingersUp(hand)
            #print(fingers)

        for lm in lmList:
            if lm[0] == 5:
                indexMid = lm[2]
                x1, y1 = lm[1], lm[2]
            elif lm[0] == 17:
                x2, y2 = lm[1], lm[2]
            distance = int(math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2))
            data.extend([lm[0], h - lm[1], lm[2] + distance])
        tmp = data

        fingers.extend(data)
        sock.sendto(str.encode(str(fingers)), serverAddressPort)
        print(fingers)


    # Display
    cv2.imshow("Image", img)
    cv2.waitKey(1)