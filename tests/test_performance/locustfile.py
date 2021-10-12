from locust import HttpUser, task


class ProjectPerfTest(HttpUser):

    
    def on_start(self):
        self.client.post('/login', {'email': 'john@simplylift.co'})

    def on_stop(self):
        self.client.get('/logout')

    @task
    def purchase_with_update_points_club_and_nb_places(self):
        
        response = self.client.post('/purchasePlaces',
                         {'competition': 'Spring Festival',
                          'club': 'Simply Lift',
                          'places': '2'})
        print(response.text)
