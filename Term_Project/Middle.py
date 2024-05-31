import tkinter as tk
import tkinter.ttk as ttk
import io
import requests
import xml.etree.ElementTree as ET
from PIL import Image, ImageTk
from googlemaps import Client
from tkinter import *
from tkinter import font

class Program:
    def setupButton(self):
        TempFont = font.Font(self.g_Tk, size=20, weight='bold', family='Consolas')
        self.Check = Button(self.g_Tk, text="Check", width=6, height=1, font=TempFont,
                            command=self.pressedCheck)
        self.Check.place(x=50, y=500)

    def pressedCheck(self):
        self.InitHospitals()
        self.InitSelected()
        self.InitListBox()

        self.si_name = self.selected_si.get()
        self.si_center = self.gmaps.geocode(f"{self.si_name} 시")[0]['geometry']['location']
        self.si_map_url = f"https://maps.googleapis.com/maps/api/staticmap?center={self.si_center['lat']},{self.si_center['lng']}&zoom=14&size=400x400&maptype=roadmap"

        self.InitMapImage()

        self.si_combo.bind("<<ComboboxSelected>>", self.on_si_select)
        self.update_map()

    def InitMapImage(self):
        self.response = requests.get(self.si_map_url + '&key=' + self.Google_API_Key)
        #self.image = (Image.open(io.BytesIO(self.response.content)))
        #self.photo = ImageTk.PhotoImage(self.image)
        #self.map_label = tk.Label(self.g_Tk, image=self.photo)
        #self.map_label.pack()

    def InitHospitals(self):
        self.hospitals = []
        for self.item in self.items:
            self.hospital = {
                'name': self.item.findtext("SPECIES_NM"),  # 보호하고 있는 동물 이름
                'address': self.item.findtext("PROTECT_PLC"),  # 보호소 주소
                'lat': self.item.findtext("REFINE_WGS84_LAT"),  # 위도
                'lng': self.item.findtext("REFINE_WGS84_LOGT"),  # 경도
                'kgs': self.item.findtext("BDWGH_INFO").strip("(Kg)")  # 몸무게
            }
            self.hospitals.append(self.hospital)

    def InitSelected(self):
        self.selected_si = tk.StringVar()
        self.selected_si.set("평택시")
        self.si_options = set(self.hospital['address'].split()[1] for self.hospital in self.hospitals)
        self.si_combo = ttk.Combobox(self.g_Tk, textvariable=self.selected_si, values=list(self.si_options))
        self.si_combo.pack()

    def MapImageUpdate(self):
        # 지도 이미지 업데이트
        self.response = requests.get(self.si_map_url + '&key=' + self.Google_API_Key)
        #self.image = Image.open(io.BytesIO(self.response.content))
        #self.photo = ImageTk.PhotoImage(self.image)
        #self.map_label.configure(image=self.photo)
        #self.map_label.image = self.photo

    def InitListBox(self):
        self.canvas = tk.Canvas(self.g_Tk, width=800, height=400)
        self.canvas.pack()

        self.hospital_list = tk.Listbox(self.g_Tk, width=60)
        self.hospital_list.pack(side=tk.LEFT, fill=tk.BOTH)

        scrollbar = tk.Scrollbar(self.g_Tk)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.hospital_list.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.hospital_list.yview)

    def Graph(self):
        max_kgs_count = max(self.kgs_counts)
        bar_width = 20
        x_gap = 30
        x0 = 60
        y0 = 250
        for i in range(len(self.hospital_names)):
            x1 = x0 + i * (bar_width + x_gap)
            y1 = y0 - 200 * self.kgs_counts[i] / max_kgs_count
            self.canvas.create_rectangle(x1, y1, x1 + bar_width, y0, fill='blue')
            self.canvas.create_text(x1 + bar_width / 2, y0 + 100, text=self.hospital_names[i], anchor='n', angle=90)
            self.canvas.create_text(x1 + bar_width / 2, y1 - 10, text=self.kgs_counts1[i], anchor='s')

            # 병원 목록에 추가
        for hospital in self.hospitals_in_si:
            self.hospital_list.insert(tk.END, f"{hospital['name']} ({hospital['kgs']})kg")

    def show_hospitals(self):
        self.hospital_list.delete(0, tk.END)

        self.si_name = self.selected_si.get()
        self.hospitals_in_si = [self.hospital for self.hospital in self.hospitals if self.hospital['address'].split()[1] == self.si_name]

        self.hospital_names = [self.hospital['name'] for self.hospital in self.hospitals_in_si]
        self.kgs_counts1 = [float(self.hospital['kgs']) for self.hospital in self.hospitals_in_si]
        self.kgs_counts = [int(float(self.hospital['kgs'])*100) for self.hospital in self.hospitals_in_si]

        self.canvas.delete('all')

        self.Graph()

    def update_map(self):
        self.hospitals_in_si = [self.hospital for self.hospital in self.hospitals if self.hospital['address'].split()[1] == self.si_name]

        for hospital in self.hospitals_in_si:
            if hospital['lat'] and hospital['lng']:
                self.lat, self.lng = float(hospital['lat']), float(hospital['lng'])
                self.marker_url = f"&markers=color:red%7C{self.lat},{self.lng}"
                self.si_map_url += self.marker_url

        self.MapImageUpdate()
        self.show_hospitals()

    def on_si_select(self, event):
        self.update_map()

    def __init__(self):
        self.api_key = "c515978432194f9ab9d94db31ae080cf"
        self.url = "https://openapi.gg.go.kr/AbdmAnimalProtect"
        self.params = {'KEY': self.api_key, 'Type': 'xml'}

        self.response = requests.get(self.url, params=self.params)
        self.g_Tk = ET.fromstring(self.response.content)
        self.items = self.g_Tk.findall("row")

        self.g_Tk = Tk()
        self.g_Tk.title("경기도 유기동물 정보 프로그램")
        self.g_Tk.geometry("800x600+750+200")

        self.Google_API_Key = 'AIzaSyCzFgc9OGnXckq1-JNhSCVGo9zIq1kSWcE'
        self.gmaps = Client(key=self.Google_API_Key)

        self.setupButton()
        self.g_Tk.mainloop()

Program()
