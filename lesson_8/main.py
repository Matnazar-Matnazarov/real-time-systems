from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.templating import Jinja2Templates
import asyncio
import psutil
import os

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.jinja", {"request": request})


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.websocket("/ws/metrics")
async def websocket_metrics(websocket: WebSocket):
    await websocket.accept()
    prev_net = psutil.net_io_counters()
    try:
        while True:
            cpu_percent = psutil.cpu_percent(interval=None)
            cpu_per_core = psutil.cpu_percent(interval=None, percpu=True)
            virtual_mem = psutil.virtual_memory()

            try:
                load1, load5, load15 = os.getloadavg()
            except (OSError, AttributeError):
                load1 = load5 = load15 = 0.0

            current_net = psutil.net_io_counters()
            if prev_net is not None:
                bytes_sent_diff = max(current_net.bytes_sent - prev_net.bytes_sent, 0)
                bytes_recv_diff = max(current_net.bytes_recv - prev_net.bytes_recv, 0)
            else:
                bytes_sent_diff = 0
                bytes_recv_diff = 0

            upload_bps = bytes_sent_diff
            download_bps = bytes_recv_diff

            data = {
                "cpu_percent": cpu_percent,
                "cpu_per_core": cpu_per_core,
                "memory_percent": virtual_mem.percent,
                "memory_used": virtual_mem.used,
                "memory_total": virtual_mem.total,
                "load_1": load1,
                "load_5": load5,
                "load_15": load15,
                "net_bytes_sent": current_net.bytes_sent,
                "net_bytes_recv": current_net.bytes_recv,
                "net_upload_bps": upload_bps,
                "net_download_bps": download_bps,
            }

            prev_net = current_net

            await websocket.send_json(data)
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        pass


if __name__ == "__main__":
    import uvicorn
    
    print("=" * 60)
    print("🚀 Real-Time System Metrics Server")
    print("=" * 60)
    print("📍 Server: http://localhost:8000")
    print("📊 Dashboard: http://localhost:8000")
    print("🔌 WebSocket: ws://localhost:8000/ws/metrics")
    print("💚 Health Check: http://localhost:8000/health")
    print("📖 API Docs: http://localhost:8000/docs")
    print("=" * 60)
    print("💡 Real vaqt rejimida sistema metrikalarini ko'rsatadi:")
    print("   • CPU foydalanish (umumiy va per-core)")
    print("   • RAM foydalanish")
    print("   • Network I/O")
    print("   • System load average")
    print("=" * 60)
    print()
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
