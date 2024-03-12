
from functools import wraps
from flask import Flask, redirect, render_template, url_for,flash
from flask_login import current_user
from flask import Flask
from flask_login import LoginManager
from flask_restful import Api
from MysqlModels.models import Operator, db
from flask_restful import Api
app = Flask(__name__)
api=Api(app)

app.secret_key = 'Windows.omar1.2000'

# Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(operatorID):
    return Operator.query.get(int(operatorID))

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/ipsattendacne'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.roleID != 1:
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function