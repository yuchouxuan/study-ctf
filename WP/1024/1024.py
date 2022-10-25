#!/usr/bin/python3

from curses import wrapper,window
import  curses,numpy as np,time
import cv2 ,random 
class col :
    def __init__(self,lenx,mask,stdscr:window,colidx,hchar=' '):
        self.mask = mask 
        self.cs = list(hchar*lenx)
        self.stdscr = stdscr
        self.head = []
        self.x = colidx
    def show(self):
        stdscr= self.stdscr
        x=self.x
        for i in range(len(self.mask)):
            if self.mask[i] !=0 and self.max > i:
                stdscr.addstr(i, x,self.cs[i], curses.color_pair(0))
            else:
                 stdscr.addstr(i,x , self.cs[i], curses.color_pair(8))
            for i in self.head:
                for j in range(4):
                    if i-j >=0 :
                        try:
                            stdscr.addstr(i-j,x, self.cs[i-j], curses.color_pair(j))
                        except:pass

    def addhead(self):
        if len( self.head) >= 3: 
            return
        if len(self.head)>0 and min(self.head) < 5:
            return
        self.head.append(0)
        

    def step(self,p=1):
        if random.random()<=p:
            self.max +=1
            self.cs[1:] = self.cs[:-1]
            self.cs[0] = random.choice('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~')
            self.head= [n+1 for n in self.head if n < len(self.cs)]
        self.show()
    def step_out(self,p=1):
        if random.random()<=p:
            for pos in range(len(self.mask)):
                if self.mask[pos] !=0:
                     self.mask *=0
                     self.head.append(pos)
                     return

def main(stdscr:window):   
    w,h = stdscr.getmaxyx()
    strarr = np.zeros((w-1,h-1),np.uint8)[:,:-4] 
    curses.noecho()
    curses.cbreak()

    curses.use_default_colors() 
    if curses.can_change_color():
        curses.init_color(7,500,1000,500)
        curses.init_color(6,400,800,400)
        curses.init_color(4,300,500,300)
        curses.init_color(2,100,200,100)


    curses.init_pair(0, 7, curses.COLOR_BLACK)
    curses.init_pair(1, 6, curses.COLOR_BLACK)
    curses.init_pair(2, 4, curses.COLOR_BLACK)
    curses.init_pair(3, 2, curses.COLOR_BLACK)
    curses.init_pair(8, curses.COLOR_BLACK, curses.COLOR_BLACK)

    stdscr.move(0,0)
    curses.curs_set(0)
    stdscr.keypad(True)
    imglist = [cv2.resize((cv2.imread(f'{i}.png')[:,:,0]),(strarr.shape[1],strarr.shape[0])) for i in [4,3,2,1] ]
    cols = []
    roundtime=strarr.shape[1]
    for i in range(strarr.shape[1]):
        colone = col(strarr.shape[0],imglist[0][:,i],stdscr,i)
        cols.append(colone)
    for img in imglist:
        for i in range(len(cols)) :
            cols[i].mask = img[:,i]
            cols[i].max = 0 

        for cont in range(roundtime+10):  
            for i in cols:
                if random.random()<0.05:
                    i.addhead()
                i.step(0.8)
            stdscr.refresh()
            time.sleep(0.1)


        for cont in range(roundtime):  
            for i in cols:
                if random.random()<0.05:
                    i.step_out(1)
                    i.addhead()
                    i.step(1)
                i.step(0.8)
            
            stdscr.refresh()
            time.sleep(0.1)
    stdscr.getkey()
    # print(cols[-1].mask)

wrapper(main)
