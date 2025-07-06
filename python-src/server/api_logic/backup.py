import uvicorn # Async API Server
from pydantic import BaseModel # DB Models
from fastapi import FastAPI, UploadFile, Form  # Simple But Robust Enterprise API Server
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles

from typing import Dict
import shutil
import json
import os
#|| Define App & Database
app = FastAPI()
app.mount("/img", StaticFiles(directory="templates/img"), name="img")
templates = Jinja2Templates(directory="templates") #|| Jinja2 Bitch
database: Dict[str, Dict] = {}

database_path = "database_save/"
IMAGE_FOLDER = database_path + "images"
os.makedirs(database_path, exist_ok=True)
os.makedirs(IMAGE_FOLDER, exist_ok=True)

def load_database():
    global database
    if os.path.exists(database_path + "database.json"):
        with open(database_path + "database.json", "r", encoding="utf-8") as f:
            database = json.load(f)
            print("Loaded Data")
def save_database():
    with open(database_path + "database.json", "w", encoding="utf-8") as f:
            json.dump(database, f, indent=4)
            print("Saved Data")    

load_database()
save_database()




class BattleStats(BaseModel):
    wins: int
    deaths: int

##
@app.post("/submit_tank/")
async def submit_tank(
    tank_id: str =      Form(...),
    image: UploadFile = Form(...),
    wins: int =         Form(...),
    deaths: int =       Form(...)
):
    # Save image to disk
    image_path = os.path.join(IMAGE_FOLDER, f"{tank_id}.png")
    with open(image_path, "wb") as f:
        shutil.copyfileobj(image.file, f)

    # Save data to in-memory database
    database[tank_id] = {
        "image": image_path,
        "battle-stats": {
            "wins": wins,
            "deaths": deaths
        }
    }

    save_database()

    return {"message": "Tank data stored", "tank_id": tank_id}


@app.get("/get_stats/{tank_id}")
def get_stats(tank_id: str):
    if tank_id not in database:
        return JSONResponse(status_code=404, content={"error": "Tank not found"})
    return database[tank_id]["battle-stats"]






@app.get("/get_image/{tank_id}")
def get_image(tank_id: str):
    if tank_id not in database:
        return JSONResponse(status_code=404, content={"error": "Tank not found"})
    return FileResponse(database[tank_id]["image"], media_type="image/png")


# @app.get("/tank_card")
# def get_stats():
#     return HTMLResponse(stats_content)
# @app.get("/gdc_2025_leaderboard")
# def get_stats():
#     return HTMLResponse(stats_content)





@app.get("/tank_card", response_class=HTMLResponse)
async def get_tank_card(request: Request, tank_id: str):
    if tank_id not in database:
        return HTMLResponse("<div>Tank not found</div>", status_code=404)

    tank = database[tank_id]
    return templates.TemplateResponse("tank_card.html", {
        "request": request,
        "tank_id": tank_id,
        "wins": tank["battle-stats"]["wins"],
        "deaths": tank["battle-stats"]["deaths"]
    })


@app.get("/view_tank/img/mcdp.gif ")
async def get_mcdp_profile_picture(tank_id: str, request: Request):
    return FileResponse("templates/img/mcdp.gif", media_type="image/png")

@app.get("/view_tank/{tank_id}", response_class=HTMLResponse)
async def get_view_tank_id(tank_id: str, request: Request):
    if tank_id not in database:
        return JSONResponse(status_code=404, content={"error": "Tank not found"})

    return templates.TemplateResponse("view_tank.html", {
        "request": request,
        "tank_id": tank_id
    })


@app.get("/view_leaderboard", response_class=HTMLResponse)
async def get_view_leaderboard(request: Request):
    tank_cards = []

    for tank_id, data in database.items():
        tank_cards.append(
            templates.get_template("tank_card.html").render({
                "request": request,
                "tank_id": tank_id,
                "wins": data["battle-stats"]["wins"],
                "deaths": data["battle-stats"]["deaths"]
            })
        )

    # Combine all cards into a single HTML string inside a wrapper template
    return HTMLResponse(
        content=templates.get_template("view_leaderboard.html").render({
            "request": request,
            "cards": tank_cards
        }),
        status_code=200
    )

#||| Jinja Example - Much Nicer
# @app.get("/tank_card", response_class=HTMLResponse)
# async def tank_card(request: Request):
#     # Ideally load real tank data here
#     return templates.TemplateResponse("tankcard.html", {"request": request})



#
@app.get("/get_image/{player_id}")
def get_image(player_id: str):
    if player_id not in database:
        return JSONResponse(status_code=404, content={"error": "Tank not found"})
    return FileResponse(database[player_id]["image"], media_type="image/png")