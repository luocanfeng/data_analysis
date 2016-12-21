# -*- coding: utf-8 -*-
"""
Created on Tue Dec 06 16:29:18 2016

@author: luocanfeng
"""
import time
import pandas as pd
import matplotlib.pyplot as plt

# TODO: 每个人的本地路径都不一样，需要从这里设置
folder = 'D:/bigdata/unicom'

# TODO: 代码调试阶段，仅抽取部分数据样本进行分析
chunk_size = 10000


group_by_location_output_file_path = folder + '/group_by_location.csv'

start = time.time()

data = pd.read_csv(group_by_location_output_file_path, encoding='gbk')
data = data.drop('Longitude', 1).drop('Latitude', 1)
data['OccurrenceTimes'] = 1
groupby = data.groupby('Counts')
groupby_count = groupby.count()
groupby_count['Counts'] = groupby_count.index
groupby_count = groupby_count[['Counts','OccurrenceTimes']]
print groupby_count.head()
x_min,x_max = min(groupby_count['Counts']), max(groupby_count['Counts'])
y_min,y_max = min(groupby_count['OccurrenceTimes']),\
              max(groupby_count['OccurrenceTimes'])
print x_min,x_max,y_min,y_max


plt.rcParams['font.sans-serif'] = ['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False #用来正常显示负号
figure = plt.figure(figsize=(12, 12), dpi=400)

ax = plt.subplot(1, 1, 1)
ax.ticklabel_format(style='plain', axis='both')
ax.set_title(u'位置出现次数统计')
ax.set_xlim(x_min - 1, x_max + 1)
ax.set_xlabel(u'位置出现次数')
ax.set_ylim(y_min - 1, y_max + 1)
ax.set_ylabel(u'出现这么多次数的位置总数')
ax.plot(groupby_count['Counts'], groupby_count['OccurrenceTimes'], 'go')

figure.show()

figure.savefig(folder + '/location_occurence_distribution.png')


end = time.time(); elapsed = (end - start); start = end;
print 'Cost %.2fs\n\n\n'%elapsed

