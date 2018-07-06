from requests import get as requests_get
from re import findall as re_findall
from pandas import DataFrame


"""
// 处理正则匹配为空
"""
def voidDeal(item):
    if(len(item)):
        return item[0]
    else:
        return None


"""
// 每场比赛球员数据统计
// *未统计职业生涯场次
"""
def gameStatOfPlayer(gameDescriptor):
    
    game = voidDeal( re_findall(r"csk=\"(\d+?)\"\s>", gameDescriptor) ) #赛季比赛场次
        
    date = voidDeal( re_findall(r"date_game=(.*?)&", gameDescriptor) ) #比赛时间
            
    age = voidDeal( re_findall(r"\"age\"\s>(.*?)<", gameDescriptor) )#年龄
    
    team = voidDeal( re_findall(r"team_id.*?>(\w{3})</a", gameDescriptor) ) #效力球队
    
    opp = voidDeal( re_findall(r"opp_id.*?>(\w{3})</a", gameDescriptor) ) #对手

    gameResult = voidDeal( re_findall(r"game_result\"\scsk=\"(.*?)\"\s>", gameDescriptor) ) #比赛结果

    gs = voidDeal( re_findall(r"gs\"\s>(\d*?)</td", gameDescriptor) ) #是否首发
    
    mp = voidDeal( re_findall(r"mp\".*?>(.*?)</td", gameDescriptor) ) #出场时间
    
    fg = voidDeal( re_findall(r"fg\"\s>(\d*?)</td", gameDescriptor) ) #2分球命中数
    
    fga = voidDeal( re_findall(r"fga\"\s>(\d*?)</td", gameDescriptor) ) #2分球出手数
    
    fg_pct = voidDeal( re_findall(r"fg_pct\"\s>(.*?)</td", gameDescriptor) ) #2分球命中率
    
    fg3 = voidDeal( re_findall(r"fg3\"\s>(\d*?)</td", gameDescriptor) ) #3分球命中数
    
    fg3a = voidDeal( re_findall(r"fg3a\"\s>(\d*?)</td", gameDescriptor) ) #3分球出手数
    
    fg3_pct = voidDeal( re_findall(r"fg3_pct\"\s>(.*?)</td", gameDescriptor) ) #3分球命中率
    
    ft = voidDeal( re_findall(r"ft\"\s>(\d*?)</td", gameDescriptor) ) #罚球命中数
    
    fta = voidDeal( re_findall(r"fta\"\s>(\d*?)</td", gameDescriptor) ) #罚球个数
    
    ft_pct = voidDeal( re_findall(r"ft_pct\"\s>(.*?)</td", gameDescriptor) ) #罚球命中率
    
    orb = voidDeal( re_findall(r"orb\"\s>(\d*?)</td", gameDescriptor) ) #进攻篮板
    
    drb = voidDeal( re_findall(r"drb\"\s>(\d*?)</td", gameDescriptor) ) #防守篮板
    
    trb = voidDeal( re_findall(r"trb\"\s>(\d*?)</td", gameDescriptor) ) #总篮板数
    
    ast = voidDeal( re_findall(r"ast\"\s>(\d*?)</td", gameDescriptor) ) #助攻数
    
    stl = voidDeal( re_findall(r"stl\"\s>(\d*?)</td", gameDescriptor) ) #抢断数
    
    blk = voidDeal( re_findall(r"blk\"\s>(\d*?)</td", gameDescriptor) ) #盖帽数
    
    tov = voidDeal( re_findall(r"tov\"\s>(\d*?)</td", gameDescriptor) ) #失误数
    
    pf = voidDeal( re_findall(r"pf\"\s>(\d*?)</td", gameDescriptor) ) #个人犯规数
    
    pts = voidDeal( re_findall(r"pts\"\s>(\d*?)</td", gameDescriptor) ) #得分
    
    game_score = voidDeal( re_findall(r"game_score\"\s>(.*?)</td", gameDescriptor) ) #效率值
    
    plus_minus = voidDeal( re_findall(r"plus_minus\"\s>(.*?)</td", gameDescriptor) ) #正负值


    return [game, date, age, team, opp, gameResult, gs, mp, fg, fga, fg_pct, fg3, fg3a, fg3_pct, \
            ft, fta, ft_pct, orb, drb, trb, ast, stl, blk, tov, pf, pts, game_score, plus_minus]



"""
// 从网页过滤得到单赛季常规赛统计数据
// strOfSeasonPage为服务器返回的单赛季网页str数据
"""
def filterDataForRegularSeason(strOfSeasonPage):
    """
    // 获取赛季所对应页面列出的所有职业生涯场次号
    // 常规赛为 pgl_basic.xxx regularSeason = Rs
    """

    RsAllGameIndex = re_findall(r"pgl_basic.(\d+?)\"", strOfSeasonPage)
    dataOfOneSeason = DataFrame(columns = ("pgl_basic", "game", "date", "age", "team", "opp", "gameResult", \
                                            "gs", "mp", "fg", "fga", "fg_pct", "fg3", "fg3a", "fg3_pct", \
                                            "ft", "fta", "ft_pct", "orb", "drb", "trb", "ast", "stl",\
                                            "blk", "tov", "pf", "pts", "game_score", "plus_minus") \
                                )


    """
    // 截取单场比赛str描述段落
    """
    initIndex = 0
    for ii in range(0, len(RsAllGameIndex)):
        strForFind = strOfSeasonPage[initIndex:]

        startStrForDes = "pgl_basic." + RsAllGameIndex[ii]
        startIndexForDes = strForFind.find(startStrForDes)
        
        if (ii + 1) < len(RsAllGameIndex):
            
            endStrForDes = "pgl_basic." + RsAllGameIndex[ii + 1]
            endIndexForDes = strForFind.find(endStrForDes)

            gameDescriptor = strForFind[startIndexForDes : endIndexForDes]
            
        else:
            endIndexForDes = -1
            gameDescriptor = strForFind[startIndexForDes : endIndexForDes] #最后一场，没有下一场

        """
        // 正则匹配每场数据，存入DataFrame 
        """
        pgl_basic = int(RsAllGameIndex[ii]) #职业生涯场次         
        allStatItems = gameStatOfPlayer(gameDescriptor)
        allStatItems.insert(0, pgl_basic) #无返回值
        
        dataOfOneSeason.loc[ii] = allStatItems
        
        initIndex = endIndexForDes

    return dataOfOneSeason


"""
// 从网页过滤得到单赛季季后赛统计数据
// strOfSeasonPage为服务器返回的单赛季网页str数据
"""
def filterDataForPlayOffs(strOfSeasonPage):
    """
    // 获取赛季所对应页面列出的所有职业生涯场次号
    // 季后赛为 pgl_basic_playoffs.xxx playoffs = Po
    """

    PoAllGameIndex = re_findall(r"pgl_basic_playoffs.(\d+?)\"", strOfSeasonPage)
    dataOfOneSeason = DataFrame(columns = ("pgl_basic", "game", "date", "age", "team", "opp", "gameResult", \
                                            "gs", "mp", "fg", "fga", "fg_pct", "fg3", "fg3a", "fg3_pct", \
                                            "ft", "fta", "ft_pct", "orb", "drb", "trb", "ast", "stl",\
                                            "blk", "tov", "pf", "pts", "game_score", "plus_minus") \
                                )

    """
    // 截取单场比赛str描述段落
    """
    initIndex = 0
    for ii in range(0, len(PoAllGameIndex)):
        strForFind = strOfSeasonPage[initIndex:] #减少检索时间

        startStrForDes = "pgl_basic_playoffs." + PoAllGameIndex[ii]
        startIndexForDes = strForFind.find(startStrForDes)
        
        if (ii + 1) < len(PoAllGameIndex):
            
            endStrForDes = "pgl_basic_playoffs." + PoAllGameIndex[ii + 1]
            endIndexForDes = strForFind.find(endStrForDes)

            gameDescriptor = strForFind[startIndexForDes : endIndexForDes]
            
        else:   
            endIndexForDes = -1
            gameDescriptor = strForFind[startIndexForDes : endIndexForDes] #最后一场，没有下一场

        """
        // 正则匹配每场数据，存入DataFrame 
        """
        pgl_basic = int(PoAllGameIndex[ii]) #职业生涯场次
        allStatItems = gameStatOfPlayer(gameDescriptor)
        allStatItems.insert(0, pgl_basic) #无返回值
        
        dataOfOneSeason.loc[ii] = allStatItems

        initIndex = endIndexForDes

    return dataOfOneSeason


"""
// 测试和样例
"""
if __name__ == "__main__":
    res = requests_get(r"https://www.basketball-reference.com/players/j/jamesle01/gamelog/2014/")
    strOfSeasonPage = res.text
    filterDataForRegularSeason(strOfSeasonPage)
    filterDataForPlayOffs(strOfSeasonPage)
    print("常规赛:\n", filterDataForRegularSeason(strOfSeasonPage))
    print("季后赛:\n", filterDataForPlayOffs(strOfSeasonPage))
