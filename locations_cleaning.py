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


data = pd.read_csv(datafilepath, encoding='gbk', header=None)
print data.head()
t1 = time.time()
print 'Load data cost %ds'%(t1 - t0)


# TODO: 取一万条数据进行分析
subdata = data.iloc[0:10000,:]


outdatas = []
for i in range(24):
    outdata = subdata.iloc[:, [0, 1, i * 2 + 2, i * 2 + 3]]
    outdata.columns = ['Date', 'IMEI', 'Longitude', 'Latitude']
    outdata = outdata.dropna(axis=0)
    outdata['DateAndHour'] = outdata['Date'] * 100 + i
    del outdata['Date']
    outdata = outdata.ix[:, ['IMEI', 'DateAndHour', 'Longitude', 'Latitude']]
    outdatas.append(outdata)
outdatas = pd.concat(outdatas)
outdatas = outdatas.sort_values(['IMEI', 'DateAndHour'], ascending=True)
print outdatas.head()


outputfilepath = folder + '/locations_out.csv'
outdatas.to_csv(outputfilepath, index=False)


t2 = time.time()
print 'Cost %ds'%(t2 - t1)

