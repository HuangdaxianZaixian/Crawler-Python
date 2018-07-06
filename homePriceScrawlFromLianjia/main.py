from districtScrawl import districtFilter
from communityScrawl import communityFilter
from homeSourceScrawl import mainpageLink2homeSourceListLink, homeSourceFilter
from pandas import DataFrame, read_csv
from os.path import exists as path_exists
from os import getcwd as os_getcwd
import logging


def homeSourceDownload():
    """
    // 目标文件如果存在，则读取；否则，新建目标文件
    """

    if (path_exists(r"allCommunity.csv")):
        allCommunity = read_csv(r"allCommunity.csv", encoding='gbk')
        print("小区信息汇总文件已存在！")
    else:    
        districtNameList, districtLinkList = districtFilter()
        districtCommunityDicList = communityFilter(districtNameList, districtLinkList)


        communityNameList = []
        communityLinkList = []
        for districtCommunityDic in districtCommunityDicList:
            for communityName, communityLink in districtCommunityDic.items():
                communityNameList.append(communityName)
                communityLinkList.append(communityLink)
                
        allCommunity = DataFrame({'communityName':communityNameList, 'communityLink':communityLinkList})
        allCommunity["descriptor"] = "No"
        allCommunity.to_csv(r"allCommunity.csv", encoding='gbk')
        print("小区信息汇总文件不存在，创建成功！")

    """
    // 如果发生异常，输出异常，并进入下一个小区
    """
    communityNum = len(allCommunity)
    for communityIndex in range(communityNum):
        try:
            if( allCommunity["descriptor"][communityIndex] == "Yes"):
                print("{0}信息已下载".format( allCommunity["communityName"][communityIndex] ))
                continue
            else:
                communityName = allCommunity["communityName"][communityIndex]
                communityLink = allCommunity["communityLink"][communityIndex]
                homeSourceListLink = mainpageLink2homeSourceListLink(communityLink)
                """
                // 返回链接有可能为空，则创建同名空文件夹
                """
                if(homeSourceListLink):
                    homeSourceFilter(communityName, homeSourceListLink)
                    allCommunity["descriptor"][communityIndex] = "Yes"
                    print("{0}下载完成".format(communityName))
                else:
                    DataFrame().to_csv(os_getcwd() + "\\" + "AllCommunity\\" + communityName + ".csv", encoding='gbk')
                    allCommunity["descriptor"][communityIndex] = "Yes"
                    print("{0}下载完成".format(communityName))

        except Exception as e:
            if(communityIndex == communityNum-1):
                allCommunity.to_csv(r"allCommunity.csv", encoding='gbk')
                print("全部下载完成")
            print("***************发生异常***************")
            print("当前处理小区名字：{0}".format(allCommunity["communityName"][communityIndex]))
            logging.exception(e)

    allCommunity.to_csv(r"allCommunity.csv", encoding='gbk')
    print("全部下载完成")
                
        
"""
// 测试与样例
"""
if __name__ == "__main__":
  homeSourceDownload()
  

    
