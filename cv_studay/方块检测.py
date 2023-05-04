import cv2
import numpy as np
def ShapeDetection(img,minarea=None):
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)  #寻找轮廓点
    if minarea is None:
        minarea = (img.shape[0]/40)**2
    for obj in contours:
        area = cv2.contourArea(obj)  #计算轮廓内区域的面积
        if area < minarea :continue
        perimeter = cv2.arcLength(obj,True)  #计算轮廓周长
        approx = cv2.approxPolyDP(obj,0.02*perimeter,True)  #获取轮廓角点坐标
        CornerNum = len(approx)   #轮廓角点的数量
        x, y, w, h = cv2.boundingRect(approx)  #获取坐标值和宽度、高度
        if CornerNum == 4:
            if w==h: objType= "Square"
            else:objType="Rectangle"
        else:
            continue
            objType="N"
        cv2.rectangle(imgContour,(x,y),(x+w,y+h),(0,0,255),2)  #绘制边界框
        cv2.putText(imgContour,objType,(x+(w//2),y+(h//2)),cv2.FONT_HERSHEY_COMPLEX,0.6,(0,0,0),1)  #绘制文字

fn = 'z:/ctf/fox.jpg'
img = cv2.imread(fn)
imgContour = img.copy()
gav=img.shape[0]//200*2+1
can=img.shape[0]//50
imgGray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)  #转灰度图
imgGray//=16
imgGray*=16
imgBlur = cv2.GaussianBlur(imgGray,(gav,gav),1)  #高斯模糊
imgCanny = cv2.Canny(imgBlur,can,can)  #Canny算子边缘检测
ShapeDetection(imgCanny)  #形状检测
cv2.imshow("imgCanny", imgCanny)
cv2.imshow("shape Detection", imgContour)
cv2.waitKey(0)