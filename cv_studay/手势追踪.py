import cv2
import mediapipe as mp
import time
import numpy as np

f_m = 5
fre = []
for i in range(f_m):
    fre.append(cv2.imread(f'fi{i}.png')[:,:,::-1])

3
cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands(static_image_mode=False,
                      max_num_hands=2,
                      min_detection_confidence=0.5,
                      min_tracking_confidence=0.5)
mpDraw = mp.solutions.drawing_utils


def findPosition(img, myHand):
    lmlist = []
    for id, lm in enumerate(myHand.landmark):
        h, w, c = img.shape
        cx, cy = int(lm.x * w), int(lm.y * h)
        lmlist.append([id, cx, cy])
    return lmlist


import random

pTime = 0
cTime = 0
xx = None
run = True
import numpy as np

success, img = cap.read()
mask = np.zeros(img.shape, np.uint8)
red = np.random.randn(10, 10, 3) * 150 + 150
fcont = 0


def dis(p1, p2):
    return (p1[1] - p2[1]) ** 2 + (p1[2] - p2[2]) ** 2
kernel =cv2.getStructuringElement(cv2.MORPH_CROSS, (5, 5))
def erode_x(img):
    return cv2.erode(img, kernel, iterations=1)


def ImageRotate(image):
    height, width = image.shape[:2]  # 输入(H,W,C)，取 H，W 的值
    center = (width / 2, height / 2)  # 绕图片中心进行旋转
    angle = random.randint(-180, 180)  # 旋转方向取（-180，180）中的随机整数值，负为逆时针，正为顺势针
    scale = 0.8  # 将图像缩放为80%
    # 获得旋转矩阵
    M = cv2.getRotationMatrix2D(center, angle, scale)
    # 进行仿射变换，边界填充为255，即白色，默认为0，即黑色
    image_rotation = cv2.warpAffine(src=image, M=M, dsize=(height, width), borderValue=(0, 0, 0))

    return image_rotation



cont = 1
while run:

    success, img = cap.read()
    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            figs = findPosition(img, handLms)
            dis8_0 = dis(figs[0], figs[8])
            dis9_0 = dis(figs[0], figs[9])
            dis12_0 = dis(figs[12], figs[0])
            disc = (dis8_0 - dis12_0) / dis9_0
            hs = int(np.sqrt(dis9_0))
            if disc > 1:
                try:
                    print(dis8_0, dis9_0, disc,hs)
                    dx = int(hs)
                    fir = cv2.resize(fre[fcont], (dx * 2, dx * 2))
                    mask[figs[8][2] - dx:figs[8][2]+dx, figs[8][1] - dx:figs[8][1] + dx] |= ImageRotate(fir)

                except:
                    pass

    mask = erode_x(mask)
    img |= mask
    cv2.imshow("Image", cv2.resize(img,(1024,768)))
    # cv2.imshow("mask", mask)
    cv2.waitKey(1)
cv2.destroyAllWindows()