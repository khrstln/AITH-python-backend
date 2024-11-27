from locust import HttpUser, TaskSet, task, between
import random


class UserBehavior(TaskSet):
    @task(1)
    def register_user(self):
        username = random.choice(["test_user_1", "test_user_2", "test_user_3"])
        name = random.choice(["user_1", "user_2", "user_3"])
        self.client.post(
            "/user-register",
            json={
                "username": username,
                "name": name,
                "birthdate": "2000-01-01T00:00:00",
                "password": "password123",
            },
        )

    @task(2)
    def get_user(self):
        username = random.choice([f"test_user_{i}" for i in range(1, 7)])
        self.client.post(
            "/user-get",
            params={"username": username},
            auth=("admin", "superSecretAdminPassword123"),
        )

    @task(1)
    def promote_user(self):
        id = random.randint(1, 7)
        password = random.choice(["superSecretAdminPassword123", "wrongPassword123"])
        self.client.post(
            "/user-promote",
            params={"id": id},
            auth=("admin", password),
        )


class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 1.5)
