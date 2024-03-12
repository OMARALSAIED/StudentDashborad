from flask import jsonify
from flask_restful import Api, Resource

from MysqlModels.models import Course, classroom


class AttendanceTracking(Resource):
    def get(self):
        tracking_data = []

        courses = Course.query.all()
        for course in courses:
            classroom1 = classroom.query.get(course.classroomID)
            if classroom1:
                course_info = {
                    'course_name': course.name,
                    'classroom_name': classroom1.caption,
                    'day_of_week': course.DayOfweek,
                    'start_time': str(course.startTime),
                    'end_time': str(course.endTime)
                }
                tracking_data.append(course_info)

        return jsonify(tracking_data)