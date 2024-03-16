from operator import or_
from flask import Blueprint, flash, redirect,render_template, request, url_for
from flask_login import current_user, login_required
from pydantic import validate_email
from decorators import app,admin_required
from MysqlModels.models import Course, Department, Lecturer, Operator, Role, Student, attendancesheet, beacon, classroom,faculty
from MysqlModels.models import db
from werkzeug.security import generate_password_hash,check_password_hash

from routes.Validationfun import validate_address, validate_numeric_input
Addfun=Blueprint("Addfun",__name__)


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
        elif not descc.strip():
            flash("Description is required.", "danger")
        else:
            # Check if the name and description are unique
            existing_faculty = faculty.query.filter_by(name=name).first()
            existing_description = faculty.query.filter_by(descc=descc).first()
            
            if existing_faculty or existing_description:
                flash("Faculty with the same name or description already exists.", "warning")
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







@app.route('/adddepartment', methods=['POST', 'GET'])
@login_required
def adddepartment():
    if request.method == 'POST':
        operatorID = current_user.operatorID
        facultyID = request.form.get('facultyID')
        name = request.form.get('name')
        descc = request.form.get('descc')
        
        # Check if a department with the same name or description already exists
        existing_department = Department.query.filter_by(name=name).first()
        
        if existing_department:
            flash("Department with the same name and description already exists.", "warning")
        else:
            # Create a new Department instance and add it to the session
            new_department = Department(
                operatorID=operatorID,
                facultyID=facultyID,
                name=name,
                descc=descc
            )
            db.session.add(new_department)
            db.session.commit()  # Commit the changes to the database
            flash('Department added successfully.', "success")

    # Fetch all faculties to display in the template
    faculties = faculty.query.all()

    return render_template('department/adddepartment.html', faculties=faculties)








@app.route('/addclassroom', methods=['POST', 'GET'])
@login_required
def addclassroom():
    if request.method == 'POST':
        operatorID = current_user.operatorID
        departmentID = request.form.get('departmentID')
        caption = request.form.get('caption')
        number = request.form.get('number')
        floor = request.form.get('floor')
        
        if not caption.strip():
            flash("Caption is required")
        elif not number.strip():
            flash("Number is required")
        else:
            existing_caption = classroom.query.filter_by(caption=caption).first()
            existing_number = classroom.query.filter_by(number=number).first()
            if existing_caption or existing_number:
                flash("classroom with the same name or description already exists.", "warning")
            else:
                # Create a new classroom instance and add it to the session
                new_classroom = classroom(
                    operatorID=operatorID,
                    departmentID=departmentID,
                    caption=caption,
                    number=number,
                    floor=floor
                )
                db.session.add(new_classroom)
                db.session.commit()  # Commit the changes to the database
                flash('Classroom added successfully.', "success")
                return redirect(url_for('classrooms_Details'))

    # Fetch all departments to display in the template
    departments = Department.query.all()

    return render_template('classroom/addclassroom.html', departments=departments)




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

