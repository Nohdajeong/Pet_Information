import datetime
import tkinter
import tkinter as tk
from tkinter import *
from tkinter import font
import requests
import xml.etree.ElementTree as ET
import time

g_Tk = Tk()
g_Tk.title("동물병원정보")
frame = tkinter.Frame(g_Tk)
frame.pack()

g_Tk.geometry("800x600+750+200")
DataList = []

#병원정보 서비스 예제
url = ' https://openapi.gg.go.kr/Animalhosptl'

# 공공데이터포털에서 발급받은 디코딩되지 않은 인증키 입력
service_key1 = "ZjZiMTFmMDI4NDlmNGI4N2FmY2Y2YjNkZTI0NTc2ODY="
service_key2 = "MzVmYTU2MDYwMTU1NGQ0MmJiZjM0YzM0ZmYzZmJjZjg="
service_key3 = "YmJkZjFmYTQzNjE2NDE0M2EzNzA0ZmJiMWQ3N2FhOTM="
service_key4 = "M2IxMTY1OWZlMDllNDU3ZjkzMGE2NWFhMDU2MWRmZGM="
service_key5 = "MjllYjk0NWI0ODU0NDZkZWIwMDQ4ZGQxOWE4NjQyOGE="
queryParams = {}

# 지역코드
SIGUNCD = [['41110', '수원시'], ['41820', '가평군']]

# 관련번호
PHONENUMBER = ['동물보호', '1577-0954', '',
               '유기견 신고센터', '110', '',
               '', '', '',
               '', '', '']

TipList = [['유기견 신고방법', '인식표나 마이크로칩을 확인 후, 확인이 된다면 곧바로 보호자에게 연락한다.'],
           ['마이크로칩 확인방법', '가까운 동물병원에 가면 무료로 확인이 가능하다.'],
           ['설명3', ''], ['설명4', ''],
           ['설명5', ''], ['설명6', ''],
           ['설명7', ''], ['설명8', '']]

# 버튼 넘버
cnt = 0

# 최상단 타이틀 이름
def InitTopText():
    TempFont = font.Font(g_Tk, size=20, weight='bold', family='Consolas')
    MainText = Label(g_Tk, font=TempFont, text="[ 경기도 동물 보호 정보 프로그램 ]")
    MainText.pack()
    MainText.place(x=200)


def InitNowTime():
    TempFont = font.Font(g_Tk, size=15, weight='bold', family='Consolas')
    current_time = time.strftime('%H:%M:%S')
    clock_label = Label(g_Tk, font=TempFont, text=current_time)
    clock_label.after(1000, InitNowTime)
    clock_label.pack()
    clock_label.place(x=620, y=530)


# 검색 버튼
def InitSearchButton():
    TempFont = font.Font(g_Tk, size=20, weight='bold', family='Consolas')
    SearchButton = Button(g_Tk, font=TempFont, text="검색", command=SearchButtonAction)
    SearchButton.pack()
    SearchButton.place(x=635, y=60)

def SearchButtonAction():
    global DataList
    DataList.clear()

# 검색창
def InitSearchPage():
    global RenderText

    RenderTextScrollbar = Scrollbar(g_Tk)
    RenderTextScrollbar.pack()
    RenderTextScrollbar.place(x=675, y=200)

    TempFont = font.Font(g_Tk, size=10, family='Consolas')
    RenderText = Text(g_Tk, width=49, height=27, borderwidth=12, relief='ridge', yscrollcommand=RenderTextScrollbar.set)
    RenderText.pack()
    RenderText.place(x=210, y=130)
    RenderTextScrollbar.config(command=RenderText.yview)
    RenderTextScrollbar.pack(side=RIGHT, fill=BOTH)

    RenderText.configure(state='disabled')

def InitSearchListBox():
    '''
    global SearchListBox
    ListBoxScrollbar = Scrollbar(g_Tk)
    ListBoxScrollbar.pack()
    ListBoxScrollbar.place(x=450, y=50)

    TempFont = font.Font(g_Tk, size=15, weight='bold', family='Consolas')
    SearchListBox = Listbox(g_Tk, font=TempFont, activestyle='none',
                            width=10, height=5, borderwidth=12, relief='ridge',
                            yscrollcommand=ListBoxScrollbar.set)

    for i in range(2):
        SearchListBox.insert(i + 1, SIGUNCD[i][1])  # 8개 지역 리스트 삽입

    SearchListBox.pack()
    SearchListBox.place(x=310, y=50)

    ListBoxScrollbar.config(command=SearchListBox.yview)
'''

# 메일 버튼
def InitMailButton():
    TempFont = font.Font(g_Tk, size=20, weight='bold', family='Consolas')
    SearchButton = Button(g_Tk, font=TempFont, text="메일", command=MailButtonAction)
    SearchButton.pack()
    SearchButton.place(x=635, y=230)

def MailButtonAction():
    pass

# 관련 전화번호 출력하는 곳
def InitAnimalPhone():
    Tempfont = font.Font(g_Tk, size=13, family='Consolas')
    PhoneNumListBox = Listbox(g_Tk, font=Tempfont, activestyle='none',
                              width=13, height=8, borderwidth=12, relief='ridge')

    for i in range(12):
        PhoneNumListBox.insert(i+1, PHONENUMBER[i])

    PhoneNumListBox.pack()
    PhoneNumListBox.place(x=600, y=310)

# 즐겨찾기 버튼
def InitLikeButton():
    TempFont = font.Font(g_Tk, size=20, weight='bold', family='Consolas')
    SearchButton = Button(g_Tk, font=TempFont, text="즐겨찾기", command=MailButtonAction)
    SearchButton.pack()
    SearchButton.place(x=40, y=150)

# 병원 버튼
def InitAniHosplButton():
    global cnt
    cnt = 0

    TempFont = font.Font(g_Tk, size=20, weight='bold', family='Consolas')
    SearchButton = Button(g_Tk, font=TempFont, text="병원", command=AniButtonAction)
    SearchButton.pack()
    SearchButton.place(x=40, y=220)

# 의료품 버튼
def InitAniSickButton():
    global cnt
    cnt = 1

    TempFont = font.Font(g_Tk, size=20, weight='bold', family='Consolas')
    SearchButton = Button(g_Tk, font=TempFont, text="의약품", command=AniButtonAction)
    SearchButton.pack()
    SearchButton.place(x=40, y=290)

# 보호소 버튼
def InitAniProtectButton():
    global cnt
    cnt = 2

    TempFont = font.Font(g_Tk, size=20, weight='bold', family='Consolas')
    SearchButton = Button(g_Tk, font=TempFont, text="보호소", command=AniButtonAction)
    SearchButton.pack()
    SearchButton.place(x=40, y=360)

def AniButtonAction():
    global SearchListBox

    RenderText.configure(state='normal')
    RenderText.delete(0.0, END)

    SearchHospl()
    RenderText.configure(state='disabled')

def SearchHospl():
    global DataList, queryParams
    DataList.clear()

    if cnt == 0:
        queryParams = {'KEY': service_key1, 'Type': 'xml', 'pIndex': '1', 'pSize': '10'}
    elif cnt == 1:
        queryParams = {'KEY': service_key2, 'Type': 'xml', 'pIndex': '1', 'pSize': '10'}
    elif cnt == 3:
        queryParams = {'KEY': service_key3, 'Type': 'xml', 'pIndex': '1', 'pSize': '10'}

    response = requests.get(url, params=queryParams)
    #print(response.text)
    root = ET.fromstring(response.text)

    row_count = 1
    for item in root.iter("row"):
        Nm = item.findtext("BIZPLC_NM")
        addr = item.findtext("REFINE_LOTNO_ADDR")
        telno = item.findtext("LOCPLC_FACLT_TELNO")
        DataList.append((Nm, addr, telno))

        for i, value in enumerate(DataList):
            RenderText.insert(INSERT, "[")
            RenderText.insert(INSERT, i + 1)
            RenderText.insert(INSERT, "] ")
            RenderText.insert(INSERT, "병원명: ")
            RenderText.insert(INSERT, DataList[i][0])
            RenderText.insert(INSERT, "\n")
            RenderText.insert(INSERT, "주소: ")
            RenderText.insert(INSERT, DataList[i][1])
            RenderText.insert(INSERT, "\n")
            RenderText.insert(INSERT, "전화번호: ")
            RenderText.insert(INSERT, DataList[i][2])
            RenderText.insert(INSERT, "\n\n")

    row_count += 1

# Tip 버튼
def InitTipButton():
    TempFont = font.Font(g_Tk, size=20, weight='bold', family='Consolas')
    SearchButton = Button(g_Tk, font=TempFont, text="TIP", command=TipButtonAction)
    SearchButton.pack()
    SearchButton.place(x=40, y=430)

def TipButtonAction():
    global SearchListBox

    RenderText.configure(state='normal')
    RenderText.delete(0.0, END)

    for i in range(8):
        RenderText.insert(INSERT, "[ TIP ")
        RenderText.insert(INSERT, i+1)
        RenderText.insert(INSERT, ' ')
        RenderText.insert(INSERT, TipList[i][0])
        RenderText.insert(INSERT, " ]")
        RenderText.insert(INSERT, '\n')
        RenderText.insert(INSERT, TipList[i][1])
        RenderText.insert(INSERT,'\n\n')

    RenderText.configure(state='disabled')

def InitMemoButton():
    TempFont = font.Font(g_Tk, size=20, weight='bold', family='Consolas')
    MemoButton = Button(g_Tk, font=TempFont, text="메모", command=AniButtonAction)
    MemoButton.pack()
    MemoButton.place(x=635, y=150)



InitTopText()

InitSearchButton()
InitSearchPage()
InitSearchListBox()

InitMailButton()
InitAnimalPhone()

InitLikeButton()
InitAniHosplButton()
InitAniSickButton()
InitAniProtectButton()
InitTipButton()

InitNowTime()
InitMemoButton()

g_Tk.mainloop()