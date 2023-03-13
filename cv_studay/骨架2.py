import time
import cv2
import mediapipe as mp
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from vpython import *

#vpython（三维画图）模型变量初始化
def vpython_variables_init():
    points = []
    boxs = []
    ids = [[12, 14, 16], [11, 13, 15], [12, 24, 26, 28, 30, 32, 28],
           [11, 23, 25, 27, 29, 31, 27], [12, 11], [24, 23]]
    c = []
 
    for x in range(33):
        points.append(sphere(radius=5, pos=vector(0, -50, 0)))
        c.append(curve(retain=2, radius=4))
    return points, boxs, ids, c

#mediapipe 模型变量初始化
def mediapipe_varibles_init():
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, model_complexity=1)
    mp_drawing = mp.solutions.drawing_utils
    return pose,mp_pose, mp_drawing


def draw_3d_pose(f):
    results = pose.process(cv2.cvtColor(f, cv2.COLOR_BGR2RGB))
    if results.pose_world_landmarks:
        for i in range(11, 33):
            if i != 18 and i!=20 and i!= 22 and i != 17 and i!=19 and i!=21:
                points[i].pos.x = results.pose_world_landmarks.landmark[mp_pose.PoseLandmark(i).value].x * -cap.get(3)
                points[i].pos.y = results.pose_world_landmarks.landmark[mp_pose.PoseLandmark(i).value].y * -cap.get(4)
                points[i].pos.z = results.pose_world_landmarks.landmark[mp_pose.PoseLandmark(i).value].z * -cap.get(3)
        for n in range(2):
            for i in range(2):
                c[i + 2 * n].append(vector(points[ids[n][i]].pos.x, points[ids[n][i]].pos.y, points[ids[n][i]].pos.z),
                                    vector(points[ids[n][i + 1]].pos.x, points[ids[n][i + 1]].pos.y,
                                           points[ids[n][i + 1]].pos.z), retaine=2)
        for n in range(2, 4):
            for i in range(6):
                    c[i+6*n].append(vector(points[ids[n][i]].pos.x, points[ids[n][i]].pos.y, points[ids[n][i]].pos.z),
                                vector(points[ids[n][i +1]].pos.x, points[ids[n][i + 1]].pos.y, points[ids[n][i+1]].pos.z), retaine = 2)
        for n in range(4, 6):
            for i in range(1):
                c[i+2*n].append(vector(points[ids[n][i]].pos.x, points[ids[n][i]].pos.y, points[ids[n][i]].pos.z),
                                            vector(points[ids[n][i +1]].pos.x, points[ids[n][i + 1]].pos.y, points[ids[n][i+1]].pos.z), retaine = 2)
    mp_drawing.draw_landmarks(image=f, landmark_list=results.pose_landmarks, connections=mp_pose.POSE_CONNECTIONS)
    

cap = cv2.VideoCapture('z:/ctf/b.mp4')
cap.set(cv2.CAP_PROP_BUFFERSIZE, 2)
points, boxs, ids, c = vpython_variables_init()
pose, mp_pose, mp_drawing = mediapipe_varibles_init()

while True:
    #获取每一帧的图像
    _, f = cap.read()
    #vpython里的一个函数，用来调整3D中的FPS
    rate(150)
    #调用在3D里画出骨架的函数
    draw_3d_pose(f)
    #在每一帧里画骨架
    #显示每一帧
    cv2.imshow('real_time', f)
    #检测是否要关闭窗口
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
