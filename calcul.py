from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
import json
from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('calcul', __name__ ) #Contrairement à auth.py pas d'utilisation d'url_prefix


				

@bp.route('/calculette', methods=['GET', 'POST'])
@login_required #=> necessite detre logué pour utiliser la calculette
def calculetteHtml():
	form =  json.loads(json.dumps(request.form))
	if request.method=='POST' and 'msg1' in form.keys() and form['msg1'] is not None:
		resultat = str(calcul(form['msg1'],form['msg2'],form['operateur1']))
		return render_template('calculette/calculette.html',resultat=resultat,form=json.dumps(request.form))
	elif request.method=='POST' and 'msg11' in form.keys() and form['msg11'] is not None:
		#pass dans javascript on fait un preventDefault
		resultat = str(calcul(form['msg11'],form['msg22'],form['operateur2']))
		return render_template('calculette/calculette.html',resultat=resultat,form=json.dumps(request.form))

	else:
		return render_template('calculette/calculette.html',resultat=0)

@bp.route('/api/calculette/<string:a>;<string:operateur>;<string:b>')
def calcul(a,b,operateur='+'):
	if operateur=='*':
		return(str(float(a)*float(b)))
	elif operateur=='-':
		return(str(float(a)-float(b)))
	elif operateur=='+':
		return(str(float(a)+float(b)))
	elif operateur=='/':
		if float(b)!=0:
			return(float(a)/float(b))
		else:
			return(str(None))
	else:
		return(str(None))		
#def calculetteApi(a,b):
#	return str(a+b)