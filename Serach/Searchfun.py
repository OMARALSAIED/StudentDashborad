from decorators import app
from MysqlModels.models import Course, Department, Lecturer, Student, attendancesheet, beacon, classroom, faculty
from flask import Blueprint, render_template,request


Search=Blueprint("Search",__name__)









@app.route('/faculties', methods=['POST'])
def faculties():
    search_query = request.form.get('search')
    if search_query:
        # Perform the search using the Student model's search_by_name method
        search_results = faculty.query.filter(faculty.name.ilike(f"%{search_query}%")).all()
        return render_template('SearchTemplates/Facultys.html', results=search_results)
    else:
        return render_template('SearchTemplates/Facultys.html', results=search_results)
    


@app.route('/Departmentsearch', methods=['POST'])
def Departmentsearch():
    search_query = request.form.get('search')  # Corrected the form field name
    getfacultyn =faculty.query.all()
    faculty_names = {faculty.facultyID: faculty.name for faculty in getfacultyn}
    if search_query:
        # Perform the search using the Department model's query method
        search_results = Department.query.filter(Department.name.ilike(f"%{search_query}%")).all()
        return render_template('SearchTemplates/Departmnetsearch.html', results=search_results,faculty_names=faculty_names)
  
    else:
        return render_template('SearchTemplates/Departmnetsearch.html', results=search_results,faculty_names=faculty_names)
    


@app.route('/coursesearch', methods=['POST'])
def coursesearch():
    departments = Department.query.all()
    classrooms = classroom.query.all()
    lecturers = Lecturer.query.all()
    
    # Creating dictionaries to map IDs to names
    department_names = {department.departmentID: department.name for department in departments}
    classroom_names = {classroom.classroomID: classroom.number for classroom in classrooms}
    lecturer_names = {lecturer.lecturerID: lecturer.fullname for lecturer in lecturers}
    
    search_query = request.form.get('search')
    if search_query:
        # Perform the search using the Student model's search_by_name method
        search_results = Course.query.filter(Course.name.ilike(f"%{search_query}%")).all()
        return render_template('SearchTemplates/CourseSearch.html', results=search_results,department_names=department_names,classroom_names=classroom_names,lecturer_names=lecturer_names)
    else:
        return render_template('SearchTemplates/CourseSearch.html', results=search_results,department_names=department_names,classroom_names=classroom_names,lecturer_names=lecturer_names)
    



@app.route('/lecturersearch', methods=['POST'])
def lecturersearch():
    departments=Department.query.all()
    department_names = {department.departmentID: department.name for department in departments}
    search_query = request.form.get('search')
    if search_query:
        # Perform the search using the Student model's search_by_name method
        search_results = Lecturer.query.filter(Lecturer.fullname.ilike(f"%{search_query}%")).all()
        return render_template('SearchTemplates/lecturersearch.html', results=search_results,department_names=department_names)
    else:
        return render_template('SearchTemplates/lecturersearch.html', results=search_results,department_names=department_names)
    

@app.route('/attendancesearch', methods=['POST'])
def attendancesearch():
    search_query = request.form.get('search')
    if search_query:
        # Perform the search using the Student model's search_by_name method
        search_results = attendancesheet.query.filter(attendancesheet.name.ilike(f"%{search_query}%")).all()
        return render_template('SearchTemplates/classroomsearch.html', results=search_results)
    else:
        return render_template('SearchTemplates/classroomsearch.html', results=search_results)
    



@app.route('/beaconsearch', methods=['POST'])
def beaconsearch():
    classrooms=classroom.query.all()
    classroom_names = {classroom.classroomID: classroom.number for classroom in classrooms}
    search_query = request.form.get('search')
    
    
    
   
    if search_query:
        # Perform the search using the Student model's search_by_name method
        search_results = beacon.query.filter(beacon.MAC.ilike(f"%{search_query}%")).all()
        return render_template('SearchTemplates/BeaconSearch.html', results=search_results,classroom_names=classroom_names)
    else:
        return render_template('SearchTemplates/BeaconSearch.html', results=search_results,classroom_names=classroom_names)
    





    


@app.route('/classroomdearch', methods=['POST'])
def classroomdearch():
    search_query = request.form.get('search')
    if search_query:
        # Perform the search using the Student model's search_by_name method
        search_results = classroom.query.filter(classroom.number.ilike(f"%{search_query}%")).all()
        return render_template('SearchTemplates/classroomsearch.html', results=search_results)
    else:
        return render_template('SearchTemplates/classroomsearch.html', results=search_results)





    



@app.route('/search', methods=['POST'])
def search():
    search_query = request.form.get('search')
    if search_query:
        # Perform the search using the Student model's search_by_name method
        search_results = Student.query.filter(Student.fullname.ilike(f"%{search_query}%")).all()
        return render_template('SearchTemplates/Students.html', results=search_results)
    else:
        return render_template('SearchTemplates/Students.html', results=search_results)
    


