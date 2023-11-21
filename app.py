"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'ihaveasecret'
app.app_context().push()


connect_db(app)
db.create_all()


@app.route("/") 
def startup_page():
    """Redirect to list of Users."""

    return redirect("/users")

@app.route("/users")
def show_all_users():
     """Show all users including links to more details"""
     users = User.query.order_by(User.last_name, User.first_name).all()
     return render_template('users/index.html', users = users)
     
@app.route("/users/new")
def show_form():
    """Show add form for new users"""
    return render_template('users/new.html')

@app.route("/users/new", methods = ["POST"])
def submit_form():
    """Process the add form, adding a newuser and going back to '/users' """
    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'] or None)

    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")

@app.route("/users/<int:user_id>")
def show_info(user_id):
    """Show information about the given user"""
    user = User.query.get_or_404(user_id)
    return render_template('users/user_detail.html', user=user)

@app.route("/users/<int:user_id>/edit")
def show_edit_form(user_id):
    """Show the edit page for a user including a cancel button"""
    user = User.query.get_or_404(user_id)
    return render_template('users/edit.html', user=user)

@app.route("/users/<int:user_id>/edit", methods=["POST"])
def submit_edit_form(user_id):
    """Process the edit form, returning user to '/users' """
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect("/users")

@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """Delete the user"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")
