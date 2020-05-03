import os

from flask import Flask


#L'usine à applications (application factory en anglais),Au lieu de créer un instance globale de la classe Flask, vous allez la créer dans une fonction
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    #indique à l’application que les fichiers de configuration sont relatifs au répertoire instance folder. 
    #Ce répertoire est localisé en dehors du package flaskr et peut contenir des données locales qui ne doivent pas être intégrées au contrôle de version, comme les secrets utilisés dans la configuration et le fichier contenant la base de données.

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        #remplace le configuration par défaut avec des paramètres spécifiés dans le fichier config.py qui se trouve dans l”instance folder
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    
    #Import de notre propre fichier db.py dercirvant la base de donnees    
    from . import db
    db.init_app(app)    

    #Import de notre propre fichier auth.py decrivant les fonctionnalités d'autehntification    
    from . import auth
    app.register_blueprint(auth.bp)#Une classe Blueprint est une façon d’organiser un groupe de vues liées et du code associé. 

    #Import de notre propre fichier blog.py decrivant les fonctionnalités du blog    
    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index') #url_for('index') que url_for('blog.index') fonctionnent et génèrent toutes les deux l’URL 


    #Import de notre propre fichier 
    from . import calcul
    app.register_blueprint(calcul.bp)

    #Import de notre propre fichier 
    from . import formulaire
    app.register_blueprint(formulaire
        .bp)
    return app