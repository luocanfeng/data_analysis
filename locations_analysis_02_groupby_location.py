# -*- coding: utf-8 -*-
"""
Created on Tue Dec 06 16:29:18 2016

@author: luocanfeng
"""
import time
import pandas as pd

# TODO: 每个人的本地路径都不一样，需要从这里设置
folder = 'D:/bigdata/unicom'

# TODO: 代码调试阶段，仅抽取部分数据样本进行分析
chunk_size = 10000


location_data_file_path = folder + '/locations_out.csv'
group_by_location_output_file_path = folder + '/group_by_location.csv'

start = time.time()
'''
IMEIs = pd.read_csv(IMEI_data_file_path, encoding='gbk')
Index2IMEIDict = IMEIs.set_index('index')['IMEI'].to_dict()
IMEIsCount = IMEIs.count()

reader = pd.read_csv(location_data_file_path, encoding='gbk', iterator=True)
chunk = reader.get_chunk(chunk_size)
print chunk.head()
chunk_max = chunk.max(0)
chunk_min = chunk.min(0)
longitde_min = chunk_min['Longitude']
longitde_max = chunk_max['Longitude']
latitude_min = chunk_min['Latitude']
latitude_max = chunk_max['Latitude']
print 'Longitude: [',longitde_min,',',longitde_max,'], Latitude: [',\
        latitude_min,',',latitude_max,']'
print chunk.groupby(['Longitude','Latitude']).count()
'''

data = pd.read_csv(location_data_file_path, encoding='gbk')
del data['DateAndHour']
groupby = data.groupby(['Longitude','Latitude'])
groupby_count = groupby.count()
groupby_count.columns = ['Counts'] #重命名表头
groupby_count.to_csv(group_by_location_output_file_path)

end = time.time(); elapsed = (end - start); start = end;
print 'Group data by location cost %.2fs\n\n\n'%elapsed

