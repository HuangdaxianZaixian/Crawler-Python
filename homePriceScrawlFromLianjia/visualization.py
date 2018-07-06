import matplotlib.pyplot as plt
from pandas import read_csv

allCommunity = read_csv(r"allCommunity.csv", encoding = "gbk")
fig = plt.figure(figsize = (10, 6.18))
ax = fig.add_subplot(1, 1, 1)

## //plot所有小区
ax.plot(allCommunity["lnt"], allCommunity["lat"], '*')

## // plot 目标小区
targetCommunity = read_csv(r"targetCommunity.csv", encoding = "gbk")
targetRow = allCommunity[ allCommunity["communityName"].isin(targetCommunity["targetCommunityName"])]
ax.plot(targetRow["lnt"], targetRow["lat"], 'ro')

## 国风美仑
origin = allCommunity.loc[(allCommunity["communityName"] == "首开国风美仑"), ["lnt", "lat"]]
ax.plot(origin["lnt"], origin["lat"], "kd", markersize = 10)
ax.set_xlim([115.9, 117])
ax.set_ylim([39.5, 40.5])

## 地铁线路
metroStation = read_csv(r"MetroStations.csv", encoding = "gbk")
ax.plot(metroStation["lng"], metroStation["lat"], "ko")

fig.show()
