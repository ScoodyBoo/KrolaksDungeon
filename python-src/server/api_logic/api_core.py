# Simple But Robust Enterprise API Server from FastAPI Server
from fastapi import FastAPI, UploadFile, Form, WebSocket
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
import json
import sys
import os
import logging
from typing import Dict, List

PORT = 8426
HOST_IP = "127.0.0.1"
URL = f"http://{HOST_IP}:{PORT}"



#|| API SETUP / DEFINE API ||#
#> Define App & Database
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
            logging.info("Loaded Data")
def save_database():
    with open(database_path + "database.json", "w", encoding="utf-8") as f:
            json.dump(database, f, indent=4)
            logging.info("Saved Data")    

load_database()
save_database()

# WebSocket Management
connected_websockets: List[WebSocket] = []
active_connections: List[Dict] = []

async def ws_send(websocket: WebSocket, message: str):
    await websocket.send_text(message)

async def ws_receive(websocket: WebSocket) -> str:
    return await websocket.receive_text()

async def send_to_all(message: str):
    for websocket in connected_websockets:
        await ws_send(websocket, message)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_websockets.append(websocket)
    client_host = websocket.client.host
    client_port = websocket.client.port
    active_connections.append({"host": client_host, "port": client_port})
    try:
        while True:
            data = await ws_receive(websocket)
            await ws_send(websocket, f"Message text was: {data}")
            logging.info(f"Received from client: {data}")    
    
    except Exception as e:
        logging.error(f"WebSocket error: {e}")
    finally:
        connected_websockets.remove(websocket)
        active_connections.remove({"host": client_host, "port": client_port})
        await websocket.close()



#|| POST, GET, API FUNCTIONALITY ||#

@app.post("/submit_register/")
async def submit_register(
    username: str =         Form(...),
    passcode: str =         Form(...),
    email: str =            Form(...) ):
     
    #| If user already Exists, Log Them In
    if username in database:
        if database[username]["online"]:
            return {"message": "Account Already Online!", "username": username}
        else:
            return {"message": "Account Already Exists!", "username": username}
        
    #| Otherwise, register the new user
    else:
        database[username] = {
            "online":False,
            "user_data": {
                "username" : username,
                "passcode": passcode,
                "email": email,
            }
        }
        save_database()
        return {"message": "Registration Successful!", "username": username}

@app.post("/submit_login/")
async def submit_login(
    username: str =         Form(...),
    passcode: str =         Form(...) ):
     
    #| If user already Exists, Log Them In
    if username in database:
        if database[username]["user_data"]["passcode"] == passcode:
            if database[username]["online"]:
                return {"message": "Account Already Online!", "username": username}
            else:
                #database[username]["online"] = True
                save_database()
                return {"message": "Logged In!", "username": username}
        else:
            return {"message": "Invalid Passcode!", "username": username}
    else:
        return {"message": "Please Register!", "username": username}











@app.post("/submit_form/")
async def submit_form(
    username: str =      Form(...),
    wins: int =         Form(...),
    deaths: int =       Form(...) ):
    #> Save data to in-memory database
    database[username]["battle-stats"] = {
        "wins": wins,
        "deaths": deaths
    }
    save_database()

    return {"message": "Tank data stored", "username": username}


@app.get("/get_stats/{username}")
def get_stats(username: str):
    if username not in database:
        return JSONResponse(status_code=404, content={"error": "User not found"})
    return database[username]["battle-stats"]

@app.get("/connected_clients")
async def get_connected_clients():
    return {"clients": active_connections}

@app.get("/view_connected_players", response_class=HTMLResponse)
async def view_connected_players(request: Request):
    return templates.TemplateResponse("view_connected_players.html", {"request": request})