#https://sites.uclouvain.be/P2SINF/flask/patterns/sqlite3.html#sqlite3
import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

#Se connecter a la db
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

#RAZ de la db
def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:  #open_resource sert juste a faire appel a un chemin relatif
        db.executescript(f.read().decode('utf8'))

#Pour raz de la base par ligne de commande =>Dans le terminal  $ flask init-db
@click.command('init-db')  #définit uns interface en ligne de commande
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    #Ce nest pas une raz ! On ajoute juste deux focntionnalutés a l'app
    app.teardown_appcontext(close_db) #demande à Flask d’appeler cette fonction lorsqu’elle libère les ressources associées à une requête après avoir retourné la réponse
    app.cli.add_command(init_db_command) #ajoute une nouvelle commande qui peut être appelée par la commande flask  