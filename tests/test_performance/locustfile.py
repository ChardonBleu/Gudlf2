from locust import HttpUser, task

class ProjectPerfTest(HttpUser):
    @task
    def index(self):
        self.client.get('index')
    
    @task
    def login(self):
        self.client.get('login')
        self.client.post('login', {'email': 'club_test1_name'})
    
    @task
    def welcome(self):
        self.client.post('login', {'email': 'club_test1_name'})
        self.client.get('welcome')
    
    @task
    def competitions(self):
        self.client.post('login', {'email': 'club_test1_name'})
        self.client.get('showSummary')
    
    @task
    def book(self):
        self.client.post('login', {'email': 'club_test1_name'})
        self.client.get('book/<competition_name>/<club_name>')
    
    @task
    def purchase_with_update_points_club_and_nb_places(self):
        self.client.post('login', {'email': 'club_test1_name'})
        response = self.client.post('purchasePlaces',
                         {'competition': 'Compet du printemps',
                          'club': 'club_test1_name',
                          'places': '2'})
        print("Response status code:", response.status_code)
        print("Response text:", response.text)
