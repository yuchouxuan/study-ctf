import wave
import matplotlib.pyplot as plt
import numpy as np
import struct
class WavF:
    strData = ''
    params = ''
    nchannels = 0
    sampwidth = 0
    framerate = 0
    nframes = 0
    strData = ''
    waveData = []
    def __init__(self, fn=''):
        self.open(fn)

    def open(self, fn=''):

        with wave.open(fn, 'rb') as f:
            self.params = f.getparams()
            print('params:', self.params)
            self.nchannels, self.sampwidth, self.framerate, self.nframes = self.params[:4]
            self.strData = f.readframes(self.nframes)  # 读取音频，字符串格式
            self.waveData = np.frombuffer(self.strData, dtype=np.int16).tolist()  # 将字符串转化为int

    def showit(self):
        time = np.arange(0, self.nframes) * (1.0 / self.framerate)
        plt.plot(time, self.waveData)
        plt.xlabel("Time(s)")
        plt.ylabel("Amplitude")
        plt.title("Single channel wavedata")
        plt.grid('on')  # 标尺，on：有，off:无。
        plt.show()


def CreateWav(fn='', datas=[0], framerate=8000, channel=2, sampwidth=2):
    with wave.open(fn, 'w') as f:
        f.setnchannels(channel)
        f.setsampwidth(sampwidth)
        f.setframerate(framerate)
        if isinstance(datas[0], list):
            for i in range(len(datas[0])):
                for j in range(channel):
                    try:
                        f.writeframesraw(struct.pack('h', int(round(datas[j][i]))))
                    except:
                        f.writeframesraw(struct.pack('h', 0))
        else:
            for i in datas:
                f.writeframesraw(struct.pack('h', int(round(i))))


from pydub import AudioSegment
def GetSoundData(fn=''):
    nchannels = 0
    sampwidth = 0
    framerate = 0
    nframes = 0
    waveData = []

    ret = {'filename ' :fn,
           'nchannels': 0,
           'sampwidth': 0,
           'framerate': 0,

           }

    if fn.endswith('.mp3'):
        f = AudioSegment.from_mp3
    elif fn.endswith('.ogg'):
        f = AudioSegment.from_ogg
    elif fn.endswith('.flv'):
        f = AudioSegment.from_flv
    elif fn.endswith('.raw'):
        f = AudioSegment.from_raw
    else:
        print('unkonwn')
        return ret
    sound = f(fn)
    print('AudioFile')
    print('- '*30)
    ret['nchannels'] = sound.channels
    ret['sampwidth'] = sound.sample_width
    ret['framerate'] = sound.frame_rate
    ret['frame_width'] =sound.frame_width
    ret['length(s)'] = sound.duration_seconds
    for i in ret:
        print(i,':',ret[i])
    print('- ' * 30)
    sds = sound.split_to_mono()
    ret['rawData'] = [x.raw_data for x in sds]
    ret['waveData'] =[x.get_array_of_samples() for x in sds]
    return ret

if __name__ == '__main__':
    ret = GetSoundData('z:/b.mp3')

    import matplotlib.pyplot as plt

    plt.figure(figsize=(20, 6))
    plt.subplot(311)
    plt.plot(ret['waveData'][1][200000::500])
    plt.subplot(312)
    plt.plot(ret['waveData'][1][200000:500000])
    a = np.abs(np.fft.fft(ret['waveData'][1][1000000:]))
    plt.subplot(313)
    '''
    fft 的 x轴 ： np.linspace(0,采样率//2,长度//2)
    '''
    fpx = np.linspace(0, 44100 // 2, len(a) // 2)
    plt.plot(fpx, a[:len(a) // 2])
    plt.show()