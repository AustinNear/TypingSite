from flask import Flask, render_template, redirect, url_for, session
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretsecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
Bootstrap(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    wpm = db.relationship('Wpms', backref='user', lazy=True)


class WPMs(db.Model):
    wpmid = db.Column(db.Integer, primary_key=True)
    wpm = db.Column(db.Integer, unique=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')


class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])


db.create_all()


@app.route('/')
def index():
    if session.get("name"):
        return render_template('index.html', name=session["name"])
    return render_template('index.html', name="Guest")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                session["name"] = form.username.data
                return redirect(url_for('index'))

    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data,
                        password=bcrypt.generate_password_hash(form.password.data).decode('UTF-8'))
        db.session.add(new_user)
        db.session.commit()
        return '<h1> New user has been created</h1>'
    return render_template('signup.html', form=form)


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/type')
def type():
    if session.get("name"):
        return render_template('type.html')
    else:
        form = RegisterForm()
        return render_template('login.html', form=form, message=" before accessing the test.")


@app.route('/logout')
def logout():
    if session.get("name"):
        del session["name"]
    return render_template('index.html', name="Guest")


if __name__ == '__main__':
    app.run(debug=True)
