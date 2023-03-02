from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
# Add Database
#Old SQLite Database config
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
#New MySql Database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:8349458001@localhost/our_users'
# Secret Key!
app.config['SECRET_KEY'] = "Secret Key"
# Initialize The Database
db = SQLAlchemy(app)

# Create Models
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Name %r>' % self.name

# Create a user form
# Create a form class
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])

    submit = SubmitField("Submit")


# Create a form class
class NamerForm(FlaskForm):
    name = StringField("What's your name?", validators=[DataRequired()])
    submit = SubmitField("Submit")


@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    our_users = Users.query.order_by(Users.id) # Move this line before the if block
    # Validate Form
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ""
        form.email.data = ""
        flash("User added successfully!")
        # Update the list of users after adding a new user
        our_users = Users.query.order_by(Users.id)
    return render_template("add_user.html",
                           form=form,
                           name=name,
                           our_users=our_users)


@app.route('/')
def index():
    first_name = "John"
    python_list = ["apple", "banana", "grapes", "oranges", "kiwi", 45]
    return render_template("index.html", first_name=first_name, python_list=python_list)


@app.route('/user/<name>')
def user(name):
    return render_template("user.html", user_name=name)


# Create custom error pages

# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


# Internal server Error URL
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500


# Create a name page
@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = NamerForm()
    # Validate Form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ""
        flash("Form submitted successfully!")
    return render_template('name.html',
                           name=name,
                           form=form
                           )


if __name__ == "__main__":
    app.run(debug=True)
