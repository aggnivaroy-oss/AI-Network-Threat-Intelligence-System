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

async def event_handler(event):
    # Update global stats
    stats["total_packets"] += 1
    if event["prediction"] == "ATTACK":
        stats["total_threats"] += 1
        stats["severity_counts"][event["severity"]] += 1

    # Store history
    history.append(event)
    if len(history) > 100:
        history.pop(0)

    # Broadcast to all connected frontend clients
    await manager.broadcast(event)

async def simulation_loop():
    service = SimulationService(event_handler)
    await service.start()

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(simulation_loop())

@app.on_event("shutdown")
async def shutdown_event():
    pass

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
