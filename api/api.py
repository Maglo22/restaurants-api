from os import name
from sqlite3.dbapi2 import Statement

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from werkzeug.exceptions import abort
from api.db import get_db
import uuid

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
@bp.route('/restaurants/create', methods=['POST'])
def create():
    name = request.json['name']
    phone = request.json['phone']
    email = request.json['email']
    city = request.json['city']
    state = request.json['state']
    street = request.json['street']
    site = request.json['site']
    lat = request.json['lat']
    lng = request.json['lng']

    id = uuid.uuid1()
    rating = 0

    db = get_db()
    db.execute(
        """
        insert into restaurant(id, rating, name, site, email, phone, street, city, state, lat, lng)
        values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """,
        (str(id), rating, name, site, email, phone, street, city, state, lat, lng)
    )
    db.commit()

    response = {
        'status': 'success',
        'message': 'Restaurant added.'
    }

    return jsonify(response)


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
    if 'id' not in request.json:
        response = {
            'status': 'error',
            'message': 'No id specified.'
        }

        return jsonify(response)

    restaurant = get_restaurant(request.json['id'])

    if restaurant is None:
        response = {
            'status': 'error',
            'message': 'Restaurant not found.'
        }

        return jsonify(response)

    name = request.json['name']
    phone = request.json['phone']
    email = request.json['email']
    city = request.json['city']
    state = request.json['state']
    street = request.json['street']
    site = request.json['site']
    lat = request.json['lat']
    lng = request.json['lng']

    db = get_db()
    db.execute(
        """
        update restaurant set name = ?, phone = ?, email = ?,
        city = ?, state = ?, street = ?, site = ?, lat = ?, lng = ?
        where id = ?
        """,
        (name, phone, email, phone, city, state, street, site, lat, lng, request.json['id'])
    )
    db.commit()

    response = {
        'status': 'success',
        'message': 'Restaurant updated.'
    }

    return jsonify(response)


# delete restaurant from db
@bp.route('/restaurants/delete', methods=['POST'])
def delete():
    if 'id' not in request.json:
        response = {
            'status': 'error',
            'message': 'No id specified.'
        }

        return jsonify(response)

    restaurant = get_restaurant(request.json['id'])

    if restaurant is None:
        response = {
            'status': 'error',
            'message': 'Restaurant not found.'
        }

        return jsonify(response)

    db = get_db()
    db.execute('DELETE FROM restaurant WHERE id = ?', (request.json['id']))
    db.commit()

    response = {
        'status': 'success',
        'message': 'Restaurant deleted.'
    }

    return jsonify(response)
