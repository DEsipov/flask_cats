from flask import render_template, jsonify, request

from cats import app, db
from cats.models import Cat


@app.route('/')
def index():
    cats = Cat.query.all()
    return render_template('index.html', cats=cats)


@app.route('/cats/')
def cats():
    cats = Cat.query.all()
    return jsonify([{cat.id: cat.name} for cat in cats])


@app.route('/cats/<int:id>/')
# Параметром указывается имя переменной:
def cat_detail(id):
    cat = Cat.query.first_or_404(id)
    return jsonify({'id': cat.id, 'name': cat.name})


@app.route('/cats/', methods=['POST'])
def create_cat():
    data = request.json
    cat = Cat(**data)
    db.session.add(cat)
    db.session.commit()

    return jsonify({'id': cat.id, 'name': cat.name}), 201
