import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = '12346578'

server_url = "http://172.20.10.7:5500"


@app.route('/', methods=['POST'])
def handle_command():
    data = request.get_json()
    button_value = data['button']
    speed_value = data['speed']
    print(button_value, speed_value)

    url = server_url + "/sendCommand"
    data = {
        "type": button_value,
        "payload": {},
    }
    requests.post(url, json=data)
    return jsonify("Command sent successfuly")


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


if __name__ == '__main__':
    url = server_url + "/connect"
    data = {
        "player_name": "Rahim",
        "ip_address": "172.20.10.6",
    }
    requests.post(url, json=data)
    app.run(debug=True, host="0.0.0.0", port=5600)


