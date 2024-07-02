import json
import os
import tempfile
import unittest

from cats import app, db
from cats.models import Cat


class CatsTestCase(unittest.TestCase):
    """Тестирование котов."""

    def setUp(self):
        self.db_uri = 'sqlite:///' + os.path.join('../.testdb.db')
        app.config['TESTING'] = True
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

    def _get_cat(self, **kwargs):
        with app.app_context():
            cat = Cat.query.filter_by(**kwargs).first()
            return cat

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

    def test_cat_detail(self):
        self._add_cat(self.cat_name)
        cat = self._get_cat(name=self.cat_name)

        response = self.app.get(f'/cats/{cat.id}/')

        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertEqual(data.get('id'), cat.id)

    def test_add_cat(self):
        data = {'name': self.cat_name}

        response = self.app.post(
            f'/cats/',
            data=json.dumps(data),
            content_type='application/json')

        self.assertEqual(response.status_code, 201)
        data = response.json
        self.assertEqual(data.get('name'), self.cat_name)
