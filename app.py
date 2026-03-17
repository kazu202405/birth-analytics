"""誕生日総合占術 — FastAPI アプリケーション"""
import sys
import os
from datetime import date, time
from pathlib import Path

from fastapi import FastAPI, Request, Form, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Add engine to path
ENGINE_PATH = str(Path(__file__).parent / "engine")
sys.path.insert(0, ENGINE_PATH)

from models import BirthData
from main import run_all

app = FastAPI(title="誕生日総合占術")

# Templates & Static files
templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))
static_dir = Path(__file__).parent / "static"
static_dir.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Category display config
CATEGORIES = {
    "eastern": {"icon": "🏯", "name": "東洋占術"},
    "western": {"icon": "🌟", "name": "西洋占術"},
    "maya": {"icon": "🌀", "name": "マヤ系"},
    "animal": {"icon": "🐾", "name": "動物・キャラクター系"},
    "ancient": {"icon": "🏛️", "name": "古代文明系"},
    "symbol": {"icon": "🔮", "name": "シンボル系"},
    "energy": {"icon": "⚡", "name": "エネルギー系"},
    "other": {"icon": "📅", "name": "その他"},
}


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/result", response_class=HTMLResponse)
async def result(
    request: Request,
    date: str = Query(...),
    time: str = Query(None),
    gender: str = Query(None),
    name: str = Query(None),
):
    try:
        birth_date = __import__("datetime").date.fromisoformat(date)
    except ValueError:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": "日付の形式が正しくありません（YYYY-MM-DD）",
        })

    birth_time = None
    if time:
        try:
            birth_time = __import__("datetime").time.fromisoformat(time)
        except ValueError:
            pass

    bd = BirthData(
        birth_date=birth_date,
        birth_time=birth_time,
        gender=gender if gender in ("M", "F") else None,
        name=name or None,
    )

    result = run_all(bd)

    return templates.TemplateResponse("result.html", {
        "request": request,
        "result": result,
        "categories": CATEGORIES,
        "birth_date": date,
        "birth_time": time,
        "gender": gender,
        "name": name,
    })


@app.get("/api/divination")
async def api_divination(
    date: str = Query(...),
    time: str = Query(None),
    gender: str = Query(None),
    name: str = Query(None),
):
    try:
        birth_date = __import__("datetime").date.fromisoformat(date)
    except ValueError:
        return JSONResponse({"error": "Invalid date"}, status_code=400)

    birth_time = None
    if time:
        try:
            birth_time = __import__("datetime").time.fromisoformat(time)
        except ValueError:
            pass

    bd = BirthData(
        birth_date=birth_date,
        birth_time=birth_time,
        gender=gender if gender in ("M", "F") else None,
        name=name or None,
    )

    return JSONResponse(run_all(bd))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
