from bs4 import BeautifulSoup
import requests
import tqdm
import pandas as pd

# from geopy.geocoders import Nominatim
# geolocator = Nominatim(user_agent='geopy')

def address_to_lonlat(path):
    url = 'http://www.geocoding.jp/api/'
    latlons = []

    # エクセルをデータフレームで読み込む
    df = pd.read_excel(path)
    address_list = df['address']
    # print(address_list)
    
    # 住所が日本の場合lon,latへ追加
    for address in tqdm.tqdm(address_list):

        payload={'q':address}
        r = requests.get(url, params=payload)
        ret = BeautifulSoup(r.content,'lxml')
        if ret.find('error'):
            raise ValueError(f"Invalid address submitted. {address}")
        else:
            lat = ret.find('lat').string
            lon = ret.find('lng').string
            latlons.append([lat,lon])
    return latlons