from flask import render_template, jsonify

from cats import app
from cats.models import Cat


@app.route('/')
def index():  # put application's code here
    cats = Cat.query.all()
    return render_template('index.html', cats=cats)


@app.route('/cats/')
def cats():  # put application's code here
    cats = Cat.query.all()
    return jsonify([{cat.id: cat.name} for cat in cats])
