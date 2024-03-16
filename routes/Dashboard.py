

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





@app.route('/Dashboard')
@login_required
@admin_required
   
def dashboard():
    # Custom MySQL query to fetch attendance data
    query = """
        SELECT
            COUNT(attendanceID) AS count,
            studentID,
            CASE
                WHEN timestamp < (SELECT startTime FROM course WHERE course.courseID = attendancesheet.courseID) THEN 'Present'
                ELSE 'Absent'
            END AS status
        FROM
            attendancesheet
        GROUP BY
            studentID, status
    """

    # Execute the query
    attendance_data = db.session.execute(text(query))

    # Formatting data for Chart.js for attendance
    present_count = 0
    absent_count = 0
    for row in attendance_data:
        if row.status == 'Present':
            present_count += row.count
        else:
            absent_count += row.count

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
                           student_chart_data=student_chart_data)