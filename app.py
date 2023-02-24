from flask import  Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = "Secret Key"

#Ceate a form class
class NamerForm(FlaskForm):
    name = StringField("What's is your name?", validators=[DataRequired()])
    submit = SubmitField("Submit")


@app.route('/')
def index():
    first_name = "John"
    python_list = ["apple", "banana", "grapes", "oranges", "kiwi", 45]
    return render_template("index.html", first_name = first_name, python_list = python_list)

@app.route('/user/<name>')
def user(name):
    return render_template("user.html", user_name = name)




#Create custom error pages

#Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html",), 404

#Internal server Error URL
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html",), 500



#Create a name page
@app.route('/name', methods = ['GET','POST'])
def name():
    name = None
    form = NamerForm()
    #Validae Form
    
    return render_template('name.html',
                           name = name,
                           form = form
                           )
    


if __name__ == "__main__":
    app.run(debug = True)