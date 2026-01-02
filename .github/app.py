from fastapi import FastAPI, Request
import httpx, base64

app = FastAPI()

@app.get("/")
def home():
    return "OK"

@app.post("/relay")
async def relay(req: Request):
    data = await req.json()

    target = data["url"]
    payload = base64.b64decode(data["data"])

    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.post(
            target,
            content=payload,
            headers={"Content-Type": "application/octet-stream"}
        )

    return {
        "data": base64.b64encode(r.content).decode()
    }
