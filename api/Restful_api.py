from aifc import Error
from datetime import datetime, time, timezone

from sqlalchemy import text
from decorators import app
from flask import abort, jsonify, request, session
from flask_restful import Resource, reqparse, marshal_with, fields
from MysqlModels.models import attendancesheet, classroom, db

class CourseID:
    @staticmethod
    def find_conflicting_course(classroom_number):
        """
        Find a course that has a conflicting start time with a specific classroom.

        :param classroom_number: Number of the classroom to check against
        :return: Conflicting course, if any, including the course ID and start time
        """
        # Retrieve the classroom ID based on the provided classroom number
        classroom_id = classroom.query.filter_by(number=classroom_number).first().classroomID

        # SQL query to find conflicting course and fetch course ID and start time
        query = text("""
        SELECT Course.courseID AS courseID, Course.startTime AS start_time
        FROM Course
        JOIN Classroom ON Course.classroomID = Classroom.classroomID
        WHERE Classroom.number = :classroom_number
        """)
        # Execute the SQL query
        result = db.session.execute(query, {'classroom_number': classroom_number})

        # Fetch the conflicting course, if any
        conflicting_course = result.fetchone()

        # Extract course ID and start time from the tuple
        if conflicting_course:
            course_id = conflicting_course[0]  # Accessing by index
            start_time = conflicting_course[1]  # Accessing by index

            # Convert timedelta to string (ISO 8601 format)
            start_time_str = str(start_time)
            
            return {'courseID': course_id, 'start_time': start_time_str}
        else:
            return None

class FindConflictingCourseResource(Resource):
    def post(self):
        # Get data from the request
        data = request.json
        classroom_number = data.get('classroom_number')

        if classroom_number is None:
            return jsonify({"error": "Classroom number is required"}), 400

        # Call the find_conflicting_course function
        conflicting_course = CourseID.find_conflicting_course(classroom_number)

        # Return the result as JSON
        return jsonify(conflicting_course)






def current_utc_timestamp():
    return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S')

CourseID()

attendance_post = reqparse.RequestParser()
attendance_post.add_argument('studentID', type=str, help="studentID is required", required=True)
attendance_post.add_argument('courseID', type=str, help="courseID is required", required=True)
attendance_post.add_argument('timestamp', 
                              type=str, 
                              help="Time stamp is required", 
                              required=False, 
                              default=current_utc_timestamp)

# Define resource fields for marshalling
resource_fields = {
    'attendanceID': fields.Integer,
    'studentID': fields.Integer,
    'courseID': fields.Integer,
    'timestamp': fields.DateTime
}

class AttendanceList(Resource):
    def get(self, attendance_ID):
        args = attendance_post.parse_args()
        attend = attendancesheet.query.filter_by(attendanceID=attendance_ID).first()
        if attend:
            abort(409)
        return
    
    @marshal_with(resource_fields)
    def post(self):
        args = attendance_post.parse_args()
        
        new_attendance = attendancesheet(studentID=args['studentID'], 
                                         courseID=args['courseID'], 
                                         timestamp=datetime.strptime(args['timestamp'], '%Y-%m-%dT%H:%M:%S'))
        db.session.add(new_attendance)
        db.session.commit()
        return new_attendance, 201
