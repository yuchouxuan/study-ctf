'''
f(x) = sin(wπ+π/6)² =0 在 (0,3π) 恰好有五个解
'''

import numpy as np
import matplotlib.pyplot as plt 
pi = np.pi 
maxxy=50
fi = plt.figure()
def rsa():
  
    sa = fi.gca()
    sa.spines['top'].set_color(None)
    sa.spines['right'].set_color(None) 
    sa.xaxis.set_ticks_position('bottom')
    sa.spines['bottom'].set_position(('data', 0))
    sa.yaxis.set_ticks_position('left')
    sa.spines['left'].set_position(('data', 0))
    plt.xlim(-pi,pi*4)
    plt.ylim(-1.5,1.5)

rsa()
x = np.linspace(-pi/2,4*pi,200)
for w in np.linspace(1,2,100):
    y = np.sin(w*x+pi/6)
    # plt.cla()
    plt.clf()
    rsa()
    
    
    
    plt.hlines(1,0,3*pi,'b','--',)
    plt.hlines(-1,0,3*pi,'b','--')
    plt.vlines(pi*3,-1.5,1.5,'r','--')
    plt.text(3*pi,0,' 3π',color='r')
    
    zeros=0
    for k in range(6): 
        x1 = (k+1/3)*pi/w
        if x1<3*pi:
            plt.plot(x1,np.sin(w*x1+pi/6),'ro')
            zeros +=1
    if zeros==5:
        plt.plot(x,y,'g')
    else:
        plt.plot(x,y,'r')
    plt.title(f'w={w:1.3} , zeros={zeros}')
    plt.pause(0.2)
    # plt.show()