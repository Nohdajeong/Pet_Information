from tkinter import *
from tkinter import font

'''
import http.client

conn = http.client.HTTPConnection("openapi.gg.go.kr")
conn.request("Get", "/Animalhosptl?")
req = conn.getresponse()
print(req.status, req.reason)
print(req.read().decode('utf-8'))
'''

g_Tk = Tk()
g_Tk.geometry("400x600+750+200")
DataList = []
url = "openapi.gg.go.kr"
query = "/Animalhosptl?"


#지역코드
SIGUN_CD = [['41110', '수원시']]

def InitTopText():
   TempFont = font.Font(g_Tk, size=20, weight='bold', family='Consolas')
   MainText = Label(g_Tk, font=TempFont, text="[경기도 동물 보호 정보 App]")
   MainText.pack()
   MainText.place(x=20)

def InitSearchListBox():
    global SearchListBox
    ListBoxScrollbar = Scrollbar(g_Tk)
    ListBoxScrollbar.pack()
    ListBoxScrollbar.place(x=150, y=50)

    TempFont = font.Font(g_Tk, size=15, weight='bold', family='Consolas')
    SearchListBox = Listbox(g_Tk, font=TempFont, activestyle='none',
                            width=10, height=5, borderwidth=12, relief='ridge',
                            yscrollcommand=ListBoxScrollbar.set)

    for i in range(1):
        SearchListBox.insert(i+1, SIGUN_CD[i][1]) #8개 지역 리스트 삽입

    SearchListBox.pack()
    SearchListBox.place(x=10, y=50)

    ListBoxScrollbar.config(command=SearchListBox.yview)

def InitSearchButton():
    TempFont = font.Font(g_Tk, size=12, weight='bold', family = 'Consolas')
    SearchButton = Button(g_Tk, font = TempFont, text="검색",  command=SearchButtonAction)
    SearchButton.pack()
    SearchButton.place(x=330, y=110)


def SearchButtonAction():
    global SearchListBox

    RenderText.configure(state='normal')
    RenderText.delete(0.0, END)
    iSearchIndex = SearchListBox.curselection()[0]

    sgguCD = SIGUN_CD[iSearchIndex][0] #시구 코드 8개구
    Search(sgguCD)

    RenderText.configure(state='disabled')

def Search(sgguCD):
    import http.client
    conn = http.client.HTTPConnection(url)
    conn.request("GET", query+sgguCD)

    req = conn.getresponse()

    global DataList
    DataList.clear()

    if req.status == 200:
        strXml = req.read().decode('utf-8')
        #print(strXml)
        from xml.etree import ElementTree
        tree = ElementTree.fromstring(strXml)
        # item 엘리먼트를 가져옵니다.
        itemElements = tree.iter("item")  # return list type
        #print(itemElements)
        for item in itemElements:
            addr = item.find("addr")    #병원주소
            name = item.find("yadmNm")  #병원명
            telno = item.find("telno")  #전화번호
            DataList.append((name.text,addr.text,telno.text))


        for i in range(len(DataList)):
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


def InitRenderText():
    global RenderText

    RenderTextScrollbar = Scrollbar(g_Tk)
    RenderTextScrollbar.pack()
    RenderTextScrollbar.place(x=375, y=200)

    TempFont = font.Font(g_Tk, size=10, family='Consolas')
    RenderText = Text(g_Tk, width=49, height=27, borderwidth=12, relief='ridge', yscrollcommand=RenderTextScrollbar.set)
    RenderText.pack()
    RenderText.place(x=10, y=215)
    RenderTextScrollbar.config(command=RenderText.yview)
    RenderTextScrollbar.pack(side=RIGHT, fill=BOTH)

    RenderText.configure(state='disabled')


InitTopText()
InitSearchListBox()
InitSearchButton()
InitRenderText()


g_Tk.mainloop()