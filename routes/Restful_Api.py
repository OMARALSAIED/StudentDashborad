
from cgitb import text
from datetime import datetime
from flask import jsonify, request
from flask_restful import  Resource
from sqlalchemy import func
from MysqlModels.models import db
from decorators import app

# Define your resource class
    

class GetCourseNametest(Resource):
    def get(self):
        # Retrieve inputs
        input_string = request.args.get('input_string')

        # Split the input string into individual values
        input_values = input_string.split(',')

        try:
            # Convert the input values to numbers
            day = input_values[0]
            time = input_values[1]
            class_number = int(input_values[2])

            # Custom SQL query to fetch course name
            query = text("""
                    SELECT c.name
                    FROM course c
                    JOIN classroom cl ON c.classroomID = cl.classroomID
                    WHERE c.DayOfweek = :day
                    AND :time BETWEEN c.startTime AND c.endTime
                    AND cl.number = :class_number
                    """)
            result = db.session.execute(query, {'day': day, 'time': time, 'class_number': class_number}).fetchone()

            if result:
                # Ensure result contains at least one value
                course_name = result[0]  # Unpack the first value of the result
                return {'course_name': course_name}, 200
            else:
                return {'error': 'No course found for the provided parameters'}, 404
        except (IndexError, ValueError):
            return {'error': 'Invalid input format'}, 400

   