import asyncio
import aiohttp
import time

URL = "http://127.0.0.1:8000/delay"
CONCURRENCY = 100

n = 0


async def monitor():
    global n
    while True:
        await asyncio.sleep(1)
        print(f"{n}/sec")
        n = 0


async def worker(session):
    global n
    while True:
        async with session.get(URL) as resp:
            await resp.text()
            n += 1


async def main():
    connector = aiohttp.TCPConnector(limit=CONCURRENCY)

    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [asyncio.create_task(worker(session)) for _ in range(CONCURRENCY)]
        tasks.append(asyncio.create_task(monitor()))

        await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())