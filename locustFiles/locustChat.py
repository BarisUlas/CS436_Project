import base64
from locust import HttpUser, TaskSet, task, between


class PostHelpTaskSet(TaskSet):
    @task
    def post_help(self):
        payload = {
            "action": "help",
            "name": "Alper"
        }
        response = self.client.post("/chat-bot", json=payload)
        print("Post Help - Status Code:", response.status_code)


class BWclass(TaskSet):
    @task
    def send_image(self):
        with open("tadic.jpg", "rb") as f:
            image_data = f.read()
        encoded_image = base64.b64encode(image_data).decode('utf-8')
        payload = {
            "action": "bw",
            "name": "Alper",
            "image": encoded_image
        }
        response = self.client.post("/chat-bot", json=payload)
        print("BW Image - Status Code:", response.status_code)


class gauss(TaskSet):
    @task
    def send_image(self):
        with open("tadic.jpg", "rb") as f:
            image_data = f.read()
        encoded_image = base64.b64encode(image_data).decode('utf-8')
        payload = {
            "action": "blurring",
            "name": "Alper",
            "image": encoded_image
        }
        response = self.client.post("/chat-bot", json=payload)
        print("Blurred Image - Status Code:", response.status_code)


class WebsiteUser(HttpUser):
    wait_time = between(1, 5)
    host = "https://us-central1-alpine-guild-417209.cloudfunctions.net"


class help(WebsiteUser):
    tasks = [PostHelpTaskSet]


class bw(WebsiteUser):
    tasks = [BWclass]


class blur(WebsiteUser):
    tasks = [gauss]
