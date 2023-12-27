from flask import Flask, render_template
from flask_socketio import SocketIO
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import json
import os

app = Flask(__name__, template_folder='web')
socketio = SocketIO(app)

limiter = Limiter(
    app,
    storage_uri="memory://",
    application_limits=["10 per minute"]
)


app.static_folder = 'web/static'

def check_codespaces():
    # Read config.json
    with open('config.json', 'r') as config_file:
        config_data = json.load(config_file)

    # Check if codespaces is true
    if config_data.get('codespaces'):
        print("codespaces is true")
        socketio.emit('codespaces_response', {'status': 'codespacesistrue'})
    else:
        print("codespaces is false")
        socketio.emit('codespaces_response', {'status': 'codespacesisfalse'})


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register/')
def register():
    return render_template('register/index.html')

@app.route('/dashboard/')
def dashboard():
    return render_template('dashboard/index.html')

@socketio.on('whatiscodespaces')
def what_is_codespaces():
    # Check codespaces status and send the response to the client
    check_codespaces()
    return "Codespaces check initiated."

@socketio.on('login')
def handle_login(data):
    # Handle login data (data['username'], data['password'], and data['type'])
    print("Received login data:", data)

    # Create the login_data.json file if it doesn't exist
    if not os.path.isfile('login_data.json'):
        with open('login_data.json', 'w') as file:
            file.write('[]')  # Write an empty JSON array

    # Read existing data from the JSON file
    with open('login_data.json', 'r') as file:
        existing_data = json.load(file)

    # Check if the received data exists in login_data.json
    if any(entry['username'] == data['username'] and entry['password'] == data['password'] for entry in existing_data):
        socketio.emit('login_response', {'status': 'success'})
    else:
        socketio.emit('login_response', {'status': 'failure'})

@socketio.on('register')
def handle_register(data):
    print("Received register data:", data)

    if not os.path.isfile('login_data.json'):
        with open('login_data.json', 'w') as file:
            file.write('[]')

    with open('login_data.json', 'r') as file:
        existing_data = json.load(file)

    # Check if the username already exists
    if any(entry['username'] == data['username'] for entry in existing_data):
        print("Username already exists. Registration failed.")
        socketio.emit('login_response', {'status': 'failure'})
        return
    else:
        existing_data.append(data)

    with open('login_data.json', 'w') as file:
        json.dump(existing_data, file)

    with open('login_data.json', 'r') as file:
        print("Updated login data:", json.load(file))
        socketio.emit('login_response', {'status': 'success'})

if __name__ == '__main__':
    print("Control panel running at http://127.0.0.1:5000")
    socketio.run(app, host='0.0.0.0', port=5000)
