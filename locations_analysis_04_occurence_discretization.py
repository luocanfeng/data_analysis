# -*- coding: utf-8 -*-
"""
Created on Tue Dec 06 16:29:18 2016

@author: luocanfeng
"""
import time
import pandas as pd
from sklearn.cluster import KMeans #导入K均值聚类算法
import matplotlib.pyplot as plt

# TODO: 每个人的本地路径都不一样，需要从这里设置
folder = 'D:/bigdata/unicom'

# TODO: 代码调试阶段，仅抽取部分数据样本进行分析
chunk_size = 10000


group_by_location_output_file_path = folder + '/group_by_location.csv'

start = time.time()

data = pd.read_csv(group_by_location_output_file_path, encoding='gbk')
print data.head()

tmp = data.drop('Longitude', 1).drop('Latitude', 1)
#print tmp.head()

# TODO: 按每个聚类数量均分进行离散化处理
k = 64 #需要进行的聚类类别数
kmodel = KMeans(n_clusters=k, init='k-means++')
kmodel.fit(tmp) #训练模型

# 对中心点进行排序，次数多的颜色深
r1 = pd.DataFrame(kmodel.cluster_centers_, columns = ['ClusterCenter'])\
        .sort_values('ClusterCenter') #聚类中心
r1['Color'] = ['#'+3*('%s'%(hex(i*2)[2:].zfill(2))) for i in range(k)[::-1]]
label2ColorDict = r1['Color'].to_dict()
#print label2ColorDict


#每个样本对应的类别
r = pd.concat([data, pd.Series(kmodel.labels_, index = data.index)], axis = 1)
r.columns = list(data.columns) + ['Classification'] #重命名表头
r['Color'] = r['Classification']
r.loc[:, 'Color'] = r.loc[:, 'Color'].apply(lambda c: label2ColorDict[c])
print r.head()

x_min,x_max = min(data['Longitude']), max(data['Longitude'])
y_min,y_max = min(data['Latitude']), max(data['Latitude'])

plt.rcParams['font.sans-serif'] = ['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False #用来正常显示负号
figure = plt.figure(figsize=(12, 12), dpi=400)

ax = plt.subplot(1, 1, 1)
ax.ticklabel_format(style='plain', axis='both')
ax.set_title(u'热力图')
ax.set_xlim(x_min, x_max)
ax.set_xlabel(u'经度')
ax.set_ylim(y_min, y_max)
ax.set_ylabel(u'纬度')
ax.scatter(r['Longitude'], r['Latitude'], color=r['Color'], marker='.')

figure.show()

figure.savefig(folder + '/location_occurence_distribution.png')


end = time.time(); elapsed = (end - start); start = end;
print 'Cost %.2fs\n\n\n'%elapsed

