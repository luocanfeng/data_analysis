# -*- coding: utf-8 -*-
"""
Created on Sat Dec 03 13:41:53 2016

@author: luocanfeng
"""
import time, copy
import pandas as pd

# TODO: 每个人的本地路径都不一样，需要从这里设置
folder = 'D:/bigdata/unicom'

# TODO: 代码调试阶段，仅抽取部分数据样本进行分析
sample_data_size = 10000


start = time.time()

datafilepath = folder + '/locations.csv'


#reader = pd.read_csv(datafilepath, encoding='gbk', header=None, iterator=True)
#data = reader.get_chunk(sample_data_size)
data = pd.read_csv(datafilepath, encoding='gbk', header=None)
cols = ['Date', 'IMEI']
for i in range(24):
    cols.append('Longitude%02d'%i)
    cols.append('Latitude%02d'%i)
data.columns = cols
print data.head()
print '记录总数: ', len(data)

IMEIs = pd.read_csv(folder + '/IMEIs.csv', encoding='gbk')
IMEI2IndexDict = IMEIs.set_index('IMEI')['index'].to_dict()
print IMEIs.head()

end = time.time(); elapsed = (end - start); start = end;
print 'Load data cost %.2fs\n\n\n'%elapsed


# indexing IMEI
data.iloc[:, 1] = data.iloc[:, 1].apply(lambda imei: IMEI2IndexDict[imei])
cols = ['IMEIIdx' if col=='IMEI' else col for col in cols]
data.columns = cols
sortedCols = copy.copy(cols)
sortedCols[0] = cols[1]; sortedCols[1] = cols[0];
data = data.ix[:, sortedCols]
data = data.sort_values(['IMEIIdx', 'Date'], ascending=True)
print data.head()

end = time.time(); elapsed = (end - start); start = end;
print 'Indexing IMEI cost %.2fs\n\n\n'%elapsed


outdatas = []
for i in range(24):
    outdata = data.iloc[:, [0, 1, i * 2 + 2, i * 2 + 3]]
    outdata.columns = ['IMEIIdx', 'DateAndHour', 'Longitude', 'Latitude']
    outdata = outdata.dropna(axis=0)
    outdata['DateAndHour'] = outdata['DateAndHour'] * 100 + i
    outdatas.append(outdata)
outdatas = pd.concat(outdatas)
outdatas = outdatas.sort_values(['IMEIIdx', 'DateAndHour'], ascending=True)
print outdatas.head()

end = time.time(); elapsed = (end - start); start = end;
print 'Process outcoming data cost %.2fs\n\n\n'%elapsed


outputfilepath = folder + '/locations_out.csv'
outdatas.to_csv(outputfilepath, index=False)

end = time.time(); elapsed = (end - start); start = end;
print 'Write outcoming data cost %.2fs\n\n\n'%elapsed


reader = pd.read_csv(outputfilepath, encoding='gbk', iterator=True)
outdatas = reader.get_chunk(sample_data_size)
print outdatas.head()

