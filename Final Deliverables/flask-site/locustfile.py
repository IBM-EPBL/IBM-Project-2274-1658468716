from locust import HttpUser, task

class Hive(HttpUser):
    @task
    def logTest(self):
        self.client.get("/login")
        self.client.get("/register")
        self.client.get("/")
        self.client.get("/index")
        self.client.post("/api/upload")
        self.client.get("home/form-upload")
