import time
import cv2
import mediapipe as mp
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose


window = cv2.namedWindow("Gi", cv2.WINDOW_FULLSCREEN)

cap = cv2.VideoCapture('z:/ctf/jntm.mp4')
cap.set(cv2.CAP_PROP_BUFFERSIZE, 2)



fps_start_time = 0
fps = 0

from mpl_toolkits.mplot3d import Axes3D
fig=plt.figure(figsize=(10,10))
ax=fig.add_subplot(projection='3d')

def processing(image):
    # 使用cv2.putText绘制FPS
    # cv2.putText(image, "FPS: {:.2f}".format(fps), (10, 85), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 3)

    # 使用image.flags.writeable = False将图像标记为只读，以加快处理速度
    image.flags.writeable = False
    # 使用cv2.resize将图像缩放到适合的尺寸
    image = cv2.resize(image, (640, 480))
    # 使用cv2.cvtColor将图像转换为RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # 使用MediaPipe Pose检测关键点
    results = pose.process(image)
    
    # 解锁图像读写
    image.flags.writeable = True
    # 将图像转换回BGR
    try:

        print(results.pose_landmarks)
        print(' - '*40)
    except:pass

    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    image*=0
    # 使用draw_landmarks()绘制关键点
    mp_drawing.draw_landmarks(
        image,
        results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

    # 返回处理后的图像
    return image



with mp_pose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as pose:
    # 当视频打开时
    ix=0
    while cap.isOpened() :
        ix+=1
        # 读取视频帧和状态
        success, image = cap.read()
        # success, image = cap.read()
        success, image = cap.read()
        # 如果初始化失败，则推出进程
        if not success:
            print("")
            exit(1)
        # 初始化FPS结束点计时器
        fps_end_time = time.time()
        # 计算FPS
        fps = 1.0 / (fps_end_time - fps_start_time)
        # 重置FPS开始点计时器
        fps_start_time = fps_end_time
        # 创建线程处理图像
        cv2.imshow('Giorg', image//2)
        image = processing(image)
        # 显示图像
        cv2.imshow('Gi', image)

        # 按下q键退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
cap.release()