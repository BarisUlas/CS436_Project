from locust import User, task, between
import socketio
import requests

# Constants
ENDPOINT = 'http://localhost:8001'
API_URL = 'http://localhost:8000/api/message/'
USER_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY2NGZiYWM4ZDFlYmMzM2NmNzRlYWI5MyIsImVtYWlsIjoiY3Jhenk3QGdtYWlsLmNvbSIsImlhdCI6MTcxNjUwMTE5MiwiZXhwIjoxNzE2NTg3NTkyfQ.9UNJuEbPlOnq2-f7MduEoBtkon2oFVIiww0oQn39q-M'  # Replace with the actual token

# Active chat and message (predetermined)
active_chat_id = '664fbaf8d1ebc33cf74eaba7'  # Replace with the actual chat ID
mesq = 'yeniyenit'  # Replace with the actual message

# Create a Socket.IO client instance
sio = socketio.Client()

# Define event handlers


@sio.event
def connect():
    print('Connected to server')

    # Once connected, send a message
    send_message_and_emit(active_chat_id, mesq)


@sio.event
def disconnect():
    print('Disconnected from server')


def send_message(body):
    """
    Send a message using an HTTP POST request.
    """
    try:
        headers = {'Authorization': f'Bearer {USER_TOKEN}'}
        response = requests.post(API_URL, json=body, headers=headers)
        response.raise_for_status()  # Raise an HTTPError on bad responses
        return response.json()
    except requests.RequestException as error:
        print(f'Error in send_message API: {error}')
        return None


def send_message_and_emit(chat_id, message):
    """
    Send a message to the server and emit the 'new message' event.
    """
    body = {'chatId': chat_id, 'message': message}

    # Debug: Check the body dictionary
    print(f'body: {body}')

    data = send_message(body)
    if data:
        sio.emit('new message', data)
        print("After Emit")
    else:
        print('Failed to send message and emit event')


class MyUser(User):
    wait_time = between(1, 5)

    @task
    def send_message_task(self):
        # Connect to the server if not connected
        if not sio.connected:
            sio.connect(ENDPOINT)

        # Perform the task here
        send_message_and_emit(active_chat_id, mesq)

    def on_stop(self):
        # Disconnect from the server when the test stops
        if sio.connected:
            sio.disconnect()
