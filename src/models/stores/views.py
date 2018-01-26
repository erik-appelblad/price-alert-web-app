from flask import Blueprint, render_template, url_for, request, redirect

import json

from src.models.stores.store import Store

store_blueprint = Blueprint('stores', __name__)

@store_blueprint.route('/store/<string:store_id>')
def store_page(store_id):
    store = Store.get_by_id(store_id)
    return render_template("stores/store.html", store=store)


@store_blueprint.route('/')
def index():
    stores = Store.all()
    return render_template("stores/store_index.html", stores=stores)


@store_blueprint.route('/new', methods=['GET', 'POST'])
def create_store():
    if request.method == 'POST':
        name = request.form['name']
        tag_name = request.form['tag_name']
        url_prefix = request.form['url_prefix']
        query = json.loads(request.form['query'])

        Store(name, url_prefix, tag_name, query).save_to_db()

        return redirect(url_for('.index'))

    return render_template("stores/create_store.html")

@store_blueprint.route('/edit/<string:store_id>', methods=['GET', 'POST'])
def edit_store(store_id):
    if request.method == 'POST':
        pass
    return "you made edit"

@store_blueprint.route('/delete/<string:store_id>')
def delete_store(store_id):
    store = Store.get_by_id(store_id)
    return render_template("stores/store.html", store=store)