from tkinter import *
from tkinter import font

g_Tk = Tk()
g_Tk.geometry("800x600+750+200")
DataList = []

# 최상단 타이틀 이름
def InitTopText():
    TempFont = font.Font(g_Tk, size=20, weight='bold', family='Consolas')
    MainText = Label(g_Tk, font=TempFont, text="[ 경기도 동물 보호 정보 프로그램 ]")
    MainText.pack()
    MainText.place(x=200)

# 검색 버튼
def InitSearchButton():
    TempFont = font.Font(g_Tk, size=12, weight='bold', family='Consolas')
    SearchButton = Button(g_Tk, font=TempFont, text="검색", command=SearchButtonAction)
    SearchButton.pack()
    SearchButton.place(x=730, y=60)

def SearchButtonAction():
    pass

# 검색창
def InitSearchPage():
    pass

# 메일 버튼
def InitMailButton():
    TempFont = font.Font(g_Tk, size=15, weight='bold', family='Consolas')
    SearchButton = Button(g_Tk, font=TempFont, text="메일", command=MailButtonAction)
    SearchButton.pack()
    SearchButton.place(x=730, y=300)

def MailButtonAction():
    pass

# 관련 전화번호 출력하는 곳
def InitAnimalPhone():
    pass

# 즐겨찾기 버튼
def InitLikeButton():
    TempFont = font.Font(g_Tk, size=20, weight='bold', family='Consolas')
    SearchButton = Button(g_Tk, font=TempFont, text="즐겨찾기", command=MailButtonAction)
    SearchButton.pack()
    SearchButton.place(x=40, y=150)

# 병원 버튼
def InitAniHosplButton():
    TempFont = font.Font(g_Tk, size=20, weight='bold', family='Consolas')
    SearchButton = Button(g_Tk, font=TempFont, text="병원", command=MailButtonAction)
    SearchButton.pack()
    SearchButton.place(x=40, y=220)

# 의료품 버튼
def InitAniSickButton():
    TempFont = font.Font(g_Tk, size=20, weight='bold', family='Consolas')
    SearchButton = Button(g_Tk, font=TempFont, text="의약품", command=MailButtonAction)
    SearchButton.pack()
    SearchButton.place(x=40, y=290)

# 보호소 버튼
def InitAniProtectButton():
    TempFont = font.Font(g_Tk, size=20, weight='bold', family='Consolas')
    SearchButton = Button(g_Tk, font=TempFont, text="보호소", command=MailButtonAction)
    SearchButton.pack()
    SearchButton.place(x=40, y=360)

# Tip 버튼
def InitTipButton():
    TempFont = font.Font(g_Tk, size=20, weight='bold', family='Consolas')
    SearchButton = Button(g_Tk, font=TempFont, text="TIP", command=MailButtonAction)
    SearchButton.pack()
    SearchButton.place(x=40, y=430)


InitTopText()

InitSearchButton()
InitSearchPage()

InitMailButton()
InitAnimalPhone()

InitLikeButton()
InitAniHosplButton()
InitAniSickButton()
InitAniProtectButton()
InitTipButton()

g_Tk.mainloop()