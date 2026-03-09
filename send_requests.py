import requests
import time

url="http://localhost:5550/"

data={
"username":"user",
"password":"bluetiger456!"
}

while True:

    try:
        r=requests.post(url,data=data)
        print("Request sent:",r.status_code)
    except Exception as e:
        print("Error:",e)

    time.sleep(15)
