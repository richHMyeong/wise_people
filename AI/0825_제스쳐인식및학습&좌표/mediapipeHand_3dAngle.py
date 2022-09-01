# 미디어 파이프를 어디에 어떻게 쓸지는 스스로 생각. 아이디어!!ㄴ
# 모양학습시키고 내가 동작 취하면 그중 가장 유사한 동작을 꺼내서 어ㄸ너 기능 등을 작동시키는 것.
# 유니티랑 미디어파이프랑 손 관절 비슷하게 생김.
# 미디어파이프로 플젝하신 분들 많음.
# https://github.com/ntu-rris/google-mediapipe 이런 것들이 가능하다!
# 두 손끝 랜드마크의 거리를 계산해서 ..뭐 그러는 거..
# 제스쳐 학습시키는 거까지만 함!!! 와!! 학습시킨는 거 나도 하ㅗㄱ 싶다!! 우와!!
# 간단한 거 만들어보라고!! 우와!!와!!!

# 각도가 이렇게 들어왔을 때 이 포즈다(마지막 컬럼). 각도포즈 데이터 존재.

import mediapipe as mp
import cv2
import numpy as np
import math
import math
import time

import numpy as np
import vg

def Angle3d(p1, p2):
    vec1 = np.array([p1.x, p1.y, p1.z])
    vec2 = np.array([p2.x, p2.y, p2.z])
    return vg.angle(vec1, vec2)

def angle3pt(a, b, c):
    """Counterclockwise angle in degrees by turning from a to c around b
        Returns a float between 0.0 and 360.0"""
    ang = math.degrees(
        math.atan2(c[1] - b[1], c[0] - b[0]) - math.atan2(a[1] - b[1], a[0] - b[0]))
    return ang + 360 if ang < 0 else ang

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

# json 파일 옵션
updown = 0 #중지의 y값 기준
angle1 = 0
angle2 = 0
time = time.time()

with mp_hands.Hands( # hands사용할 때 받을 옵션값 설정
    max_num_hands=1, #최대 1개인식
    min_detection_confidence=0.5, #손인식 컨피던스 0.5이상인 겨우에만
    min_tracking_confidence=0.5 #트래킹정확도도 0.5이상인 겨웅에만
) as hands:
    while cap.isOpened(): #카메라 켜져있는 동안
        success, image = cap.read()

        # 카메라가 불러와지지 않으면
        if not success:
            continue #지나침

        # 미디어파이프로 처리해야함. rgb로 넣음. 헷갈리지 않도록 flip도 해주기
        image = cv2.flip(image, 1)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) #flip(image,1)은 좌우반전. 위에서 플립먼저 해도 됨
        results = hands.process(image) # 랜드마크 값 받아옴

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:

                # 각도 계산
                p1 = hand_landmarks.landmark[8] # a
                p2 = hand_landmarks.landmark[12] #b
                # p3 = hand_landmarks.landmark[12] #c
                # angle = angle3pt([p1.x, p1.z], [p2.x, p2.z], [p3.x, p3.z])
                # angle = round(angle, 2)
                angle = Angle3d(p1, p2)
                angle = round(angle, 2)

                # 동영상에 그림 그리기
                cv2.putText(
                    image, text='angle: %f'%angle, org= (10, 30),#위치값 설정
                    fontFace = cv2.FONT_HERSHEY_SIMPLEX, fontScale = 1,
                    color = 255, thickness = 2
                )
                #print('현재 각도: ', angle)

                # 화면상에
                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS
                ) # 랜드마크 표시

        cv2.imshow('angle', image)
        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
# 혹시 필요하면 이 코드 그대로 가져가서 쓰기 ㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋ생색내기