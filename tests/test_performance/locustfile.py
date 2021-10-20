from locust import HttpUser, task


class CompetitionsPerfTest(HttpUser):
    """Performance test on display list competition

    Arguments:
        HttpUser {User} -- for client requests
    """

    def on_start(self):
        self.client.post('/login', {'email': 'john@simplylift.co'})

    def on_stop(self):
        self.client.get('/logout')

    @task
    def display_competitions_list(self):
        self.client.get('/showSummary')


class PointsPerfTest(HttpUser):
    """Performance test on update points while purchase places
        and display points balance.

    Arguments:
        HttpUser {User} -- for client requests
    """

    def on_start(self):
        self.client.post('/login', {'email': 'john@simplylift.co'})

    def on_stop(self):
        self.client.get('/logout')

    @task
    def purchase_with_update_points_club_and_nb_places(self):
        self.client.post('/purchasePlaces',
                         {'competition': 'Spring Festival',
                          'club': 'Simply Lift',
                          'places': '2'})
