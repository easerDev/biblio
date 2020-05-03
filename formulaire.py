from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
import os
import json
from flaskr.auth import login_required
from flaskr.db import get_db
from werkzeug.utils import secure_filename

bp = Blueprint('formulaire', __name__ ) #Contrairement à auth.py pas d'utilisation d'url_prefix

@bp.route('/formulaire', methods=['GET', 'POST'])
@login_required #=> necessite detre logué pour utiliser la calculette
def formulaire():
	form =  json.loads(json.dumps(request.form))
	files =  request.files
	#return(files.fichier)
	if request.method=='POST':
		if 'fichier' in files.keys() and files['fichier'] is not None:
			fichier = files['fichier']
			nom_fichier = fichier.filename
			if nom_fichier[-4:] == '.pdf':
				nom_fichier = secure_filename(nom_fichier)
				#return(str(os.listdir()))
				fichier.save('biblio/uploads/' + nom_fichier)
				print('Fichier copié')
				return render_template('formulaire/formulaire.html')
			else:
				return render_template('formulaire/formulaire.html')
		elif 'msg1' in form.keys() and form['msg1'] is not None:
			return render_template('formulaire/formulaire.html',votreNom=form['msg1'],votreMessage=form['msg2'])		
		else:	
			return render_template('formulaire/formulaire.html')
	else:
		return render_template('formulaire/formulaire.html')