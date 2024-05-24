from locust import HttpUser, task, between
from faker import Faker
import random
import json
import socketio
import requests

fake = Faker()

# Constants
ENDPOINT = 'http://104.154.206.230/socket.io/'
API_URL = 'http://104.154.206.230/api/message/'
USER_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY2NTBlNWZmYmI2ODM4MzA0MjYyZTZhNyIsImVtYWlsIjoib2t0YXlAZXhhbXBsZS5jb20iLCJpYXQiOjE3MTY1ODE4OTMsImV4cCI6MTcxNjY2ODI5M30.PGV_IzAnfSGL-FJQzvgfpxeodcCYH16lcsFxOoodiLU'
# Active chat and message (predetermined)
active_chat_id = '6650ea92bb6838304262e6f1'  # Replace with the actual chat ID
message = 'yeniyenit'  # Replace with the actual message

# Create a Socket.IO client instance
sio = socketio.Client()

# Define event handlers


@sio.event
def connect():
    print('Connected to server')

    # Once connected, send a message
    send_message_and_emit(active_chat_id, message)


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

    data = send_message(body)
    if data:
        sio.emit('new message', data)
    else:
        print('Failed to send message and emit event')


class RegisterUser(HttpUser):
    wait_time = between(1, 5)  # Wait time between tasks

    @task
    def register_and_send_message(self):

        url = "/api/auth/register"
        headers = {
            "Content-Type": "application/json"
        }
        # Generate random user data
        email = f"{fake.user_name()}{random.randint(1000, 9999)}@example.com"
        payload = {
            "firstname": fake.first_name(),
            "lastname": fake.last_name(),
            "email": email,
            "password": "password"
        }
        response = self.client.post(url, json=payload, headers=headers)
        token = ""
        if not sio.connected:
            sio.connect(ENDPOINT)
        if response.status_code == 200:
            print(f"Registered {email}")
            token = response.json().get("token")
            url = "/api/user"
            headers = {
                "Authorization": f"Bearer {token}",
            }
            response = self.client.get(url, headers=headers)
            if response.status_code == 200:
                jsonArr = response.json()
                for _ in range(10):
                    random_index = random.randint(0, len(jsonArr) - 1)
                    targetID = jsonArr[random_index]["_id"]
                    url = "/api/chat"
                    headers = {
                        "Authorization": f"Bearer {token}",
                        "Content-Type": "application/json",
                    }
                    body = {
                        "userId": targetID
                    }
                    response = self.client.post(
                        url, headers=headers, data=json.dumps(body))
                    if response.status_code == 200:
                        chatID = response.json()[0]['_id']
                        print(f"Created chat with {targetID}")
                        print(f"Chat ID with {chatID}")
                        for i in range(10):
                            message = str(i)
                            send_message_and_emit(chatID, message)
                        print("Messages sent")


if __name__ == "__main__":
    import os
    os.system("locust -f locustfile.py")
