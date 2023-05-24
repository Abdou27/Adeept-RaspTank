import random
import threading
import time

import requests
from fastapi import FastAPI, Request, HTTPException

app = FastAPI()
player_ips = {}
connected_players = {}
robots = {}
bonus_points = {}
blocked = {}


@app.get("/")
def ping():
    return {"status": "up"}


@app.post("/connect")
async def connect(player_info: dict, request: Request):
    sender_ip = request.client.host  # Retrieve the IP address of the sender
    player_name = player_info["player_name"]
    robot_ip = player_info["ip_address"]

    if sender_ip in connected_players:
        return {"message": "Already connected with this IP"}
    if player_name in player_ips:
        return {"message": "This name is already taken"}
    if robot_ip in robots.values():
        return {"message": "This robot ip is already taken"}

    player_ips[player_name] = sender_ip
    connected_players[sender_ip] = player_name
    robots[sender_ip] = robot_ip
    bonus_points[sender_ip] = 0  # Initialise les points bonus du joueur à 0
    blocked[sender_ip] = False

    threading.Thread(target=try_giving_bonus, args=(sender_ip,), daemon=True).start()

    return {"message": "Connected successfully"}


def try_giving_bonus(sender_ip):
    player_name = connected_players[sender_ip]
    while sender_ip in connected_players:
        if random.random() < 1/4:
            bonus_points[sender_ip] += 1
            print(f"Gave {player_name} a bonus!")
        time.sleep(10)


@app.get("/getList")
async def get_list():
    return {"data": list(connected_players.values())}


@app.post("/sendCommand")
async def send_command(command: dict, request: Request):
    sender_ip = request.client.host  # Retrieve the IP address of the sender
    if sender_ip not in connected_players:
        return {"message": "Command sent successfully"}
    robot_ip = robots[sender_ip]
    await route_command(command, robot_ip)
    return {"message": "Command sent successfully"}


async def route_command(command: dict, robot_ip: str):
    command_type = command["type"]
    payload = command["payload"]
    url = f"http://{robot_ip}:5400/sendCommand"
    data = {
        "type": command_type,
        "payload": payload,
    }
    requests.post(url, json=data)


@app.get("/account")
async def get_account(request: Request):
    sender_ip = request.client.host  # Retrieve the IP address of the sender
    return {"data": bonus_points.get(sender_ip, 0)}


@app.post("/sendPenalty")
async def send_penalty(player_info: dict, request: Request):
    sender_ip = request.client.host  # Retrieve the IP address of the sender
    if bonus_points.get(sender_ip, 0) <= 0:
        raise HTTPException(status_code=400, detail="Penalty not applied: no bonus points")
    target_name = player_info["player"]
    target_ip = player_ips.get(target_name, None)
    if target_ip is None:
        raise HTTPException(status_code=400, detail="Penalty not applied: player doesn't exist")
    bonus_points[sender_ip] -= 1
    threading.Thread(target=block_player, args=(target_ip,), daemon=True).start()
    return {"message": "Penalty applied successfully"}


def block_player(target_ip):
    blocked[target_ip] = True
    time.sleep(3)
    blocked[target_ip] = False
