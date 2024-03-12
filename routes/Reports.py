from flask import Blueprint, make_response, render_template
from MysqlModels.models import Course, Lecturer, Operator, Role, Student, attendancesheet, beacon, classroom ,db,Department, faculty
from decorators import app
import pdfkit

Report= Blueprint('Report', __name__)


@app.route('/download/course_report/pdf')
def generate_course_pdf():
    # Fetch course data from the database
    courses = Course.query.all()
    departments = Department.query.all()
    lecturers = Lecturer.query.all()
    operators = Operator.query.all()
    classrooms = classroom.query.all()

    # Calculate total number of items
    total_courses = len(courses)
    total_departments = len(departments)
    total_lecturers = len(lecturers)
    total_classrooms = len(classrooms)

    # Calculate number of occupied instances
    occupied_courses = sum(1 for course in courses if course.departmentID or course.lecturerID or course.classroomID)
    occupied_departments = sum(1 for department in departments if department.name)
    occupied_lecturers = sum(1 for lecturer in lecturers if lecturer.fullname)
    occupied_classrooms = sum(1 for classroom in classrooms if classroom.number)

    # Calculate percentage of usage
    percentage_courses = ( total_courses/occupied_courses) * 100 if total_courses > 0 else 0
    percentage_departments = (total_departments /occupied_departments ) * 100 if total_departments > 0 else 0
    percentage_lecturers = (occupied_lecturers / total_lecturers) * 100 if total_lecturers > 0 else 0
    percentage_classrooms = (occupied_classrooms / total_classrooms) * 100 if total_classrooms > 0 else 0
    
    percentage_courses_ans=percentage_courses-100
    percentage_departments_ans=percentage_departments-100
    percentage_lecturers_ans=percentage_lecturers-100
    percentage_classrooms_ans=percentage_classrooms-100

    # Create dictionaries for quick lookup
    department_names = {department.departmentID: department.name for department in departments}
    operator_names = {operator.operatorID: operator.name for operator in operators}
    classroom_numbers = {classroom.classroomID: classroom.number for classroom in classrooms}
    lecturer_names = {lecturer.lecturerID: lecturer.fullname for lecturer in lecturers}

    # Render HTML template with course data, summary, and total students
    rendered_html = render_template('pdfTempltae/courset.html',
                                    courses=courses,
                                    department_names=department_names,
                                    operator_names=operator_names,
                                    classroom_numbers=classroom_numbers,
                                    lecturer_names=lecturer_names,
                                    total_courses=total_courses,
                                    total_departments=total_departments,
                                    total_lecturers=total_lecturers,
                                    total_classrooms=total_classrooms,
                                    percentage_courses_ans=percentage_courses_ans,
                                    percentage_departments_ans=percentage_departments_ans,
                                    percentage_lecturers_ans=percentage_lecturers_ans,
                                    percentage_classrooms_ans=percentage_classrooms_ans)

    # Generate PDF from HTML
    config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')
    pdf = pdfkit.from_string(rendered_html, configuration=config)

    # Create a response with PDF content
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=course_report.pdf'

    return response




@app.route('/download/student_report/pdf')
def generate_student_pdf():
    # Fetch student data from the database
    departments = Department.query.all()
    students = Student.query.all()

    # Calculate total number of students and departments
    total_students = len(students)
    total_departments = len(departments)

    # Create a dictionary for department names for quick lookup
    department_names = {department.departmentID: department.name for department in departments}

    # Render HTML template with student data, summary, and total students
    rendered_html = render_template('pdfTempltae/studentt.html',
                                    students=students,
                                    department_names=department_names,
                                    total_students=total_students,
                                    total_departments=total_departments)

    # Generate PDF from HTML
    config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')
    pdf = pdfkit.from_string(rendered_html, configuration=config)

    # Create a response with PDF content
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=student_report.pdf'

    return response