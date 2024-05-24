from locust import HttpUser, TaskSet, task, between


class UserBehavior(TaskSet):
    @task
    def post_help(self):
        # Define the payload
        payload = {
            "action": "help",
            "name": "Alper"
        }

        # Send the POST request
        response = self.client.post("/chat-bot", json=payload)

        # Print the response (optional, for debugging purposes)
        print("Status Code:", response.status_code)
        print("Response Body:", response.text)


class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 5)  # Wait time between task executions

    # Set the host
    host = "https://us-central1-alpine-guild-417209.cloudfunctions.net"


if __name__ == "__main__":
    import os
    os.system("locust -f locustfile.py")
