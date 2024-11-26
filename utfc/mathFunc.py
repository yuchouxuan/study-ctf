#阿尔伯特曲线
def _hilbert(direction, rotation, order):
    if order == 0:
        return
    direction += rotation
    _hilbert(direction, -rotation, order - 1)
    step(direction)
    direction -= rotation
    _hilbert(direction, rotation, order - 1)
    step(direction)
    _hilbert(direction, rotation, order - 1)
    direction -= rotation
    step(direction)
    _hilbert(direction, -rotation, order - 1)

def rot_3d(pList,ali='x',ang=0):
    '''
    3d旋转 
        pList 需要是numpy类型([  [x,y,z],[x,y,z],[x,y,z]......])
        ang为角度制
    '''
    from math import cos,sin,radians
    import numpy as np
    a=radians(ang) 
    mats = {
        'x':[[1,0,0], [0,cos(a),-sin(a)], [0,sin(a),cos(a)]],# Rx
        'y':[[cos(a),0,sin(a)], [0,1,0], [-sin(a),0,cos(a)]],# Ry
        'z':[[cos(a),-sin(a),0], [sin(a),cos(a),0], [0,0,1]],# Rz
    }
    argMat = np.array(mats[ali])
    ret = []
    for i in pList:
        ret.append(argMat.dot(i))
    return np.array(ret)


def step(direction):
    next = {0: (1, 0), 1: (0, 1), 2: (-1, 0), 3: (0, -1)}[direction & 0x3]
    global x, y
    x.append(x[-1] + next[0])
    y.append(y[-1] + next[1])
def hilbert(order):
    global x, y
    x = [0,]
    y = [0,]
    _hilbert(0, 1, order)
    return (x, y)
