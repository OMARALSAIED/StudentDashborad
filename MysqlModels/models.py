from datetime import  datetime
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.orm import relationship

db = SQLAlchemy()

class Role(db.Model):
    roleID = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(255), nullable=False, unique=True)





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
    deleted = db.Column(db.Boolean, default=False, onupdate='CASCADE')
    



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
    attendanceID = db.Column(db.Integer, primary_key=True, nullable=False)
    studentID = db.Column(db.Integer, db.ForeignKey('student.studentID', onupdate='CASCADE', ondelete='CASCADE'))
    courseID = db.Column(db.Integer, db.ForeignKey('course.courseID', onupdate='CASCADE', ondelete='CASCADE'))
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    deleted = db.Column(db.Boolean, default=False)



