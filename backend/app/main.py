from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from app.api.routes import router, stats, history
from app.api.websockets import manager
from app.services.sniffer import SnifferService
from app.services.simulation import SimulationService
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix=settings.API_V1_STR)

def event_handler(event):
    # Update global stats
    stats["total_packets"] += 1
    if event["prediction"] == "ATTACK":
        stats["total_threats"] += 1
        stats["severity_counts"][event["severity"]] += 1
    
    # Store history
    history.append(event)
    if len(history) > 100:
        history.pop(0)
    
    # Broadcast to frontend
    asyncio.run_coroutine_threadsafe(manager.broadcast(event), loop)

sniffer = SnifferService(event_handler)
simulator = SimulationService(event_handler)

@app.on_event("startup")
async def startup_event():
    global loop
    loop = asyncio.get_event_loop()
    # sniffer.start()  # Uncomment for live sniffing
    asyncio.create_task(simulator.start()) # Default to simulator for demo safety

@app.on_event("shutdown")
def shutdown_event():
    sniffer.stop()
    simulator.stop()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
