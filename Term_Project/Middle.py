import tkinter
import tkinter.messagebox
from tkinter import *
from tkinter import font

g_Tk = Tk()
g_Tk.title("경기도 동불 보호 정보 프로그램")
frame = tkinter.Frame(g_Tk)
frame.pack()

g_Tk.geometry("800x600+750+200")


# 최상단 타이틀
def InitTopText():
    TempFont = font.Font(g_Tk, size=20, weight='bold', family='Consolas')
    MainText = Label(g_Tk, font=TempFont, text="[ 경기도 동물 보호 정보 프로그램 ]")
    MainText.pack()
    MainText.place(x=200)

def InitInputLabel():
    global InputLabel
    TempFont = font.Font(g_Tk, size=15, family='Consolas')
    InputLabel = Entry(g_Tk, font=TempFont, width=30)
    InputLabel.pack()
    InputLabel.place(x=200, y=55)

def InitSearchButton():
    TempFont = font.Font(g_Tk, size=15, family='Consolas')
    SearchButton = Button(g_Tk, font=TempFont, text="검색")
    SearchButton.pack()
    SearchButton.place(x=555, y=50)

def InitRenderText():
    global RenderText

    RenderTextScrollbar = Scrollbar(g_Tk)
    RenderTextScrollbar.pack()
    RenderTextScrollbar.place(x=675, y=200)

    TempFont = font.Font(g_Tk, size=10, family='Consolas')
    RenderText = Text(g_Tk, width=60, height=30, relief='ridge', yscrollcommand=RenderTextScrollbar.set)
    RenderText.pack()
    RenderText.place(x=200, y=110)
    RenderTextScrollbar.config(command=RenderText.yview)
    RenderTextScrollbar.pack(side=RIGHT, fill=BOTH)

    RenderText.configure(state='disabled')

InitTopText()
InitInputLabel()
InitSearchButton()
#InitRenderText()

g_Tk.mainloop()