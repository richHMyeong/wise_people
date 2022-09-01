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
import socket # 손가락 사이 거리를 사용해주는 쪽에 실시간으로 전달해주어야 함
# rest api : 요청하면 주는 방식.
# socket통신을 통해 특정 아이피로 계속 값을 전달해주는 udp통신. (상대방이 잘 받는지 신경x)
# xr에서도 udp로 우리쪽 서버로 줌. 받고 싶을 때 받아서 쓰면 됨.

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #소켓 설정
sendport = ('127.0.0.1', 5053) #상대방이 접속할 수 잇는 포트(주소)를 줌. 일단은 로컬로 진행
# 나중에 본인만의 포트 번호.옮겨서 아무튼 자신만의 포트 만들어서.. 아니면 각 팀별로 공유기 줄 수도.

cap = cv2.VideoCapture(0)
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
                # 필요한 랜드마크만 가져오면 됨. #엄지검지 끝은 4번 8번
                p1 = hand_landmarks.landmark[4] # 순서대로 배열로 들어옴
                p2 = hand_landmarks.landmark[8]

                f1 = np.array([p1.x, p1.y, p1.z])
                f2 = np.array([p2.x, p2.y, p1.z])

                # 손 제스쳐는 학습 데이터가 있어야 함. 보통 관절 사이 하긋ㅂ된 데이터로 함.
                # mediapipe 사이트에 데이터 존재

               # norm np.linalg.norm

                volume = int(temp * 100)
                # 소켓에 보니ㅐㄹ 때는 볼륨값을 문자여롤 보내면 됨


                #p1.x, p1.y, p1.z # x, y, z값 다 써야 정확히 인시 됨. 두 벡터 간 거리 구하는 거 써야 함.
                '''
                a = p2.x-p1.x
                b = p2.y - p1.y
                c = math.sqrt((a*a) + (b*b)) # 거리

                # 결과가 소수점으로 나오므로 *100해줌
                volume = int(c*100)
                '''

                socket.sendto(str.encode(str(volume)), sendport) #스트링으로 만들어서 전다해주기
                # 해당포트넘버로 볼륨값을 계~속 던져줌
                # 볼륨에 따라 실제 소리가 줄어들거나 커지거나 한느 거 할 수 있음
                # 포인터 손가락. 손가락으로 마우스 포인터하는 것도 가능..

                cv2.putText(
                    image, text='Volume : %d' % volume, org= (10, 30),#위치값 설정
                    fontFace = cv2.FONT_HERSHEY_SIMPLEX, fontScale = 1,
                    color = 255, thickness = 2
                )

                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS
                ) # 랜드마크 표시

        cv2.imshow('hand_volume', image)
        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
# 혹시 필요하면 이 코드 그대로 가져가서 쓰기 ㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋ생색내기