import os
from fastapi import FastAPI, Query
from miio import Device

app = FastAPI(title="Mi Home REST API")

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

@app.post("/device/command")
def send_command(
    method: str,
    params: list = [],
    ip: str = Query(default=None),
    token: str = Query(default=None)
):
    ip = ip or os.environ.get("DEVICE_IP")
    token = token or os.environ.get("DEVICE_TOKEN")
    dev = Device(ip=ip, token=token)
    result = dev.send(method, params)
    return {"result": result}
