import json
from flask import Flask, render_template, abort, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required, current_user
from flask_security.forms import RegisterForm, Required, StringField, LoginForm, get_form_field_label

# sqlalchemy config

app = Flask(__name__)
app.config['SECRET_KEY'] = ''
app.config[
    'SQLALCHEMY_DATABASE_URI'] = ''
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_LOGIN_URL'] = '/acceder'
app.config['SECURITY_LOGOUT_URL'] = '/salir'
app.config['SECURITY_REGISTER_URL'] = '/registrarse'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECURITY_PASSWORD_HASH'] = 'sha512_crypt'
app.config['SECURITY_PASSWORD_SALT'] = ''
app.config['SECURITY_USER_IDENTITY_ATTRIBUTES'] = ('username', 'email')
app.config['SECURITY_SEND_REGISTER_EMAIL'] = False
db = SQLAlchemy(app)


# para crear la db en postgresql por primera vez
# correr "from appfamilia import db > db.create_all()" en consola

# class casa(db.Model):
#     usuario = db.Column(db.String(40), primary_key=True)
#     email = db.Column(db.String(40), unique=True)
#     password = db.Column(db.String(40), unique=False)
#     actividad7 = db.Column(db.String(25), unique=True)
#     actividad14 = db.Column(db.String(25), unique=False)
#     multas = db.Column(db.Integer, unique=False)
#     lista_super = db.Column(db.Text, unique=False)

#     def __init__(self, usuario, email, password, actividad7=None, actividad14=None, multas=None, lista_super=None):
#         self.usuario = usuario
#         self.email = email
#         self.password = password
#         self.actividad7 = actividad7
#         self.actividad14 = actividad14
#         self.multas = multas
#         self.lista_super = lista_super
#
#    def __repr__(self):
#        return '<User %r>' % self.usuario

# Define models
roles_users = db.Table('roles_users', db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, index=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    actividad_7 = db.Column(db.String(255), unique=True)
    actividad_14 = db.Column(db.String(255))
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))


class ExtendedLoginForm(LoginForm):
    email = StringField('Username or Email Address', [Required()])


class ExtendedRegisterForm(RegisterForm):
    username = StringField('Username', [Required()])


# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore, login_form=ExtendedLoginForm, register_form=ExtendedRegisterForm)


# Create a user to test with(run first time only or add manually in postgres)
# @app.before_first_request
# def create_user():
#     db.create_all()
#     # user_datastore.create_user(username='', email='', password='')
#     db.session.commit()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/index.html')
def dashboard():
    return redirect(url_for('index'))


@app.route('/flot.html')
def flot():
    return render_template('flot.html')


@app.route('/morris.html')
def morris():
    return render_template('morris.html')


@app.route('/tables.html')
def tables():
    return render_template('tables.html')


@app.route('/forms.html')
def forms():
    return render_template('forms.html')


@app.route('/panels-wells.html')
def panelswells():
    return render_template('panels-wells.html')


@app.route('/buttons.html')
def buttons():
    return render_template('buttons.html')


@app.route('/notifications.html')
def notifications():
    return render_template('notifications.html')


@app.route('/typography.html')
def typography():
    return render_template('typography.html')


@app.route('/icons.html')
def icons():
    return render_template('icons.html')


@app.route('/grid.html')
def grid():
    return render_template('grid.html')


@app.route('/blank.html')
def blank():
    return render_template('blank.html')


@app.route('/notifications.html')
def notification():
    return render_template('notifications.html')


@app.route('/<user>/perfil')
@login_required
def useractividades(user):
        return render_template('Perfil.html')


@app.route('/pruebasjs')
def pruebasjs():
    return render_template('blank2.html')


@app.route('/AllPages')
def alllayout():
    return render_template('/layouts/AllPages.html')


@app.route('/Actividades')
@login_required
def actividades():
    return render_template('/Actividades.html')


@app.route('/Multas')
@login_required
def multas():
    return render_template('/Multas.html')


@app.route('/Estadisticas')
@login_required
def estadisticas():
    return render_template('/Estadisticas.html')


@app.route('/Lista')
@login_required
def lista():
    return render_template('/Lista.html')


@app.route('/Calendario')
@login_required
def Calendario():
    usuario = User.query.filter_by(username=current_user.username).first()
    return render_template('/Calendario.html', usuario=usuario)


# @app.route('/dbuser')
# def dbactividades():
#     update = User.update().\
#                     where(User.username == current_user.usuario).\
#                     values(actividad_14='holaa!')
#     conn.execute(update)
#     return("base actualizada")

@app.route('/spinact', methods=['POST'])
def dbactividades():
    data7 = request.form['actividad7']
    data14 = request.form['actividad14']
    User.query.filter_by(username=current_user.username).update(dict(actividad_7=data7, actividad_14=data14))
    db.session.commit()
    return(redirect(url_for('actividades')))


@app.route('/json')
def dict2json():
    usuario = User.query.filter_by(username=current_user.username).first()
    print(usuario)
    sampledict = ({'title': 'All Day Event', 'start': '2017-01-01'}, {'title': 'Long Event', 'start': '2017-01-07', 'end': '2017-01-10'})

    with open('JQueryData.json', 'w') as result:
        json.dump(sampledict, result)
    return('', 200)


# error 404 personalizado
# @app.errorhandler(404)
# def page_not_found(e):
#    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=8000)
