from requests import get as requests_get
from bs4 import BeautifulSoup
import re
from pandas import DataFrame

"""
// 爬取所有帖子链接网址，并保存到目录下allPostLinker.csv
"""
def postLinkerFilter():
    
    page_index = 0

    #网址前缀
    mainPage = "http://www.xoxohth.com"

    all_post_linker = [];

    while True:
            
        pageLinker_trunct = "http://www.xoxohth.com/index.php?forum_id=2&hid=&qu=&p=" + str(page_index)

        res = requests_get(pageLinker_trunct)
        soup = BeautifulSoup(res.text, 'lxml')

        # 帖子链接所在标签
        all_a_tag = soup.select('tr > td > font > a')

        linker_num = 0
        for a_tag in all_a_tag:
            trunct_linker = a_tag['href']

            # 不记录前面的 “t 6 hrs / 24 hrs / week / month” 链接信息
            if(trunct_linker[0] != '?'):           
                all_post_linker.append( mainPage + trunct_linker)
                linker_num += 1

        #如果只有单个帖子，说明页面为空，退出结束
        if linker_num == 1:
            break;

        #进入下一个页面
        page_index += 1

    #去除重复链接
    all_post_linker = list(set(all_post_linker))

    #保存链接到本地
    allPostLinker = DataFrame({'postLinker':all_post_linker})
    allPostLinker["descriptor"] = "No"
    allPostLinker.to_csv(r"allPostLinker.csv", encoding='gbk')

    return allPostLinker

"""
// 测试与样例
"""
if __name__ == "__main__":
  postLinkerFilter()
    
