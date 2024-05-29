'''import requests
import xml.etree.ElementTree as ET
import tkinter
#병원정보 서비스 예제
url = ' https://openapi.gg.go.kr/Animalhosptl'
# 공공데이터포털에서 발급받은 디코딩되지 않은 인증키 입력
service_key = "MzVmYTU2MDYwMTU1NGQ0MmJiZjM0YzM0ZmYzZmJjZjg="
queryParams = {'KEY': service_key, 'Type': 'xml', 'pIndex': '1', 'pSize': '10'}

response = requests.get(url, params=queryParams)
print(response.text)
root = ET.fromstring(response.text)

window = tkinter.Tk()
window.title("병원정보")
frame = tkinter.Frame(window)
frame.pack()

header = ["Name", "Addr", "Tel"]

for i, col_name in enumerate(header):
    label = tkinter.Label(frame, text=col_name, font=("Helvetica", 14, "bold"))
    label.grid(row=0, column=i)

row_count = 1
for item in root.iter("row"):
    Nm = item.findtext("BIZPLC_NM")
    addr = item.findtext("REFINE_LOTNO_ADDR")
    telno = item.findtext("LOCPLC_FACLT_TELNO")

    data = [Nm, addr, telno]
    for i, value in enumerate(data):
        label = tkinter.Label(frame, text=value, font=("Helvetica", 12))
        label.grid(row=row_count, column=i)

    row_count += 1

window.mainloop()
'''

import requests
import xml.etree.ElementTree as ET
import tkinter
#병원정보 서비스 예제
url = 'https://openapi.gg.go.kr/Animalhosptl'
# 공공데이터포털에서 발급받은 디코딩되지 않은 인증키 입력
service_key = "35fa560601554d42bbf34c34ff3fbcf8"
queryParams = {'KEY': service_key, 'Type': 'xml', 'pIndex': '1', 'pSize': '10'}

response = requests.get(url, params=queryParams)
print(response.text)
root = ET.fromstring(response.text)

window = tkinter.Tk()
window.title("병원정보")
frame = tkinter.Frame(window)
frame.pack()

header = ["Name", "Addr", "State"]

for i, col_name in enumerate(header):
    label = tkinter.Label(frame, text=col_name, font=("Helvetica", 14, "bold"))
    label.grid(row=0, column=i)

row_count = 1
for item in root.iter("row"):
    Nm = item.findtext("BIZPLC_NM")
    addr = item.findtext("REFINE_LOTNO_ADDR")
    State = item.findtext("BSN_STATE_NM")

    data = [Nm, addr, State]
    for i, value in enumerate(data):
        label = tkinter.Label(frame, text=value, font=("Helvetica", 12))
        label.grid(row=row_count, column=i)

    row_count += 1

window.mainloop()

"""
import requests
import xml.etree.ElementTree as ET
import tkinter
#병원정보 서비스 예제
url = 'https://openapi.gg.go.kr/AnimalPharmacy'
# 공공데이터포털에서 발급받은 디코딩되지 않은 인증키 입력
service_key = "bbdf1fa436164143a3704fbb1d77aa93"
queryParams = {'KEY': service_key, 'Type': 'xml', 'pIndex': '1', 'pSize': '10'}

response = requests.get(url, params=queryParams)
print(response.text)
root = ET.fromstring(response.text)

window = tkinter.Tk()
window.title("병원정보")
frame = tkinter.Frame(window)
frame.pack()

header = ["Name", "Addr", "State"]

for i, col_name in enumerate(header):
    label = tkinter.Label(frame, text=col_name, font=("Helvetica", 14, "bold"))
    label.grid(row=0, column=i)

row_count = 1
for item in root.iter("row"):
    Nm = item.findtext("BIZPLC_NM")
    addr = item.findtext("REFINE_LOTNO_ADDR")
    State = item.findtext("BSN_STATE_NM")

    data = [Nm, addr, State]
    for i, value in enumerate(data):
        label = tkinter.Label(frame, text=value, font=("Helvetica", 12))
        label.grid(row=row_count, column=i)

    row_count += 1

window.mainloop()
"""