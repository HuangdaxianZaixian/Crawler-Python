from requests import get as requests_get
from bs4 import BeautifulSoup
import re


"""
// 区县爬取
"""
def districtFilter():
    res = requests_get(r"https://bj.lianjia.com/xiaoqu/")
    soup = BeautifulSoup(res.text, 'lxml')

    """
    // 获取区县的名字和链接
    """
    districtNameList = []
    districtLinkList = []

    for districtItem in soup.select('div[data-role="ershoufang"]')[0].find_all('a'):
        districtNameList.append( districtItem.string )
        if districtItem['href'].startswith("https"):
            districtLinkList.append( districtItem['href'] )
        else:   
            districtLinkList.append( r"https://bj.lianjia.com" + districtItem['href'] )

    return districtNameList, districtLinkList



"""
// 测试与样例
"""
if __name__ == "__main__":
    districtNameList, districtLinkList = districtFilter()
