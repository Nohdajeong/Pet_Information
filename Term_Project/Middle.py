import tkinter
import tkinter.messagebox
import tkinter as tk
import tkinter.ttk as ttk
import requests
import xml.etree.ElementTree as ET
import io
from tkinter import *
from tkinter import font
from PIL import Image, ImageTk
from googlemaps import Client

g_Tk = Tk()
g_Tk.title("경기도 유기동물 정보 프로그램")
g_Tk.geometry("430x600+750+200")
frame = tkinter.Frame(g_Tk)
frame.pack()

class Program:
    # 최상단 타이틀
    def InitTopText(self):
        TempFont = font.Font(g_Tk, size=20, weight='bold', family='Consolas')
        MainText = Label(g_Tk, font=TempFont, text="[경기도 유기동물 정보 프로그램]")
        MainText.pack()
        MainText.place(x=10)

    def InitInputLabel(self):
        global InputLabel
        TempFont = font.Font(g_Tk, size=15, family='Consolas')
        InputLabel = Entry(g_Tk, font=TempFont, width=30)
        InputLabel.pack()
        InputLabel.place(x=10, y=55)

    def InitSearchButton(self):
        TempFont = font.Font(g_Tk, size=15, family='Consolas')
        SearchButton = Button(g_Tk, font=TempFont, text="검색")
        SearchButton.pack()
        SearchButton.place(x=350, y=50)

    def InitRenderText(self):
        global RenderText

        RenderTextScrollbar = Scrollbar(g_Tk)
        RenderTextScrollbar.pack()
        RenderTextScrollbar.place(x=675, y=200)

        TempFont = font.Font(g_Tk, size=10, family='Consolas')
        RenderText = Text(g_Tk, width=55, height=30, relief='ridge', yscrollcommand=RenderTextScrollbar.set)
        RenderText.pack()
        RenderText.place(x=10, y=110)
        RenderTextScrollbar.config(command=RenderText.yview)
        RenderTextScrollbar.pack(side=RIGHT, fill=BOTH)

        RenderText.configure(state='disabled')

    def InitAniHospitl(self):
        TempFont = font.Font(g_Tk, size=25, family='Consolas')
        HosptlButton = Button(g_Tk, font=TempFont, text="약국", command=self.Mapcommand)
        HosptlButton.pack()
        HosptlButton.place(x=10, y=530)

    def Mapcommand(self):
        pass

    def InitAniSick(self):
        TempFont = font.Font(g_Tk, size=25, family='Consolas')
        SickButton = Button(g_Tk, font=TempFont, text="보호소")
        SickButton.pack()
        SickButton.place(x=100, y=530)

    def InitAniProtect(self):
        TempFont = font.Font(g_Tk, size=25, family='Consolas')
        ProtectButton = Button(g_Tk, font=TempFont, text="보호소")
        ProtectButton.pack()
        ProtectButton.place(x=215, y=530)

    def InitTip(self):
        TempFont = font.Font(g_Tk, size=25, family='Consolas')
        TipButton = Button(g_Tk, font=TempFont, text="TIP")
        TipButton.pack()
        TipButton.place(x=325, y=530)

    def __init__(self):
        self.InitTopText()
        self.InitInputLabel()
        self.InitSearchButton()
        # InitRenderText()
        self.InitAniHospitl()
        self.InitAniSick()
        self.InitAniProtect()
        self.InitTip()

        g_Tk.mainloop()

Program()