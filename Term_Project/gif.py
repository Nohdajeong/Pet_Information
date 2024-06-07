from tkinter import *
from io import BytesIO
import urllib
import urllib.request
from PIL import Image,ImageTk
window=Tk()
window.geometry("500x500+500+200")
url="http://www.animal.go.kr/files/shelter/2024/05/202406011306171.jpg"
with urllib.request.urlopen(url) as u:
    raw_data=u.read()
im=Image.open(BytesIO(raw_data))
image = ImageTk.PhotoImage(im)
Label(window, image=image, height=400,width=400).pack()
window.mainloop()