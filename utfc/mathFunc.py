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
