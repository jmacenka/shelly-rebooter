import asyncio

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.config import settings
from app.logging_handler import add_log, IN_MEMORY_LOGS
from app.routes import router
from app.core import connectivity_monitor

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve the favicon from /static automatically
@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return StaticFiles(directory="static").lookup_path("favicon.ico")[0]

# Include routes
app.include_router(router)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(connectivity_monitor())
    add_log("Application startup complete.")

@app.get("/")
def dashboard(request: Request):
    hours = settings.total_duration // 3600
    minutes = (settings.total_duration % 3600) // 60
    total_duration_str = f"{hours:02d}:{minutes:02d}"
    logs_for_ui = list(reversed(IN_MEMORY_LOGS[-50:]))

    return templates.TemplateResponse("index.html", {
        "request": request,
        "logs": logs_for_ui,
        "config": settings,
        "total_duration_str": total_duration_str,
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=settings.port,
        reload=True,
        ssl_certfile=settings.ssl_certfile,
        ssl_keyfile=settings.ssl_keyfile
    )
