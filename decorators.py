
from datetime import datetime, timedelta
from functools import wraps
from flask import Flask, jsonify, redirect, request,url_for,flash
from flask_login import current_user
from flask import Flask
from flask_login import LoginManager
from flask_restful import Api
import jwt
from MysqlModels.models import Operator, db
from flask_restful import Api

app = Flask(__name__)
api=Api(app)

My_SECRET_KEY =app.secret_key = 'Windows.omar1.2000'

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


def required_token(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"error": "Token is missing"}), 401
        # Here you can add the logic to validate the token
        # For example, you can decode the token and verify it against your database
        # If the token is invalid, return a response with status code 401 (Unauthorized)
        # If the token is valid, proceed with the original function
        return func(*args, **kwargs)
    return wrapper


TOKEN_EXPIRATION_TIME = timedelta(hours=1)
# Generate token function
def generate_token(cardID):
    try:
        payload = {
            'cardID': cardID,
            'exp': datetime.utcnow() + TOKEN_EXPIRATION_TIME
        }
        token = jwt.encode(payload, My_SECRET_KEY, algorithm='HS256')
        return token
    except Exception as e:
        return str(e)