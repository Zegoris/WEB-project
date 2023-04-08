from forms.user import RegisterForm
from forms.login import LoginForm
from forms.settings import SettForm
from data.timer import RepeatTimer
from flask_login import LoginManager, login_user, login_required,\
    logout_user, current_user
from data import db_session
from data.users import User
from data.russian import Russian
from data.foreign import Foreign
from data.mixed import Mixed
from flask import Flask, render_template, redirect, request,\
    make_response, jsonify, abort
from time import strftime
from random import randint, shuffle

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)

db_session.global_init("db/quotes.db")
db_sess = db_session.create_session()


def get_quote():
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == current_user.id).first()
    if user:
        if user.type == 'rus':
            quote = db_sess.query(Russian).filter(Russian.id == User.current_quote).first()
        elif user.type == 'for':
            quote = db_sess.query(Foreign).filter(Foreign.id == User.current_quote).first()
        else:
            quote = db_sess.query(Mixed).filter(Mixed.id == User.current_quote).first()
        if quote:
            return quote


def choice_quote():
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == current_user.id).first()
    if user:
        user.current_quote = randint(1, 100)
        db_sess.commit()


def check():
    try:
        db_sess = db_session.create_session()
        now = strftime("%H:%M")
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        if user:
            if now == f"{user.date}:00":
                choice_quote()
    except AttributeError:
        pass


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


def main():
    RepeatTimer(10, check).start()
    app.run(port=8000, host='127.0.0.1')


@app.route('/')
def index():
    try:
        quote = get_quote()
        return render_template('index.html', title='Homepage', quote=quote)
    except AttributeError:
        return redirect('/login')


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Registration',
                                   form=form,
                                   message="The passwords do not match")
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Registration',
                                   form=form,
                                   message="Such a user already exists")

        user = User(
            email=form.email.data,
            date=form.time.data,
            type=form.type.data,
            current_quote=randint(1, 100)
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Registration', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Incorrect login or password",
                               form=form)
    return render_template('login.html', title='Authorization', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/login")

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def sett():
    form = SettForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        if user:
            form.type.data = user.type
            form.time.data = user.date
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        if user:
            user.date = form.time.data
            user.type = form.type.data
            db_sess.commit()
        else:
            abort(404)
        return redirect('/')
    return render_template('settings.html', title='Settings', form=form)

@app.route('/all')
@login_required
def all_quotes():
    db_sess = db_session.create_session()
    quotes = list(db_sess.query(Mixed).all())
    shuffle(quotes)
    return render_template('all_quotes.html', title='All quotes', quotes=quotes)


if __name__ == '__main__':
    main()
