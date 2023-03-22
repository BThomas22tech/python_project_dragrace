from school_project import app
from school_project.model.user_model import User
from flask_bcrypt import Bcrypt
from flask import render_template,redirect,session,request,flash


bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template("login.html")

@app.route('/', methods = ['POST'])
def user_added():
    email_data = {
        "email": request.form["email"]
    }
    email_in_db = User.get_by_email(email_data)
    if email_in_db:
        flash("email already in use")
        return redirect('/')
    if not User.validate_user_reg(request.form):
        return redirect('/')
    if request.form['password'] != request.form['confirm_password']:
        flash("Passwords do not match")
        return redirect('/')
    if not User.validate_user_reg(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data ={
            'id':id,
            "first_name": request.form["first_name"],
            "last_name": request.form["last_name"],
            "email": request.form["email"],
            "password": pw_hash
            }
    user_id = User.save(data)
    session['user_id'] = user_id
    return redirect('/states')

@app.route('/login', methods =['POST'])
def login():
    data = {"email": request.form["email"]}
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password")
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect('/states')

@app.route("/log_out")
def log_out():

    session.clear()
    return redirect("/")