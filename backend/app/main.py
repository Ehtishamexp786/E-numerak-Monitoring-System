from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.db.database import create_tables
from app.api.routes import monitors, alerts, logs, dashboard
from app.core.scheduler import start_scheduler, stop_scheduler

@asynccontextmanager
async def lifespan(app: FastAPI):
    """This function is used to ensures when the server will run before start running 
    all tables should create first then server will run"""
    await create_tables()
    await start_scheduler()
    yield
    await stop_scheduler()


app = FastAPI(
    title="Production Monitoring System",
    description="AI-Powered Server Monitoring with WhatsApp Alerts",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(dashboard.router, prefix="/api/dashboard", tags=["Dashboard"])
app.include_router(monitors.router, prefix="/api/monitors", tags=["Monitors"])
app.include_router(alerts.router, prefix="/api/alerts", tags=["Alerts"])
app.include_router(logs.router, prefix="/api/logs", tags=["Logs"])

@app.get("/")
async def root():
    return {"message": "Monitoring System Running!", "status": "ok"}


@app.get("/health")
async def health():
    return {"status": "healthy"}