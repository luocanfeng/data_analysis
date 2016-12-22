# -*- coding: utf-8 -*-
"""
Created on Thu Dec 22 18:10:30 2016

@author: dongjie
"""
#-*- coding:utf-8 -*-
from __future__ import division
from pandas import Series, DataFrame
import pandas as pd
from numpy.random import randn
import numpy as np
pd.options.display.max_rows = 12
np.set_printoptions(precision=4, suppress=True)
import matplotlib.pyplot as plt
plt.rc('figure', figsize=(12, 4))
plt.rc('font',**{'family':'sans-serif','sans-serif':['AR PL KaitiM GB']})
import pymongo_class as mongdb_class           
import location_compute as computer
Locationcomputer = computer.LocationComputeClass()

get_mongo_imei = mongdb_class.MongoClass('10.82.0.1',27017,'unicom','imei');
get_mongo_location = mongdb_class.MongoClass('10.82.0.1',27017,'unicom','location');
get_mongo_date = mongdb_class.MongoClass('10.82.0.1',27017,'unicom','date');
get_mongo_address = mongdb_class.MongoClass('10.82.0.1',27017,'unicom','address');

folder = 'G:\BigData\code\data'

data_location = pd.read_csv(folder + '\location_10000.csv',encoding='gbk') 
tz_counts = data_location['IMEI'].value_counts()
IMEI = pd.DataFrame(tz_counts.index)
IMEI.columns = ['imei']

#将IMEI插入到mongo
for i in range(len(IMEI)):
    temp = {}
    temp['IMEI'] =  IMEI['imei'][i]
    #get_mongo_imei.insert_mongo(temp)
date_counts = data_location['date'].value_counts()
len(date_counts)
date = pd.DataFrame(date_counts.index)
date.columns = ['date']    
#将日期插入到mongo数据库
for i in range(len(date)):
    temp = {}
    temp['date'] = str(date['date'][i])
    temp['week'] = str("星期一")
    #get_mongo_date.insert_mongo(temp)
    
for i in range(len(data_location)):
    temp = {}
    norepeatroute = []
    temp['date'] = str(data_location['date'][i])
    temp['IMEI'] = data_location['IMEI'][i]
    #去除一天中用户所有坐标，及相邻的重复点坐标
    norepeatroute, route = Locationcomputer.removalAdjacentDuplicatePoints(data_location.ix[i])
    temp['route'] = route
    temp['norepeatroute'] = norepeatroute
    
    location = Locationcomputer.nonRepeatingPoint(norepeatroute)    
    routecountTmp = Locationcomputer.locationcount(location, data_location.ix[i])
    routecount = Locationcomputer.mostCommonLocation(routecountTmp)
    temp['routecount'] = routecount
    #get_mongo_location.insert_mongo(temp)
    
address=get_mongo_address.find_mongo()
location = get_mongo_location.find_mongo()
Locationcomputer.locationAdress(location,address)

    


