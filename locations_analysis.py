# -*- coding: utf-8 -*-
"""
Created on Tue Dec 06 16:29:18 2016

@author: luocanfeng
"""
import time,datetime,math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# TODO: 每个人的本地路径都不一样，需要从这里设置
folder = 'D:/bigdata/unicom'

# TODO: 代码调试阶段，仅抽取部分数据样本进行分析
sample_data_size = 10000


# Suspend the SettingWithCopyWarning
# pd.options.mode.chained_assignment = None  # default='warn'


start = time.time()

datafilepath = folder + '/locations_out.csv'

IMEIs = pd.read_csv(folder + '/IMEIs.csv', encoding='gbk')
Index2IMEIDict = IMEIs.set_index('index')['IMEI'].to_dict()
IMEIsCount = IMEIs.count()
#print IMEIs.head()


sampleIMEISize = 16
randomIMEIIndexes = np.random.randint(0, 1000, sampleIMEISize)
randomIMEIIndexes.sort()
#print randomIMEIIndexes
maxIMEIIndex = max(randomIMEIIndexes)
#print 'maxIMEIIndex=', maxIMEIIndex

datas = {}
finished = False
large=1024*1024*1024; small=-large;
xmin,xmax,ymin,ymax,zmin,zmax=large,small,large,small,large,small
start_date=np.datetime64(datetime.datetime(2016, 12, 12))
reader = pd.read_csv(datafilepath, encoding='gbk', iterator=True)
while not finished:
    chunk = reader.get_chunk(sample_data_size)
    IMEIIdxes = chunk.groupby(['IMEIIdx']).groups.keys()
    for IMEIIdx in IMEIIdxes:
        if IMEIIdx in randomIMEIIndexes:
            data = chunk[chunk['IMEIIdx'] == IMEIIdx]
            data.loc[:, 'DateAndHour'] = pd.to_datetime(\
                    data['DateAndHour'].apply(str)
                            .apply(lambda s:s[0:4] + '-' + s[4:6] + '-'\
                                       + s[6:8] + ' ' + s[8:10]))
            '''
            data.loc[:, 'DateAndHour'] = data['DateAndHour'].apply(str)
            data.loc[:, 'DateAndHour'] = data['DateAndHour'].apply(lambda s:\
                    s[0:4] + '-' + s[4:6] + '-' + s[6:8] + ' ' + s[8:10])
            data.loc[:, 'DateAndHour'] = pd.to_datetime(data['DateAndHour'])
            '''
            xmin = min(xmin, min(data['Longitude']))
            xmax = max(xmax, max(data['Longitude']))
            ymin = min(ymin, min(data['Latitude']))
            ymax = max(ymax, max(data['Latitude']))
            start_date = min(start_date, min(data['DateAndHour']))
            if IMEIIdx in datas.keys():
                datas[IMEIIdx].append(data)
            else:
                datas[IMEIIdx] = data
        if IMEIIdx > maxIMEIIndex:
            finished = True
            break

# compute zmin and zmax
for IMEIIdx in randomIMEIIndexes:
    data = datas[IMEIIdx]
    data.columns = ['IMEIIdx', 'Hours', 'Longitude', 'Latitude']
    data.loc[:, 'Hours'] = data['Hours'].apply(lambda x:\
                                (x - start_date) / np.timedelta64(3600, 's'))
    #print data.head()
    zmin = min(zmin, min(data['Hours']))
    zmax = max(zmax, max(data['Hours']))


plt.rcParams['font.sans-serif'] = ['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False #用来正常显示负号
figure = plt.figure(figsize=(20, 20), dpi=400)
#for ax in figure.axes:
#    ax.get_xaxis().get_major_formatter().set_scientific(False)
#    ax.get_yaxis().get_major_formatter().set_scientific(False)

i = 1
for IMEIIdx in randomIMEIIndexes:
    IMEI = Index2IMEIDict[IMEIIdx]

    ax = plt.subplot(4, 4, i, projection='3d')
    plt.title(IMEI)
    plt.xlim(math.floor(xmin*10)/10, math.ceil(xmax*10)/10);
    plt.xlabel('Longitude')
    plt.ylim(math.floor(ymin*10)/10, math.ceil(ymax*10)/10);
    plt.ylabel('Latitude')
    ax.set_zlim(zmin, zmax)
    ax.set_zlabel('Hours')
    ax.get_xaxis().get_major_formatter().set_scientific(False)
    ax.get_yaxis().get_major_formatter().set_scientific(False)
    plt.plot(data['Longitude'], data['Latitude'], zs=data['Hours'], zdir='z')
    i = i + 1


figure.show()
figure.savefig(folder + '/test.png')


