from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    date = db.Column(db.String(100), nullable=False)
    time = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for('index'))
    return render_template('register.html')


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' not in session:
        flash("Please log in to access the dashboard.", "danger")
        return redirect(url_for('index'))
    user_events = Event.query.filter_by(creator_id=session['user_id']).all()
    return render_template('dashboard.html', events=user_events)


@app.route('/create', methods=['GET', 'POST'])
def create():
    if 'user_id' not in session:
        flash("Please log in to create an event.", "danger")
        return redirect(url_for('index'))
    if request.method == 'POST':
        name = request.form['name']
        date = request.form['date']
        time = request.form['time']
        location = request.form['location']
        description = request.form['description']
        event = Event(name=name, date=date, time=time, location=location, description=description, creator_id=session['user_id'])
        db.session.add(event)
        db.session.commit()
        flash("Event created successfully!", "success")
        return redirect(url_for('dashboard'))
    return render_template('create.html')


@app.route('/event/<int:event_id>')
def event_detail(event_id):
    event = Event.query.get(event_id)
    if not event:
        flash("Event not found.", "danger")
        return redirect(url_for('dashboard'))
    return render_template('event_detail.html', event=event)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
