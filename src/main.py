from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from src.api import router
from src.db import init_db

app = FastAPI(
    title="Notes",
    version="1.0",
    description="Notes",
)
app.include_router(router)

@app.on_event("startup")
def startup():
    init_db()

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def frontend():
    return FileResponse("static/index.html")

