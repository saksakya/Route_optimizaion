from decimal import Decimal
import os

import folium
import openrouteservice
from branca.element import Figure
from openrouteservice import convert
from dotenv import load_dotenv

import model.coordinates as coordinates
import model.find_route
import model.input_number as inum

load_dotenv()
key = os.getenv('OPEN_ROUTE_SERVICE_API_KEY')
client = openrouteservice.Client(key=key)


def reverse_lat_long(list):
    """緯度経度をひっくり返す"""
    return [(p[1], p[0]) for p in list]

mode_tuple = ('foot-walking', 'cycling-regular', 'driving-car')

mode_num = inum.input_number('Choose your means of transportation 0:walking 1:cycling 2:driving  Your choice:', 0, 2)
method = inum.input_number('Choose a traveling method  0:start to end 1:back to start Your choice:', 0, 1)

latlongs = coordinates.address_to_lonlat('data/address_ex2.xlsx')
print(latlongs)
#testdata（上記のAPIは特に負荷をかけるのでテスト段階ではこっちを使うこと)
# latlongs = [['35.67009', '139.702466'], ['35.666553', '139.696979'], ['35.660664', '139.695053'], ['35.660519', '139.709969'], ['35.655542', '139.711482'], ['35.656409', '139.699354'], ['35.662048', '139.698777'],['35.667287','139.708616'], ['35.646714', '139.710078']]

longlats = reverse_lat_long(latlongs)

# 中間点を計算
average_latlongs=[0, 0 , 0]
for i,p in enumerate(latlongs):
    average_latlongs[0] += Decimal(p[0])
    average_latlongs[1] += Decimal(p[1])
    average_latlongs[2] += 1
else:
    average_latlongs[0] = str(average_latlongs[0] / average_latlongs[2])
    average_latlongs[1] = str(average_latlongs[1] / average_latlongs[2])
    average_latlongs.pop(2)
    
# print(average_latlongs)

# 徒歩での各地点間の移動距離を取得
distance_matrix = client.distance_matrix(locations=longlats, profile=mode_tuple[mode_num])['durations']
print(distance_matrix)

# testdata
# distance_matrix =[[0.0, 735.62, 1159.31, 1180.13, 1629.17, 1358.07, 798.86, 2338.93],
#     [735.62, 0.0, 808.93, 1285.64, 1763.98, 1135.21, 462.87, 2165.55],
#     [1159.31, 808.93, 0.0, 1194.45, 1544.57, 753.91, 460.39, 1946.15], 
#     [1180.13, 1285.64, 1194.45, 0.0, 616.12, 926.34, 896.19, 1419.9], 
#     [1629.17, 1763.98, 1544.57, 616.12, 0.0, 1131.22, 1357.5, 1023.45], 
#     [1358.07, 1135.21, 753.91, 926.34, 1131.22, 0.0, 728.73, 1415.71], 
#     [798.86, 462.87, 460.39, 896.19, 1357.5, 728.73, 0.0, 1759.07], 
#     [2338.93, 2165.55, 1946.15, 1419.9, 1023.45, 1415.71, 1759.07, 0.0]]

# 移動経路を計算
route = model.find_route.Route(distance_matrix)

if method == 0 :
    # スタートとゴール固定の場合
    u = route.start_to_end()
elif method == 1 :
    # スタートに戻る場合
    u = route.return_start()
    # 最終目的値にスタート地点を代入
    u.append(len(u))
    longlats.append(longlats[0])
    latlongs.append(latlongs[0])

#print(u)

# ルート順に並び替えた配列を新しく定義
new_longlats = [0] * len(u)

for i in range(len(u)):
    new_longlats[u[i]] = longlats[i]

# print(longlats)
# print(new_longlats)

# 複数点間の経路を検索
routedict=client.directions(new_longlats,profile=mode_tuple[mode_num])
geometry = routedict["routes"][0]["geometry"]
decoded = convert.decode_polyline(geometry)
route = reverse_lat_long(decoded["coordinates"])

# foliumでサイズ(600, 400)の地図を描画
fig = Figure(width=600, height=400)
map = folium.Map(location=(average_latlongs[0], average_latlongs[1]), zoom_start=16)

# 各目的地にマーカー設置
for i in range(len(latlongs)):
    folium.Marker(location=(latlongs[i])).add_to(map)

# 経路情報をPolyLineで地図に追加
folium.vector_layers.PolyLine(locations=route).add_to(map)

# 描画・ファイル出力
fig.add_child(map)
map.save("route.html")
