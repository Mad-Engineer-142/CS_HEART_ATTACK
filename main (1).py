from fastapi import FastAPI
from service import ServiceManager

app = FastAPI()


@app.get("/search")
async def root(q: str):
    manager = ServiceManager()
    manager.addService("github", q)
    # manager.addService("vk", q)

    return {"response": {
        "items": manager.getServiceInfo()
    }}
