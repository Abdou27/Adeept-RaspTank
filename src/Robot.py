from fastapi import FastAPI
import move

app = FastAPI()
move.setup()


@app.get("/")
def ping():
    return {"status": "up"}


@app.post("/sendCommand")
async def send_command(command: dict):
    print(command)
    cmd_type = command['type']
    if cmd_type in ['forward', 'backward']:
        move.move(100, cmd_type, 'no')
    elif cmd_type in ['left', 'right']:
        move.move(100, 'no', cmd_type)
    elif 'stop' == cmd_type:
        move.motorStop()
    pass
