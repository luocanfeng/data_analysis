#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 22:15:15 2016

@author: luocanfeng
"""
import math,time
import pandas as pd

# TODO: 每个人的本地路径都不一样，需要从这里设置
folder = 'D:/bigdata/unicom'


def outputInterests(GroupByIMEIs, IMEIDataFrame, columns, IMEIIndexRange, outputfile):
    output_start = time.time()
    # build result dataframe
    resultCols = ['IMEIIdx', 'AttendanceTimes', 'BankSMSCount', 'CarAppPv',\
                  'FinancialAppPv', 'StockAppPv', 'ScaleOfSocialCircle',\
                  'MonthsInterstates', 'MonthsAbroad', 'ShoppingSitePV',\
                  'ITSitePV', 'CateringSitePV', 'EstateSitePV', 'HealthySitePV',\
                  'FinancialSitePV', 'TourismSitePV', 'SportsSitePV',\
                  'CarSitePV', 'CurrentAffairsSitePV', 'SocialSitePV',\
                  'RecreationSitePV', 'RecruitSitePV', 'EducationSitePV',\
                  'OthersSitePV', 'OnlineGamesSitePV']
    IMEICount = IMEIDataFrame[cols[0]].count()
    result = pd.DataFrame(columns=resultCols)
    
    for i in IMEIIndexRange:
        if i >= IMEICount:
            break
        IMEI = IMEIDataFrame.get_value(i, col='IMEI')
        #print '%d, %s'%(i, IMEI)
        group = GroupByIMEIs.get_group(IMEI)
        groupCount = group[cols[0]].count()
        if groupCount > 10:
            row = [i, \
                   group[cols[0]].count(), \
                   sum(group[cols[1]]), \
                   sum(group[cols[2]]), \
                   sum(group[cols[3]]), \
                   sum(group[cols[4]]), \
                   group[cols[5]].mean(), \
                   sum(group[cols[6]]), \
                   sum(group[cols[7]]), \
                   sum(group[cols[8]]), \
                   sum(group[cols[9]]), \
                   sum(group[cols[10]]), \
                   sum(group[cols[11]]), \
                   sum(group[cols[12]]), \
                   sum(group[cols[13]]), \
                   sum(group[cols[14]]), \
                   sum(group[cols[15]]), \
                   sum(group[cols[16]]), \
                   sum(group[cols[17]]), \
                   sum(group[cols[18]]), \
                   sum(group[cols[19]]), \
                   sum(group[cols[20]]), \
                   sum(group[cols[21]]), \
                   sum(group[cols[22]]), \
                   sum(group[cols[23]])]
            result.loc[i] = row
        elif groupCount > 1:
            row = group.sum().tolist()
            row[0] = i
            row.insert(1, group[cols[0]].count())
            row[6] = group[cols[5]].mean()
            result.loc[i] = row
            '''statistics = group.describe()
            #print statistics.count, statistics.sum, statistics.mean
            row = [i, \
                   statistics.count, \
                   statistics[cols[1]].sum, \
                   statistics[cols[2]].sum, \
                   statistics[cols[3]].sum, \
                   statistics[cols[4]].sum, \
                   statistics[cols[5]].mean, \
                   statistics[cols[6]].sum, \
                   statistics[cols[7]].sum, \
                   statistics[cols[8]].sum, \
                   statistics[cols[9]].sum, \
                   statistics[cols[10]].sum, \
                   statistics[cols[11]].sum, \
                   statistics[cols[12]].sum, \
                   statistics[cols[13]].sum, \
                   statistics[cols[14]].sum, \
                   statistics[cols[15]].sum, \
                   statistics[cols[16]].sum, \
                   statistics[cols[17]].sum, \
                   statistics[cols[18]].sum, \
                   statistics[cols[19]].sum, \
                   statistics[cols[20]].sum, \
                   statistics[cols[21]].sum, \
                   statistics[cols[22]].sum, \
                   statistics[cols[23]].sum]'''
        else:
            row = group.iloc[0].values.tolist()
            row[0] = i
            row.insert(1, 1)
            result.loc[i] = row

    #intCols = copy.copy(resultCols)
    #intCols.remove('ScaleOfSocialCircle')
    #result[intCols].astype(int)
    #result.set_index('IMEIIdx')
    result.to_csv(outputfile, index=False)
    print '==== 已写入%s =====,耗时：%ds\n'%(outputfile, time.time() - output_start)



def processInterests(filepath, interestsColumns):
    start = time.time()
    
    cols = interestsColumns
    
    # load data
    df = pd.read_csv(filepath, encoding='gbk')
    print '记录总数: ', len(df)
    print '当前总耗时：%ds'%(time.time() - start), '\n'
    
    
    # 数据预处理
    #df.replace(regular=None, value=0)
    for i in [6, 7]:
        col = cols[i] # 是否有跨省行为, 是否有出国行为
        #df[col].replace(u'是', 1)
        #df[col].replace(u'否', 0)
        df[col][df[col] == u'是'] = 1
        df[col][df[col] == u'否'] = 0
    df = df.fillna(0)
    print '数据预处理完成'
    print '当前总耗时：%ds'%(time.time() - start), '\n'
    
    # IMEI
    col = cols[0]
    IMEIs = df[col].unique() # array
    print 'IMEI总数: ', len(IMEIs)
    print '当前总耗时：%ds'%(time.time() - start), '\n'
    
    # indexing IMEI
    IMEIDf = pd.DataFrame(data = {'IMEI': IMEIs})
    #print IMEIDf.head()
    #print IMEIDf.describe()
    IMEIDf.to_csv(folder + '/out/IMEIs.csv', index=True, index_label='index')
    #print IMEIDf.get_value(0, col='IMEI')
    #print IMEIDf.get_value(1, col='IMEI')
    print 'IMEI写入完成'
    print '当前总耗时：%ds'%(time.time() - start), '\n'
    #IMEIDf = pd.read_csv('D:/bigdata/unicom/out_03/IMEIs.csv', encoding='gbk')
    
    # group
    groupByIMEIs = df.groupby(by=[cols[0]])
    
    splitSize = 10000
    numberOfBlocks = int(math.ceil(len(IMEIs) / splitSize))
    for i in range(0, numberOfBlocks + 1):
        outputInterests(groupByIMEIs, IMEIDf, cols, \
                        range(i * splitSize, (i + 1) * splitSize), \
                        folder + '/out/interests_%02d.csv'%(i))

    end = time.time()
    print 'Cost %ds'%(end - start)



filepath = folder + '/original_interests.csv'
# filepath = folder + '/interest_10000.csv'
cols = [u'IMEI', u'月银行短信通知次数', u'使用汽车类APP的PV数', u'使用理财类APP的PV数',\
        u'使用股票类APP的PV数', u'交往圈规模', u'是否有跨省行为', u'是否有出国行为',\
        u'访问购物类网站的次数', u'访问IT类网站的次数', u'访问餐饮类网站的次数',\
        u'访问房产类网站的次数', u'访问健康类网站的次数', u'访问金融类网站的次数',\
        u'访问旅游类网站的次数', u'访问体育类网站的次数', u'访问汽车类网站的次数',\
        u'访问时事类网站的次数', u'访问社会类网站的次数', u'访问文娱类网站的次数',\
        u'访问招聘类网站的次数', u'访问教育类网站的次数', u'访问其他类网站的次数',\
        u'访问网游类网站的次数']

processInterests(filepath, cols)


