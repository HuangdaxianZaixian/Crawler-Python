from bs4 import BeautifulSoup
import requests
from pandas import read_csv

"""
// 调用百度API查询位置
"""
def getlocation(name):
    bdurl = 'http://api.map.baidu.com/geocoder/v2/?address='
    output = 'json'
    ak = 'wXuGjkD0VHrGlmqYKL3xPXh4n6ZufAqG' ##每天有配额，配额用完，返回为空
    callback = 'showLocation'
    uri = bdurl+name+'&output=t'+output+'&ak='+ak+'&callback='+callback
    res = requests.get(uri)
    s = BeautifulSoup(res.text, 'lxml')
    lng = s.find('lng')
    lat = s.find('lat')
    if lng:
        print("返回非空")
        return float( lng.get_text() ), float( lat.get_text() )
    else:
        print("返回为空")
        return None, None


"""
// 测试与样例
"""
if __name__ == "__main__":
    lntList = []; latList = []
    allCommunity = read_csv(r"allCommunity.csv", encoding = "gbk")
    for communityIndex in range(len(allCommunity)):
        lnt, lat = getlocation("北京" + allCommunity["communityName"][communityIndex])
        lntList.append(lnt)
        latList.append(lat)

    allCommunity["lnt"] = lntList
    allCommunity["lat"] = latList

    allCommunity.to_csv(r"allCommunity.csv", encoding = "gbk")
        
    
