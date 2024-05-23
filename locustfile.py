from locust import HttpUser, task, between
import socketio

ENDPOINT = 'http://localhost:8001'
API_URL = 'http://localhost:8000/api/message/'
USER_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY2NGZiYWM4ZDFlYmMzM2NmNzRlYWI5MyIsImVtYWlsIjoiY3Jhenk3QGdtYWlsLmNvbSIsImlhdCI6MTcxNjUwMTE5MiwiZXhwIjoxNzE2NTg3NTkyfQ.9UNJuEbPlOnq2-f7MduEoBtkon2oFVIiww0oQn39q-M'  # Replace with the actual token

active_chat_id = '664fbaf8d1ebc33cf74eaba7'  # Replace with the actual chat ID
message = 'allo'

sio = socketio.Client()  # Create a Socket.IO client instance outside the class


class MyUser(HttpUser):
    host = "http://localhost:8000"  # Add the base host here
    wait_time = between(1, 5)

    def on_start(self):
        # Set headers including OAuth2 token
        self.headers = {
            "Authorization": f"Bearer {USER_TOKEN}",
            "Content-Type": "application/json"
        }

    @task
    def send_message(self):
        # Define the request payload
        payload = {
            "chatId": active_chat_id,
            "message": message
        }
        response = self.client.post(
            "/api/message", json=payload, headers=self.headers)

        # Emit the message if the response is successful
        if response.status_code == 200:
            sio.emit('new message', payload)

# Define event handlers or further Socket.IO configuration here


sio.connect(ENDPOINT)  # Connect the Socket.IO client to the server
