from flask import Blueprint, make_response, render_template
from sqlalchemy import text
from MysqlModels.models import Course, Lecturer, Operator, Role, Student, attendancesheet, beacon, classroom ,db,Department, faculty
from decorators import app
import pdfkit

Report= Blueprint('Report', __name__)


@app.route('/download/course_report/pdf')
def generate_course_pdf():
    # Custom SQL query to fetch data from multiple tables
    query = text("""
        SELECT c.*, d.name AS department_name, o.name AS operator_name,
               cl.number AS classroom_number, l.fullname AS lecturer_name
        FROM Course c
        LEFT JOIN Department d ON c.departmentID = d.departmentID
        LEFT JOIN Operator o ON c.operatorID = o.operatorID
        LEFT JOIN classroom cl ON c.classroomID = cl.classroomID
        LEFT JOIN Lecturer l ON c.lecturerID = l.lecturerID
    """)

    # Execute the query
    results = db.session.execute(query)

    
    

    # Render HTML template with course data, summary, and total students
    rendered_html = render_template('pdfTempltae/courset.html',results=results
                                   
    )

    # Generate PDF from HTML
    config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')
    pdf = pdfkit.from_string(rendered_html, configuration=config)

    # Create a response with PDF content
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=course_report.pdf'

    return response




@app.route('/download/lecturer_report/pdf')
def generate_lecturer_pdf():
    # Custom SQL query to fetch data from multiple tables
    query = text("""
        SELECT l.*, d.name AS department_name, o.name AS operator_name
        FROM Lecturer l
        LEFT JOIN Department d ON l.departmentID = d.departmentID
        LEFT JOIN Operator o ON l.operatorID = o.operatorID
    """)

    # Execute the query
    results = db.session.execute(query)
  
  


    # Render HTML template with lecturer data and total lecturers
    rendered_html = render_template('pdfTempltae/lecturert.html', results=results)

    # Generate PDF from HTML
    config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')
    pdf = pdfkit.from_string(rendered_html, configuration=config)

    # Create a response with PDF content
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=lecturer_report.pdf'

    return response






@app.route('/download/student_report/pdf')
def generate_student_pdf():
    # Custom SQL query to fetch data from multiple tables
    query = text("""
        SELECT fullname,email,gender,DateOfBirth
        FROM Student s
        
    """)

    # Execute the query
    results = db.session.execute(query)


    
    # Render HTML template with student data and summary
    rendered_html = render_template('pdfTempltae/studentt.html', results=results)

    # Generate PDF from HTML
    config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')
    pdf = pdfkit.from_string(rendered_html, configuration=config)

    # Create a response with PDF content
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=student_report.pdf'

    return response




@app.route('/download/attendance_report/pdf')
def generate_attendance_pdf():
    # Custom SQL query to fetch attendance data with course name and student name
    query = text("""
        SELECT c.name AS course_name, s.fullname AS student_name, a.timestamp
        FROM AttendanceSheet a
        LEFT JOIN Course c ON a.courseID = c.courseID
        LEFT JOIN Student s ON a.studentID = s.studentID
        ORDER BY c.name, s.fullname, a.timestamp
    """)
    # Execute the query
    results = db.session.execute(query)

    # Render HTML template with attendance data
    rendered_html = render_template('pdfTempltae/attendance.html', results=results)

    # Generate PDF from HTML
    config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')
    pdf = pdfkit.from_string(rendered_html, configuration=config)

    # Create a response with PDF content
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=attendance_report.pdf'

    return response
