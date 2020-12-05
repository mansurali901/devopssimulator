import urllib.request
url = "http://127.0.0.1:5000/Connect"
request = urllib.request.Request(url)
response = urllib.request.urlopen(request)
print (response.read().decode('utf-8'))