import os
import tempfile
import unittest

from cats import app, db
from cats.models import Cat


class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.db_uri = 'sqlite:///' + os.path.join('../.testdb.db')
        app.config['TESTING'] = True
        # app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = self.db_uri
        self.app = app.test_client()
        with app.app_context():
            db.create_all()
            db.session.commit()

        self.cat_name = 'Bars'

    def tearDown(self):
        """Очистка БД после тестов."""
        with app.app_context():
            db.drop_all()

    def _add_cat(self, name):
        """Добавление кота."""
        with app.app_context():
            cat = Cat(name=name)
            db.session.add(cat)
            db.session.commit()

    def test_index(self):
        """Проверка шаблона."""
        self._add_cat(self.cat_name)

        response = self.app.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertIn(self.cat_name, str(response.data))

    def test_cats(self):
        self._add_cat(self.cat_name)

        response = self.app.get('/cats/')

        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertIn(self.cat_name, data[0].values())

