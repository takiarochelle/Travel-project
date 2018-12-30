import server
import unittest

class FlaskIntegrationTestCase(unittest.TestCase):
    """Test Flask server"""

    def setUp(self):
        app = server.app
        self.client = app.test_client()
        app.config['TESTING'] = True
        server.connect_to_db(app, 'testdb')
        server.db.create_all()


    def test_index(self):
        """Test that homepage is rendering properly"""

        result = self.client.get('/')
        self.assertIn(b'<h1>Tripster</h1>', result.data)


    def test_validate_login(self):
        """Test that a successful login renders users profile page"""

        result = self.client.post('/validate-login', data={'email': 'takia@gmail.com', 
                                                            'password': 'abc123'}, 
                                                            follow_redirects=True)
        self.assertIn(b'Welcome, Takia', result.data)


    def test_validate_user(self):
        """Test creating a new user"""

        result = self.client.post('/validate-user', data={'fname': 'Takia',
                                                            'lname': 'Rudolph',
                                                            'reg-email': 'takia@gmail.com',
                                                            'reg-password': 'abc123',
                                                            'confirm-email': 'takia@gmail.com',
                                                            'confirm-password': 'abc123',
                                                            'reg-username': 'takiaroc5'})
        self.assertNotIn(b'Welcome, Takia', result.data)


    def test_user_profile(self):
        """Test that profile is rendering proper html"""

        with self.client.session_transaction() as sess:
            sess['email'] = 'takia@gmail.com'

        result = self.client.get('/profile/takiaroc5')
        self.assertIn(b'Welcome, Takia', result.data)


    def test_trip_itinerary(self):
        """Test that itinerary page is rendering properly"""

        with self.client.session_transaction() as sess:
            sess['email'] = 'takia@gmail.com'

        result = self.client.get('/barcelona-1')
        self.assertIn(b'Invite Friends', result.data)


if __name__ == '__main__':
    unittest.main()



