
from operator import or_
from flask import Blueprint,render_template, request
from flask_login import login_required
from decorators import app,admin_required
from MysqlModels.models import Course, Department, Lecturer, Operator, Role, Student, attendancesheet, beacon, classroom,faculty


DetalsRoutes=Blueprint("DeltasRoutes",__name__)






#=================================Faculties Routes
@app.route('/faculty_Details')
@login_required
@admin_required
def faculty_Details():
    # Fetch all faculties, including deleted ones
    query = faculty.query.filter(or_(faculty.deleted == False, faculty.deleted == None)).all()
    operator_names = {}
    operators = Operator.query.all()
    for operator in operators:
        operator_names[operator.operatorID] = operator.name
    
    return render_template('faculties/faculty.html', query=query, operator_names=operator_names)
   



#=================================Departments Routes


@app.route('/DepartmentDetails')
@login_required
@admin_required
def Department_Details():
    # Filter out deleted departments
    query = Department.query.filter(or_(Department.deleted == False, Department.deleted == None)).all()
    
    operators = Operator.query.all()
    faculties = faculty.query.all()
    
    operator_names = {operator.operatorID: operator.name for operator in operators}
    faculty_names = {faculty.facultyID: faculty.name for faculty in faculties}
    
    return render_template('department/department.html', query=query, operator_names=operator_names, faculty_names=faculty_names)




#=================================ClassRooms Routes

@app.route('/classroomsDetails')
@login_required
@admin_required
def classrooms_Details():
   query = classroom.query.filter(or_(classroom.deleted == False, classroom.deleted == None)).all()
   opreators=Operator.query.all()
   departments=Department.query.all()
  

   operator_names = {operator.operatorID: operator.name for operator in opreators}
   department_names = {department.departmentID: department.name for department in departments}
      
       
   return render_template('classroom/classrooms.html',query=query,operator_names=operator_names,department_names=department_names)

#=================================Courses Routes

@app.route('/Courses')
@login_required
@admin_required
def Courses():
    
    query = Course.query.filter(or_(Course.deleted == False, Course.deleted == None)).all()
    # Fetching data for department, operator, classroom, and lecturer
    departments = Department.query.all()
    operators = Operator.query.all()
    classrooms = classroom.query.all()
    lecturers = Lecturer.query.all()
    
    # Creating dictionaries to map IDs to names
    department_names = {department.departmentID: department.name for department in departments}
    operator_names = {operator.operatorID: operator.name for operator in operators}
    classroom_names = {classroom.classroomID: classroom.number for classroom in classrooms}
    lecturer_names = {lecturer.lecturerID: lecturer.fullname for lecturer in lecturers}
    
    # Fetching course data
    
    
    return render_template('courese/course.html', query=query, department_names=department_names, operator_names=operator_names, classroom_names=classroom_names, lecturer_names=lecturer_names)



#=================================Lecturer Routes

@app.route('/lecturer')
@login_required
@admin_required
def lecturer():
     
    query = Lecturer.query.filter(or_(Lecturer.deleted == False, Lecturer.deleted == None)).all()
    departments=Department.query.all()
    operators=Operator.query.all()
    


    department_names = {department.departmentID: department.name for department in departments}
    operator_names = {operator.operatorID: operator.name for operator in operators}


    return render_template('/lecturer/lecturer.html',query=query,department_names=department_names,operator_names=operator_names)



#=================================Student Routes



@app.route('/details')
@login_required
@admin_required
def Details():
       

       departments=Department.query.all()
       operators=Operator.query.all()
       query = Student.query.filter(or_(Student.deleted == False, Student.deleted == None)).all()

       department_names = {department.departmentID: department.name for department in departments}
       operator_names = {operator.operatorID: operator.name for operator in operators}
       
       return render_template('Students/details.html', query=query,department_names=department_names,operator_names=operator_names)



#=================================AttendanceSheet Routes

@app.route('/attendance')
@login_required
@admin_required
def attendance():
    students = Student.query.all()  # Fetch all students
    courses = Course.query.all() 
    query = attendancesheet.query.filter(or_(attendancesheet.deleted==False,attendancesheet.deleted==None)).all()

    students_names = {student.studentID: student.fullname for student in students}
    course_names = {course.courseID: course.name for course in courses}
    
    return render_template('/attendance/attendance.html', query=query,students_names=students_names,course_names=course_names)




@app.route('/beacons')
@login_required
@admin_required
def Beacon():
    opreators=Operator.query.all()
    classrooms=classroom.query.all()
    query=beacon.query.all()
    operator_names = {operator.operatorID: operator.name for operator in opreators}
    classrooms_names = {classrooom.classroomID: classrooom.number for classrooom in classrooms}
    return render_template('beacons/beacons.html',query=query,opreators_names=operator_names,classrooms_names=classrooms_names)




