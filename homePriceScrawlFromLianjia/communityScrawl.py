from requests import get as requests_get
from bs4 import BeautifulSoup
import re
from districtScrawl import districtFilter

"""
// 按区县爬取小区名字和链接
// 【区县名字、链接、所有小区名字和链接】存储在【districtNameList, districtLinkList，districtCommunityDicList】
//
"""
def communityFilter(districtNameList, districtLinkList):
        
    """
    // 按区县爬取小区名字和链接
    """
    districtCommunityDicList = []

    """
    // 分区县处理
    """

    for districtLink in districtLinkList:
        districtAllCommunity = {}

        """
        // 每个区县所有小区列表是分页展示的
        // 首先获取区县小区列表的第一页，获取页面信息
        """
        
        res = requests_get(districtLink)
        soup = BeautifulSoup(res.text, 'lxml')

        page_data = soup.select('div[class="page-box house-lst-page-box"]')[0]['page-data']
        page_data = eval(page_data)
        totalPage = page_data["totalPage"]

        """
        // 分页处理
        """

        for pageIndex in range(1, totalPage + 1):

            if (pageIndex > 1):
                pageLink = districtLink + 'pg' + str(pageIndex) + '/'
                res = requests_get(pageLink)
                soup = BeautifulSoup(res.text, 'lxml')
                
            communityResourceList = soup.select('li[class="clear xiaoquListItem"]')

            for communityResource in communityResourceList:
                communityLink = communityResource.a['href']
                communityName = communityResource.img['alt']
                districtAllCommunity[communityName] = communityLink
                
        districtCommunityDicList.append(districtAllCommunity)

    return districtCommunityDicList



"""
// 测试和样例
"""
if __name__ == "__main__":
    
    districtNameList, districtLinkList = districtFilter()
    districtCommunityDicList = communityFilter(districtNameList, districtLinkList)

    
