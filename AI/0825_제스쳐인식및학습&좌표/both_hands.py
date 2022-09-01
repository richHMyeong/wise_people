import cv2
import time

video = cv2.VideoCapture(0)

import mediapipe as mp
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)

with mp_hands.Hands( # hands사용할 때 받을 옵션값 설정
    max_num_hands=2, #최대 1개인식
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

        if results.multi_hand_landmarks:
            # 두 개 있을 때만 [1]이 생김.
            points =[]
            for hand_landmarks in results.multi_hand_landmarks: # 양손돌면서(또는 한 손만)

                points.append(hand_landmarks.landmark[9])
                # 화면상에
                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS
                )  # 랜드마크 표시

            mp_drawing.draw_landmarks(
                image, hand_landmarks, mp_hands.HAND_CONNECTIONS
            )  # 랜드마크 표시

            if len(points)==2:
                print('0번: ',points[0])
                print('1번: ', points[1])

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) # 화면 출력 색

        cv2.imshow('angle', image)
        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()