from requests import get as requests_get
from bs4 import BeautifulSoup
import re
from pandas import DataFrame
from os import getcwd as os_getcwd


"""
// 从小区首页的 "查看小区全部在售二手房" 跳转到 小区二手出售房源列表页面
// 即小区首页链接到房源列表的链接的转换
"""
def mainpageLink2homeSourceListLink(mainpageLink):
    """
    // 获取首页
    """
    res = requests_get(mainpageLink, timeout=(20, 60))
    soup = BeautifulSoup(res.text, 'lxml')
    
    homeSourceSec = soup.select('div[class="box-l xiaoquMainContent"]')

    if len(homeSourceSec) == 0:
        return None
    else:
        if(len( homeSourceSec[0].select('a[class="fr"]') )):
            return homeSourceSec[0].select('a[class="fr"]')[0]['href']           
        else:
            return None


"""
// 获取某个小区的所有二手出售房源信息
"""

def homeSourceFilter(communityName, communityLink):
    """
    // 小区房源基本信息存储list
    """
    addresses = []
    floods = []
    followInfoes = []
    
    
    """
    // 获取首页
    """
    res = requests_get(communityLink, timeout=(20, 60))
    soup = BeautifulSoup(res.text, 'lxml')


    """
    // 获取分页信息
    """
    if len( soup.select('div[class="page-box house-lst-page-box"]') ) == 0:
        print("{0}:未找到分页信息".format(communityName))
        raise Exception("未找到分页信息")
    else:
        page_data = soup.select('div[class="page-box house-lst-page-box"]')[0]['page-data']
        page_data = eval(page_data)
        totalPage = page_data["totalPage"]

    """
    // 分页处理
    // 涵盖只有单页的情况
    """
    for pageIndex in range(1, totalPage + 1):
        if (pageIndex > 1):
            insertIndex = communityLink.rfind('/', 0, -2)
            pageLink = communityLink[:insertIndex+1] + 'pg' + str(pageIndex) + communityLink[insertIndex+1:]
            res = requests_get(pageLink, timeout=(20, 60))
            soup = BeautifulSoup(res.text, 'lxml')

        """
        // 通过li标签定位房源
        // 每个房源有三个class属性存有所需信息: address, flood, followInfo
        """
        houseResourceList = soup.select('li[class="clear"]')

        for houseResource in houseResourceList:
            """
            // address
            """
            address = houseResource.find_all('div', class_="address")
            """
            // flood
            """
            flood = houseResource.find_all('div', class_="flood")
            """
            // followInfo
            """
            followInfo = houseResource.find_all('div', class_="followInfo")
            
            addresses.append( "".join(list( address[0].stripped_strings ) ) )
            floods.append( "".join(list( flood[0].stripped_strings ) ) )
            followInfoes.append( "".join(list( followInfo[0].stripped_strings ) ) )
            

    allHomeSourceInfo = DataFrame({"address":addresses, "flood":floods, "followInfo":followInfoes})
    allHomeSourceInfo.to_csv(os_getcwd() + "\\" + "AllCommunity\\" + communityName + ".csv", encoding='gbk')
    


"""
// 测试与样例
"""
if __name__ == "__main__":
    mainpageLink = r"https://bj.lianjia.com/xiaoqu/1111027373684/"
    communityName = "不知名"
    homeSourceListLink = mainpageLink2homeSourceListLink(mainpageLink)
    homeSourceFilter(communityName, homeSourceListLink)

