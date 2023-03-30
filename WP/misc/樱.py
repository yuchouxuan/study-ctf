#因为水平有限，所以用了cv2，
#如果不想用轮子装X也可以自己实现光流

import cv2,numpy as np,matplotlib.pyplot as plt
cap = cv2.VideoCapture('out_flag.mp4')
ret, frame = cap.read()
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
mask = np.zeros_like(gray).astype(np.float64)
fr = 0
plt.figure(figsize=(12,8))
while True:
    fr +=1
    ret, frame = cap.read()
    if not ret:
        break
    gray_next = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    flow = cv2.calcOpticalFlowFarneback(gray, gray_next, None, 0.5, 3, 15, 3, 5, 1.2, 0)
    h, w = gray.shape
    y, x = np.mgrid[0:h:10, 0:w:10].reshape(2, -1).astype(int)
    fx, fy = flow[y, x].T
    lines = np.vstack([x, y, x + fx, y + fy]).T.reshape(-1, 2, 2)
    lines = np.int32(lines + 0.5)
    vis = np.zeros_like(gray)
    for (x1, y1), (x2, y2) in lines:
        if x1 > x2  and y1<y2:
            cv2.line(vis, (x1, y1), (x2, y2), 255 , 2)
    mask += vis&gray
    if fr % 10 ==0:
        show=mask.copy()
        cv2.putText(show,f'{fr}',(5,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, 255, 2)
        cv2.imshow('frame2', show)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    gray=gray_next
plt.imshow(np.log(mask))
plt.imshow(np.log(mask+1))
plt.show()
cap.release()
cv2.destroyAllWindows()
