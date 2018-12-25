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


if __name__ == '__main__':
    unittest.main()