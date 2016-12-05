# -*- coding: utf-8 -*-
"""
Created on Sat Dec 03 13:41:53 2016

@author: luocanfeng
"""
import time
import pandas as pd

# TODO: 每个人的本地路径都不一样，需要从这里设置
folder = 'D:/bigdata/unicom'

# TODO: 代码调试阶段，仅抽取部分数据样本进行分析
sample_data_size = 20000


t0 = time.time()

datafilepath = folder + '/locations.csv'


reader = pd.read_csv(datafilepath, encoding='gbk', header=None, iterator=True)
data = reader.get_chunk(sample_data_size)
#data = pd.read_csv(datafilepath, encoding='gbk', header=None)
print data.head()

IMEIs = pd.read_csv(folder + '/IMEIs.csv', encoding='gbk')
IMEI2IndexDict = IMEIs.set_index('IMEI')['index'].to_dict()
print IMEIs.head()


t1 = time.time()
print 'Load data cost %ds'%(t1 - t0)


# indexing IMEI
data.iloc[:, 1] = data.iloc[:, 1].apply(lambda imei: IMEI2IndexDict[imei])
print data.head()
t2 = time.time()
print 'Indexing IMEI cost %ds'%(t2 - t1)


outdatas = []
for i in range(24):
    outdata = data.iloc[:, [0, 1, i * 2 + 2, i * 2 + 3]]
    outdata.columns = ['Date', 'IMEI', 'Longitude', 'Latitude']
    outdata = outdata.dropna(axis=0)
    outdata['DateAndHour'] = outdata['Date'] * 100 + i
    del outdata['Date']
    outdata = outdata.ix[:, ['IMEI', 'DateAndHour', 'Longitude', 'Latitude']]
    outdatas.append(outdata)
outdatas = pd.concat(outdatas)
outdatas = outdatas.sort_values(['IMEI', 'DateAndHour'], ascending=True)
print outdatas.head()
t3 = time.time()
print 'Process outcoming data cost %ds'%(t3 - t2)


outputfilepath = folder + '/locations_out.csv'
#outdatas.to_csv(outputfilepath, index=False)

t4 = time.time()
print 'Write outcoming data cost %ds'%(t4 - t3)



