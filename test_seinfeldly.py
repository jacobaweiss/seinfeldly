import os
import seinfeldly
import url_encoder
import unittest
import tempfile

class UrlpyTestCase(unittest.TestCase):
    def setUp(self):
        self.db_fd, seinfeldly.app.config['DATABASE'] = tempfile.mkstemp()
        seinfeldly.app.config['TESTING'] = True
        self.app = seinfeldly.app.test_client()

        with seinfeldly.app.app_context():
            seinfeldly.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(seinfeldly.app.config['DATABASE'])

    def post(self, long):
        return self.app.post('/add', data={'long': long})

    def test_homepage(self):
        """The homepage allows users to enter a link to be shortened."""
        rv = self.app.get('/')
        assert 'Enter your url here' in rv.data

    def test_create_shortlink(self):
        """Posting a url returns the created shortlink."""
        rv = self.post('https://www.seinfeld.com')
        assert 'localhost:5000/TheStakeOut is now short for https://www.seinfeld.com' in rv.data

    def test_redirects_shortlink(self):
        """Visiting a shortlink redirects to its corresponding long url."""
        rv = self.post('https://www.seinfeld.com')
        assert 'localhost:5000/TheStakeOut is now short for https://www.seinfeld.com' in rv.data
        rv = self.app.get('/TheStakeOut')
        assert rv.status_code == 302
        assert rv.location == 'https://www.seinfeld.com'

    def test_missing_shortlink(self):
        """Visiting a nonexistent shortlink presents a link not found error."""
        rv = self.app.get('/TheStakeOut')
        assert 'No url found' in rv.data

class UrlEncoderTestCase(unittest.TestCase):
    def test_encode(self):
        """It encodes a number into a base 62 shortlink."""
        assert url_encoder.encode(1) == 'TheStakeOut'
        assert url_encoder.encode(800) == 'TheStockTip-TheSeven'
        assert url_encoder.encode(99999) == 'MaleUnbonding-TheConversion-TheAndreaDoria'

    def test_decode(self):
        """It decodes a shortlink id into a url."""
        assert url_encoder.decode('TheStakeOut') == 1
        assert url_encoder.decode('TheStockTip-TheSeven') == 800
        assert url_encoder.decode('MaleUnbonding-TheConversion-TheAndreaDoria') == 99999

if __name__ == '__main__':
    unittest.main()