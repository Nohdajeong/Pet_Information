import tkinter as tk
import requests
import time
import xml.etree.ElementTree as ET
import urllib
import urllib.request
from io import BytesIO
from PIL import Image, ImageTk
from googlemaps import Client
from tkinter import *
from tkinter import font
from tkinter import ttk
from ttkthemes import ThemedTk

class Program:
    def Frame(self):
        mylist1 = self.g_Tk.place_slaves()
        mylist2 = self.g_Tk.pack_slaves()
        for i in mylist1:
            i.destroy()
        for i in mylist2:
            i.destroy()

        self.setupMainButton()
        self.InitNowTime()

        TempFont = font.Font(self.g_Tk, size=20, weight='bold', family='Consolas')
        self.MainText = Label(self.g_Tk, font=TempFont, text="[ 경기도 동물 보호 정보 프로그램 ]")
        self.MainText.place(x=200, y=15)

        self.photo = PhotoImage(file="Image/gif.gif")
        self.resize = self.photo.subsample(5, 5)
        self.imglabel = Label(self.g_Tk, image=self.resize)
        self.imglabel.place(x=50, y=20)

    def InitNowTime(self):
        TempFont = font.Font(self.g_Tk, size=15, weight='bold', family='Consolas')
        current_time = time.strftime('%H:%M:%S')
        clock_label = Label(self.g_Tk, font=TempFont, text=current_time)
        clock_label.after(1000, self.InitNowTime)
        clock_label.pack()
        clock_label.place(x=650, y=530)

    def InitSearchListBox(self):
        ListBoxScrollbar = Scrollbar(self.g_Tk)
        ListBoxScrollbar.pack()
        ListBoxScrollbar.place(x=180, y=150)

        TempFont = font.Font(self.g_Tk, size=15, family='Consolas')
        SearchListBox = Listbox(self.g_Tk, font=TempFont, activestyle='none',
                            width=10, height=3, borderwidth=12, relief='ridge',
                            yscrollcommand=ListBoxScrollbar.set)

        SearchListBox.insert(1, "강아지")
        SearchListBox.insert(2, "고양이")
        SearchListBox.insert(3, "기타")
        SearchListBox.pack()
        SearchListBox.place(x=40, y=150)

        ListBoxScrollbar.config(command=SearchListBox.yview)

    def setupMainButton(self):
        TempFont = font.Font(self.g_Tk, size=15, weight='bold', family='Consolas')
        self.Home = Button(self.g_Tk, text="Home", width=6, height=1, font=TempFont,
                           command=self.pressedHome)
        self.Home.place(x=170, y=70)

        self.Search = Button(self.g_Tk, text="Search", width=6, height=1, font=TempFont,
                             command=self.pressedSearch)
        self.Search.place(x=270, y=70)

        self.GraphButton = Button(self.g_Tk, text="Graph", width=6, height=1, font=TempFont,
                            command=self.pressedCheck)
        self.GraphButton.place(x=370, y=70)

        self.Tip = Button(self.g_Tk, text="TIP", width=6, height=1, font=TempFont,
                          command=self.pressedTip)
        self.Tip.place(x=470, y=70)

        self.Star = Button(self.g_Tk, text="★", width=6, height=1, font=TempFont,
                           command=self.pressedStar)
        self.Star.place(x=570, y=70)

    def pressedHome(self):
        self.InitMain()

    def Imageview(self):
        url = "http://www.animal.go.kr/files/shelter/2024/05/202406011306171.jpg"
        with urllib.request.urlopen(url) as u:
            raw_data = u.read()
        im = Image.open(BytesIO(raw_data))
        self.animalimg = ImageTk.PhotoImage(im)
        Label(self.g_Tk, image=self.animalimg, height=400, width=400).pack()

    def pressedSearch(self):
        self.Frame()
        self.Imageview()

    def TextBox(self):
        TipList = [['유기견 신고방법', '인식표나 마이크로칩을 확인 후, 확인이 된다면 곧바로 보호자에게 연락한다.'],
                   ['마이크로칩 확인방법', '가까운 동물병원에 가면 무료로 확인이 가능하다.'],
                   ['설명3', ''], ['설명4', ''],
                   ['설명5', ''], ['설명6', ''],
                   ['설명7', ''], ['설명8', '']]

        RenderTextScrollbar = Scrollbar(self.g_Tk)
        RenderTextScrollbar.pack()
        RenderTextScrollbar.place(x=675, y=200)

        TempFont = font.Font(self.g_Tk, size=10, family='Consolas')
        RenderText = Text(self.g_Tk, width=50, height=30, borderwidth=12, relief='ridge',
                          yscrollcommand=RenderTextScrollbar.set)
        RenderText.pack()
        RenderText.place(x=210, y=130)
        RenderTextScrollbar.config(command=RenderText.yview)
        RenderTextScrollbar.pack(side=RIGHT, fill=BOTH)

        RenderText.configure(state='normal')
        RenderText.delete(0.0, END)

        for i in range(8):
            RenderText.insert(INSERT, "[ TIP ")
            RenderText.insert(INSERT, i + 1)
            RenderText.insert(INSERT, ' ')
            RenderText.insert(INSERT, TipList[i][0])
            RenderText.insert(INSERT, " ]")
            RenderText.insert(INSERT, '\n')
            RenderText.insert(INSERT, TipList[i][1])
            RenderText.insert(INSERT, '\n\n')

        RenderText.configure(state='disabled')

    def pressedTip(self):
        self.Frame()
        self.TextBox()

    def pressedStar(self):
        self.Frame()

    def pressedCheck(self):
        self.Frame()
        self.InitHospitals()
        self.InitSelected()
        self.InitListBox()
        self.setupMainButton()

        self.si_name = self.selected_si.get()
        self.si_center = self.gmaps.geocode(f"{self.si_name} 시")[0]['geometry']['location']
        self.si_map_url = f"https://maps.googleapis.com/maps/api/staticmap?center={self.si_center['lat']},{self.si_center['lng']}&zoom=14&size=400x400&maptype=roadmap"

        self.InitMapImage()

        self.si_combo.bind("<<ComboboxSelected>>", self.on_si_select)
        self.update_map()

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
        self.si_combo.place()

    def InitMapImage(self):
        self.response = requests.get(self.si_map_url + '&key=' + self.Google_API_Key)
        #self.image = (Image.open(io.BytesIO(self.response.content)))
        #self.photo = ImageTk.PhotoImage(self.image)
        #self.map_label = tk.Label(self.g_Tk, image=self.photo)
        #self.map_label.pack()

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

        self.scrollbar = tk.Scrollbar(self.g_Tk)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.hospital_list.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.hospital_list.yview)

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

    def InitMain(self):
        self.Frame()
        self.InitSearchListBox()

    def __init__(self):
        self.api_key = "c515978432194f9ab9d94db31ae080cf"
        self.url = "https://openapi.gg.go.kr/AbdmAnimalProtect"
        self.params = {'KEY': self.api_key, 'Type': 'xml'}

        self.response = requests.get(self.url, params=self.params)
        self.g_Tk = ET.fromstring(self.response.content)
        self.items = self.g_Tk.findall("row")

        self.g_Tk = ThemedTk(theme="")
        self.g_Tk.title("경기도 유기동물 정보 프로그램")
        self.g_Tk.geometry("800x600+750+200")

        self.Google_API_Key = 'AIzaSyCzFgc9OGnXckq1-JNhSCVGo9zIq1kSWcE'
        self.gmaps = Client(key=self.Google_API_Key)

        self.InitMain()
        self.g_Tk.mainloop()

Program()
