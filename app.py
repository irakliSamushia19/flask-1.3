import base64
import requests as requests
import sentry_sdk
from flask import Flask, redirect, url_for, render_template, request, flash, session
from flask_sqlalchemy import SQLAlchemy
import sqlite3
import requests
from bs4 import BeautifulSoup


app = Flask(__name__)

app.config['SECRET_KEY'] = 'lecture14'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(40), nullable=False)
    gender = db.Column(db.String, nullable=False)
    email = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(30), nullable=False)
    photo = db.Column(db.LargeBinary())

    def __str__(self):
        return f'first_name:{self.first_name}; last_name: {self.last_name}; gender: {self.gender}; email: {self.email}; password: {self.password}'


class Film(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(200), nullable=False)
    title = db.Column(db.String(30), nullable=False)
    year = db.Column(db.Integer(), nullable=False)
    rate = db.Column(db.Float(), nullable=False)


class Watch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    video_name = db.Column(db.String(30), nullable=False)
    url = db.Column(db.String(250), nullable=False)





# db.session.add(Watch(video_name='Top Gun: Maverick', url='https://www.youtube.com/embed/giXco2jaZ_4'))
# db.session.commit()


# item = Watch.query.get(14)
# db.session.delete(item)
# db.session.commit()

@app.route('/')
def log():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():

    if 'email' not in session:
        if request.method == 'POST':
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            gender = request.form.getlist('gender')
            email = request.form['email']
            password = request.form['password']
            file = request.files.get('userimage')
            file = file.read()
            b1 = Person(first_name=first_name, last_name=last_name, gender='male', email=email, password=password, photo=file)
            db.session.add(b1)
            db.session.commit()
            log_password = request.form['log_password']
            log_name = request.form['log_name']

            if log_name == '' or log_password == '':
                flash('შეიყვანეთ ინფორმაცია')
                return render_template('login.html')
            else:
                login = Person.query.filter_by(email=log_name, password=log_password).first()
                if login is None:
                    flash('მომხმარებელი არ არის დარეგისტრირებული')
                    return render_template('login.html')
                else:
                    session['email'] = log_name
                    return redirect(url_for('home'))
            return render_template('login.html')
        return render_template('login.html')
    else:
        return redirect(url_for('home'))


@app.route('/home')
def home():
    if 'email' in session:
        # url = 'https://www.imdb.com/search/title/?groups=top_100'
        # r = requests.get(url)
        # soup_all = BeautifulSoup(r.text, 'html.parser')
        # soup = soup_all.find('div', class_='lister-list')
        # all_movies = soup.find_all('div', class_='lister-item')
        # for each in all_movies:
        #     title = each.h3.a.text
        #     img = each.img.attrs.get('loadlate')
        #     year = each.find('span', class_='lister-item-year').text
        #     year = year.replace('(', '')
        #     year = year.replace(')', '')
        #     imdb = each.strong.text
        #     b2 = Film(image=img, title=title, year=year, rate=imdb)
        #     db.session.add(b2)
        #     db.session.commit()
        films = Film.query.all()
        return render_template('index.html', films=films)


@app.route('/user', methods=['GET', 'POST'] )
def user():
    if 'email' in session:
        person = Person.query.filter_by(email=session['email']).first()
        name = person.first_name
        lastname = person.last_name
        gend = person.gender
        password = person.password
        photo = person.photo
        try:
            base64_images = base64.b64encode(photo).decode("utf-8")
        except:
            base64_images = None
        info = Person.query.filter_by(email=session['email']).first()
        if request.method == 'POST':
            ch_name = request.form.get('ch-name')
            ch_last = request.form.get('ch-last')
            ch_gender = request.form.get('ch-gender')
            ch_password = request.form.get('ch-password')
            info.first_name = ch_name
            info.last_name = ch_last
            info.gender = ch_gender
            info.password = ch_password
            db.session.commit()
            return redirect(url_for('user'))

        return render_template('user.html', name=name, lastname=lastname, gend=gend, password=password, photo=base64_images)


# @app.route('/admin')
# def admin():
#     return redirect('/')


@app.route('/watch', methods=['GET', 'POST'])
def watch():

    if 'email' in session:
        if request.method == 'POST':
            video_name = request.form['find-movie']
            videos = Watch.query.filter_by(video_name=video_name).first()
            url = videos.url
            kino = videos.video_name
            return render_template('watch.html', url=url, kino=kino)
        return render_template('watch.html')


@app.route('/watch/user')
def w():
    return redirect(url_for('user'))



@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('login'))


# conn = sqlite3.connect('user.sqlite')
# cursor = conn.cursor()
# q = "DELETE FROM watch"
# cursor.execute(q)
# conn.commit()

if __name__ == '__main__':
    app.run(debug=True)





















