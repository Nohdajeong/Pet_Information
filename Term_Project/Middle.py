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
import mysmtplib
from email.mime.multipart import MIMEMultipart
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

        self.winlistbox()
        self.winInitButton()
        self.winRendertext()

        self.window.mainloop()

    def winInitButton(self):
        TempFont = font.Font(self.window, size=15, weight='bold', family='Consolas')
        textButton = Button(self.window, font=TempFont, text='출력', command=self.textButtonAction)
        textButton.pack()
        textButton.place(x=40, y=240)
        mailButton = Button(self.window, font=TempFont, text='메일', command=self.mailButtonAction)
        mailButton.pack()
        mailButton.place(x=100, y=240)
        starButton = Button(self.window, font=TempFont, text='즐겨찾기', command=self.starButtonAction)
        starButton.pack()
        starButton.place(x=40, y=300)
    def starButtonAction(self):
        self.indexpage = self.winiSearchIndex
        self.datalist = []
        self.datalist.append(self.indexpage)

    def textButtonAction(self):
        self.winiSearchIndex = self.wlistbox.curselection()[0]
        self.renderText.configure(state='normal')
        self.renderText.delete(0.0, END)

        self.InitHospitals()
        self.renderText.insert(INSERT, "공고기간 : ")
        self.renderText.insert(INSERT, self.hospitals[self.winiSearchIndex]['begin'] + "~" + self.hospitals[self.winiSearchIndex]['end'])
        self.renderText.insert(INSERT, "\n종류 : ")
        self.renderText.insert(INSERT, self.hospitals[self.winiSearchIndex]['name'])
        self.renderText.insert(INSERT, "\n성별 : ")
        self.renderText.insert(INSERT, self.hospitals[self.winiSearchIndex]['sex'])
        self.renderText.insert(INSERT, "\n나이 : ")
        self.renderText.insert(INSERT, self.hospitals[self.winiSearchIndex]['age'])
        self.renderText.insert(INSERT, "\n중성화 여부 : ")
        self.renderText.insert(INSERT, self.hospitals[self.winiSearchIndex]['nuet'])
        self.renderText.insert(INSERT, "\n색 : ")
        self.renderText.insert(INSERT, self.hospitals[self.winiSearchIndex]['color'])
        self.renderText.insert(INSERT, "\n특이사항 : ")
        self.renderText.insert(INSERT, self.hospitals[self.winiSearchIndex]['info'])
        self.renderText.insert(INSERT, "\n\n보호 여부 : ")
        self.renderText.insert(INSERT, self.hospitals[self.winiSearchIndex]['pro'])
        self.renderText.insert(INSERT, "\n보호소명 : ")
        self.renderText.insert(INSERT, self.hospitals[self.winiSearchIndex]['shter'])
        self.renderText.insert(INSERT, "\n보호소 주소 : ")
        self.renderText.insert(INSERT, self.hospitals[self.winiSearchIndex]['address'])
        self.renderText.insert(INSERT, "\n보호소 번호 : ")
        self.renderText.insert(INSERT, self.hospitals[self.winiSearchIndex]['tel'])
        self.renderText.insert(INSERT, "\n\n")

        self.Imageviewwin()

    def winlistbox(self):
        listboxscrollbar = Scrollbar(self.window)
        listboxscrollbar.pack()
        listboxscrollbar.place(x=180, y=100)

        TempFont = font.Font(self.window, size=12, family='Consolas')
        self.wlistbox = Listbox(self.window, font=TempFont, activestyle='none',
                          width=13, height=5, borderwidth=10, relief='ridge',
                          yscrollcommand=listboxscrollbar.set)

        ani_list = list(self.hospital['name'] for self.hospital in self.hospitals)

        for i in range(len(self.hospitals)):
            self.wlistbox.insert(i + 1, ani_list[i])

        self.wlistbox.pack()
        self.wlistbox.place(x=40, y=100)

        listboxscrollbar.config(command=self.wlistbox.yview)

    def winRendertext(self):
        renderTextscrollbar = Scrollbar(self.window)
        renderTextscrollbar.pack()
        renderTextscrollbar.place(x=675, y=200)

        renderTempfont = font.Font(self.window, size=10, family='Consolas')
        self.renderText = Text(self.window, width=40, height=30, borderwidth=12, relief='ridge',
                          yscrollcommand=renderTextscrollbar.set)
        self.renderText.pack()
        self.renderText.place(x=210, y=100)

        renderTextscrollbar.config(command=self.renderText.yview)
        renderTextscrollbar.pack(side=RIGHT, fill=BOTH)
        self.renderText.configure(state='normal')
        self.renderText.configure(state='disabled')

    def Imageviewwin(self):
        #url = "http://www.animal.go.kr/files/shelter/2024/05/202406011306171.jpg"
        url = list(self.hospital['image'] for self.hospital in self.hospitals)
        with urllib.request.urlopen(url[self.winiSearchIndex]) as u:
            raw_data = u.read()
        im = Image.open(BytesIO(raw_data))
        self.animalimg = ImageTk.PhotoImage(im)
        image = Label(self.window, image=self.animalimg)
        image.pack()
        image.place(x=570, y=150)

    def InitRenderText(self):
        self.RenderTextScrollbar = Scrollbar(self.g_Tk)
        self.RenderTextScrollbar.pack()
        self.RenderTextScrollbar.place(x=675, y=200)

        TempFont = font.Font(self.g_Tk, size=10, family='Consolas')
        self.RenderText = Text(self.g_Tk, width=55, height=30, borderwidth=12, relief='ridge',
                               yscrollcommand=self.RenderTextScrollbar.set)
        self.RenderText.pack()
        self.RenderText.place(x=210, y=150)
        self.RenderTextScrollbar.config(command=self.RenderText.yview)
        self.RenderTextScrollbar.pack(side=RIGHT, fill=BOTH)

        self.RenderText.configure(state='normal')
        self.RenderText.delete(0.0, END)

    def TipButton(self):
        TempFont = font.Font(self.g_Tk, size=15, weight='bold', family='Consolas')
        microButton = Button(self.g_Tk, font=TempFont, text='동물등록절차', command=self.microbuttonaction)
        microButton.pack()
        microButton.place(x=40, y=180)

        rowButton = Button(self.g_Tk, font=TempFont, text='동물 관련 법', command=self.rowbuttonaction)
        rowButton.pack()
        rowButton.place(x=40, y=230)

        proButton = Button(self.g_Tk, font=TempFont, text='야생동물 구조요령', command=self.probuttonaction)
        proButton.pack()
        proButton.place(x=40, y=280)

    def probuttonaction(self):
        self.RenderText.configure(state='normal')
        self.RenderText.delete(0.0, END)
        TipList = ['야생동물 구조 요령', '1. 구조자 자신을 보호해야 합니다. 가능하면 장갑을 착용합니다. 아픈 야생동물도 갑자기 공격(물기, 할퀴기 등)을 시도할 수 있습니다.또한 사람에 옮길 수 있는 기생충(벼룩, 이, 진드기 등)이나 질병(광견병, AI등)을 갖고 있을 수 있습니다.',
                   '2. 공기 구멍이 있는 상자를 준비 합니다. 종이상자나 애완동물용 이동장의 바닥에 부드러운 수건을 깔고 공기가 통하도록 작은 구멍들을 뚫어 줍니다. 동물의 크기보다 약간 큰 정도가 좋습니다. 철망으로 된 이동장은 새의 깃털을 손상시키고 너구리가 물어뜯으면서 상처를 입으므로 적합하지 않습니다.',
                   '3. 구조할 동물을 수건으로 덮은 후 상자에 넣습니다. 동물의 시야를 가려주어 스트레스를 줄이고 안정되게 합니다. 또한 동물이 탈출하지 않도록 보안에 주의해야 합니다.', ' 4. 날씨가 춥거나 동물이 떨고 있으면 보온을 해야 합니다. 특히 어린 동물은 스스로 체온조절을 못하기 때문에 체온 유지는 매우 중요합니다. 데운 찜질팩이나 따뜻한 물병을 수건에 싸서 상자 구석에 깔아줍니다. 너무 뜨거워 화상을 입지 않도록 주의 해야 합니다.',
                   '5. 짧은 시간 내에 야생동물센터로 이송한다면 물이나 먹이를 함부로 주지 말아야 합니다. 적합하지 않은 먹이는 영양 불균형으로 인해 동물을 더욱 아프게 합니다. 평소 먹는 먹이라도 쇠약한 동물에게 억지로 먹이면 기도로 넘어가거나 장에서 먹이를 소화시키지 못해 상태가 더 악화됩니다.',
                   '6. 정확한 발견 장소를 알아두면 후에 자연으로 방생 시 중요한 정보가 됩니다.', '7. 가능한 빨리 야생동물 구조 단체에 연락합니다. 필요이상으로 동물을 장기간 집에 두지 말아야 합니다. 전문지식이 없는 부적절한 사육환경으로 폐사할 확률이 높습니다.', '8. 사체 발견 시 함부로 만지지 말아야 합니다. 특히 새가 집단 폐사한 경우, AI와 같은 전염병일 가능성이 있으므로 접촉하지 말고 해당 지역의 시군구청이나 가축위생시험소에 연락하여 사체를 수거하도록 합니다.',
                   '9. 동물과 접촉한 후 손과 물건을 깨끗이 소독 합니다. 질병이나 기생충이 구조자 또는 애완동물에게 전파되는 것을 막기 위해 야생동물과 접촉한 모든 물건(수건, 옷, 담요, 이동장 등)도 깨끗이 씻어야 합니다.', '10. 교통사고 발생 시 사체는 도로에서 멀리 떨어진 곳에 두십시오. 사체를 먹으려고 다른 동물들이 도로 위로 모여들어 추가적인 희생을 야기 합니다.']

        for i in range(len(TipList)):
            self.RenderText.insert(INSERT, TipList[i])
            self.RenderText.insert(INSERT, '\n\n\n')

        self.RenderText.configure(state='disabled')

    def microbuttonaction(self):
        self.RenderText.configure(state='normal')
        self.RenderText.delete(0.0, END)
        TipList = [['동물등록절차안내', '1. 최초 등록시 동물등록에게 무선식별장치를 장착하기 위해 반드시 등록대상동물과 동반하여 방문신청.',
                    '2. 지자체조례에 따라 대행업체를 통해서만 등록이 가능한 지역이 있으니 시·군·구청 등록을 원할때는 가능여부를 사전에 확인',
                    '3.대리인이 신청할때는 위임장, 신분증 사본 등 필요 -> 등록기관에 사전연락해서 필요서류를 확인, 준비.'],
                   ['내장형 마이크로칩 등록 방법', '1. 반려동물과 인근 동물병원 방문', '2. 소유자 인적사항 및 반려동물 정보 작성',
                    '3. 신청 후 수일 내 승인이 완료되면 시군구청 방문해 등록증 수령']]
        for i in range(len(TipList)):
            self.RenderText.insert(INSERT, TipList[i][0])
            self.RenderText.insert(INSERT, '\n\n')
            self.RenderText.insert(INSERT, TipList[i][1])
            self.RenderText.insert(INSERT, '\n\n')
            self.RenderText.insert(INSERT, TipList[i][2])
            self.RenderText.insert(INSERT, '\n\n')
            self.RenderText.insert(INSERT, TipList[i][3])
            self.RenderText.insert(INSERT, '\n\n\n\n')

        self.RenderText.configure(state='disabled')

    def rowbuttonaction(self):
        self.RenderText.configure(state='normal')
        self.RenderText.delete(0.0, END)
        TipList = [['동물보호법 제16조(신고 등), 20조(동물의 소유권취득)', '①항 2인 유실·유기동물에 해당하는 동물을 발견한 때에는 동물보호센터나 지방자치 단체의 장에게 신고 할 수 있다. 또한 공고가 있는 날부터 10일이 경과하여도 소유자 등을 알 수 없는 경우에는 유실물법 제12조 및 민법 제253조의 규정에 불구하고 해당 시·군· 자치구가 그 동물의 소유권을 취득한다.', '-> 야생동물은 7일간, 주인이 있는 동물은 10일간 공고하면 지자체가 소유권을 획득 하지만 소유권을 획득한 동물이 분양되지 않으면 안락사를 시키고 있다.'],
                   ['유실물법 제12조(준유실물)', '착오로 인하여 점유한 물건, 타인이 놓고 간 물건이나 일실한 가축에는 본법 및 민법 제253조의 규정을 준용한다. 단 착오로 인하여 점유한 물건에 대하여는 제3조의 비용과 제4조의 보상금을 청구할 수 없다.', '-> 동물보호법 제정이후 유기견은 유실물법보다 동물보호법의 적용을 받으며 시·군· 자치구 소관이다']]

        for i in range(len(TipList)):
            self.RenderText.insert(INSERT, TipList[i][0])
            self.RenderText.insert(INSERT, '\n\n')
            self.RenderText.insert(INSERT, TipList[i][1])
            self.RenderText.insert(INSERT, '\n\n')
            self.RenderText.insert(INSERT, TipList[i][2])
            self.RenderText.insert(INSERT, '\n\n\n')

        self.RenderText.configure(state='disabled')

    def pressedTip(self):
        self.Frame()
        self.InitNowTime()
        self.InitRenderText()
        self.TipButton()

    def pressedStar(self):
        self.Frame()
        self.InitNowTime()
        self.StarListBox()
        self.InitRenderText()
        self.StarButton()

    def StarButton(self):
        TempFont = font.Font(self.g_Tk, size=15, weight='bold', family='Consolas')
        starButton = Button(self.g_Tk, font=TempFont, text='출력', command=self.StarButtonAction)
        starButton.pack()
        starButton.place(x=40, y=400)

    def StarButtonAction(self):
        self.index = self.starlistbox.curselection()[0]

        self.RenderText.configure(state='normal')
        self.RenderText.delete(0.0, END)
        self.InitHospitals()
        self.RenderText.insert(INSERT, "공고기간 : ")
        self.RenderText.insert(INSERT, self.hospitals[self.index]['begin'] + "~" +
                               self.hospitals[self.index]['end'])
        self.RenderText.insert(INSERT, "\n종류 : ")
        self.RenderText.insert(INSERT, self.hospitals[self.index]['name'])
        self.RenderText.insert(INSERT, "\n성별 : ")
        self.RenderText.insert(INSERT, self.hospitals[self.index]['sex'])
        self.RenderText.insert(INSERT, "\n나이 : ")
        self.RenderText.insert(INSERT, self.hospitals[self.index]['age'])
        self.RenderText.insert(INSERT, "\n중성화 여부 : ")
        self.RenderText.insert(INSERT, self.hospitals[self.index]['nuet'])
        self.RenderText.insert(INSERT, "\n색 : ")
        self.RenderText.insert(INSERT, self.hospitals[self.index]['color'])
        self.RenderText.insert(INSERT, "\n특이사항 : ")
        self.RenderText.insert(INSERT, self.hospitals[self.index]['info'])
        self.RenderText.insert(INSERT, "\n\n보호 여부 : ")
        self.RenderText.insert(INSERT, self.hospitals[self.index]['pro'])
        self.RenderText.insert(INSERT, "\n보호소명 : ")
        self.RenderText.insert(INSERT, self.hospitals[self.index]['shter'])
        self.RenderText.insert(INSERT, "\n보호소 주소 : ")
        self.RenderText.insert(INSERT, self.hospitals[self.index]['address'])
        self.RenderText.insert(INSERT, "\n보호소 번호 : ")
        self.RenderText.insert(INSERT, self.hospitals[self.index]['tel'])
        self.RenderText.insert(INSERT, "\n\n")

        self.Imageview()

    def Imageview(self):
        url = list(self.hospital['image'] for self.hospital in self.hospitals)
        with urllib.request.urlopen(url[self.indexpage]) as u:
            raw_data = u.read()
        im = Image.open(BytesIO(raw_data))
        self.animalimg = ImageTk.PhotoImage(im)
        image = Label(self.g_Tk, image=self.animalimg)
        image.pack()
        image.place(x=300, y=400)

    def StarListBox(self):
        ListBoxScrollbar = Scrollbar(self.g_Tk)
        ListBoxScrollbar.pack()
        ListBoxScrollbar.place(x=140, y=150)

        TempFont = font.Font(self.g_Tk, size=12, family='Consolas')
        self.starlistbox = Listbox(self.g_Tk, font=TempFont, activestyle='none',
                                     width=12, height=10, borderwidth=12, relief='ridge',
                                     yscrollcommand=ListBoxScrollbar.set)

        for i in range(len(self.datalist)):
            self.starlistbox.insert(i + 1, self.hospitals[self.indexpage]['name'])


        self.starlistbox.pack()
        self.starlistbox.place(x=40, y=150)

        ListBoxScrollbar.config(command=self.starlistbox.yview)

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
                'image': self.item.findtext("THUMB_IMAGE_COURS"),
                'shter': self.item.findtext("SHTER_NM"),
                'tel': self.item.findtext("SHTER_TELNO"),
                'sigun': self.item.findtext("SIGUN_NM"),
                'sigunCD': self.item.findtext("SIGUN_CD"),
                'nuet': self.item.findtext("NEUT_YN"),
                'chr': self.item.findtext("CHRGPSN_NM"),
                'chrtel' : self.item.findtext("CHRGPSN_CONTCT_NO"),
                'dis': self.item.findtext("DISCVRY_PLC_INFO")
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

    def mailButtonAction(self):
        host = "smtp.gmail.com"
        port = "587"

        senderAddr = "rose20020622@gmail.com"  # 보내는 사람 email 주소.
        recipientAddr = "dajeong0404@naver.com"  # 받는 사람 email 주소.

        msg = MIMEMultipart('alternative')
        msg['Subject'] = "경기도 보호 동물 정보"
        msg['From'] = senderAddr
        msg['To'] = recipientAddr

        msgtext = ("공고기간 : "+self.hospitals[self.winiSearchIndex]['begin'] + "~" + self.hospitals[self.winiSearchIndex]['end']+
                   "\n종류 : "+self.hospitals[self.winiSearchIndex]['name']+"\n성별 : "+self.hospitals[self.winiSearchIndex]['sex']+
                   "\n나이 : "+self.hospitals[self.winiSearchIndex]['age']+"\n중성화 여부 : "+self.hospitals[self.winiSearchIndex]['nuet']+
                   "\n색 : "+self.hospitals[self.winiSearchIndex]['color']+"\n특이사항 : "+self.hospitals[self.winiSearchIndex]['info']+
                   "\n\n보호여부 : "+self.hospitals[self.winiSearchIndex]['pro']+"\n보호소명 : "+self.hospitals[self.winiSearchIndex]['shter']+
                   "\n보호소 주소 : "+self.hospitals[self.winiSearchIndex]['address']+"\n보호소 번호 : "+self.hospitals[self.winiSearchIndex]['tel']+
                   "\n\n이미지 주소 : "+self.hospitals[self.winiSearchIndex]['image'])
        msgPart = MIMEText(msgtext, 'plain')
        msg.attach(msgPart)

        # 메일을 발송한다.
        s = mysmtplib.MySMTP(host, port)
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
            elif self.iSearchIndex == 2 and self.ani_set[i] == '[기타축종]':
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
