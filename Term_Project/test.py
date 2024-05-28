import http.client

conn = http.client.HTTPConnection("openapi.gg.go.kr")
conn.request("Get", "/Animalhosptl")
req = conn.getresponse()
print(req.status, req.reason)
print(req.read().decode('utf-8'))
