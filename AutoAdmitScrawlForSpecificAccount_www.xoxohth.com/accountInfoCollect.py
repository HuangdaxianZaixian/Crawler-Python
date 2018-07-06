from postLinkerCollect import postLinkerFilter
from singlePostPro import accountQueryInSinglePost

from pandas import DataFrame, read_csv
from os.path import exists as path_exists
import logging


def accountInfoDownload(account_query):
    """
    // 目标文件如果存在，则读取；否则，新建目标文件
    """

    if (path_exists(r"allPostLinker.csv")):
        allPostLinker = read_csv(r"allPostLinker.csv", encoding='gbk')
        print("帖子链接网址汇总文件已存在！")
    else:    
        allPostLinker = postLinkerFilter()
        print("帖子链接网址汇总文件不存在，创建成功！")

    """
    // 如果发生异常，输出异常，并进入下一个小区
    """
    postLinkerNum = len(allPostLinker)
    for postLinkerIndex in range(postLinkerNum):
        try:
            if( allPostLinker["descriptor"][postLinkerIndex] == "Yes"):
                print("帖子：{0} 已处理".format( allPostLinker["postLinker"][postLinkerIndex] ))
                continue
            else:
                accountQueryInSinglePost(allPostLinker["postLinker"][postLinkerIndex], account_query)

                allPostLinker["descriptor"][postLinkerIndex] = "Yes"
                print("帖子：{0}, 编号：{1} 处理完成".format( allPostLinker["postLinker"][postLinkerIndex], postLinkerIndex ))

        except Exception as e:
            print("***************发生异常***************")
            print("当前处理网址链接：{0}, 编号： {1}".format(allPostLinker["postLinker"][postLinkerIndex], postLinkerIndex))
            logging.exception(e)
            
            if( postLinkerIndex == postLinkerNum-1 ):
                allPostLinker.to_csv(r"allPostLinker.csv", encoding='gbk')
                print("全部帖子处理完成")
                

    allPostLinker.to_csv(r"allPostLinker.csv", encoding='gbk')
    print("全部帖子处理完成")
                
        
"""
// 测试与样例
"""
if __name__ == "__main__":
    account_query = "...;.,,,,.....,.,,....;..,,,.."
    accountInfoDownload(account_query)
  

    
