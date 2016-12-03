# -*- coding: utf-8 -*-
"""
Created on Sat Dec 03 13:41:53 2016

@author: Administrator
"""
import time
import numpy as np
import pandas as pd

# TODO: 还跑不起来，待完善。

# TODO: 每个人的本地路径都不一样，需要从这里设置
folder = 'D:/bigdata/unicom'

t0 = time.time()

datafilepath = folder + '/locations.csv'

cols = ['Date', 'IMEI']
for i in range(24):
    cols.append(['Longitude%2d'%i, 'Latitude%2d'%i])
print cols
outCols = ['Date', 'IMEI', 'Longitude', 'Latitude']

data = pd.read_csv(datafilepath, encoding='gbk', header=None)
print data.columns

outData = data['Date', 'IMEI', 'Longitude00', 'Latitude00']
for i in range(1, 24):
    outData = outData.append(data['Date', 'IMEI', 'Longitude%2d'%i, 'Latitude%2d'%i])

t1 = time.time()
print 'Cost %ds'%(t1 - t0)

outputfilepath = folder + '/locations_out.csv'
data.to_csv(outputfilepath, index=False)

t2 = time.time()
print 'Cost %ds'%(t2 - t1)

