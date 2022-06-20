import cv2
import tqdm as tqdm
import libnum
import numpy as np


class VideoFunc:
    def __init__(self, fn=None):
        if fn == None:
            self.fps = 30
            self.size = (1280, 720)
            self.fNUMS = 0
            self.forucc = '1cva'
            fn = 'noname'
        else:
            self.fn = fn
            videoCapture = cv2.VideoCapture(self.fn)
            # 获得码率及尺寸
            self.fps = videoCapture.get(cv2.CAP_PROP_FPS)
            self.size = (
            int(videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH)), int(videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
            self.fNUMS = videoCapture.get(cv2.CAP_PROP_FRAME_COUNT)
            self.forucc = libnum.n2s(int(videoCapture.get(cv2.CAP_PROP_FOURCC))).decode()

        print('- ' * 30)
        print(f'fourcc: {self.forucc}')
        print(f'fps   : {self.fps}')
        print(f'size  : {self.size[0]}*{self.size[1]}')
        print(f'Fnum  : {self.fNUMS}')
        print('- ' * 30)
        self.frames = []
        videoCapture = cv2.VideoCapture(fn)

    def getFrames(self, fn=None):
        if fn==None:
            fn = self.fn
        frames = []
        videoCapture = cv2.VideoCapture(fn)
        for i in tqdm.trange(int(self.fNUMS)):
            success, frame = videoCapture.read()  # 获取下一帧
            frames.append(frame)
        videoCapture.release()
        self.frames = frames
        return frames

    def writeFile(self, fn='noname.mp4', cc='mp4v'):
        '''cc
        MJPG   ->.avi
        mp4v   ->.mp4
        '''
        writer = cv2.VideoWriter_fourcc(*cc)
        videoWriter = cv2.VideoWriter(fn, writer, self.fps, self.size)
        for i in tqdm.tqdm(self.frames):
            videoWriter.write(np.array(i))
        videoWriter.release()