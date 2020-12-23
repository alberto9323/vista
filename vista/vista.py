from flask import Flask, render_template,send_from_directory,session, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_migrate import Migrate
import os
from flask_sqlalchemy import SQLAlchemy
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
bootstrap = Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] =\
'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
class NameForm(FlaskForm):
	name = StringField('What is your name?', validators=[DataRequired()])
	submit = SubmitField('Submit')
class Role(db.Model):
	__tablename__ = 'roles'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), unique=True)
	def __repr__(self):
		return '<Role %r>' % self.name
class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), unique=True, index=True)
	def __repr__(self):
		return '<User %r>' % self.username

@app.route('/',methods=['GET', 'POST'])
def index():
	
	form = NameForm()
	
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.name.data).first()
		if user is None:
			user = User(username=form.name.data)
			db.session.add(user)
			db.session.commit()
			session['known'] = False
		else:
			session['known'] = True
		session['name'] = form.name.data
		form.name.data = ''
		return redirect(url_for('index'))
	return render_template('index.html',form=form, name=session.get('name'),known=session.get('known', False))
"""form=form, name=session.get('name'),
known=session.get('known', False)
	name = form.name.data
	form.name.data = ''
	return render_template('index.html', form=form, name=name)"""
@app.route('/user/<name>')
def user2(name):
	return render_template('user.html',name=name)

@app.route('/frambuesa')
def fruta():
	filename="jitomate.jpg"
	return render_template('fruta.html', filename=filename)

@app.shell_context_processor
def make_shell_context():
	return dict(db=db, User=User, Role=Role)

	
