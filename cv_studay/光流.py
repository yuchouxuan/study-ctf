import cv2
import numpy
import matplotlib.pyplot as plot
import numpy as np
cap = cv2.VideoCapture(0) 
# 创建随机颜色
color = np.random.randint(0, 255, (100, 3))

# 读取第一帧
ret, frame = cap.read()
# 转换为灰度图像
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
mask = np.zeros_like(frame)
while True:
    # 读取下一帧
    ret, frame = cap.read()
    if not ret:
        break
    # 转换为灰度图像
    gray_next = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # 计算光流
    flow = cv2.calcOpticalFlowFarneback(gray, gray_next, None, 0.5, 3, 15, 3, 5, 1.2, 0)
    # 绘制光流
    h, w = gray.shape
    y, x = np.mgrid[0:h:10, 0:w:10].reshape(2, -1).astype(int)
    fx, fy = flow[y, x].T
    lines = np.vstack([x, y, x + fx, y + fy]).T.reshape(-1, 2, 2)
    lines = np.int32(lines + 0.5)
    vis = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    for (x1, y1), (x2, y2) in lines:
        cv2.line(vis, (x1, y1), (x2, y2), (0, 255, 0), 1)
    # 将光流叠加到原始图像上
    img = cv2.add(frame, vis)

    # 显示图像
    cv2.imshow('frame', vis)
    gray=gray_next
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

# 清理并退出
cap.release()
cv2.destroyAllWindows()