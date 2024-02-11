import unittest
from app import create_app
from models import Email, User, db

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()
        
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()
        
    def test_save_emails_endpoint(self):
        response = self.client.post('/save_emails', json={
            'event_id': 1,
            'email_subject': 'Email Subject',
            'email_content': 'Email Body',
            'timestamp': '2022-03-11T10:00'
        })
        data = response.json
        self.assertEqual(response.status_code, 201)
        self.assertIn('message', data)
        self.assertIn('email', data)
        
if __name__ == '__main__':
    unittest.main()