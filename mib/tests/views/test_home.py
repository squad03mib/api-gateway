from .view_test import ViewTest
from faker import Faker


class TestHome(ViewTest):
    faker = Faker()

    BASE_URl = 'http://localhost'

    @classmethod
    def setUpClass(cls):
        super(TestHome, cls).setUpClass()

    def test_home(self):
        rv = self.client.get(self.BASE_URL+'/')
        print(rv)
        assert rv.status_code == 200

    def test_user_info(self):
        self.login_test_user()

        reply = self.app.get("/userinfo")
        self.assertIn(b'Profile', reply.data)

        reply = self.app.post("/userinfo", data=dict(
            email='new_' + self.sender,
            firstname='Prova_new',
            lastname='Prova_new',
            password='',
            date_of_birth='2001-01-01'
        ))
        self.assertIn(b"Prova_new", reply.data)

        reply = self.app.post("/userinfo", data=dict(
            email='new_' + self.sender,
            firstname='Prova_new',
            lastname='Prova_new',
            password='12345',
            date_of_birth='2001-01-01'
        ))

