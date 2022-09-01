## 제스쳐 생성!!!

# 미디어 파이프로 자세 인식하면서 동시에 각도, 손가락 끝 좌표(달리기) txt로 작성해서 보내기.


import cv2
import mediapipe as mp
import numpy as np
import pandas as pd

gesture = { 0:'walk' , 1:'run', 2:'swim', 3:'speed_swim', 4:'fly', 5:'fly_high' }
# up, down 둘 다 false인 게 기본.
# 이거 동작만 만들어두고 up, down은 내가 1초 전 프레임과 비교해서 up, down만들도록 하자. up, down을 0, 1, 2로 표현. 올라가면 1에서 2, 내려가면 -1, 올라가면 +1


mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

#
# # x,y로 나누어서 학습 시킨다.
# df = pd.read_csv('gesture_new.csv', header=None) # csv파일에 헤더없으므로 none
# angle = df.iloc[:,:-1] #매 마지막 레이블 빼고
# label = df.iloc[:, -1]
#
# angle = angle.to_numpy().astype(np.float32) #numpy로 만ㄷ름
# label = label.to_numpy().astype(np.float32)
#
# #opncv안에 knn존재
# knn = cv2.ml.KNearest_create()
# knn.train(angle, cv2.ml.ROW_SAMPLE, label) # 데이터랑 레이블 넣고 학습시킴
#




total_result = []

def on_click(event, x,y,flags,param):
    global data,file

    if event == cv2.EVENT_LBUTTONDOWN:
        total_result.append(data)


cap = cv2.VideoCapture(0)
cv2.namedWindow('Dataset')
cv2.setMouseCallback('Dataset',on_click)

while cap.isOpened():
    ret,img = cap.read()
    if not ret:
        break

    img = cv2.cvtColor(cv2.flip(img,1) , cv2.COLOR_BGR2RGB) # 랜드마크 인식하려면 있어야 함.

    result = hands.process(img)

    if result.multi_hand_landmarks is not None:
        for res in result.multi_hand_landmarks:
            joint = np.zeros((21,3))

            for j,lm in enumerate(res.landmark):
                joint[j] = [lm.x, lm.y, lm.z]

            # Get direction vector of bone from parent to child
            v1 = joint[[0, 1, 2, 3, 0, 5, 6, 7, 0, 9, 10, 11, 0, 13, 14, 15, 0, 17, 18, 19], :]  # Parent joint
            v2 = joint[[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], :]  # Child joint
            v = v2 - v1  # [20,3]
            # Normalize v
            v = v / np.linalg.norm(v, axis=1)[:, np.newaxis]

            # Get angle using arcos of dot product
            angle = np.arccos(np.einsum('nt,nt->n',
                                            v[[0, 1, 2, 4, 5, 6, 8, 9, 10, 12, 13, 14, 16, 17, 18], :],
                                            v[[1, 2, 3, 5, 6, 7, 9, 10, 11, 13, 14, 15, 17, 18, 19], :]))  # [15,]

            angle = np.degrees(angle)

            data = np.array([angle], dtype=np.float32)
            #ret, results, neighbors, dist = knn.findNearest(data, 1)  # 현재 내가 추출한 데이ㅓ ㅌ중 가장 비슷한 거 5게 뽑음)

            #idx = int(results[0][0])

            # if idx in gesture.keys():
            #     cv2.putText(img, text=gesture[idx].upper(),
            #                 org=(int(res.landmark[0].x * img.shape[1]),
            #                      int(res.landmark[0].y * img.shape[0])),
            #                 fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(255, 255, 255),
            #                 thickness=2
            #                 )
                # 위치는 손목에. 실제 이미지에 띄워야 하므로 shape 곱해주기




            data = np.array([angle],dtype = np.float32)
            data = np.append(data, 1) # 데이터랑 정답레이블 같이 저장

            mp_drawing.draw_landmarks( img, res, mp_hands.HAND_CONNECTIONS)

    cv2.imshow('Dataset',img)
    if cv2.waitKey(1) == 27:
        break

total_result = np.array(total_result,dtype=np.float32)
df = pd.DataFrame(total_result)
df.to_csv('gesture_new.csv',mode='a',index=None,header=None)
cap.release()