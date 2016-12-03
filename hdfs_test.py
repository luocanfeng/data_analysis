# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 16:47:53 2016

@author: Administrator
"""
# 需要安装hdfs，pip install hdfs
# 需要使用OpenVPN代理才能访问这个域名
from hdfs.client import Client

client = Client("http://hd1.dc.lan:50070")
# print dir(client)
print client.list("/data/unioncomm_data/original")

#with client.read("/data/unioncomm_data/original/location.csv") as fs:
#    df = pd.read_csv(fs, encoding='gbk')
#    print df.head()
