import os
from typing import List, Any
from fastapi import FastAPI, Query
from pydantic import BaseModel
from miio import Device

app = FastAPI(title="Mi Home REST API")

# ✅ Pydantic model for POST request body
class CommandRequest(BaseModel):
    method: str
    params: List[Any] = []
    ip: str | None = None
    token: str | None = None

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/device/info")
def device_info(
    ip: str = Query(default=None),
    token: str = Query(default=None)
):
    ip = ip or os.environ.get("DEVICE_IP")
    token = token or os.environ.get("DEVICE_TOKEN")
    dev = Device(ip=ip, token=token)
    info = dev.info()
    return {
        "model": info.model,
        "firmware": info.firmware_version,
        "hardware": info.hardware_version,
        "mac": info.mac_address,
    }

# ✅ Uses JSON body instead of form data
@app.post("/device/command")
def send_command(request: CommandRequest):
    ip = request.ip or os.environ.get("DEVICE_IP")
    token = request.token or os.environ.get("DEVICE_TOKEN")
    dev = Device(ip=ip, token=token)
    result = dev.send(request.method, request.params)
    return {"result": result}
