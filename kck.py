from scipy.io import wavfile
from scipy.fftpack import fft
import numpy as np,os

def ff(signal,w):
    if len(np.shape(signal))>1:
        signal = [s[0] for s in signal]
        
    n = len(signal)
    freqs = np.arange(0,w,w/n)    

    signal1 = fft(signal)
    signal1 = abs(signal1)        
    signal1 = signal1 / n*2
    signal1[0]/=2
    
    sig = np.ones(np.shape(signal1))
    sig[:int(70*n/w)]=0
    sig[int(n/2)+1:]=0
    for i in np.arange(1,5):
        for j in range(int(len(sig)/i)):
            sig[j]*=signal1[j*i]

    return freqs[np.argmax(sig)]

    
def pred(ff):
    if ff <= 165 :pred = 'M'
    else:pred = 'K'
    return pred


def fp():
    n = len(signal)
    vote = {'M':0,'K':0}
    for j in range(3):
        for i in range(j+2):
            vote[pred(ff(signal[int(i*n/(2+j)):int((i+1)*n/(2+j))],w))]+=(1/(j+2))
    if vote['M']>1.5:p='M'
    else: p = 'K'
    #print(vote)
    return p


acc,full = 0,0

for file in os.listdir('trainall'):
    if(file == '008_K.wav'):continue #zatrymuje sie na tym pliku (?)
    
    w, signal = wavfile.read('trainall/'+file)
    signal = signal[::10]
    w = round(w/10)

    p = fp()
    print(p,file[4],end='')
    
    if p==file[4]:acc+=1;print()
    else:print('*')
    full+=1

print(acc/full)

