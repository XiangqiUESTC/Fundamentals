# server.py
from fastapi import FastAPI
import asyncio

app = FastAPI()

@app.get("/delay")
async def delay(ms: int = 100):
    await asyncio.sleep(ms / 1000)
    return {"ok": True, "delay_ms": ms}