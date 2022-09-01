
from math import atan2, pi

import math

def angle3pt(a, b, c):
    """Counterclockwise angle in degrees by turning from a to c around b
        Returns a float between 0.0 and 360.0"""
    ang = math.degrees(
        math.atan2(c[1] - b[1], c[0] - b[0]) - math.atan2(a[1] - b[1], a[0] - b[0]))
    return ang + 360 if ang < 0 else ang




def angle(A, B, C, /):
    Ax, Ay = A[0]-B[0], A[1]-B[1]
    Cx, Cy = C[0]-B[0], C[1]-B[1]
    a = atan2(Ay, Ax)
    c = atan2(Cy, Cx)
    if a < 0: a += pi*2
    if c < 0: c += pi*2
    return (pi*2 + c - a) if a > c else (c - a)












def get_num():

    # 좌표입력 받음
    x1 = int(input('점 a의 x: '))
    y1 = int(input('점 a의 y: '))
    x2 = int(input('점 b의 x: '))
    y2 = int(input('졈 b의 y: '))
    return [x1,y1,x2,y2]

#아크 탄젠트로 각도를 라디안 값으로 구한다
def cal_rad(arr):
    # y거리, x거리 순으로 입력해야 함.
    rad = math.atan2(arr[3]-arr[1],arr[2]-arr[0])
    #print('라디안 : ',rad)
    return rad

# 라디안->디그리
def radTodeg(rad):
    # 파이값 가져와서
    PI = math.pi
    #라디안에 180도 곱하고 파이를 나눈다
    deg = (rad*180)/PI
    #반올림
    deg = round(deg, 2) # 소숫점 두 번째자리까지
    #print('디그리: ', )
    return deg

# arr = get_num()
# rad = cal_rad(arr)
# radTodeg(rad)