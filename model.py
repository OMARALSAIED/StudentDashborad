
import datetime
from main import app
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/ipsattendacne'
db = SQLAlchemy(app)
class attendancesheet(db.Model):
      
      attendanceID=db.Column(db.Integer, primary_key=True, nullable=False)
      studentID=db.Column(db.Integer, db.ForeignKey('student.studentID', onupdate='CASCADE', ondelete='CASCADE'))
      courseID=db.Column(db.Integer, db.ForeignKey('course.courseID', onupdate='CASCADE', ondelete='CASCADE'))
      timestamp=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
      deleted = db.Column(db.Boolean, default=False)