from functools import wraps
import subprocess
import MySQLdb
from flask import Flask, abort, make_response, render_template, request, redirect,url_for,flash,jsonify,send_file
from datetime import date, datetime
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy 
from flask_login import UserMixin
from flask_login import login_user,logout_user,login_manager,LoginManager,login_required,current_user
from fpdf import FPDF
from werkzeug.security import generate_password_hash,check_password_hash
from sqlalchemy import func, text
import streamlit.components.v1 as components
import pdfkit
# Data Base Connection
local_server = True
app = Flask(__name__)
app.secret_key = 'Windows.omar1.2000'

#This is for getting  unique user access

login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(operatorID):
    return Operator.query.get(int(operatorID))

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/ipsattendacne'

db = SQLAlchemy(app)

# Create Data Base Models

class Role(db.Model):
    roleID = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(255), nullable=False,unique=True)

class Operator(UserMixin, db.Model):
    operatorID = db.Column(db.Integer, primary_key=True)
    createBy = db.Column(db.Integer, db.ForeignKey('operator.operatorID'))  # self-referencing relationship
    roleID = db.Column(db.Integer, db.ForeignKey('role.roleID'))  # foreign key relationship
    creationDate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    name = db.Column(db.String(255))
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    
    # Define the relationships
    created_by = db.relationship('Operator', remote_side=[operatorID], backref='creator')
    role = db.relationship('Role', backref='operators')

    # Implement the get_id method to return the operatorID
    def get_id(self):
        return str(self.operatorID)
    
class Lecturer(db.Model):
      lecturerID=db.Column(db.Integer, primary_key=True, nullable=False)
      operatorID = db.Column(db.Integer, db.ForeignKey('operator.operatorID', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
      departmentID = db.Column(db.Integer, db.ForeignKey('department.departmentID', onupdate='CASCADE', ondelete='CASCADE'))
      creationDate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
      gender=db.Column(db.String(255))
      fullname=db.Column(db.String(255))
      deleted=db.Column(db.Boolean,default=False)
    

class faculty(db.Model):
    facultyID = db.Column(db.Integer, primary_key=True, nullable=False)
    operatorID = db.Column(db.Integer, db.ForeignKey('operator.operatorID', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    creationDate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    name = db.Column(db.String(255), unique=True)
    descc = db.Column(db.String(255))
    deleted = db.Column(db.Boolean, default=False)

class Department(db.Model):
    departmentID = db.Column(db.Integer, primary_key=True, nullable=False)
    operatorID = db.Column(db.Integer, db.ForeignKey('operator.operatorID', onupdate='CASCADE', ondelete='CASCADE'))
    facultyID = db.Column(db.Integer, db.ForeignKey('faculty.facultyID', onupdate='CASCADE', ondelete='CASCADE'))
    creationDate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    name = db.Column(db.String(255), unique=True)
    descc = db.Column(db.String(255))
    deleted = db.Column(db.Boolean, default=False)


class classroom(db.Model):
       classroomID = db.Column(db.Integer, primary_key=True, nullable=False)
       operatorID = db.Column(db.Integer, db.ForeignKey('operator.operatorID', onupdate='CASCADE', ondelete='CASCADE'))
       departmentID = db.Column(db.Integer, db.ForeignKey('department.departmentID',onupdate='CASCADE', ondelete='CASCADE'))#بين قوسين الاسم في قاعدة البيانات
       creationDate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
       caption = db.Column(db.String(255), unique=True)
       number = db.Column(db.Integer, nullable=False, unique=True)
       floor = db.Column(db.Integer, nullable=False)
       deleted = db.Column(db.Boolean, default=False)

class Course(db.Model):
      courseID=db.Column(db.Integer, primary_key=True, nullable=False)
      departmentID = db.Column(db.Integer, db.ForeignKey('department.departmentID',onupdate='CASCADE', ondelete='CASCADE'))#بين قوسين الاسم في قاعدة البيانات
      classroomID=db.Column(db.Integer, db.ForeignKey('classroom.classroomID',onupdate='CASCADE', ondelete='CASCADE'))
      lecturerID=db.Column(db.Integer, db.ForeignKey('lecturer.lecturerID',onupdate='CASCADE', ondelete='CASCADE'))
      operatorID=db.Column(db.Integer, db.ForeignKey('operator.operatorID',onupdate='CASCADE', ondelete='CASCADE'))
      creationDate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
      name=db.Column(db.String(255),unique=True)
      DayOfweek=db.Column(db.String(255))
      startTime = db.Column(db.Time)
      endTime=db.Column(db.Time)
      deleted = db.Column(db.Boolean, default=False)



class Student(db.Model):
    studentID = db.Column(db.Integer, primary_key=True, nullable=False)
    operatorID = db.Column(db.Integer, db.ForeignKey('operator.operatorID',onupdate='CASCADE',ondelete='CASCADE'))
    departmentID = db.Column(db.Integer, db.ForeignKey('department.departmentID', onupdate='CASCADE', ondelete='CASCADE'))
    creationDate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    cardID = db.Column(db.String(255), unique=True)  # Changed from db.Integer(255)
    nationalID = db.Column(db.String(255), unique=True)
    gender = db.Column(db.String(255))
    fullname = db.Column(db.String(255))
    DateOfBirth = db.Column(db.DateTime)
    enrollmentDate = db.Column(db.DateTime)
    phoneNumber = db.Column(db.String(255), unique=True)
    address = db.Column(db.String(255))
    MAC = db.Column(db.String(255), unique=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    deleted = db.Column(db.Boolean, default=False)



      

class beacon(db.Model):
      beaconID=db.Column(db.Integer, primary_key=True, nullable=False)
      operatorID=db.Column(db.Integer, db.ForeignKey('operator.operatorID', onupdate='CASCADE', ondelete='CASCADE'))
      classroomID=db.Column(db.Integer, db.ForeignKey('classroom.classroomID', onupdate='CASCADE', ondelete='CASCADE'))
      creationDate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
      caption=db.Column(db.String(255),unique=True)
      UUID=db.Column(db.String(255),unique=True)
      MAC=db.Column(db.String(255),unique=True)
      deleted = db.Column(db.Boolean, default=False)




class attendancesheet(db.Model):
      
      attendanceID=db.Column(db.Integer, primary_key=True, nullable=False)
      studentID=db.Column(db.Integer, db.ForeignKey('student.studentID', onupdate='CASCADE', ondelete='CASCADE'))
      courseID=db.Column(db.Integer, db.ForeignKey('course.courseID', onupdate='CASCADE', ondelete='CASCADE'))
      timestamp=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
      deleted = db.Column(db.Boolean, default=False)



@app.route('/download/lecturer_report/pdf')
def generate_lecturer_pdf():
    # Fetch lecturer data from the database
    lecturers = Lecturer.query.all()

    # Initialize PDF object
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Set font for the report title
    pdf.set_font("Arial", size=16, style='B')

    # Add title to the report
    pdf.cell(200, 10, txt="Lecturer Data Report", ln=True, align='C')

    # Add date to the report
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, txt=f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align='L')

    # Add lecturer data to the report
    pdf.set_font("Arial", size=12)
    pdf.ln(10)  # Add a new line
    for lecturer in lecturers:
        pdf.cell(0, 10, txt=f"Lecturer ID: {lecturer.lecturerID}", ln=True)

        # Fetch operator name by operator ID
        operator = Operator.query.filter_by(operatorID=lecturer.operatorID).first()
        if operator:
            pdf.cell(0, 10, txt=f"Operator Name: {operator.name}", ln=True)
        else:
            pdf.cell(0, 10, txt="Operator Name: Not found", ln=True)

        # Fetch department name by department ID
        department = Department.query.filter_by(departmentID=lecturer.departmentID).first()
        if department:
            pdf.cell(0, 10, txt=f"Department Name: {department.name}", ln=True)
        else:
            pdf.cell(0, 10, txt="Department Name: Not found", ln=True)

        pdf.cell(0, 10, txt=f"Creation Date: {lecturer.creationDate}", ln=True)
        pdf.cell(0, 10, txt=f"Gender: {lecturer.gender}", ln=True)
        pdf.cell(0, 10, txt=f"Full Name: {lecturer.fullname}", ln=True)
        pdf.cell(0, 10, txt=f"Deleted: {lecturer.deleted}", ln=True)
        pdf.ln(10)  # Add a new line

    # Create a response with PDF content
    response = make_response(pdf.output(dest='S').encode('latin1'))
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=lecturer_report.pdf'

    return response




@app.route('/download/student_report/pdf', methods=['GET', 'POST'])
def download_student_report():
    # Fetch student data from the database
    students = Student.query.all()

    # Initialize PDF object
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Set font for the report title
    pdf.set_font("Arial", size=16, style='B')

    # Add title to the report
    pdf.cell(200, 10, txt="Student Data Report", ln=True, align='C')

    # Add date to the report
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, txt=f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align='L')

    # Add student data to the report
    pdf.set_font("Arial", size=12)
    pdf.ln(10)  # Add a new line
    for student in students:
        pdf.cell(0, 10, txt=f"Student ID: {student.studentID}", ln=True)
        
        # Fetch operator name by operator ID
        operator = Operator.query.filter_by(operatorID=student.operatorID).first()
        if operator:
            pdf.cell(0, 10, txt=f"Operator Name: {operator.name}", ln=True)
        else:
            pdf.cell(0, 10, txt="Operator Name: Not found", ln=True)
        
        # Fetch department name by department ID
        department = Department.query.filter_by(departmentID=student.departmentID).first()
        if department:
            pdf.cell(0, 10, txt=f"Department Name: {department.name}", ln=True)
        else:
            pdf.cell(0, 10, txt="Department Name: Not found", ln=True)

        pdf.cell(0, 10, txt=f"Creation Date: {student.creationDate}", ln=True)
        pdf.cell(0, 10, txt=f"Card ID: {student.cardID}", ln=True)
        pdf.cell(0, 10, txt=f"National ID: {student.nationalID}", ln=True)
        pdf.cell(0, 10, txt=f"Gender: {student.gender}", ln=True)
        pdf.cell(0, 10, txt=f"Full Name: {student.fullname}", ln=True)
        pdf.cell(0, 10, txt=f"Date of Birth: {student.DateOfBirth}", ln=True)
        pdf.cell(0, 10, txt=f"Enrollment Date: {student.enrollmentDate}", ln=True)
        pdf.cell(0, 10, txt=f"Phone Number: {student.phoneNumber}", ln=True)
        pdf.cell(0, 10, txt=f"Address: {student.address}", ln=True)
        pdf.cell(0, 10, txt=f"MAC: {student.MAC}", ln=True)
        pdf.cell(0, 10, txt=f"Email: {student.email}", ln=True)
        pdf.cell(0, 10, txt=f"Deleted: {student.deleted}", ln=True)
        pdf.ln(10)  # Add a new line

    # Create a response with PDF content
    response = make_response(pdf.output(dest='S').encode('latin1'))
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=student_report.pdf'

    return response







@app.route('/download/report/pdf', methods=['GET', 'POST'])
def download_report():
    # Fetch beacon data from the database
    beacons = beacon.query.all()

    # Initialize PDF object
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Set font for the report title
    pdf.set_font("Arial", size=16, style='B')

    # Add title to the report
    pdf.cell(200, 10, txt="Beacon Data Report", ln=True, align='C')

    # Add date to the report
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, txt=f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align='L')

    # Add beacon data to the report
    pdf.set_font("Arial", size=12)
    pdf.ln(10)  # Add a new line
    for beacon1 in beacons:
        pdf.cell(0, 10, txt=f"Beacon ID: {beacon1.beaconID}", ln=True)
        
        # Fetch operator name by operator ID
        operator = Operator.query.filter_by(operatorID=beacon1.operatorID).first()
        if operator:
            pdf.cell(0, 10, txt=f"Operator Name: {operator.name}", ln=True)
        else:
            pdf.cell(0, 10, txt="Operator Name: Not found", ln=True)
        
        # Fetch classroom name by classroom ID
        classroom1 = classroom.query.filter_by(classroomID=beacon1.classroomID).first()
        if classroom1:
            pdf.cell(0, 10, txt=f"Classroom Number: {classroom1.number}", ln=True)
        else:
            pdf.cell(0, 10, txt="Classroom Number: Not found", ln=True)

        pdf.cell(0, 10, txt=f"Creation Date: {beacon1.creationDate}", ln=True)
        pdf.cell(0, 10, txt=f"Caption: {beacon1.caption}", ln=True)
        pdf.cell(0, 10, txt=f"UUID: {beacon1.UUID}", ln=True)
        pdf.cell(0, 10, txt=f"MAC: {beacon1.MAC}", ln=True)
        pdf.cell(0, 10, txt=f"Deleted: {beacon1.deleted}", ln=True)
        pdf.ln(10)  # Add a new line

    # Create a response with PDF content
    response = make_response(pdf.output(dest='S').encode('latin1'))
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=beacon_report.pdf'

    return response






def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.roleID != 1:
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


      



@app.route('/')
def index():
    return render_template('index.html')




@app.route('/faculty_Details')
@login_required
@admin_required
def faculty_Details():
    query = faculty.query.all()
    operator_names = {}  #
    operators = Operator.query.all()
    for operator in operators:
        operator_names[operator.operatorID] = operator.name  # Use operator.operatorID, not Operator.operatorID
    
    return render_template('facultiesMethod/faculty.html', query=query, operator_names=operator_names)



@app.route("/facultyedit/<int:facultyID>", methods=['GET', 'POST'])
@login_required
def facultyedit(facultyID):

    faculty1 = faculty.query.filter_by(facultyID=facultyID).first()

    if request.method == 'POST':
        operatorID = request.form.get('operatorID')
        creationDate = request.form.get('creationDate')
        name = request.form.get('name')
        descc = request.form.get('descc')
        deleted = request.form.get('deleted')
        deleted = deleted.lower() == 'true'
        # Update the fields
        if faculty1 is not None:
           faculty1.operatorID = operatorID
           faculty1.creationDate = datetime.strptime(creationDate, '%Y-%m-%d')
           faculty1.name = name
           faculty1.descc = descc
           faculty1.deleted = deleted

        # Commit the changes to the database
        db.session.commit()

        # Redirect to a success page or another route
        flash('Faculty updated successfully.', 'success')
        return redirect(url_for('faculty_Details'))

    # Render the form template for GET requests
    return render_template('facultiesMethod/facultyedit.html', faculty1=faculty1, facultyID=facultyID)



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
    return render_template('facultiesMethod/faculty.html')

    

@app.route('/addfaculty',methods=['POST','GET'])
@login_required
def addfaculty():
     
    if request.method == 'POST':
        operatorID = current_user.operatorID
        name = request.form.get('name')
        descc = request.form.get('descc')
        new_faculty = faculty.query.filter_by(name=name).first()


        if new_faculty:
            flash("Faculty already exists.", "warning")
        else:
            # Create a new Lecturer instance and add it to the session
            new_faculty = faculty(
                operatorID=operatorID,
                name=name,
                descc=descc,
            )
            
            db.session.add(new_faculty)
            db.session.commit()  # Commit the changes to the database
            flash('Faculty  successfully Added.', "success")

    return render_template('facultiesMethod/addfaculty.html')










 



@app.route('/DepartmentDetails')
@login_required
@admin_required
def Department_Details():
    query=Department.query.all()
    operators = Operator.query.all()
    faculties = faculty.query.all()
    
    operator_names = {operator.operatorID: operator.name for operator in operators}
    faculty_names = {faculty.facultyID: faculty.name for faculty in faculties}
    
    return render_template('departmentMethod/department.html', query=query, operator_names=operator_names, faculty_names=faculty_names)




@app.route("/departmentedit/<int:departmentID>", methods=['GET', 'POST'])
@login_required
def departmentedit(departmentID):
    department1 = Department.query.filter_by(departmentID=departmentID).first()
    faculties = faculty.query.all()  # Fetch all faculties from the database
    departments = Department.query.all()  # Fetch all departments from the database
    operators = Operator.query.all()
    if request.method == 'POST':
        # Retrieve form data
        operatorID = request.form.get('operatorID')
        facultyID = request.form.get('facultyID')
        creationDate = request.form.get('creationDate')
        name = request.form.get('name')
        descc = request.form.get('descc')
        deleted = request.form.get('deleted')
        deleted = deleted.lower() == 'true'

        # Update the fields
        if department1 is not None:
            department1.operatorID = operatorID
            department1.facultyID = facultyID
            department1.creationDate = datetime.strptime(creationDate, '%Y-%m-%d')
            department1.name = name
            department1.descc = descc
            department1.deleted = deleted

            # Commit the changes to the database
            db.session.commit()

            # Redirect to a success page or another route
            flash('Department updated successfully.', 'success')
            return redirect(url_for('Department_Details'))

    # Render the form template for GET requests and POST requests that fail validation
    return render_template('departmentMethod/departmentedit.html', department1=department1, departmentID=departmentID, faculties=faculties, departments=departments, operators=operators)







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
    return render_template('departmentMethod/department.html')


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

    return render_template('departmentMethod/adddepartment.html', faculties=faculties)














@app.route('/classroomsDetails')
def classrooms_Details():
   opreators=Operator.query.all()
   departments=Department.query.all()
   query=classroom.query.all()

   operator_names = {operator.operatorID: operator.name for operator in opreators}
   department_names = {department.departmentID: department.name for department in departments}
      
       
   return render_template('classroomMethod/classrooms.html',query=query,operator_names=operator_names,department_names=department_names)





@app.route("/classroomedit/<int:classroomID>", methods=['GET', 'POST'])
@login_required
def classroomedit(classroomID):
    classroom1 = classroom.query.filter_by(classroomID=classroomID).first()

    if request.method == 'POST':
        operatorID = request.form.get('operatorID')
        departmentID = request.form.get('departmentID')
        creationDate = request.form.get('creationDate')
        caption = request.form.get('caption')
        number = request.form.get('number')
        floor = request.form.get('floor')
        deleted = request.form.get('deleted')
        deleted = deleted.lower() == 'true'
        
        # Update the fields
        if classroom1 is not None:
           classroom1.operatorID = operatorID
           classroom1.departmentID = departmentID
           classroom1.creationDate = datetime.strptime(creationDate, '%Y-%m-%d')
           classroom1.caption = caption
           classroom1.number = number
           classroom1.floor = floor
           classroom1.deleted = deleted

        # Commit the changes to the database
        db.session.commit()

        # Redirect to a success page or another route
        flash('ClassRoom updated successfully.', 'success')
        return redirect(url_for('classrooms_Details'))

    # Fetch operators and departments from the database
    operators = Operator.query.all()
    departments = Department.query.all()

    # Render the form template for GET requests
    return render_template('classroomMethod/classroomedit.html', classroom1=classroom1, classroomID=classroomID, operators=operators, departments=departments)


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
            flash("Classroom already exists.", "warning")
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

    return render_template('classroomMethod/addclassroom.html', departments=departments)




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



        return render_template('classroomMethod/classrooms.html')






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
        operatorID = request.form.get('operatorID')
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
           course1.operatorID = operatorID
           course1.creationDate = datetime.strptime(creationDate, '%Y-%m-%d')
           course1.name = name
           course1.DayOfweek = DayOfweek
           course1.startTime = startTime
           course1.endTime = endTime

        # Commit the changes to the database
        db.session.commit()

        # Redirect to a success page or another route
        flash('Course updated successfully.', 'success')
        return redirect(url_for('Courses'))

    # Fetch operators, departments, and classrooms from the database
    departments = Department.query.all()
    lecturers = Lecturer.query.all()
    classrooms = classroom.query.all()

    # Render the form template for GET requests
    return render_template('courese/editcourse.html', course1=course1, courseID=courseID, departments=departments, lecturers=lecturers, classrooms=classrooms)












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

  
    
















@app.route('/students',methods=['POST', 'GET'])
@login_required
def students():
    departments = Department.query.all()
    if request.method == 'POST':
        # Create a new Student instance with the provided data
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

        new_student = Student.query.filter_by(email=email).first()

        if new_student:
            flash("Username already exists", "warning")
            return render_template('/students.html')

        encpassword = generate_password_hash(password)

        sql_query = text("INSERT INTO `Student` (`operatorID`, `departmentID`, `cardID`, `nationalID`, `gender`, `fullname`, `DateOfBirth`, `enrollmentDate`, `phoneNumber`, `address`, `MAC`, `email`, `password`) VALUES (:operatorID, :departmentID, :cardID, :nationalID, :gender, :fullname, :DateOfBirth, :enrollmentDate, :phoneNumber, :address, :MAC, :email, :encpassword)")

        params = {
            'operatorID': operatorID,
            'departmentID': departmentID,
            'cardID': cardID,
            'nationalID': nationalID,
            'gender': gender,
            'fullname': fullname,
            'DateOfBirth': DateOfBirth,
            'enrollmentDate': enrollmentDate,
            'phoneNumber': phoneNumber,
            'address': address,
            'MAC': MAC,
            'email': email,
            'encpassword': encpassword,
        }

        new_student = db.session.execute(sql_query, params)

        db.session.commit()  # Commit the changes to the database
        flash('Student Add Success ', "success")

    return render_template('/addstudents.html', departments=departments)



@app.route('/details')

def Details():
       

       departments=Department.query.all()
       operators=Operator.query.all()
       query = Student.query.all()

       department_names = {department.departmentID: department.name for department in departments}
       operator_names = {operator.operatorID: operator.name for operator in operators}
       
       return render_template('details.html', query=query,department_names=department_names,operator_names=operator_names)



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
    return render_template('edit.html', student=student, studentID=studentID,opreators=opreators,departments=departments)


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


      

   


@app.route('/some_redirect_route')
def some_redirect_route():
    # Your route logic here
    return "Hello, this is the redirect route!"




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

    if request.method == 'POST':
        operatorID = request.form.get('operatorID')
        classroomID=request.form.get('classroomID')  
        creationDate = request.form.get('creationDate')
        caption = request.form.get('caption')
        UUID = request.form.get('UUID')
        MAC = request.form.get('MAC')
      
        # Update the fields
        if beacon1 is not None:
           beacon1.operatorID = operatorID
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
    return render_template('beacons/beaconsedit.html', beacon1=beacon1, beaconID=beaconID)










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
    }

    return render_template('dashboard.html', attendance_chart_data=attendance_chart_data, student_chart_data=student_chart_data)











@app.route('/signUp', methods=['POST', 'GET'])
def signup():
    if request.method == "POST":
        if current_user.is_authenticated and current_user.roleID == 1:  # Check if the user is authenticated and has roleID 1
            createBy = current_user.createBy  
        else:
            # Handle the case where the user is not authenticated or doesn't have the required role
            flash("You must be logged in as an admin to sign up", "warning")
            return redirect(url_for('login'))  

        # Assuming you have a mapping of role IDs to role names
        role_names = {
            1: "Admin",
            2: "User",
            # Add more role IDs and their corresponding names as needed
        }

        roleID = request.form.get('roleID')
        role_string = role_names.get(int(roleID), "Unknown")  # Get the role name based on the roleID

        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        user = Operator.query.filter_by(username=username).first()

        if user:
            flash("Username already exists", "warning")
            return render_template('signup.html')  # Redirect to the signup page to provide feedback

        encpassword = generate_password_hash(password)

        # Escape single quote in the username field by doubling it
        username = username.replace("'", "''")

        sql_query = text(f"INSERT INTO `Operator` (`createBy`, `roleID`, `name`, `username`, `password`) VALUES ('{createBy}', '{roleID}', '{name}', '{username}', '{encpassword}')")
      
        new_user = db.session.execute(sql_query)
        db.session.commit()  # Commit the changes to the database
        flash('Sign Up Success. Please Login', "success")
        return render_template('login.html')

    return render_template('signup.html')












# Apply the admin_required decorator to the login route
@app.route('/login', methods=['POST', 'GET'])

def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        user = Operator.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            if user.roleID is not None:
                role = Role.query.get(user.roleID)
                if role.name == 'admin':
                    return redirect(url_for('index'))
                elif role.name == 'superadm':
                    return redirect(url_for('dashboard'))
        
        flash('Password or Username is not correct', 'danger')
        return redirect(url_for('login'))

    return render_template('login.html')




@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logout SuccessFul" ,"warning")
    return redirect(url_for('login'))


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



app.run(debug=True)
