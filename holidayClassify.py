
import pandas as pd
import getDate
 
folder = 'G:\BigData\unioncom_data'
datafilepath = folder + '/locations_out_2.csv'
data = pd.read_csv(datafilepath, encoding='gbk', header=None)
print data.head()
MyDate = getDate.getDate()   

outdatas_holiday = []
outdatas_home = []
outdatas_work = []


for i in range(len(data)):
    outdata = []
   
    if( i == 0 ):
        outdata = data.iloc[0:1]
        outdatas_holiday.append(outdata)
        outdatas_home.append(outdata)
        outdatas_work.append(outdata)
        continue  
    #if MyDate.get_day_type(data.iloc[i][1][:-2]) == 0:
    if(data.iloc[i][1][:-2]) == '20151227' or data.iloc[i][1][:-2] == '20160101' or data.iloc[i][1][:-2] == '20160102' or data.iloc[i][1][:-2] == '20160103':
        outdata = data.iloc[i-1:i]
        outdatas_holiday.append(outdata)
        continue
    if(int(data.iloc[i][1][-2:]) >= 0 and int(data.iloc[i][1][-2:]) < 9 ) or (int(data.iloc[i][1][-2:]) >= 19 and int(data.iloc[i][1][-2:]) <= 23 ):
        outdata = data.iloc[i-1:i]
        outdatas_home.append(outdata)
        continue
    if(int(data.iloc[i][1][-2:]) and int(data.iloc[i][1][-2:])):
        outdata = data.iloc[i-1:i]
        outdatas_work.append(outdata)
        continue
outdatas_holiday = pd.concat(outdatas_holiday)
outdatas_home = pd.concat(outdatas_home)
outdatas_work = pd.concat(outdatas_work)

outputholidayfilepath = folder + '/locations_holiday.csv'
outdatas_holiday.to_csv(outputholidayfilepath, index=False)

outputworkfilepath = folder + '/locations_work.csv'
outdatas_work.to_csv(outputworkfilepath, index=False)

outputhomefilepath = folder + '/locations_home.csv'
outdatas_home.to_csv(outputhomefilepath, index=False)

print ("end")