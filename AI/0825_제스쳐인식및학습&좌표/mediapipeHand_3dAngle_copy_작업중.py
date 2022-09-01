
# 각도만 실시간으로 전달(updown도 같이 전달하기는 함). 즉, 디텍션은 매 프레임마다 해야 함
# 그러나 y좌표 저장과 updown갱신은 1/5초마다 하면 됨. 1.2배 이상이 되면? 점프. 0.8배 이하가 되면? down. <이 검사를 1/5초마다.
# 초기 y좌표를 뭘로? 처음에 들어온 y값으로. 
# 그리고 1초마다 검사해서 만약 updown이 1이라면 0으로 바꾸도록
# 1. 각도 2. updown 검사 3. y좌표 갱신 & updown갱신


# 각도가 이렇게 들어왔을 때 이 포즈다(마지막 컬럼). 각도포즈 데이터 존재.

import mediapipe as mp
import cv2
import time

import numpy as np
import vg

import json

import math

def Angle3d(p1, p2): # 각도
    vec1 = np.array([p1.x, p1.y, p1.z])
    vec2 = np.array([p2.x, p2.y, p2.z])
    return vg.angle(vec1, vec2)


mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

# json 파일 옵션
updown = 0 #중지의 y값 기준 (12번) -1, 0, 1로 둡시다.
# angle,distance는 내부에서 변경됨
angle = 0 ; dist = 0
json_path = './jsonfiles/'

# FPS 설정.
FPS = 4 # 1초를 4프레임으로 나누었을 때의 시간. 4는 1초를 4프레임으로 나눈다는 의미인 듯 https://deep-eye.tistory.com/10
prev_time = 0
prev_y = 0
start=False

with mp_hands.Hands( # hands사용할 때 받을 옵션값 설정
    max_num_hands=1, #최대 1개인식
    min_detection_confidence=0.5, #손인식 컨피던스 0.5이상인 겨우에만
    min_tracking_confidence=0.5 #트래킹정확도도 0.5이상인 겨웅에만
) as hands:
    while cap.isOpened(): #카메라 켜져있는 동안
        success, image = cap.read() # 웹캠에서 읽어서
        # 카메라가 불러와지지 않으면
        if not success:
            continue #지나침

        # 미디어파이프로 처리해야함. rgb로 넣음. 헷갈리지 않도록 flip도 해주기
        image = cv2.flip(image, 1)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) #flip(image,1)은 좌우반전. 위에서 플립먼저 해도 됨
        results = hands.process(image) # 랜드마크 값 받아옴

        if results.multi_hand_landmarks: # 랜드마크를 잘 받아왔다면
            fly_points=[]
            for hand_landmarks in results.multi_hand_landmarks: #랜드마크에 대한 처리
                # 한손의 랜드마크(results.multi_hand_landmarks의 크기가 1이므로 한 번 돌고 끝)
                ### 1. 각도 계산
                ### 1-1. (달리기, 수영)
                p1 = hand_landmarks.landmark[8] # a 검지
                p2 = hand_landmarks.landmark[12] #b 중지
                # 손이 두 개일 때는 왼손 하나 오른손 하나 이렇게 생김.

                angle = Angle3d(p1, p2)
                angle = round(angle, 3)

                #print('현재 각도: ', angle)

                ### 1-2. 날기
                fly_p1 = hand_landmarks.landmark[8]
                fly_p2 = hand_landmarks.landmark[9]
                dist = math.dist([fly_p1.x, fly_p1.y], [fly_p2.x, fly_p2.y])
                dist = round(dist, 3)

                # 엄지손가락 저장. 계산은 for문 나온 다음에 해야.


                ### 2. updown 상태 표시
                wrist = hand_landmarks.landmark[0]  # 맨 처음 손목 위치

                current_time = time.time() - prev_time

                # 1/4초마다
                if (success is True) and (current_time > 1. / FPS):
                    if start:  # 처음으로 들어온 것이 아니라면
                        y_change = wrist.y - prev_y  # 이전에 기록해둔 y값과의 변화량을 구함. 현재 y가 더 크면 양수
                        # current_y = wrist.y - prev_y  # 이전 프레임과의 변화량을 구함
                        # 구한 변화량이... 좌표값은 좌상단 기준!!!!!!!슈발!!!!!!
                        # wrist.y가 prev_y보다 크다는 것은 wrist.y가 더 내려갔다는 것
                        # prev_y가 wrist.y보다 더 크다? -> 올라온 거야
                        # 변화량이 존재하면서(점프) 이미 기존에 점프라면 1을 유지한다

                        ## 조금만 움직여도 적용될 수 있ㄷ록!! 매우 민감하므로 주의!!!! 연습이 좀 필요함.
                        if (y_change < 0 and abs(y_change) > 0.05) and (updown == 0 or updown == -1):
                            updown += 1  # 점프를 한 경우
                        elif y_change > 0.05 and (updown == 0 or updown == 1):
                            updown -= 1  # 다운을 한 경우
                        else:
                            pass  # 변화량이 없다면 현재의 updown을 유지.

                        prev_y = wrist.y  # prev_y를 갱신한다.

                    else:  # 처음으로 들어온 것이라면 변화량 안 구함
                        prev_y = wrist.y
                        start = True
                        continue  # updown의 처음 상태인 0을 유지

                    prev_time = time.time()
                    # 여기에 y좌표 저장하기
                    prev_y = wrist.y
                    # print('저장된 y: ', prev_y)

                    # print('현재 상태: ', updown)

                # 동영상에 그림 그리기
                cv2.putText(
                    image, text='angle1: %.3f  dist: %.3f updown:%d' % (angle, dist, updown), org=(10, 30),  # 위치값 설정
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.8,
                    color=255, thickness=2
                )

                # 화면상에 랜드마크 표시
                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS
                )

        ## json 파일 작성
        data = { 'angle1': angle,
                 'distance': dist,
                 'updown': updown }
        with open(json_path+'status.json', 'w') as outfile:
            json.dump(data, outfile, indent=4)

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) # 화면 출력 색
        cv2.imshow('angle', image)
        if cv2.waitKey(1) == 27:
            break



    cap.release()
    cv2.destroyAllWindows()
# 혹시 필요하면 이 코드 그대로 가져가서 쓰기 ㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋ생색내기
