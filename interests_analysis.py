# -*- coding: utf-8 -*-
"""
Created on Thu Dec 01 12:05:07 2016

@author: Administrator
"""
import time, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import pairwise_distances_argmin

# TODO: 每个人的本地路径都不一样，需要从这里设置
folder = 'D:/bigdata/unicom'


def loadAndPreprocess(filepath):
    data = pd.read_csv(filepath, encoding='gbk')
    cols = ['IMEIIdx', 'AttendanceTimes', 'BankSMSCount', 'CarAppPv',\
                  'FinancialAppPv', 'StockAppPv', 'ScaleOfSocialCircle',\
                  'MonthsInterstates', 'MonthsAbroad', 'ShoppingSitePV',\
                  'ITSitePV', 'CateringSitePV', 'EstateSitePV', 'HealthySitePV',\
                  'FinancialSitePV', 'TourismSitePV', 'SportsSitePV',\
                  'CarSitePV', 'CurrentAffairsSitePV', 'SocialSitePV',\
                  'RecreationSitePV', 'RecruitSitePV', 'EducationSitePV',\
                  'OthersSitePV', 'OnlineGamesSitePV']
    divCols = copy.copy(cols)
    divCols.remove('IMEIIdx')
    divCols.remove('AttendanceTimes')
    divCols.remove('ScaleOfSocialCircle')
    
    sub = data.copy()
    sub ['IMEIIdx'] = 1
    sub ['ScaleOfSocialCircle'] = 1
    for col in divCols:
        sub[col] = sub['AttendanceTimes']
    
    data = data / sub
    data = data.set_index('IMEIIdx')
    del data['AttendanceTimes']
    
    return data

def kmeans(data):
    t0 = time.time()
    
    k = 30 #聚类的类别
    threshold = 200 #离散点阈值
    
    data_zs = 1.0 * (data - data.mean()) / data.std() #数据标准化
    data_zs = data_zs.fillna(0)
    
    model = KMeans(n_clusters=k, init='k-means++', verbose=1)
    model.fit(data_zs)
    
    #标准化数据及其类别
    r = pd.concat([data_zs, pd.Series(model.labels_, index = data.index)], axis = 1)  #每个样本对应的类别
    r.columns = list(data.columns) + ['classification'] #重命名表头
    
    norm = []
    for i in range(k): #逐一处理
        norm_tmp = r[data.columns][r['classification'] == i] - model.cluster_centers_[i]
        norm_tmp = norm_tmp.apply(np.linalg.norm, axis = 1) #求出绝对距离
        norm.append(norm_tmp / norm_tmp.median()) #求相对距离并添加
    norm = pd.concat(norm) #合并
    print norm.head()

    plt.rcParams['font.sans-serif'] = ['SimHei'] #用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False #用来正常显示负号
    norm[norm <= threshold].plot(style = 'go') #正常点

    discrete_points = norm[norm > threshold] #离群点
    discrete_points.plot(style = 'ro')

    #for i in range(len(discrete_points)): #离群点做标记
    #    id = discrete_points.index[i]
    #    n = discrete_points.iloc[i]
    #    plt.annotate('(%s, %0.2f)'%(id, n), xy = (id, n), xytext = (id, n))

    plt.xlabel(u'编号')
    plt.ylabel(u'相对距离')
    plt.show()
    
    #print 'labels_: \n', kmeans.labels_, '\n'
    #print 'cluster_centers_: \n', kmeans.cluster_centers_, '\n'
    print 'inertia_: \n', kmeans.inertia_, '\n'
    t1 = time.time()
    tcost = t1 - t0
    print 'KMeans cost %ds'%tcost
    
    ##############################################################################
    # Plot result
    #创建一个绘图对象, 并设置对象的宽度和高度, 如果不创建直接调用plot, Matplotlib会直接创建一个绘图对象
    '''
    当绘图对象中有多个轴的时候，可以通过工具栏中的Configure Subplots按钮，
    交互式地调节轴之间的间距和轴与边框之间的距离。
    如果希望在程序中调节的话，可以调用subplots_adjust函数，
    它有left, right, bottom, top, wspace, hspace等几个关键字参数，
    这些参数的值都是0到1之间的小数，它们是以绘图区域的宽高为1进行正规化之后的坐标或者长度。
    '''
    '''
    fig = plt.figure(figsize=(8, 3))
    fig.subplots_adjust(left=0.02, right=0.98, bottom=0.05, top=0.9)

    colors = ['#000000', '#080808', '#111111', '#191919', '#222222', '#2a2a2a',\
              '#333333', '#3b3b3b', '#444444', '#4c4c4c', '#555555', '#5d5d5d',\
              '#666666', '#6e6e6e', '#777777', '#808080', '#888888', '#919191',\
              '#999999', '#a2a2a2', '#aaaaaa', '#b3b3b3', '#bbbbbb', '#c4c4c4',\
              '#cccccc', '#d5d5d5', '#dddddd', '#e6e6e6', '#eeeeee', '#f7f7f7']
    
    # We want to have the same colors for the same cluster from the
    # MiniBatchKMeans and the KMeans algorithm. Let's pair the cluster centers per
    # closest one.
    k_means_cluster_centers = np.sort(kmeans.cluster_centers_, axis=0)
    k_means_labels = pairwise_distances_argmin(X, k_means_cluster_centers)
    
    # KMeans
    ax = fig.add_subplot(1, 3, 1) #add_subplot  图像分给为 一行三列，第一块
    for k, col in zip(range(30), colors):
        k_members = k_means_labels == k
        cluster_center = k_means_cluster_centers[k]
        ax.plot(X[k_members, 0], X[k_members, 1], 'w', markerfacecolor=col,\
                marker='.')
        ax.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,\
                markeredgecolor='k', markersize=6)
    ax.set_title('KMeans')
    ax.set_xticks(())
    ax.set_yticks(())
    plt.text(-3.5, 1.8, 'train time: %.2fs\ninertia: %f'%(tcost, kmeans.inertia_))
    '''
    
def pca(X):
    t0 = time.time()
    pca = PCA()
    pca.fit(X)
    t1 = time.time()
    tcost = t1 - t0
    print 'KMeans cost %ds'%tcost
    print 'explained_variance_ratio_: \n', pca.explained_variance_ratio_, '\n'



data = loadAndPreprocess(folder + '/interests.csv')
#print data.head(21)
#print data.isnull().sum()
#print data.isnull().sum().sum()
kmeans(data)
#pca(data)


