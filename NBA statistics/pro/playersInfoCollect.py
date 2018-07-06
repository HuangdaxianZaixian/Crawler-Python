from requests import get as requests_get
from re import findall as re_findall
from pandas import DataFrame
from handleForOneSeason import voidDeal



"""
// 球员基本信息统计统计
"""
def basicInfoOfPlayer(tempStr):
    """
    // 部分item的提取过程中会出现>strong<的乱入
    // 所以需要特殊处理
    """
    playerName = voidDeal( re_findall(r"player\"\s><.{20}.+?>(.+?)<", tempStr) ) #球员姓名
    
    mainPageUrl = r"https://www.basketball-reference.com" + \
                  voidDeal( re_findall(r"player\"\s><.+?\"(.+?)\"", tempStr) )   #球员主页网址
    
    firstYear = voidDeal( re_findall(r"\"year_min\"\s>(\d+?)<", tempStr) )      #新秀年份
    
    lastYear = voidDeal( re_findall(r"\"year_max\"\s>(\d+?)<", tempStr) )       #退役年份
    
    pos = voidDeal( re_findall(r"\"pos\"\s>(.+?)<", tempStr) )                   #位置
    
    height = voidDeal( re_findall(r"\"height\".+?>(.+?)<", tempStr) )           #身高
    
    weight = voidDeal( re_findall(r"\"weight\"\s>(\d+?)<", tempStr) )           #体重

    birthday = voidDeal( re_findall(r"\"birth_date\"\scsk=\"(.+?)\"", tempStr) )    #出生日期
        
    college = voidDeal( re_findall(r"college=.+?>(.+?)<", tempStr) )               #毕业大学

    return [playerName, mainPageUrl, firstYear, lastYear, \
            pos, height, weight, birthday, college]

"""
// 球员在网页上以名字首字母进行索引
// 通过遍历26个字母，获取所有球员基本信息，包括主页网址
// 将所有球员信息存储在DataFrame中
"""
def filterDataForAllPlayers():
    
    letterTable = [chr(i) for i in range(97,123)]
    InfoOfAllPlayer = DataFrame(columns = ("playerName", "mainPageUrl", "firstYear", "lastYear", \
                                       "pos", "height", "weight", "birthday", "college") \
                                )

    """
    // 
    """
    num = 0
    for ii in range(0, len(letterTable)):
        initialAllPlayerUrl = r"https://www.basketball-reference.com/players/" + letterTable[ii] + "/"

        res = requests_get(initialAllPlayerUrl)
        strOfNameListPage = res.text

        """
        //  每位球员条目header部分都有data-append-csv
        """
        startIndexOfPlayerInfo = strOfNameListPage.find("data-append-csv")
        if(startIndexOfPlayerInfo == -1):
            print("can't find 'data-append-csv' at first time!")
            print("当前检索字母为： {0}, 未检索到球员信息".format(letterTable[ii]))
            continue
        
        """
        //  该首字母最后一位球员条目需要特殊处理
        """
        endFlag = True
        while(endFlag):
            endIndexOfPlayerInfo = strOfNameListPage.find("data-append-csv", startIndexOfPlayerInfo + 1)
            if(endIndexOfPlayerInfo == -1):
                endIndexOfPlayerInfo = startIndexOfPlayerInfo + 1000
                endFlag = False
                
            tempStr = strOfNameListPage[startIndexOfPlayerInfo : endIndexOfPlayerInfo]
            startIndexOfPlayerInfo = endIndexOfPlayerInfo
     
            InfoOfAllPlayer.loc[num] = basicInfoOfPlayer(tempStr)
            num += 1

    return InfoOfAllPlayer



"""
// 测试和样例
"""
if __name__ == "__main__":
    print(filterDataForAllPlayers())
