import sys, urllib, urllib2, json  
class getDate:  
    def __init__(self):  
        pass  
    def get_day_type(self, query):  
        """ 
        @query a single date: string eg."20160404" 
        @return day_type: 0 workday -1 holiday 
 
        20161001:2 20161002:2 20161003:2 20161004:1  
        """  
          
        url = 'http://www.easybots.cn/api/holiday.php?d=' + query   
        req = urllib2.Request(url)  
        resp = urllib2.urlopen(req)  
        content = resp.read()  
  
        if(content):  
            # "0"workday, "1"leave, "2"holiday  
            day_type = content[content.rfind(":")+2:content.rfind('"')]  
            if day_type == '0':  
                return 0  
            else:  
                return -1  
  
if __name__ == '__main__':  
    MyDate = getDate()   
    print(MyDate.get_day_type("20170106"))  