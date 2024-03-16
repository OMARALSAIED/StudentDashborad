from flask import Blueprint, render_template,  redirect, url_for, flash
from flask_login import login_required


from MysqlModels.models import Course, Department, Lecturer, Operator, Role, Student, attendancesheet, beacon, classroom,faculty
from decorators import app
from MysqlModels.models import db



Deletefun = Blueprint('Deletefun', __name__)



@app.route('/deletefaculty/<int:facultyID>', methods=['POST', 'GET'])
@login_required
def delete_faculty(facultyID):
    faculty_instance = faculty.query.get(facultyID)

    if faculty_instance:
        # Soft delete the faculty by setting the 'deleted' attribute to True
        faculty_instance.deleted = True
        db.session.commit()
        flash("Faculty successfully marked as deleted", "danger")
        # Redirect to a page or route after successful deletion
        return redirect(url_for('faculty_Details'))  # Replace 'faculty_Details' with the appropriate route

    # If the faculty is not found, you can handle this case accordingly
    flash("Faculty not found", "danger")
    return redirect(url_for('faculty_Details'))


#=================================Department Routes



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






#=================================ClassRoos Routes




from flask import request, redirect, url_for




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


#=================================Lecturer Routes



    

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





#=================================Students Routes






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



#====================================Beacons Routes




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




