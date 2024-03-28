

from sqlalchemy import case, text
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from pydantic import validate_email
from sqlalchemy import  func
from MysqlModels.models import Course, Department, Lecturer, Role, Student, attendancesheet, beacon, classroom,faculty

from MysqlModels.models import db
from decorators import admin_required,app
from datetime import datetime

# Create a Blueprint instance
Dashboard = Blueprint('Dashboard', __name__)




@app.route('/testdb')

def testdb():
    try: 
        Role.query.all()
        return 'My Data Base is Connected'
    except :
        return 'My Data Base is not Connected'
    

@app.route('/Home')
def Home():
    return 'Home'



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sidebar')
def side():

    return render_template('sidebar.html')





@app.route('/Dashboard')
@login_required
@admin_required
def dashboard():
    courses=Course.query.all()

    course_names = {course.courseID: course.name for course in courses}
    # Custom MySQL query to fetch attendance data
    query = """
        SELECT
            COUNT(attendanceID) AS count,
            courseID,
            CASE
                WHEN timestamp < (SELECT startTime FROM course WHERE course.courseID = attendancesheet.courseID) THEN 'Present'
                ELSE 'Absent'
            END AS status
        FROM
            attendancesheet
        GROUP BY
            courseID, status
    """

    # Execute the query
    attendance_data = db.session.execute(text(query))

    # Dictionary to store attendance and absence counts for each course
    course_attendance_counts = {}
    course_absence_counts = {}

    # Iterate through attendance data to calculate counts for each course
    for row in attendance_data:
        course_id = row.courseID

        # Initialize counts if the course is encountered for the first time
        if course_id not in course_attendance_counts:
            course_attendance_counts[course_id] = 0
            course_absence_counts[course_id] = 0

        if row.status == 'Present':
            course_attendance_counts[course_id] += row.count
        else:
            course_absence_counts[course_id] += row.count

    # Dictionary to store percentages of attendance and absence for each course
    course_percentages = {}

    # Calculate percentages for each course
    for course_id in course_attendance_counts:
        total_records = course_attendance_counts[course_id] + course_absence_counts[course_id]
        attendance_percentage = (course_attendance_counts[course_id] / total_records) * 100
        absence_percentage = (course_absence_counts[course_id] / total_records) * 100
        course_percentages[course_id] = {'attendance': attendance_percentage, 'absence': absence_percentage}

    # Formatting data for Chart.js for attendance
    present_count = sum(course_attendance_counts.values())
    absent_count = sum(course_absence_counts.values())

    attendance_chart_data = {
        'labels': ['Present', 'Absent'],
        'datasets': [{
            'data': [present_count, absent_count],
            'backgroundColor': ['#5DA5DA', '#FAA43A']
        }]
    }

    # Example query to fetch student data (you can replace this with your actual query)
    student_data = db.session.query(
        Department.name,
        func.count(Student.studentID).label('count')
    ).join(Student).group_by(Department.name).all()

    department_labels = [data[0] for data in student_data]
    student_counts = [data[1] for data in student_data]

    student_chart_data = {
        'labels': department_labels,
        'datasets': [{
            'data': student_counts,
            'backgroundColor': ['#FF6384', '#36A2EB', '#FFCE56']
        }]
    }

    # Retrieve counts for each category (you can replace this with your actual queries)
    lecturers_count = Lecturer.query.count()
    faculties_count = faculty.query.count()
    departments_count = Department.query.count()
    classrooms_count = classroom.query.count()
    courses_count = Course.query.count()
    students_count = Student.query.count()
    beacons_count = beacon.query.count()
    attendance_records_count = attendancesheet.query.count()

    return render_template('dashboard.html',
                           lecturers_count=lecturers_count,
                           faculties_count=faculties_count,
                           departments_count=departments_count,
                           classrooms_count=classrooms_count,
                           courses_count=courses_count,
                           students_count=students_count,
                           beacons_count=beacons_count,
                           attendance_records_count=attendance_records_count,
                           attendance_chart_data=attendance_chart_data,
                           student_chart_data=student_chart_data,
                           course_percentages=course_percentages,course_names=course_names)


@app.route('/testdashboard')
def calculate_course_attendance():
    # Custom MySQL query to fetch attendance data
    query = """
        SELECT
            courseID,
            SUM(CASE WHEN timestamp < (SELECT startTime FROM course WHERE course.courseID = attendancesheet.courseID) THEN 1 ELSE 0 END) AS attendance_count,
            SUM(CASE WHEN timestamp >= (SELECT startTime FROM course WHERE course.courseID = attendancesheet.courseID) THEN 1 ELSE 0 END) AS absence_count,
            COUNT(*) AS total_records
        FROM
            attendancesheet
        GROUP BY
            courseID
    """

    # Execute the query
    attendance_data = db.session.execute(text(query))

    # Dictionary to store percentages of attendance and absence for each course
    course_percentages = {}

    # Calculate percentages for each course
    for row in attendance_data:
        course_id = row.courseID
        attendance_count = row.attendance_count
        absence_count = row.absence_count
        total_records = row.total_records

        if total_records > 0:
            attendance_percentage = (attendance_count / total_records) * 100
            absence_percentage = (absence_count / total_records) * 100
        else:
            attendance_percentage = 0
            absence_percentage = 0

        # Fetch course name by ID
        course_name = Course.query.filter_by(courseID=course_id).first().name

        course_percentages[course_name] = {'attendance': attendance_percentage, 'absence': absence_percentage}

    return render_template('testdashbord.html', course_percentages=course_percentages)