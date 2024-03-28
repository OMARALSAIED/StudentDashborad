from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import generate_password_hash,check_password_hash
from MysqlModels.models import Operator, Role,db
from decorators import app
from sqlalchemy import func, text


Auth = Blueprint('Auth', __name__)

@app.route('/signUp', methods=['POST', 'GET'])
def signup():
    if request.method == "POST":
        if current_user.is_authenticated and current_user.roleID == 1:  # Check if the user is authenticated and has roleID 1
            createBy = current_user.createBy  
        else:
            # Handle the case where the user is not authenticated or doesn't have the required role
            flash("You must be logged in as an admin to sign up", "warning")
            return redirect(url_for('login'))  

        # Assuming you have a mapping of role IDs to role names
        role_names = {
            1: "Admin",
            2: "User",
            # Add more role IDs and their corresponding names as needed
        }

        roleID = request.form.get('roleID')
        role_string = role_names.get(int(roleID), "Unknown")  # Get the role name based on the roleID

        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        user = Operator.query.filter_by(username=username).first()

        if user:
            flash("Username already exists", "warning")
            return render_template('auth/signup.html')  # Redirect to the signup page to provide feedback

        encpassword = generate_password_hash(password)

        # Escape single quote in the username field by doubling it
        username = username.replace("'", "''")

        sql_query = text(f"INSERT INTO `Operator` (`createBy`, `roleID`, `name`, `username`, `password`) VALUES ('{createBy}', '{roleID}', '{name}', '{username}', '{encpassword}')")
      
        new_user = db.session.execute(sql_query)
        db.session.commit()  # Commit the changes to the database
        flash('Sign Up Success. Please Login', "success")
        return render_template('auth/login.html')

    return render_template('auth/signup.html')












# Apply the admin_required decorator to the login route
@app.route('/login', methods=['POST', 'GET'])

def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        user = Operator.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('side'))
        
        flash('Password or Username is not correct', 'danger')
        return redirect(url_for('login'))

    return render_template('auth/login.html')




@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logout Successfully" ,"warning")
    return redirect(url_for('login'))
