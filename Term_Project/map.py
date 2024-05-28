import tkinter as tk
import tkinter.ttk as ttk
import xml.etree.ElementTree as ET
import io
import requests
from PIL import Image, ImageTk
from googlemaps import Client

zoom = 13

# 경기도 동물병원 공공데이터 API 키
api_key = "f6b11f02849f4b87afcf6b3de2457686"

# 경기도 동물병원 정보 데이터
url = "https://openapi.gg.go.kr/Animalhosptl"
params = {
    "serviceKey": api_key,
    "numOfRows": 350,
    "sidoCd": 31000
}
response = requests.get(url, params=params)
root = ET.fromstring(response.content)
items = root.findall(".//item")

AnimalHospitals = []
for item in items:
    AnimalHospital = {
        "name": item.findtext("yadmNm"),   # 병원 이름
        "address": item.findtext("addr"),  # 병원 주소
        "lat": item.findtext("YPos"),      # 위도
        "lng": item.findtext("XPos"),      # 경도
        "doctors": item.findtext("drTotCnt")   # 종업원수
    }
    AnimalHospitals.append(AnimalHospital)

# Google Maps API 클라이언트 생성
Google_API_Key = 'AIzaSyBfFhkb6C0JDDiDK__pRNdeXWAzDOesv40'
gmaps = Client(key=Google_API_Key)

# 경기도 지도 생성
gg_center = gmaps.geocode("경기도 가평군 가평읍 대곡리 166-1번지")[0]['geometry']['location']
gg_map_url = f"https://maps.googleapis.com/maps/api/staticmap?center={gg_center['lat']},{gg_center['lng']}&zoom={zoom}&size=400x400&maptype=roadmap"

# 경기도 구별 병원 위치 마커 추가
for AnimalHospital in AnimalHospitals:
    if AnimalHospital['lat'] and AnimalHospitals['lng']:
        lat, lng = float(AnimalHospital['lat']), float(AnimalHospital['lng'])
        marker_url = f"&markers=color:red%7C{lat},{lng}"
gg_map_url += marker_url

# tkinter GUI 생성
root = tk.Tk()
root.title("경기도 동물병원정보")

# 선택 콤보박스 생성
selected_sigun = tk.StringVar()
selected_sigun.set('수원시')
sigun_options = set([AnimalHospital['address'].split()[1] for AnimalHospital in AnimalHospitals])
sigun_combo = ttk.Combobox(root, textvariable=selected_sigun, values=list(sigun_options))
sigun_combo.pack()

# 목록 표시 함수
def show_AnimalHospitals():
    AnimalHospital_list.delete(0, tk.END)

    sigun_name = selected_sigun.get()
    AnimalHospitals_in_sigun = []

    # 캔버스 초기화
    canvas.delete('all')

# 캔버스 생성
canvas = tk.Canvas(root, width=800, height=400)
canvas.pack()

# 병원 목록 리스트 박스
AnimalHospital_list = tk.Listbox(root, width=60)
AnimalHospital_list.pack(side=tk.LEFT, fill=tk.BOTH)

# 스크롤바 생성
scrollbar = tk.Scrollbar(root)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
