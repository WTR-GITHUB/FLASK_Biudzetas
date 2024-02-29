import os
from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager
from flask_mail import Message, Mail
from biudzetas import credentials


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__, template_folder="templates")
app.config["SECRET_KEY"] = "4654f5dfadsrfasdr54e6rae"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    basedir, "biudzetas.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = credentials.MAIL_USERNAME
app.config["MAIL_PASSWORD"] = credentials.MAIL_PASSWORD

db = SQLAlchemy(app)
with app.app_context():
    db.create_all()

mail = Mail(app)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "registruotis"
login_manager.login_message_category = "info"

from biudzetas.models.models import Vartotojas, ManoModelView, Irasas

admin = Admin(app)
admin.add_view(ManoModelView(Vartotojas, db.session))
admin.add_view(ModelView(Irasas, db.session))


@login_manager.user_loader
def load_user(vartotojo_id):
    db.create_all()
    return Vartotojas.query.get(int(vartotojo_id))


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message(
        "Slaptažodžio atnaujinimo užklausa",
        sender="el@pastas.lt",
        recipients=[user.el_pastas],
    )
    msg.body = f"""Norėdami atnaujinti slaptažodį, paspauskite nuorodą:
    {url_for('reset_token', token=token, _external=True)}
    Jei jūs nedarėte šios užklausos, nieko nedarykite ir slaptažodis nebus pakeistas.
    """
    print(msg)
    mail.send(msg)


from biudzetas.routes import routes
