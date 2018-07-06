from pandas import read_csv, DataFrame
import os
import re


targetCommunityName = []

allCommunity = read_csv(r"allCommunity.csv", encoding = 'gbk')

for communityIndex in range(len(allCommunity)):
    filePath = "./AllCommunity/" + allCommunity["communityName"][communityIndex] + ".csv"
    if os.path.getsize(filePath) < 5:
        continue
    else:
        homeDataFrame = read_csv(filePath, encoding = 'gbk')
        """
        // 对总价和单价正则匹配
        """
        template = re.compile(r".+?(\d{3,4})万.+?(\d{5,6})元.+?")
        for homeIndex in range(len(homeDataFrame)):
            m = re.match(template, homeDataFrame["followInfo"][homeIndex])
            if(m):
                total = m.group(1)
                perMeter = m.group(2)

                if float(total) <=300 :
                    targetCommunityName.append( allCommunity["communityName"][communityIndex] )
                    break
            else:
                continue


DataFrame({"targetCommunityName": targetCommunityName}).to_csv(r"targetCommunity.csv", encoding = 'gbk')                


            

