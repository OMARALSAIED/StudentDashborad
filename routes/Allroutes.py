from functools import wraps
from email_validator import EmailNotValidError
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from pydantic import validate_email
from sqlalchemy import func
from MysqlModels.models import Course, Department, Lecturer, Operator, Role, Student, attendancesheet, beacon, classroom,faculty
from werkzeug.security import generate_password_hash,check_password_hash
from MysqlModels.models import db
from decorators import admin_required,app
from datetime import datetime
from routes.Validationfun import validate_address,validate_email , validate_numeric_input
 
# Create a Blueprint instance
Allroutes = Blueprint('Allroutes', __name__)




#=================================Faculties Routes
@app.route('/faculty_Details')
@login_required
@admin_required
def faculty_Details():
    query = faculty.query.all()
    operator_names = {}  #
    operators = Operator.query.all()
    for operator in operators:
        operator_names[operator.operatorID] = operator.name  # Use operator.operatorID, not Operator.operatorID
    
    return render_template('faculties/faculty.html', query=query, operator_names=operator_names)
   


@app.route("/facultyedit/<int:facultyID>", methods=['GET', 'POST'])
@login_required
def facultyedit(facultyID):

    faculty1 = faculty.query.filter_by(facultyID=facultyID).first()

    if request.method == 'POST':
       
        creationDate = request.form.get('creationDate')
        name = request.form.get('name')
        descc = request.form.get('descc')
        deleted = request.form.get('deleted')
       
        # Update the fields
        if faculty1 is not None:
           
           faculty1.creationDate = datetime.strptime(creationDate, '%Y-%m-%d')
           faculty1.name = name
           faculty1.descc = descc
           

        # Commit the changes to the database
        db.session.commit()

        # Redirect to a success page or another route
        flash('Faculty updated successfully.', 'success')
        return redirect(url_for('faculty_Details'))

    # Render the form template for GET requests
    return render_template('faculties/facultyedit.html', faculty1=faculty1, facultyID=facultyID)
    


@app.route('/deletfaculty/<string:facultyID>',methods=['POST','GET'])
@login_required
def DeletFaculty(facultyID):


    Faculty =faculty.query.filter_by(facultyID=facultyID).first()

    if Faculty:
        # Delete the Faculty from the database
        db.session.delete(Faculty)
        db.session.commit()
        flash("Faculty  successfully Deleted", "danger")
        # Redirect to a page or route after successful deletion
        return redirect(url_for('faculty_Details')) # Replace 'index' with the appropriate route

    # If the Faculty is not found, you can handle this case accordingly
    return render_template('faculties/faculty.html')

    

@app.route('/addfaculty', methods=['POST', 'GET'])
@login_required
def addfaculty():
    if request.method == 'POST':
        operatorID = current_user.operatorID
        name = request.form.get('name')
        descc = request.form.get('descc')
        
        # Server-side validation: Check if the name is empty or contains only whitespace
        if not name.strip():
            flash("Name is required.", "danger")
        else:
            new_faculty = faculty.query.filter_by(name=name).first()
            if new_faculty:
                flash("Faculty already exists.", "warning")
            else:
                # Create a new Faculty instance and add it to the session
                new_faculty = faculty(
                    operatorID=operatorID,
                    name=name,
                    descc=descc
                )
                db.session.add(new_faculty)
                db.session.commit()  # Commit the changes to the database
                flash('Faculty successfully added.', "success")

    return render_template('faculties/addfaculty.html')





#=================================Department Routes


@app.route('/DepartmentDetails')
@login_required
@admin_required
def Department_Details():
    query=Department.query.all()
    operators = Operator.query.all()
    faculties = faculty.query.all()
    
    operator_names = {operator.operatorID: operator.name for operator in operators}
    faculty_names = {faculty.facultyID: faculty.name for faculty in faculties}
    
    return render_template('department/department.html', query=query, operator_names=operator_names, faculty_names=faculty_names)




@app.route("/departmentedit/<int:departmentID>", methods=['GET', 'POST'])
@login_required
def departmentedit(departmentID):
    department1 = Department.query.filter_by(departmentID=departmentID).first()
    faculties = faculty.query.all()  # Fetch all faculties from the database
    departments = Department.query.all()  # Fetch all departments from the database
    operators = Operator.query.all()
    if request.method == 'POST':
        # Retrieve form data
        
        facultyID = request.form.get('facultyID')
        creationDate = request.form.get('creationDate')
        name = request.form.get('name')
        descc = request.form.get('descc')
        deleted = request.form.get('deleted')
       

        # Update the fields
        if department1 is not None:
            
            department1.facultyID = facultyID
            department1.creationDate = datetime.strptime(creationDate, '%Y-%m-%d')
            department1.name = name
            department1.descc = descc
           

            # Commit the changes to the database
            db.session.commit()

            # Redirect to a success page or another route
            flash('Department updated successfully.', 'success')
            return redirect(url_for('Department_Details'))

    # Render the form template for GET requests and POST requests that fail validation
    return render_template('department/departmentedit.html', department1=department1, departmentID=departmentID, faculties=faculties, departments=departments, operators=operators)







@app.route('/deletdepartment/<string:departmentID>',methods=['POST','GET'])
@login_required
def Deletdepartment(departmentID):


    department =Department.query.filter_by(departmentID=departmentID).first()

    if department:
        # Delete the Faculty from the database
        db.session.delete(department)
        db.session.commit()
        flash("Department successfully Deleted", "danger")
        # Redirect to a page or route after successful deletion
        return redirect(url_for('Department_Details')) # Replace 'index' with the appropriate route

    # If the Faculty is not found, you can handle this case accordingly
    return render_template('department/department.html')


@app.route('/adddepartment',methods=['POST','GET'])
@login_required
def adddepartment():
    if request.method == 'POST':
        operatorID = current_user.operatorID
        facultyID = request.form.get('facultyID')
        name = request.form.get('name')
        descc = request.form.get('descc')
        new_department = Department.query.filter_by(name=name).first()

        if new_department:
            flash("Department already exists.", "warning")
        else:
            # Create a new Department instance and add it to the session
            new_department = Department(
                operatorID=operatorID,
                facultyID=facultyID,
                name=name,
                descc=descc,
            )
            
            db.session.add(new_department)
            db.session.commit()  # Commit the changes to the database
            flash('Department added successfully.', "success")

    # Fetch all faculties to display in the template
    faculties = faculty.query.all()

    return render_template('department/adddepartment.html', faculties=faculties)



#=================================ClassRoos Routes


@app.route('/classroomsDetails')
def classrooms_Details():
   opreators=Operator.query.all()
   departments=Department.query.all()
   query=classroom.query.all()

   operator_names = {operator.operatorID: operator.name for operator in opreators}
   department_names = {department.departmentID: department.name for department in departments}
      
       
   return render_template('classroom/classrooms.html',query=query,operator_names=operator_names,department_names=department_names)





@app.route("/classroomedit/<int:classroomID>", methods=['GET', 'POST'])
@login_required
def classroomedit(classroomID):
    classroom1 = classroom.query.filter_by(classroomID=classroomID).first()

    if request.method == 'POST':
       
        departmentID = request.form.get('departmentID')
        creationDate = request.form.get('creationDate')
        caption = request.form.get('caption')
        number = request.form.get('number')
        floor = request.form.get('floor')
      
        # Update the fields
        if classroom1 is not None:
         
           classroom1.departmentID = departmentID
           classroom1.creationDate = datetime.strptime(creationDate, '%Y-%m-%d')
           classroom1.caption = caption
           classroom1.number = number
           classroom1.floor = floor
          

        # Commit the changes to the database
        db.session.commit()

        # Redirect to a success page or another route
        flash('ClassRoom updated successfully.', 'success')
        return redirect(url_for('classrooms_Details'))

    # Fetch operators and departments from the database
    operators = Operator.query.all()
    departments = Department.query.all()

    # Render the form template for GET requests
    return render_template('classroom/classroomedit.html', classroom1=classroom1, classroomID=classroomID, operators=operators, departments=departments)


from flask import request, redirect, url_for

@app.route('/addclassroom', methods=['POST', 'GET'])
@login_required
def addclassroom():
    if request.method == 'POST':
        operatorID = current_user.operatorID
        departmentID = request.form.get('departmentID')
        caption = request.form.get('caption')
        number = request.form.get('number')
        floor = request.form.get('floor')
        new_classroom = classroom.query.filter_by(number=number).first()
        if new_classroom:
            flash("Classroom already used.", "warning")
        else:
            # Create a new Classroom instance and add it to the session
            new_classroom = classroom(
                operatorID=operatorID,
                departmentID=departmentID,
                caption=caption,
                number=number,
                floor=floor,
            )
            
            db.session.add(new_classroom)
            db.session.commit()  # Commit the changes to the database
            flash('Classroom added successfully.', "success")
            return redirect(url_for('classrooms_Details'))

    # Fetch all departments to display in the template
    departments = Department.query.all()

    return render_template('classroom/addclassroom.html', departments=departments)







@app.route('/deleteclassroom/<int:classroomID>', methods=['GET', 'POST'])
@login_required
def deleteclassroom(classroomID):

    
        classrooms =classroom.query.filter_by(classroomID=classroomID).first()

        if classrooms:
            # Delete the classroom from the database
            db.session.delete(classrooms)
            db.session.commit()
            
           
            flash("classroom deleted successfully.", "danger")
            return redirect(url_for('classrooms_Details'))



        return render_template('classroom/classrooms.html')



#=================================Courss Routes


@app.route('/Courses')
def Courses():
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
    query = Course.query.all()
    
    return render_template('courese/course.html', query=query, department_names=department_names, operator_names=operator_names, classroom_names=classroom_names, lecturer_names=lecturer_names)
    



@app.route('/addcourse',methods=['POST','GET'])
@login_required
def addcourse():
     
    departments = Department.query.all()  # Fetch all departments
    lecturers = Lecturer.query.all()      # Fetch all lecturers
    classrooms=classroom.query.all()
    
    if request.method == 'POST':
        # Process the form submission
        departmentID = request.form.get('departmentID')
        classroomID = request.form.get('classroomID')
        lecturerID = request.form.get('lecturerID')
        operatorID = current_user.operatorID
        name = request.form.get('name')
        DayOfweek = request.form.get('DayOfweek')
        startTime = request.form.get('startTime')
        endTime = request.form.get('endTime')
        
        new_course = Course.query.filter_by(name=name).first()

        if new_course:
            flash("Course already exists.", "warning")
        else:
            # Create a new Course instance and add it to the session
            new_course = Course(
                departmentID=departmentID,
                classroomID=classroomID,
                lecturerID=lecturerID,
                operatorID=operatorID,
                name=name,
                DayOfweek=DayOfweek,
                startTime=startTime,
                endTime=endTime,
            )
            db.session.add(new_course)
            db.session.commit()
            flash('Course added successfully.', "success")
            return redirect(url_for('Courses'))

    return render_template('courese/addcourse.html', departments=departments, lecturers=lecturers,classrooms=classrooms)


@app.route('/deletecourse/<int:courseID>', methods=['GET', 'POST'])
@login_required
def deletecourse(courseID):

    
        course =Course.query.filter_by(courseID=courseID).first()

        if course:
            # Delete the course from the database
            db.session.delete(course)
            db.session.commit()
            flash("Course deleted successfully.", "success")
            redirect(url_for('Courses'))
        flash("Course deleted successfully.", "success")

        return redirect(url_for('Courses'))  # Redirect to the Courses page after deletion
   



@app.route("/courseedit/<int:courseID>", methods=['GET', 'POST'])
@login_required
def courseedit(courseID):
    course1 = Course.query.filter_by(courseID=courseID).first()

    if request.method == 'POST':
        departmentID = request.form.get('departmentID')
        classroomID = request.form.get('classroomID')
        lecturerID = request.form.get('lecturerID')
        
        creationDate = request.form.get('creationDate')
        name = request.form.get('name')
        DayOfweek = request.form.get('DayOfweek')
        startTime = request.form.get('startTime')
        endTime = request.form.get('endTime')
        
        # Update the fields
        if course1 is not None:
           course1.departmentID = departmentID
           course1.classroomID = classroomID
           course1.lecturerID = lecturerID
          
           course1.creationDate = datetime.strptime(creationDate, '%Y-%m-%d')
           course1.name = name
           course1.DayOfweek = DayOfweek
           course1.startTime = startTime
           course1.endTime = endTime

        # Commit the changes to the database
        db.session.commit()

        # Redirect to a success page or another route
        flash("Course Updated successfully.", "success")
        return redirect(url_for('Courses'))

    # Fetch operators, departments, and classrooms from the database
    departments = Department.query.all()
    lecturers = Lecturer.query.all()
    classrooms = classroom.query.all()

    # Render the form template for GET requests
    return render_template('courese/editcourse.html', course1=course1, courseID=courseID, departments=departments, lecturers=lecturers, classrooms=classrooms)


#=================================Lecturer Routes


@app.route('/lecturer')
@login_required
@admin_required
def lecturer():
     
    departments=Department.query.all()
    operators=Operator.query.all()
    query=Lecturer.query.all()


    department_names = {department.departmentID: department.name for department in departments}
    operator_names = {operator.operatorID: operator.name for operator in operators}


    return render_template('/lecturer/lecturer.html',query=query,department_names=department_names,operator_names=operator_names)
    



@app.route('/addlecturer',methods=['POST','GET'])
@login_required
def addlecturer():
     
    operators=Operator.query.all()
    departments=Department.query.all()

    if request.method == 'POST':
        operatorID = current_user.operatorID
        departmentID = request.form.get('departmentID')
        gender = request.form.get('gender')
        fullname = request.form.get('fullname')

        new_lecturer = Lecturer.query.filter_by(fullname=fullname).first()


        if new_lecturer:
            flash("classroom already exists.", "warning")
        else:
            # Create a new Lecturer instance and add it to the session
            new_lecturer = Lecturer(
                operatorID=operatorID,
                departmentID=departmentID,
                gender=gender,
                fullname=fullname,
            
            )
            
            db.session.add(new_lecturer)
            db.session.commit()  # Commit the changes to the database
            flash('new_lecturer add successfully.', "success")
            return redirect(url_for('lecturer'))

    return render_template('lecturer/addlecturer.html',departments=departments,operators=operators)



@app.route('/deletlecturer/<string:lecturerID>',methods=['POST','GET'])
@login_required
def Deletlecturer(lecturerID):


    lecturer =Lecturer.query.filter_by(lecturerID=lecturerID).first()

    if lecturer:
        # Delete the Faculty from the database
        db.session.delete(lecturer)
        db.session.commit()
        flash("Course Deleted Seccessful, danger")
        # Redirect to a page or route after successful deletion
        return redirect(url_for('lecturer')) # Replace 'index' with the appropriate route

    # If the Faculty is not found, you can handle this case accordingly
    return render_template('lecturer/lecturer.html')



@app.route("/lectureredit/<int:lecturerID>", methods=['GET', 'POST'])
@login_required
def edit_lecturer(lecturerID):
    lecturer = Lecturer.query.get_or_404(lecturerID)
    if request.method == 'POST':
        lecturer.operatorID = current_user.operatorID
        lecturer.departmentID = request.form.get('departmentID')
        lecturer.gender = request.form.get('gender')
        lecturer.fullname = request.form.get('fullname')

        db.session.commit()
        flash("Lecturer updated successfully.", "success")
        return redirect(url_for('lecturer'))

    operators = Operator.query.all()
    departments = Department.query.all()
    return render_template('lecturer/lectureredit.html', lecturer=lecturer, departments=departments, operators=operators)


#=================================Students Routes



@app.route('/students', methods=['POST', 'GET'])
@login_required
def students():
    departments = Department.query.all()
    if request.method == 'POST':
        operatorID = current_user.operatorID
        departmentID = request.form.get('departmentID')
        cardID = request.form.get('cardID')
        nationalID = request.form.get('nationalID')
        gender = request.form.get('gender')
        fullname = request.form.get('fullname')
        DateOfBirth = request.form.get('DateOfBirth')
        enrollmentDate = request.form.get('enrollmentDate')
        phoneNumber = request.form.get('phoneNumber')
        address = request.form.get('address')
        MAC = request.form.get('MAC')
        email = request.form.get('email')
        password = request.form.get('password')

        # Perform server-side validation
        if not validate_numeric_input(cardID):
            flash("Please enter a valid Card ID.", "danger")
            return redirect(request.url)

        if not validate_numeric_input(nationalID):
            flash("Please enter a valid National ID.", "danger")
            return redirect(request.url)

        if not validate_address(address):
            flash("Please enter a valid address containing only letters and numbers.", "danger")
            return redirect(request.url)

        if not validate_email(email):
            flash("Please enter a valid email address.", "danger")
            return redirect(request.url)

        # Check for existing student with the same email
        new_student = Student.query.filter_by(email=email).first()
        if new_student:
            flash("Username already exists", "warning")
            return redirect(request.url)

        # Add the student to the database
        encpassword = generate_password_hash(password)
        new_student = Student(
            operatorID=operatorID,
            departmentID=departmentID,
            cardID=cardID,
            nationalID=nationalID,
            gender=gender,
            fullname=fullname,
            DateOfBirth=DateOfBirth,
            enrollmentDate=enrollmentDate,
            phoneNumber=phoneNumber,
            address=address,
            MAC=MAC,
            email=email,
            password=encpassword
        )
        db.session.add(new_student)
        db.session.commit()  # Commit the changes to the database
        flash('Student added successfully.', "success")

    return render_template('Students/addstudents.html', departments=departments)



@app.route('/details')

def Details():
       

       departments=Department.query.all()
       operators=Operator.query.all()
       query = Student.query.all()

       department_names = {department.departmentID: department.name for department in departments}
       operator_names = {operator.operatorID: operator.name for operator in operators}
       
       return render_template('Students/details.html', query=query,department_names=department_names,operator_names=operator_names)



@app.route("/edit/<string:studentID>", methods=['GET', 'POST'])
@login_required
def edit(studentID):
    student = Student.query.filter_by(studentID=studentID).first()

    if request.method == 'POST':
        operatorID = request.form.get('operatorID')
        departmentID = request.form.get('departmentID')
        cardID = request.form.get('cardID')
        nationalID = request.form.get('nationalID')
        gender = request.form.get('gender')
        fullname = request.form.get('fullname')
        DateOfBirth = request.form.get('DateOfBirth')
        enrollmentDate = request.form.get('enrollmentDate')
        phoneNumber = request.form.get('phoneNumber')
        address = request.form.get('address')
        MAC = request.form.get('MAC')
        email = request.form.get('email')
        password = request.form.get('password')

        if student is not None:
            # Update the fields
            student.operatorID = operatorID
            student.departmentID = departmentID
            student.cardID = cardID
            student.nationalID = nationalID
            student.gender = gender
            student.fullname = fullname
            student.DateOfBirth = DateOfBirth
            student.enrollmentDate = enrollmentDate
            student.phoneNumber = phoneNumber
            student.address = address
            student.MAC = MAC
            student.email = email
            student.password = password

            # Commit the changes to the database
            db.session.commit()

            # Redirect to a success page or another route
            flash('student Updated Success','success')
        return  redirect(url_for('Details'))
    opreators=Operator.query.all()
    departments=Department.query.all()
    # Render the form template for GET requests or when the student is not found
    return render_template('Students/edit.html', student=student, studentID=studentID,opreators=opreators,departments=departments)


@app.route("/delete/<string:studentID>", methods=['GET', 'POST'])
@login_required
def delete(studentID):

    student = Student.query.filter_by(studentID=studentID).first()

    if student:
        # Delete the student from the database
        db.session.delete(student)
        db.session.commit()
        flash('Student Deleted Seccessful','danger')
        # Redirect to a page or route after successful deletion
        return redirect('/details') # Replace 'index' with the appropriate route

    # If the student is not found, you can handle this case accordingly
    return render_template('details.html')


#=================================Attendacne Routes


@app.route('/attendance')
def attendance():
    students = Student.query.all()  # Fetch all students
    courses = Course.query.all() 
    query = attendancesheet.query.all()

    students_names = {student.studentID: student.fullname for student in students}
    course_names = {course.courseID: course.name for course in courses}
    
    return render_template('/attendance/attendance.html', query=query,students_names=students_names,course_names=course_names)


@app.route('/addattendance',methods=['POST','GET'])
@login_required
def  addattendance():
    students = Student.query.all()  # Fetch all students
    courses = Course.query.all()    # Fetch all courses
   
    if request.method == 'POST':
        # Process the form submission
        studentID = request.form.get('studentID')
        courseID = request.form.get('courseID')
        timestamp = request.form.get('timestamp')

        new_attendance = attendancesheet.query.filter_by(studentID=studentID, courseID=courseID).first()

        if new_attendance:
            flash("Student already added to attendance sheet.", "warning")
        else:
            # Create a new attendance instance and add it to the session
            new_attendance = attendancesheet(
                studentID=studentID,
                courseID=courseID,
                timestamp=timestamp
            )
            db.session.add(new_attendance)
            db.session.commit()
            flash('Attendance added successfully.', "success")
            return redirect(url_for('attendance'))

    return render_template('attendance/addattendancesheet.html', students=students, courses=courses)




@app.route('/deleteattendance/<string:attendanceID>',methods=['POST','GET'])
@login_required
def Deleteattendace(attendanceID):


    attendance =attendancesheet.query.filter_by(attendanceID=attendanceID).first()

    if attendance:
        # Delete the Faculty from the database
        db.session.delete(attendance)
        db.session.commit()
        flash("Attendance Deleted Seccessfully", "danger")
        # Redirect to a page or route after successful deletion
        return redirect(url_for('attendance')) # Replace 'index' with the appropriate route

    # If the Faculty is not found, you can handle this case accordingly
    return render_template('attendance/attendance.html')




@app.route("/attendaceedit/<int:attendanceID>", methods=['GET', 'POST'])
@login_required
def attendaceedit(attendanceID):
    attendace1 = attendancesheet.query.get_or_404(attendanceID)
    students=Student.query.all()
    courese=Course.query.all()

    if request.method == 'POST':
        studentID = request.form.get('studentID')
        courseID = request.form.get('courseID')
        timestamp = request.form.get('timestamp')
        
        # Convert the timestamp string to a datetime object
        timestamp = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M')

        # Update the fields
        if attendace1 is not None:
           attendace1.studentID = studentID
           attendace1.courseID = courseID
           attendace1.timestamp = timestamp
           
        # Commit the changes to the database
        db.session.commit()

        # Redirect to a success page or another route
        flash('Attendance updated successfully.', 'success')
        return redirect(url_for('attendance', attendanceID=attendanceID))
    

    # Render the form template for GET requests
    return render_template('attendance/attendaceedit.html', attendace1=attendace1, attendanceID=attendanceID,students=students,courese=courese)



#====================================Beacons Routes
@app.route('/beacons')
def Beacon():
    opreators=Operator.query.all()
    classrooms=classroom.query.all()
    query=beacon.query.all()
    operator_names = {operator.operatorID: operator.name for operator in opreators}
    classrooms_names = {classrooom.classroomID: classrooom.number for classrooom in classrooms}
    return render_template('beacons/beacons.html',query=query,opreators_names=operator_names,classrooms_names=classrooms_names)






@app.route('/addbeacon',methods=['POST','GET'])
@login_required
def addbeacon():
    classrooms=classroom.query.all()
    if request.method == 'POST':
        operatorID = current_user.operatorID
        classroomID = request.form.get('classroomID')
        creationDate = request.form.get('creationDate')
        caption = request.form.get('caption')
        UUID = request.form.get('UUID')
        MAC = request.form.get('MAC')
        
       

        new_beacon = beacon.query.filter_by(MAC=MAC).first()


        if new_beacon:
            flash("Sutdent already Added to attendace sheet.", "warning")
        else:
            # Create a new beacon instance and add it to the session
            new_beacon = beacon(
                operatorID=operatorID,
                classroomID=classroomID,
                creationDate=creationDate,
                caption=caption, 
                UUID=UUID,
                MAC=MAC
            
            )
            
            db.session.add(new_beacon)
            db.session.commit()  # Commit the changes to the database
            flash('new_Becaons add successfully.', "success")
            return redirect(url_for('Beacon'))

    return render_template('beacons/addbeacon.html',classrooms=classrooms)


@app.route('/deletebeacon/<string:beaconID>',methods=['POST','GET'])
@login_required
def Deletebeacon(beaconID):


    beacon1 =beacon.query.filter_by(beaconID=beaconID).first()

    if beacon1:
        # Delete the Faculty from the database
        db.session.delete(beacon1)
        db.session.commit()
        flash("Beacon Deleted Seccessfully", "danger")
        # Redirect to a page or route after successful deletion
        return redirect(url_for('Beacon')) # Replace 'index' with the appropriate route

    # If the Faculty is not found, you can handle this case accordingly
    return render_template('beacons/beacons.html')





@app.route("/beaconedit/<int:beaconID>", methods=['GET', 'POST'])
@login_required
def beaconedit(beaconID):

    beacon1 = beacon.query.filter_by(beaconID=beaconID).first()
    classrooms=classroom.query.all()

    if request.method == 'POST':
       
        classroomID=request.form.get('classroomID')  
        creationDate = request.form.get('creationDate')
        caption = request.form.get('caption')
        UUID = request.form.get('UUID')
        MAC = request.form.get('MAC')
      
        # Update the fields
        if beacon1 is not None:
          
           beacon1.classroomID=classroomID
           beacon1.creationDate = datetime.strptime(creationDate, '%Y-%m-%d')
           beacon1.caption=caption
           beacon1.UUID = UUID
           beacon1.MAC = MAC
         
           

        # Commit the changes to the database
        db.session.commit()

        # Redirect to a success page or another route
        flash('ClassRoos updated successfully.', 'success')
        return redirect(url_for('Beacon'))

    # Render the form template for GET requests
    return render_template('beacons/beaconsedit.html', beacon1=beacon1, beaconID=beaconID,classrooms=classrooms)




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
    # Example query to fetch attendance data
    attendance_data = db.session.query(
        func.count(attendancesheet.attendanceID).label('count'),
        attendancesheet.studentID
    ).group_by(attendancesheet.studentID).all()

    # Formatting data for Chart.js for attendance
    labels = ['Present', 'Absent', 'Late']  # Assuming you have these attendance statuses
    attendance_chart_data = {
        'labels': labels,
        'datasets': [{
            'data': [count for count, _ in attendance_data],
            'backgroundColor': ['#5DA5DA', '#FAA43A', '#60BD68']
        }]
    }

    # Example query to fetch student data
    student_data = db.session.query(
        Department.name,
        func.count(Student.studentID).label('count')
    ).join(Student).group_by(Department.name).all()

    department_labels = [data[0] for data in student_data]  # Extract department names
    student_counts = [data[1] for data in student_data]     # Extract student counts

    student_chart_data = {
        'labels': department_labels,
        'datasets': [{
            'data': student_counts,
            'backgroundColor': ['#FF6384', '#36A2EB', '#FFCE56']  # Example colors
        }]
    } # Retrieve counts for each category
    lecturers_count = Lecturer.query.count()
    faculties_count = faculty.query.count()
    departments_count = Department.query.count()
    classrooms_count = classroom.query.count()
    courses_count = Course.query.count()
    students_count = Student.query.count()
    beacons_count = beacon.query.count()
    attendance_records_count = attendancesheet.query.count()

    # Dummy data for charts (replace with your actual data)
    attendance_chart_data_1 = [65, 59, 80, 81, 56, 55]
    attendance_chart_data_2 = [75, 69, 85, 84, 66, 60]
    months = ['January', 'February', 'March', 'April', 'May', 'June']

    return render_template('dashboard.html', 
                            lecturers_count=lecturers_count,
                            faculties_count=faculties_count,
                            departments_count=departments_count,
                            classrooms_count=classrooms_count,
                            courses_count=courses_count,
                            students_count=students_count,
                            beacons_count=beacons_count,
                            attendance_records_count=attendance_records_count,
                            attendance_chart_data_1=attendance_chart_data_1,
                            attendance_chart_data_2=attendance_chart_data_2,
                            months=months, attendance_chart_data=attendance_chart_data, student_chart_data=student_chart_data)

