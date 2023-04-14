import numpy as np, cv2,matplotlib.pyplot as plt 
import random 
flag='ctfshow{0bd8350e-1f03-46cc-bd26-fdd55edd548e}'
img0= cv2.imread('z:/ctf/fox2.png')
# img0=np.round(np.mean(img0,axis=2)).astype(np.uint8)


class window:
    vy,vx = 9,9 
    x,y,=0,0
    h,w,=0,0
    win=0
    def __init__(self,img,win=32,vmax=9):
        self.win=win
        self.vmax=vmax
        self.img=img
        self.h,self.w = img.shape[0],img.shape[1]
        self.x = random.randint(0, self.w-win)
        self.y = random.randint(0,self.h-win) 
    def getimg(self):
        return self.img[self.y:self.y+self.win,self.x:self.x+self.win]
    
    def next(self,ap=0.2,debug=False):
        if debug:
            print(self.x,self.y,self.vx,self.vy,'=>',end='')
        #步进
        self.x+=self.vx 
        self.y+=self.vy 
        if self.x<0 :
            self.vx*=-1
            self.x=0
        elif self.x>self.w-self.win : 
            self.vx*=-1
            self.x=self.w-self.win
        if self.y<0 :
            self.vy*=-1
            self.y=0
        elif self.y>self.h-self.win : 
            self.vy*=-1
            self.y=self.h-self.win  
        #计算加速度         
        if random.random() > ap:
            ax,ay=0,0
        else:
            self.vx = self.vx + random.randint(-5, 5)
            self.vy = self.vy + random.randint(-5, 5)
            if self.vx > self.vmax :
                self.vx = self.vmax
            elif self.vx < -self.vmax:
                self.vx = -self.vmax
            if self.vy >self.vmax:
                self.vy=self.vmax
            elif self.vy < -self.vmax:
                self.vy = -self.vmax
        if debug:
            print(self.x,self.y,self.vx,self.vy)
            

win = window(img0)        
size = (win.win,win.win)
fourcc = cv2.VideoWriter_fourcc(*'MP4V') 
out = cv2.VideoWriter('z:/ctf/flag.mp4', fourcc, 3000.0, size)

plt.imshow(win.getimg())
img = np.zeros_like(img0)
for i in range(40000):
    img_t=win.getimg()&0xf0 +random.randint(0, 0x0f)
    img[win.y:win.y+win.win, win.x:win.x+win.win] = img_t
    out.write(img_t)
    if i % 1000==0:
        cv2.imshow('view',img)
        cv2.imshow('view-small', img_t)
        cv2.waitKey(30)
        print(i)
    win.next()
out.release()
cv2.destroyAllWindows()
plt.imshow(img)
plt.show()
