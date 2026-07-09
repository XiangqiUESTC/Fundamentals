import time
import requests
from threading import Thread
n = 0

def monitor():
    while True:
        global n
        time.sleep(1)
        print(f"{n}/sec")
        n = 0

Thread(target=monitor, daemon=True).start()

while True:
    resp = requests.get("http://127.0.0.1:8000/delay")
    n += 1
