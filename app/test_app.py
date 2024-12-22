import unittest
from app import app, db, Partner, Material

class TestApp(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_add_partner(self):
        response = self.app.post('/partners', json={'name': 'Partner1', 'email': 'partner1@example.com'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('New partner added!', response.get_data(as_text=True))

    def test_add_material(self):
        partner = Partner(name='Partner1', email='partner1@example.com')
        db.session.add(partner)
        db.session.commit()
        response = self.app.post('/materials', json={'title': 'Material1', 'description': 'Description1', 'partner_id': partner.id})
        self.assertEqual(response.status_code, 200)
        self.assertIn('New material added!', response.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()
