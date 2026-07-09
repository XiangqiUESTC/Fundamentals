from concurrent.futures import ProcessPoolExecutor as Pool
import time
from threading import Thread
import requests

n = 0


def monitor():
    global n
    while True:
        time.sleep(1)
        print(f"{n}/sec")
        n = 0


def process_request():
    req = requests.get("http://127.0.0.1:8000/delay")
    return req.status_code


def done_callback(future):
    global n
    future.result()
    n += 1


if __name__ == "__main__":
    Thread(target=monitor, daemon=True).start()

    with Pool(10) as pool:
        while True:
            future = pool.submit(process_request)
            future.add_done_callback(done_callback)