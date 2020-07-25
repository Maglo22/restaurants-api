import functools
from os import name
from sqlite3.dbapi2 import Statement

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from werkzeug.exceptions import abort
from api.db import get_db

bp = Blueprint('api', __name__, url_prefix='/api')

# Retrieve all restaurants in db
@bp.route('/restaurants', methods=['GET'])
def get_restaurants():
    db = get_db()
    all_restaurants = []

    cur = db.execute('select * from restaurant;')
    columns = [column[0] for column in cur.description]
    rows = cur.fetchall()

    for row in rows:
        all_restaurants.append(dict(zip(columns, row)))

    return jsonify(all_restaurants)


# add a new restaurant to db
@bp.route('/restaurants/add', methods=['POST'])
def create():
    name = request.args['name']
    phone = request.args['phone']
    email = request.args['email']
    city = request.args['city']
    state = request.args['state']
    street = request.args['street']
    site = request.args['site']
    lat = request.args['lat']
    lng = request.args['lang']

    id = 'something random'
    rating = 0

    db = get_db()
    db.execute(
        """
        insert into restaurant(id, rating, name, site, email, phone, street, city, state, lat, lng)
        values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """,
        (id, rating, name, site, email, phone, street, city, state, lat, lng)
    )
    db.commit()

    return 'Restaurant added.'


# check if restaurant exists
def get_restaurant(id):
    restaurant = get_db().execute(
        """
        select name, phone, email, city, state, street, site, lat, lng
        from restaurant
        where id = ?;
        """,
        (id)
    ).fetchone()

    return restaurant


# update restaurant in db
@bp.route('restaurants/update', methods=['POST'])
def update():
    if 'id' not in request.args:
        return 'No id specified.'

    restaurant = get_restaurant(request.args['id'])

    if restaurant is None:
        return 'Restaurant not found.'

    name = request.args['name']
    phone = request.args['phone']
    email = request.args['email']
    city = request.args['city']
    state = request.args['state']
    street = request.args['street']
    site = request.args['site']
    lat = request.args['lat']
    lng = request.args['lang']

    db = get_db()
    db.execute(
        """
        update restaurant set name = ?, phone = ?, email = ?,
        city = ?, state = ?, street = ?, site = ?, lat = ?, lng = ?
        where id = ?
        """,
        (name, phone, email, phone, city, state, street, site, lat, lng, id)
    )
    db.commit()

    return 'Restaurant updated.'


# delete restaurant from db
@bp.route('/restaurants/delete', methods=['POST'])
def delete():
    if 'id' not in request.args:
        return 'No id specified.'

    restaurant = get_restaurant(request.args['id'])

    if restaurant is None:
        return 'Restaurant not found.'

    db = get_db()
    db.execute('DELETE FROM restaurant WHERE id = ?', (request.args['id']))
    db.commit()

    return 'Restaurant deleted.'
