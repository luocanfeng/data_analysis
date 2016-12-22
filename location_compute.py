# -*- coding: utf-8 -*-
"""
Created on Thu Dec 22 18:44:35 2016

@author: dongjie
"""
from pandas import Series, DataFrame
import pandas as pd
from numpy.random import randn
import numpy as np
from bson.objectid import ObjectId
class LocationComputeClass:
    #去除一天中用户相邻的重复点坐标
    def removalAdjacentDuplicatePoints(self,data_location):
        tmp_x, tmp_y, count = 0, 0 , 0
        norepeatPoint = []
        originalPoint = []
        for j in range(24):
            arry_point = []
            array_no_repeat = []
            if np.isnan( data_location[ j * 2 + 2]):
                continue
            if count == 0:
                tmp_x = data_location[ j * 2 + 2]
                tmp_y = data_location[ j * 2 + 3]
                array_no_repeat.append(data_location[ j * 2 + 2])
                array_no_repeat.append(data_location[ j * 2 + 3])
                norepeatPoint.append(array_no_repeat)
                count = 1
                arry_point.append(data_location[ j * 2 + 2])
                arry_point.append(data_location[ j * 2 + 3])
                originalPoint.append(arry_point) 
                continue
            if (count != 0) and (data_location[ j * 2 + 2] != tmp_x) and (data_location[ j * 2 + 3] != tmp_y):
                tmp_x = data_location[ j * 2 + 2]
                tmp_y = data_location[ j * 2 + 3]
                array_no_repeat.append(data_location[ j * 2 + 2])
                array_no_repeat.append(data_location[ j * 2 + 3])
                norepeatPoint.append(array_no_repeat)
            arry_point.append(data_location[ j * 2 + 2])
            arry_point.append(data_location[ j * 2 + 3])
            originalPoint.append(arry_point) 
        return norepeatPoint,originalPoint
    
    #统计一天中用户出现的不重复坐标
    def nonRepeatingPoint(self,norepeatroute):
        location = []
        for i in range(len(norepeatroute)):
            if i == 0:
                location.append(norepeatroute[i])
                continue
            for j in range(len(location)):
                if (norepeatroute[i][0] == location[j][0]) and (norepeatroute[i][1] == location[j][1]):
                    break
                if (j == len(location) -1) :
                    location.append(norepeatroute[i])
        return location 
        
    def coutertime(self,times):
        time = []
        start = times[0]
        timestr = ""
        tmp = 0
        for i in range(len(times)):
            if ( len(times) == 1):
                time.append(str(times[i])+"点")
                break
            if (i == len(times) - 2):
                if (times[i + 1] - times[i] == 1):
                    end = times[i+1]
                    timestr = str(start) +"点~"+ str(end) +"点"
                    time.append(timestr)
                    break
                else:
                    end = times[i]
                    if start - end == 0:
                        timestr = start
                        time.append(str(timestr)+"点")
                        time.append(str(times[i+1])+"点")
                        break
                    else:
                        timestr = str(start) +"点~"+ str(end) +"点"
                        time.append(timestr) 
                        time.append(str(times[i+1])+"点")
                        break
                
            tmp = times[i + 1] - times[i]
            if tmp == 1 :           
                 continue
            else:
                end = times[i]
                if start - end == 0:
                    timestr = start
                    time.append(str(timestr)+"点")
                    start = times[i + 1]
                else:
                    timestr = str(start) +"点~"+ str(end)+"点"
                    start = times[i + 1]
                    time.append(timestr)
        
        return time
        
    #统计一天中用户出现的不重复坐标及坐标出现时间
    def locationcount(self,location, data_location):
        routecount = []
        for t in range(len(location)):
            locationcount = {}
            locationcount['location'] = location[t]
            time = []
            for k in range(24):          
                if(np.isnan( data_location[ k * 2 + 2])):
                   continue
                if(data_location[ k * 2 + 2] == location[t][0] and data_location[ k * 2 + 3] == location[t][1]):
                    time.append(k)
            locationcount['time'] = time
            #print time
            #print coutertime(coutertime(time))
            locationcount['timerange'] = self.coutertime(time)
            routecount.append(locationcount)
        return routecount
        
    def mostCommonLocation(self,routecount):
        times = []
        newroutecount = []
        for t in range(len(routecount)):
            times.append(len(routecount[t]['time']))
            routecount[t]['flag'] = 1
        times.sort(reverse = True)
        for j in range(len(times)):
            locationcount = {}
            for k in range(len(routecount)):
                if (routecount[k]['flag'] == 0):
                    continue
                if(len(routecount[k]['time']) == times[j]):               
                    locationcount['location'] = routecount[k]['location']
                    locationcount['time'] = routecount[k]['time']
                    locationcount['timerange'] = routecount[k]['timerange']
                    routecount[k]['flag'] = 0
                    newroutecount.append(locationcount)
                    break
            
        return newroutecount
        
    def locationAdress(self,location,address):
        locationnew = location
        for i in range(len(location)): 
            for j in range(len(location[i]['routecount'])):
                for k in range(len(address)):
                    addresstmp = {}
                    if locationnew[i]['routecount'][j]['location'] == address[k]['location'] and len(address[k]["result"]["pois"]) > 0: 
                        addresstmp['name'] = address[k]["result"]["pois"][0]["name"]
                        addresstmp['tag'] = address[k]["result"]["pois"][0]["tag"]
                        locationnew[i]['routecount'][j]['address'] = addresstmp
                        locationnew[i]["_id"] = ObjectId(location[i]["_id"])
                        #print  locationnew[i]
                        #get_mongo_location.updata_mongo({"_id":ObjectId(location[i]["_id"])},  locationnew[i])
                        break
                    

        
