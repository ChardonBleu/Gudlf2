from locust import HttpUser, task

class ProjectPerfTest(HttpUser):
    @task
    def index(self):
        self.client.get('index')
    
    @task
    def login(self):
        self.client.get('login')

