#Une classe Blueprint est une façon d’organiser un groupe de vues liées et du code associé. 
#Plutôt que d’enregistrer les vues et le code associé directement avec une application, elles sont enregistrées à un plan. 
#Ensuite, le plan est enregistré dans l’application dès qu’il est disponible dans la fonction qui contient l’usine à applications.
#https://sites.uclouvain.be/P2SINF/flask/tutorial/views.html

import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth') #Une classe Blueprint est une façon d’organiser un groupe de vues liées et du code associé. 

#Crerr un nouveau compte
@bp.route('/register', methods=('GET', 'POST')) #Lorsque Flask reçoit une requête vers l’URL /auth/register car url_prefix='/auth'
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        #test si utilisateur n'existe pas deja
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None: #fetchone() retourne une ligne de la requête.
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password)) # est utilisée pour calculer un hash du mot de passe et c’est ce hash qui est stocké
            )
            db.commit() #Comme cette requête modifie des données, il ne faut pas oublier d’appeler db.commit() pour sauver les modifications.
            return redirect(url_for('auth.login')) #Après avoir stocké l’information relative à l’utilisateur, celui-ci est redirigé vers la page de login

        flash(error) #Message d'erreur qui pourra etre utiliser dans la vue pour indiquer erreur dans les templates dans l'objet get_flashed_messages()

    return render_template('auth/register.html')

#Se loguer
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone() #fetchone() retourne une ligne de la requête.

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear() #session est un dict qui stocke des données d’une requête à l’autre La donnée est stockée dans un cookie qui est envoyé au navigateur. 
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

#Avant chaque on veirifi que la data g?user est renseigné pour pouvoir utiliser et afficher uniquement les donnees de l'utilisateur par exemple
@bp.before_app_request #enregistre une fonction qui s’exécute avant la fonction « vue », quelle que soit l’URL demandée
def load_logged_in_user():
	#vérifie si l”id de l’utilisateur est stocké dans la session et récupère son information dans la base de données et la stocke dans :data`g.user
    user_id = session.get('user_id')
    #g est directement accessible dans les templates
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

#Se deconnecter
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

#Besoins d’authentification dans d’autres vues
#Cette nouvelle fonction vérifie si un utilisateur est chargé et sinon redirige vers la page de login
#On utilisera ce decorateur selon les vues ou l'authentification est necessaire => from flaskr.auth import login_required
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view