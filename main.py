from decimal import Decimal
import os

import folium
import pulp as pp
import openrouteservice
from branca.element import Figure
from openrouteservice import convert
from dotenv import load_dotenv

import model.coordinates as coordinates
import model.find_route

load_dotenv()
key = os.getenv('OPEN_ROUTE_SERVICE_API_KEY')
client = openrouteservice.Client(key=key)


def reverse_lat_long(list):
    """緯度経度をひっくり返す"""
    return [(p[1], p[0]) for p in list]

#latlongs = coordinates.address_to_lonlat('data/address.xlsx')
latlongs = [['35.671243', '139.702661'], ['35.665846', '139.695831'], ['35.660761', '139.695675'], ['35.662143', '139.698496'], ['35.659443', '139.711598']]
#print(latlongs)
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
#distance_matrix = client.distance_matrix(locations=longlats, profile="foot-walking")['durations']

distance_matrix = [
    [0, 899.8, 1283.97, 905.28, 1285.66], 
    [899.8, 0, 923.11, 558.75, 1560.26], 
    [1283.97, 923.11, 0, 404.39, 1354.36], 
    [905.28, 558.75, 404.39, 0, 1112.71], 
    [1285.66, 1560.26, 1354.36, 1121.71, 0]
    ]

print(distance_matrix)

#移動経路を計算
route = model.find_route.Route(distance_matrix)
route.start_to_end
#u = route.return_start()
# print(u)

# ルート順に並び替えた配列を新しく定義
new_longlats = [0] * len(u)

for i in range(len(u)):
    new_longlats[u[i]] = longlats[i]

print(longlats)
print(new_longlats)



# 複数点間の経路を検索
# routedict=client.directions(new_longlats,profile="foot-walking")
# geometry = routedict["routes"][0]["geometry"]
# decoded = convert.decode_polyline(geometry)
# route = reverse_lat_long(decoded["coordinates"])

# # foliumでサイズ(600, 400)の地図を描画
# fig = Figure(width=600, height=400)
# map = folium.Map(location=(average_latlongs[0], average_latlongs[1]), zoom_start=16)

# # 各目的地にマーカー設置
# for i in range(len(latlongs)):
#     folium.Marker(location=(latlongs[i])).add_to(map)

# # 経路情報をPolyLineで地図に追加
# folium.vector_layers.PolyLine(locations=route).add_to(map)

# # 描画・ファイル出力
# fig.add_child(map)
# map.save("route.html")
