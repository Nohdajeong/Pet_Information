import tkinter as tk
from tkinter import *
from tkinter import font
from tkinter import ttk
from ttkthemes import ThemedTk
import requests
import time
import xml.etree.ElementTree as ET
import urllib
import urllib.request
import io
from io import BytesIO
from PIL import Image, ImageTk
from googlemaps import Client

import mimetypes
import smtplib
from email.mime.base import MIMEBase
from email.mime.text import MIMEText



class Program:
    def Frame(self):
        mylist1 = self.g_Tk.place_slaves()
        mylist2 = self.g_Tk.pack_slaves()
        for i in mylist1:
            i.destroy()
        for i in mylist2:
            i.destroy()

        self.setupMainButton()

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

    def pressedSearch(self):
        self.InitInterface()

    def InitInterface(self):
        self.window = Toplevel()
        self.window.title("search")
        self.window.geometry("800x600")

        TempFont = font.Font(self.window, size=20, weight='bold', family='Consolas')
        self.MainText = Label(self.window, font=TempFont, text="[ 세부 검색창 ]")
        self.MainText.place(x=300, y=15)

        renderTextscrollbar = Scrollbar(self.window)
        renderTextscrollbar.pack()
        renderTextscrollbar.place(x=675, y=200)

        renderTempfont = font.Font(self.window, size=10, family='Consolas')
        renderText = Text(self.window, width=60, height=30, borderwidth=12, relief='ridge', yscrollcommand=renderTextscrollbar.set)
        renderText.pack()
        renderText.place(x=210, y=135)

        renderTextscrollbar.config(command=renderText.yview)
        renderTextscrollbar.pack(side=RIGHT, fill=BOTH)
        renderText.configure(state='normal')
        renderText.configure(state='disabled')

        self.Imageview()

        self.window.mainloop()

    def Imageview(self):
        #url = "http://www.animal.go.kr/files/shelter/2024/05/202406011306171.jpg"
        url = list(self.hospital['image'].split()[0] for self.hospital in self.hospitals)
        with urllib.request.urlopen(url[0]) as u:
            raw_data = u.read()
        im = Image.open(BytesIO(raw_data))
        self.animalimg = ImageTk.PhotoImage(im)
        Label(self.window, image=self.animalimg, height=400, width=400).pack()


    def InitRenderText(self):
        self.RenderTextScrollbar = Scrollbar(self.g_Tk)
        self.RenderTextScrollbar.pack()
        self.RenderTextScrollbar.place(x=675, y=200)

        TempFont = font.Font(self.g_Tk, size=10, family='Consolas')
        self.RenderText = Text(self.g_Tk, width=50, height=30, borderwidth=12, relief='ridge',
                               yscrollcommand=self.RenderTextScrollbar.set)
        self.RenderText.pack()
        self.RenderText.place(x=210, y=130)
        self.RenderTextScrollbar.config(command=self.RenderText.yview)
        self.RenderTextScrollbar.pack(side=RIGHT, fill=BOTH)

        self.RenderText.configure(state='normal')
        self.RenderText.delete(0.0, END)

    def TextBox(self):
        self.InitRenderText()
        TipList = [['유기견 신고방법', '인식표나 마이크로칩을 확인 후, 확인이 된다면 곧바로 보호자에게 연락한다.'],
                   ['마이크로칩 확인방법', '가까운 동물병원에 가면 무료로 확인이 가능하다.'],
                   ['설명3', ''], ['설명4', ''],
                   ['설명5', ''], ['설명6', ''],
                   ['설명7', ''], ['설명8', '']]

        for i in range(8):
            self.RenderText.insert(INSERT, "[ TIP ")
            self.RenderText.insert(INSERT, i + 1)
            self.RenderText.insert(INSERT, ' ')
            self.RenderText.insert(INSERT, TipList[i][0])
            self.RenderText.insert(INSERT, " ]")
            self.RenderText.insert(INSERT, '\n')
            self.RenderText.insert(INSERT, TipList[i][1])
            self.RenderText.insert(INSERT, '\n\n')

        self.RenderText.configure(state='disabled')

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
                'kgs': self.item.findtext("BDWGH_INFO").strip("(Kg)"),  # 몸무게
                'pro': self.item.findtext("STATE_NM"),           # 보호여부
                'info': self.item.findtext("SFETR_INFO"),
                'sex': self.item.findtext("SEX_NM"),
                'age': self.item.findtext("AGE_INFO"),
                'color': self.item.findtext("COLOR_NM"),
                'begin': self.item.findtext("PBLANC_BEGIN_DE"),
                'end': self.item.findtext("PBLANC_END_DE"),
                'image': self.item.findtext("IMAGE_COURS"),
                'shter': self.item.findtext("SHTER_NM"),
                'tel': self.item.findtext("SHTER_TELNO"),
                'sigun': self.item.findtext("SIGUN_NM"),
                'sigunCD': self.item.findtext("SIGUN_CD"),
                'nuet': self.item.findtext("NEUT_YN")
            }
            self.hospitals.append(self.hospital)

    def InitSelected(self):
        self.selected_si = tk.StringVar()
        self.selected_si.set("시흥시")
        self.si_options = set(self.hospital['address'].split()[1] for self.hospital in self.hospitals)
        self.si_combo = ttk.Combobox(self.g_Tk, textvariable=self.selected_si, values=list(self.si_options))
        self.si_combo.pack()
        self.si_combo.place()

    def InitMapImage(self):
        self.response = requests.get(self.si_map_url + '&key=' + self.Google_API_Key)
        self.image = (Image.open(io.BytesIO(self.response.content)))
        self.photo = ImageTk.PhotoImage(self.image)
        self.map_label = tk.Label(self.g_Tk, image=self.photo)
        self.map_label.pack()

    def MapImageUpdate(self):
        # 지도 이미지 업데이트
        self.response = requests.get(self.si_map_url + '&key=' + self.Google_API_Key)
        self.image = Image.open(io.BytesIO(self.response.content))
        self.photo = ImageTk.PhotoImage(self.image)
        self.map_label.configure(image=self.photo)
        self.map_label.image = self.photo

    def InitListBox(self):
        self.canvas = tk.Canvas(self.g_Tk, width=800, height=400)
        self.canvas.pack()

        self.hospital_list = tk.Listbox(self.g_Tk, width=60)
        self.hospital_list.pack(side=tk.LEFT, fill=tk.BOTH)

        self.scrollbar = tk.Scrollbar(self.g_Tk)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.hospital_list.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.hospital_list.yview)

    def show_hospitals(self):
        self.hospital_list.delete(0, tk.END)

        self.si_name = self.selected_si.get()
        self.hospitals_in_si = [self.hospital for self.hospital in self.hospitals if self.hospital['address'].split()[1] == self.si_name]

        self.hospital_names = [self.hospital['name'] for self.hospital in self.hospitals_in_si]
        self.kgs_counts1 = [float(self.hospital['kgs']) for self.hospital in self.hospitals_in_si]
        self.kgs_counts = [int(float(self.hospital['kgs']) * 100) for self.hospital in self.hospitals_in_si]

        self.canvas.delete('all')
        self.Graph()

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


    def update_map(self):
        self.si_name = self.selected_si.get()
        self.si_center = self.gmaps.geocode(f"{self.si_name} 시")[0]['geometry']['location']
        self.si_map_url = f"https://maps.googleapis.com/maps/api/staticmap?center={self.si_center['lat']},{self.si_center['lng']}&zoom=14&size=400x400&maptype=roadmap"

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

    def InitSearchListBox(self):
        self.ANIMAL = ['개', '고양이', '기타']

        self.InitHospitals()
        ListBoxScrollbar = Scrollbar(self.g_Tk)
        ListBoxScrollbar.pack()
        ListBoxScrollbar.place(x=180, y=150)

        TempFont = font.Font(self.g_Tk, size=15, family='Consolas')
        self.SearchListBox = Listbox(self.g_Tk, font=TempFont, activestyle='none',
                                width=10, height=3, borderwidth=12, relief='ridge',
                                yscrollcommand=ListBoxScrollbar.set)

        for i in range(len(self.ANIMAL)):
            self.SearchListBox.insert(i+1, self.ANIMAL[i])

        self.SearchListBox.pack()
        self.SearchListBox.place(x=40, y=150)

        ListBoxScrollbar.config(command=self.SearchListBox.yview)

    def InitmainButton(self):
        TempFont = font.Font(self.g_Tk, size=15, weight='bold', family='Consolas')
        mainButton = Button(self.g_Tk, font=TempFont, text='출력', command=self.mainButtonAction)
        mainButton.pack()
        mainButton.place(x=40, y=300)
        mailButton = Button(self.g_Tk, font=TempFont, text='메일', command=self.mailButtonAction)
        mailButton.pack()
        mailButton.place(x=100, y=300)

    def mailButtonAction(self):
        host = "smtp.gmail.com"
        port = "587"
        htmlFileName = "logo.html"

        senderAddr = "rose20020622@gmail.com"  # 보내는 사람 email 주소.
        recipientAddr = "dajeong0404@naver.com"  # 받는 사람 email 주소.

        msg = MIMEBase("multipart", "alternative")
        msg['Subject'] = "보호동물 정보"  # 제목
        msg['From'] = senderAddr
        msg['To'] = recipientAddr

        htmlFD = open(htmlFileName, 'rb')
        HtmlPart = MIMEText(htmlFD.read(), 'html', _charset='UTF-8')
        htmlFD.close()

        # 메일을 발송한다.
        s = smtplib.SMTP(host, port)
        # s.set_debuglevel(1)        # 디버깅이 필요할 경우 주석을 푼다.
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login("rose20020622@gmail.com", "kmvvmolsqkndseet")
        s.sendmail(senderAddr, [recipientAddr], msg.as_string())
        s.close()


    def mainButtonAction(self):
        self.RenderText.configure(state='normal')
        self.RenderText.delete(0.0, END)

        self.iSearchIndex = self.SearchListBox.curselection()[0]
        self.AnimalAction()

    def AnimalAction(self):
        self.InitHospitals()
        self.ani_set = list(self.hospital['name'].split()[0] for self.hospital in self.hospitals)

        for i in range(len(self.hospitals)):
            if (self.iSearchIndex == 0 and self.ani_set[i] == '[개]'):
                self.RenderText.insert(INSERT, "공고기간 : ")
                self.RenderText.insert(INSERT, self.hospitals[i]['begin'] + "~" + self.hospitals[i]['end'])
                self.RenderText.insert(INSERT, "\n종류 : ")
                self.RenderText.insert(INSERT, self.hospitals[i]['name'])
                self.RenderText.insert(INSERT, "\n성별 : ")
                self.RenderText.insert(INSERT, self.hospitals[i]['sex'])
                self.RenderText.insert(INSERT, "\n나이 : ")
                self.RenderText.insert(INSERT, self.hospitals[i]['age'])
                self.RenderText.insert(INSERT, "\n보호소명 : ")
                self.RenderText.insert(INSERT, self.hospitals[i]['shter'])
                self.RenderText.insert(INSERT, "\n\n")
            elif self.iSearchIndex == 1 and self.ani_set[i] == '[고양이]':
                self.RenderText.insert(INSERT, "공고기간 : ")
                self.RenderText.insert(INSERT, self.hospitals[i]['begin'] + "~" + self.hospitals[i]['end'])
                self.RenderText.insert(INSERT, "\n종류 : ")
                self.RenderText.insert(INSERT, self.hospitals[i]['name'])
                self.RenderText.insert(INSERT, "\n성별 : ")
                self.RenderText.insert(INSERT, self.hospitals[i]['sex'])
                self.RenderText.insert(INSERT, "\n나이 : ")
                self.RenderText.insert(INSERT, self.hospitals[i]['age'])
                self.RenderText.insert(INSERT, "\n보호소명 : ")
                self.RenderText.insert(INSERT, self.hospitals[i]['shter'])
                self.RenderText.insert(INSERT, "\n\n")
            elif self.iSearchIndex == 2 and self.ani_set[i] == '[기타]':
                self.RenderText.insert(INSERT, "공고기간 : ")
                self.RenderText.insert(INSERT, self.hospitals[i]['begin'] + "~" + self.hospitals[i]['end'])
                self.RenderText.insert(INSERT, "\n종류 : ")
                self.RenderText.insert(INSERT, self.hospitals[i]['name'])
                self.RenderText.insert(INSERT, "\n성별 : ")
                self.RenderText.insert(INSERT, self.hospitals[i]['sex'])
                self.RenderText.insert(INSERT, "\n나이 : ")
                self.RenderText.insert(INSERT, self.hospitals[i]['age'])
                self.RenderText.insert(INSERT, "\n보호소명 : ")
                self.RenderText.insert(INSERT, self.hospitals[i]['shter'])
                self.RenderText.insert(INSERT, "\n\n")

     # SearchListBox.insert(i+1, self.ani_list[i])


    def InitMain(self):
        self.Frame()
        self.InitNowTime()
        self.InitSearchListBox()
        self.InitmainButton()
        self.InitRenderText()


    def __init__(self):
        self.api_key = "c515978432194f9ab9d94db31ae080cf"
        self.url = "https://openapi.gg.go.kr/AbdmAnimalProtect"
        self.params = {'KEY': self.api_key, 'Type': 'xml'}

        self.response = requests.get(self.url, params=self.params)
        self.g_Tk = ET.fromstring(self.response.content)
        self.items = self.g_Tk.findall("row")

        self.window = ET.fromstring(self.response.content)
        self.witems = self.window.findall("row")

        self.g_Tk = ThemedTk(theme="")
        self.g_Tk.title("경기도 유기동물 정보 프로그램")
        self.g_Tk.geometry("800x600+750+200")

        self.Google_API_Key = 'AIzaSyCzFgc9OGnXckq1-JNhSCVGo9zIq1kSWcE'
        self.gmaps = Client(key=self.Google_API_Key)

        self.InitMain()
        self.g_Tk.mainloop()

Program()
