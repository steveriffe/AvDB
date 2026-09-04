"""
AvDB Native API — FastAPI Backend for Native iOS SwiftUI Client & Web Services
Hosted on Google Cloud Run (api.avdb.riffe.co.uk)
"""
import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from api.config import settings
from api.schemas import SettingsResponse
from api.cache import get_cache
from api.routers import airports, airlines, fleet

app = FastAPI(
    title="AvDB Native API",
    description="High-performance REST API serving aviation analytics, route networks, airport KPIs, and fleet dynamics for the AvDB native iOS app.",
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc"
)

# -------------------------------------------------------------
# CORS Configuration for Native iOS & Web Clients
# -------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permits iOS native URLSession calls & web frontends
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------------------
# Performance & Latency Instrumentation Middleware
# -------------------------------------------------------------
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = (time.perf_counter() - start_time) * 1000
    response.headers["X-Process-Time-Ms"] = f"{process_time:.2f}"
    return response

# -------------------------------------------------------------
# Mount Routers
# -------------------------------------------------------------
app.include_router(airports.router)
app.include_router(airlines.router)
app.include_router(fleet.router)


# -------------------------------------------------------------
# Core Root & Utility Endpoints
# -------------------------------------------------------------
@app.get("/", tags=["Root"])
def root():
    return {
        "app": settings.app_name,
        "version": settings.app_version,
        "status": "online",
        "docs": "/docs",
        "endpoints": [
            "/api/airports",
            "/api/airports/{code}/routes",
            "/api/airports/{code}/kpis",
            "/api/airlines/{code}/network",
            "/api/airlines/{code}/kpis",
            "/api/fleet/summary",
            "/api/settings"
        ]
    }


@app.get("/health", tags=["Root"])
def health():
    cache = get_cache()
    return {
        "status": "healthy",
        "cache_entries": cache.size(),
        "project_id": settings.gcp_project_id
    }


@app.get("/api/settings", response_model=SettingsResponse, tags=["Settings"])
def get_app_settings() -> SettingsResponse:
    """Provides configuration tokens, Mapbox styles, and supported parameters to iOS app."""
    return SettingsResponse(
        mapbox_token=settings.mapbox_token,
        mapbox_style_personal=settings.mapbox_style_personal,
        mapbox_style_love=settings.mapbox_style_love,
        mapbox_style_mono=settings.mapbox_style_mono,
        supported_years=[2024, 2023, 2022, 2021],
        api_version=settings.app_version
    )


@app.post("/api/cache/clear", tags=["Settings"])
def clear_cache():
    """Clears API cache."""
    cache = get_cache()
    cache.clear()
    return {"message": "Cache successfully cleared."}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
