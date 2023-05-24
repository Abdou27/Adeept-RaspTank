from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = '12346578'
socketio = SocketIO(app)


@socketio.on('command')
def handle_command(data):
    button_value = data['button']
    speed_value = data['speed']
    print(button_value, speed_value)

    # Process the command here and send it to the robot server
    # ...


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)
