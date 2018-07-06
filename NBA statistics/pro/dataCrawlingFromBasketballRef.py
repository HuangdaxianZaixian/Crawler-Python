from playersInfoCollect import filterDataForAllPlayers
from handleForOnePlayer import filterDataForallSeasonWebLog
from handleForOneSeason import filterDataForRegularSeason, filterDataForPlayOffs
from pandas import read_csv as pandas_read_csv
from os.path import exists as os_path_exists
from shutil import rmtree as shutil_rmtree
from requests import get as requests_get
from os import mkdir as os_mkdir


"""
// 1. 所有球员的个人基本信息保存在infoOfAllPlayers，添加了"downloaded"列表示该球员历年比赛信息是否保存到了本地
// 2. 遍历infoOfAllPlayers，检查球员"downloaded"列的值，若为"Yes"，则跳过
//    若为"No"，则根据球员姓名，在主目录下创建同名文件夹；根据球员主页网址，下载其历年比赛信息，并保持到该文件夹内
// 3. 若2成功，则将该球员的"downloaded"列改为"Yes"，否则，报错。方便断点续传
"""
def gameInfoDownloadForAllPlayers(restoreMainPath):
    """
    // 文件保存主目录 restoreMainPath
    // 一旦发生异常，则捕获并更新infoOfAllPlayers到本地
    """
    """
    // 读取infoOfAllPlayers，若本地不存在，则新建并初始化
    """
    try:
        if( os_path_exists(restoreMainPath + "\infoOfAllPlayers.csv") ):
            infoOfAllPlayers = pandas_read_csv(restoreMainPath + "\infoOfAllPlayers.csv")
            print("已读取本地球员基本信息")
        else:
            infoOfAllPlayers = filterDataForAllPlayers()
            infoOfAllPlayers["downloaded"] = "No"
            print("创建本地球员基本信息")

        for ii in range(0, len(infoOfAllPlayers)):
            restoreFilePathOfPlayer = restoreMainPath + "\\" + infoOfAllPlayers["playerName"][ii]
            if(infoOfAllPlayers["downloaded"][ii] == "No"):
                if(os_path_exists( restoreFilePathOfPlayer )):
                    shutil_rmtree(restoreFilePathOfPlayer)
                    print("{0}信息不完整，删除重建".format(infoOfAllPlayers["playerName"][ii]))
                if( os_mkdir(restoreFilePathOfPlayer) == False ):
                    print( "文件夹{0}创建不成功".format(restoreFilePathOfPlayer) )
                    raise Exception()

                """
                // 获取球员所有赛季的统计信息链接页面
                """
                print("开始获取{0}信息".format(infoOfAllPlayers["playerName"][ii]))
                allSeasonWebLog = filterDataForallSeasonWebLog(infoOfAllPlayers["mainPageUrl"][ii])

                for singleSeasonWebLog in allSeasonWebLog:
                    res = requests_get(singleSeasonWebLog)
                    strOfSeasonPage = res.text

                    """
                    // 保存常规赛和季后赛每场比赛数据到本地
                    """
                    yearStr = singleSeasonWebLog[-5:-1] #有可能为无效链接，最后四位非数字
                    if(yearStr.isdigit()):
                        filterDataForRegularSeason(strOfSeasonPage).to_csv(restoreFilePathOfPlayer + "\\" \
                                                                           + "regularSeason" + singleSeasonWebLog[-5:-1] + ".csv")
                        
                        filterDataForPlayOffs(strOfSeasonPage).to_csv(restoreFilePathOfPlayer + "\\" \
                                                                      + "playOffs" + singleSeasonWebLog[-5:-1] + ".csv")
                    else:
                        continue
                """
                // 该球员信息保存成功
                """            
                infoOfAllPlayers["downloaded"][ii] = "Yes"
            else:
                print("{0}信息已下载".format(infoOfAllPlayers["playerName"][ii]))
                continue
       
    except Exception as e:
        infoOfAllPlayers.to_csv(restoreMainPath + "\infoOfAllPlayers.csv")
        print(e)
        print("本地球员基本信息已更新")
    else:
        infoOfAllPlayers.to_csv(restoreMainPath + "\infoOfAllPlayers.csv")
        print("下载完成")


"""
// 测试和样例
"""
if __name__ == "__main__":
    restoreMainPath = r"C:\Users\huangyang_desktop\Desktop\NBA statistics\Basketball Reference"
    gameInfoDownloadForAllPlayers(restoreMainPath)
    






