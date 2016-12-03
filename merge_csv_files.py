# -*- coding: utf-8 -*-
"""
Created on Thu Dec 01 16:20:03 2016

@author: Administrator
"""
import time
import pandas as pd

# TODO: 每个人的本地路径都不一样，需要从这里设置
folder = 'D:/bigdata/unicom'

def loadSplitedData(folder):
    filepath = folder + '/interests_%02d.csv'%0
    df = pd.read_csv(filepath, encoding='gbk')
    data = df
    for i in range(0, 64 + 1):
        filepath = folder + '/interests_%02d.csv'%i
        df = pd.read_csv(filepath, encoding='gbk')
        data = data.append(df)
    return data

def merge(folder):
    data = loadSplitedData(folder)
    #print data.head()
    #print data.describe()
    data.to_csv(folder + '/interests.csv', index=False)
    print 'merge finished'

start = time.time()
merge(folder)
print 'merge cost %ds'%(time.time() - start)

