from requests import get as requests_get
from re import findall as re_findall
from re import compile as re_compile

"""
// 获取某球员的主页str内容
// 提取该球员单赛季网页链接
// 获取的网页链接是部分的，需要添加前缀https://www.basketball-reference.com
"""
def filterDataForallSeasonWebLog(mainPageUrl):
    
    res = requests_get(mainPageUrl)
    strOfMainPage = res.text

    """
    // 获取球员所有效力年份
    // 去除重复年份
    """
    allSeasonYears = re_findall(r"per_game.(\d+?)\"", strOfMainPage)

    allSeasonYears = list( set(allSeasonYears) )
    allSeasonYears = [int(year) for year in allSeasonYears]
    allSeasonYears = sorted(allSeasonYears)
    allSeasonYears = [str(year) for year in allSeasonYears]

    """
    // 截取单场比赛str描述段落
    // 最后一段的切片是经验的，有可能不稳定
    """
    allSeasonWebLog = []
    for ii in range(0, len(allSeasonYears)):
        startStrForDes = "per_game." + str( allSeasonYears[ii] )
        startIndexForDes = strOfMainPage.find(startStrForDes)
        
        if (ii + 1) < len(allSeasonYears):            
            endStrForDes = "per_game." + str( allSeasonYears[ii+1] )
            endIndexForDes = strOfMainPage.find(endStrForDes)

            SeasonDescriptor = strOfMainPage[startIndexForDes : endIndexForDes]
                
        else:   
            SeasonDescriptor = strOfMainPage[startIndexForDes : startIndexForDes + 300] #最后一赛季，无下赛季

        reTemplate = re_compile(r"href=\"(.+?)\">" + str( int(allSeasonYears[ii]) - 1) )  
        seasonWebLog = reTemplate.findall(SeasonDescriptor)
        if(seasonWebLog):
            seasonWebLog = seasonWebLog[0]
        else:
            continue

        allSeasonWebLog.append(r"https://www.basketball-reference.com" + seasonWebLog)
    """
    // 去除重复链接
    """    
    return allSeasonWebLog 

"""
// 测试和样例
"""
if __name__ == "__main__":
    
    mainPageUrl = r"https://www.basketball-reference.com/players/a/abdulma02.html"    
    print(filterDataForallSeasonWebLog(mainPageUrl))
