from datetime import datetime, timedelta, timezone
from sqlalchemy import or_, text
from decorators import My_SECRET_KEY, generate_token
from flask import Blueprint ,request
from flask_restful import Resource, reqparse, marshal_with, fields
from MysqlModels.models import Student,db


User_Auth = Blueprint('User_Auth', __name__)

SECRET_KEY = My_SECRET_KEY

# Define the expiration time for the token (e.g., 1 hour)
TOKEN_EXPIRATION_TIME = timedelta(hours=1)

# Define a parser for parsing request arguments
student_parser = reqparse.RequestParser()
# Add arguments for student creation here
student_parser.add_argument('operatorID', type=int)
student_parser.add_argument('departmentID', type=int)
student_parser.add_argument('cardID', type=str)
student_parser.add_argument('nationalID', type=str)
student_parser.add_argument('gender', type=str)
student_parser.add_argument('fullname', type=str)
student_parser.add_argument('DateOfBirth', type=str)
student_parser.add_argument('enrollmentDate', type=str)
student_parser.add_argument('phoneNumber', type=str)
student_parser.add_argument('address', type=str)
student_parser.add_argument('MAC', type=str)
student_parser.add_argument('email', type=str)
student_parser.add_argument('password', type=str)



student_fields = {
    'studentID': fields.Integer,
    'operatorID': fields.Integer,
    'departmentID': fields.Integer,
    'creationDate': fields.DateTime(dt_format='iso8601'),
    'cardID': fields.String,
    'nationalID': fields.String,
    'gender': fields.String,
    'fullname': fields.String,
    'DateOfBirth': fields.DateTime(dt_format='iso8601'),
    'enrollmentDate': fields.DateTime(dt_format='iso8601'),
    'phoneNumber': fields.String,
    'address': fields.String,
    'MAC': fields.String,
    'email': fields.String,
    'password': fields.String,
    'deleted': fields.Boolean
}


class StudentResource(Resource):
    @marshal_with(student_fields)
    def get(self, student_id):
        student = Student.query.get_or_404(student_id)
        return student

    @marshal_with(student_fields)
    def post(self):
        args = student_parser.parse_args()
        
        # Check if any of the provided fields already exist in the database
        existing_student = Student.query.filter(
            or_(
                Student.cardID == args['cardID'],
                Student.nationalID == args['nationalID'],
                Student.phoneNumber == args['phoneNumber'],
                Student.MAC == args['MAC'],
                Student.email == args['email']
            )
        ).first()

        if existing_student:
            return {'message': 'One or more fields already exist for another user'}, 400
        
        new_student = Student(**args)
        db.session.add(new_student)
        db.session.commit()
        return new_student, 201




# Define the LoginResource class
class LoginResource(Resource):
    
    def post(self):
        data = request.get_json()
        studentID=data.get('studentID')
        cardID = data.get('cardID')
        password = data.get('password')

        # Example authentication logic
        student = Student.query.filter_by(cardID=cardID, password=password,studentID=studentID).first()
        if student:
            # Generate token for the authenticated user
            token = generate_token(cardID)
            # Return token and other relevant information
            return {
                'message': 'Login successful',
                'token': token
            }, 200
        else:
            return {
                'message': 'Invalid cardID or password'
            }, 401
