
import datetime
from flask import Blueprint, flash, redirect, request, url_for,render_template
from flask_login import current_user, login_required
from decorators import app,admin_required
from MysqlModels.models import Course, Department, Lecturer, Operator, Role, Student, attendancesheet, beacon, classroom,faculty
from MysqlModels.models import db


Editfun=Blueprint("Editfun",__name__)



@app.route("/facultyedit/<int:facultyID>", methods=['GET', 'POST'])
@login_required
def facultyedit(facultyID):

    faculty1 = faculty.query.filter_by(facultyID=facultyID).first()

    if request.method == 'POST':
       
        
        name = request.form.get('name')
        descc = request.form.get('descc')
        
        # Update the fields
        if faculty1 is not None:
           
           faculty1.name = name
           faculty1.descc = descc
           

        # Commit the changes to the database
        db.session.commit()

        # Redirect to a success page or another route
        flash('Faculty updated successfully.', 'success')
        return redirect(url_for('faculty_Details'))

    # Render the form template for GET requests
    return render_template('faculties/facultyedit.html', faculty1=faculty1, facultyID=facultyID)





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
        name = request.form.get('name')
        descc = request.form.get('descc')
       

        # Update the fields
        if department1 is not None:
            department1.facultyID = facultyID
           
            department1.name = name
            department1.descc = descc

            # Commit the changes to the database
            db.session.commit()

            # Redirect to a success page or another route
            flash('Department updated successfully.', 'success')
            return redirect(url_for('Department_Details'))

    # Render the form template for GET requests and POST requests that fail validation
    return render_template('department/departmentedit.html', department1=department1, departmentID=departmentID, faculties=faculties, departments=departments, operators=operators)




@app.route("/classroomedit/<int:classroomID>", methods=['GET', 'POST'])
@login_required
def classroomedit(classroomID):
    classroom1 = classroom.query.filter_by(classroomID=classroomID).first()

    if request.method == 'POST':
       
        departmentID = request.form.get('departmentID')
      
        caption = request.form.get('caption')
        number = request.form.get('number')
        floor = request.form.get('floor')
      
        # Update the fields
        if classroom1 is not None:
         
           classroom1.departmentID = departmentID
            # Adjust format here
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



@app.route("/courseedit/<int:courseID>", methods=['GET', 'POST'])
@login_required
def courseedit(courseID):
    course1 = Course.query.filter_by(courseID=courseID).first()

    if request.method == 'POST':
        departmentID = request.form.get('departmentID')
        classroomID = request.form.get('classroomID')
        lecturerID = request.form.get('lecturerID')
        
        
        name = request.form.get('name')
        DayOfweek = request.form.get('DayOfweek')
        startTime = request.form.get('startTime')
        endTime = request.form.get('endTime')
        
        # Update the fields
        if course1 is not None:
           course1.departmentID = departmentID
           course1.classroomID = classroomID
           course1.lecturerID = lecturerID
          
    
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




@app.route("/edit/<string:studentID>", methods=['GET', 'POST'])
@login_required
def edit(studentID):
    student = Student.query.filter_by(studentID=studentID).first()

    if request.method == 'POST':
        
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




@app.route("/attendaceedit/<int:attendanceID>", methods=['GET', 'POST'])
@login_required
def attendaceedit(attendanceID):
    attendace1 = attendancesheet.query.get_or_404(attendanceID)
    students=Student.query.all()
    courese=Course.query.all()

    if request.method == 'POST':
        studentID = request.form.get('studentID')
        courseID = request.form.get('courseID')
        
       

        # Update the fields
        if attendace1 is not None:
           attendace1.studentID = studentID
           attendace1.courseID = courseID
            
        # Commit the changes to the database
        db.session.commit()

        # Redirect to a success page or another route
        flash('Attendance updated successfully.', 'success')
        return redirect(url_for('attendance', attendanceID=attendanceID))
    

    # Render the form template for GET requests
    return render_template('attendance/attendaceedit.html', attendace1=attendace1, attendanceID=attendanceID,students=students,courese=courese)

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