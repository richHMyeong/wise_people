
import cv2
import time

video = cv2.VideoCapture(0)

fps = video.get(cv2.CAP_PROP_FPS)
print("fps :", fps)
count = 0
prev_time = 0
FPS = 4 # fps는 5로 해두자.
 # 2연속(5프레임 2번)으로 위에 존재하면 값을 0으로 초기화.

import mediapipe as mp
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)

start =False

with mp_hands.Hands( # hands사용할 때 받을 옵션값 설정
    max_num_hands=1, #최대 1개인식
    min_detection_confidence=0.5, #손인식 컨피던스 0.5이상인 겨우에만
    min_tracking_confidence=0.5 #트래킹정확도도 0.5이상인 겨웅에만
) as hands:
    while cap.isOpened(): #카메라 켜져있는 동안
        # 맨 처음에 좀 딜레이
        if not start:
            start=True
            print('3초뒤 시작:')
            time.sleep(3)

        success, image = cap.read() # 웹캠에서 읽어서
        # 카메라가 불러와지지 않으면
        if not success:
            continue #지나침

        # 미디어파이프로 처리해야함. rgb로 넣음. 헷갈리지 않도록 flip도 해주기
        image = cv2.flip(image, 1)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) #flip(image,1)은 좌우반전. 위에서 플립먼저 해도 됨
        results = hands.process(image) # 랜드마크 값 받아옴

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                p = hand_landmarks.landmark[0]


                # 동영상에 그림 그리기
                # cv2.putText(
                #     image, text='angle: %f'%angle, org= (10, 30),#위치값 설정
                #     fontFace = cv2.FONT_HERSHEY_SIMPLEX, fontScale = 1,
                #     color = 255, thickness = 2
                # )
                #print('현재 각도: ', angle)

                # 화면상에
                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS
                ) # 랜드마크 표시

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) # 화면 출력 색

        cv2.imshow('angle', image)
        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

#
# while True:
#
#     ret, frame = video.read()
#
#     current_time = time.time() - prev_time
#
#     if (ret is True) and (current_time > 1. / FPS):
#
#         print('현재 시간: ', current_time)
#         prev_time = time.time()
#
#         cv2.imshow('VideoCapture', frame)
#         cv2.imwrite('./abcd.jpg', frame)
#         print(prev_time, ' 초')
#         if cv2.waitKey(1) > 0:
#             break