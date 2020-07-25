import sqlite3, csv

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

    with current_app.open_resource('restaurantes.csv', 'r') as f:
        reader = csv.DictReader(f)
        to_db = [(
                    row['id'], row['rating'], row['name'], row['site'],
                    row['email'], row['phone'], row['street'], row['city'],
                    row['state'], row['lat'], row['lng']
                ) for row in reader]

    db.executemany(
        """
        insert into restaurant(id, rating, name, site, email, phone, street, city, state, lat, lng)
        values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """,
        to_db)

    db.commit()


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Database initialized.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)