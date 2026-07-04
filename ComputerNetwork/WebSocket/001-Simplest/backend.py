import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from openai import OpenAI, AsyncOpenAI

client = OpenAI(
    api_key="sk-e1b5f2160a6b45308d52c8bfbb3850bf",
    base_url="https://api.deepseek.com",
)
app = FastAPI() 


@app.websocket('/chat')
async def chat(websocket: WebSocket):
    await websocket.accept()
    print("连接成功")
    try:
        while True:
            msg = await websocket.receive_text()
            stream = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": msg,
                    }
                ],
                model="deepseek-v4-pro",
                stream=True
            )

            print(msg)

            for chunk in stream:
                delta = chunk.choices[0].delta
                if delta.content:
                    await websocket.send_text(delta.content)

            await websocket.send_text("[DONE]")

    except WebSocketDisconnect:
        print("客户端断开连接")

if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8000)
