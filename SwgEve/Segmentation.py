import numpy as np
import matplotlib.pyplot as plt
import PreProcessing as pre
def smooth(zList,tList):
    zList_tmp=zList
    length = len(zList)
    config1 = 300
    config2 = 100
    newSize = config1 + config2 - 2
    tSmooth = tList[(int)(newSize / 2):length - (int)(newSize / 2)]
    # tSmooth = tList[:]
    zSmooth = [0 for i in range(0, length - newSize)]
    zList_tmp[:] = np.abs(zList_tmp)
    zSmooth[:] = np.convolve(zList_tmp, np.ones(config1) / config1, mode='valid')
    zSmooth[:] = np.convolve(zSmooth, np.ones(config2) / config2, mode='valid')
    return zSmooth,tSmooth

def findCuttingPoints(tSmooth,zSmooth,para):
    zSmooth=np.array(zSmooth)
    Mmax=np.max(zSmooth)
    Mmin=np.min(zSmooth)
    leng=zSmooth.size
    thres=para[0]*Mmin+para[1]*Mmax
    cuttingpoints=[]
    # =========================
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8, 6), sharey=True)
    # plt.xticks(np.linspace(0, 35000, 10))
    ax.set_title('cuttingpoints', fontsize=20)
    y = tSmooth * 0 + thres
    ax.plot(tSmooth, y, color='red')
    ax.plot(tSmooth, zSmooth, color='blue')

     # ========================
    for i in range(0,leng-1):
        if zSmooth[i]<=thres and zSmooth[i+1]>thres:
            cuttingpoints.append(i)
        elif zSmooth[i]>=thres and zSmooth[i+1]<thres:
            cuttingpoints.append(i)

    for i in cuttingpoints:
        plt.scatter(tSmooth[i], zSmooth[i], color='purple',linewidths=1)
    fig.show()
    return cuttingpoints
'''
1. ifft
2. smooth(moving average)
3. find Mmax and Mmin
4. set a threshold as 0.8Mmax+0.2Mmin
'''
# if __name__ == '__main__':
    # tList, xList, yList, zList = pre.readFile('siri_digits/siri_two_up_bass1.tsv')
    # # 714time==25039ms
    # tList, freqList, xList, yList, zList = pre.standardize(tList, xList, yList, zList, highpass=120/1000)
    # # pre.showMap(freqList, xList, yList, zList, 'high passed', ylim=(0, 15))
    # xList, yList, zList = pre.reverseFFT(xList, yList, zList)
    # # pre.showMap(tList, xList, yList, zList, '160hz filter')
    # zSmooth, tSmooth = smooth(zList, tList)
    #
    # # pre.showZMap(tSmooth, zSmooth, 'smoothed_conv')
    # cuttingpoints=findCuttingPoints(tSmooth,zSmooth)
    # print(cuttingpoints)
