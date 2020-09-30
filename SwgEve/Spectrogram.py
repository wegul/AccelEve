import SwgEve.PreProcessing as pre
import SwgEve.Segmentation as seg
import matplotlib.pyplot as plt
import math
import numpy as np
import cv2

def generateMap(xList, yList, zList):
    # global tList, xList, yList, zList

    NFFT = 128  # the length of the windowing segments
    noverlap=120
    Fs = 1000  # the sampling frequency
    fig,(plot_X,plot_Y,plot_Z)=plt.subplots(ncols=3)


    specX,ts,freqsX,picX=plot_X.specgram(xList,NFFT=NFFT,Fs=Fs,noverlap=noverlap)
    specY,ts,freqsY,picY=plot_Y.specgram(yList, NFFT=NFFT, Fs=Fs, noverlap=noverlap)
    specZ,ts,freqZ,picZ=plot_Z.specgram(zList, NFFT=NFFT, Fs=Fs, noverlap=noverlap)

    plot_X.set_title("X AXIS_ONE")
    plot_X.set_xlabel("time")
    plot_X.set_ylabel("frequency")
    plot_Y.set_title("Y AXIS_ONE")
    plot_Y.set_xlabel("time")
    plot_Y.set_ylabel("frequency")
    plot_Z.set_title("Z AXIS_ONE")
    plot_Z.set_xlabel("time")
    plot_Z.set_ylabel("frequency")
    plt.show()
    return specX, specY, specZ


def generateRGB(specX, specY, specZ,name):
    R_x=np.zeros(shape=specX.shape)
    G_y=np.zeros(shape=specX.shape)
    B_z=np.zeros(shape=specX.shape)
    for i in range(specX.shape[0]):
        for j in range(specX.shape[1]):
            R_x[i,j]=math.sqrt(specX[i,j])
    maxi=np.max(R_x)

    mini=np.min(R_x)
    R_x=np.ceil((255/(maxi-mini))*(R_x-mini))

    for i in range(specX.shape[0]):
        for j in range(specX.shape[1]):
            G_y[i,j]=math.sqrt(specY[i,j])
    maxi = np.max(G_y)
    mini = np.min(G_y)
    G_y = np.ceil((255 / (maxi - mini)) * (G_y - mini))
    print(np.mean(G_y))
    for i in range(specX.shape[0]):
        for j in range(specX.shape[1]):
            B_z[i,j]=math.sqrt(specZ[i,j])

    maxi=np.max(B_z)
    mini=np.min(B_z)

    B_z=np.ceil((255/(maxi-mini))*(B_z-mini))
    print(np.mean(B_z))

    img=np.zeros(shape=(specX.shape[0],specX.shape[1],3))
    for i in range(specX.shape[0]):
        for j in range(specX.shape[1]):
            img[i,j,2]=0
            img[i, j, 1] = 0
            img[i,j,0]=255-B_z[i,j]
    cv2.imwrite(name,img)
    # cv2.imshow('rgb',img)
    # cv2.waitKey()


def main():
    global tList, xList, yList, zList
    tList, xList, yList, zList = pre.readFile('src/handhold926swgfive.tsv')

    tList, freqList, xList, yList, zList = \
        pre.standardize(tList, xList, yList, zList, highpass=85/ 1000)

    xList, yList, zList = pre.reverseFFT(xList, yList, zList)
    #pre.showMap(tList, xList, yList, zList, '85hz filter')
    # zSmooth, tSmooth = seg.smooth(zList, tList)
    # cuttingpoints=seg.findCuttingPoints(tSmooth,zSmooth)
    # print(cuttingpoints)
    cuttingpoints=[1401, 2266, 4928, 6239, 7386, 7790, 10175, 11822]



    # cuttingpoints = [2409, 2954, 4915, 5346, 7241, 7623, 9472, 9837, 11690, 11916, 14050,
    #                  14262, 16384, 16652, 18341, 18706, 20431, 20978, 22846, 23242]
    cnt=0
    for i in range(0,8,2):
        x_one=xList[cuttingpoints[i]:cuttingpoints[i+1]+1]
        y_one=yList[cuttingpoints[i]:cuttingpoints[i+1]+1]
        z_one=zList[cuttingpoints[i]:cuttingpoints[i+1]+1]
        specX,specY,specZ=generateMap(x_one,y_one,z_one)
        generateRGB(specX, specY, specZ,'./RGB'+str(cnt)+'five.png')
        cnt+=1



if __name__=='__main__':
    tList=[]
    xList=[]
    yList=[]
    zList=[]
    main()