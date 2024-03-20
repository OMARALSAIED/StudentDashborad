from decorators import app
from MysqlModels.models import Department, Student, faculty
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
    


@app.route('/Departments', methods=['POST'])
def Departments():
    search_query = request.form.get('search')
    search_results = None  # Initialize the variable outside the if-else block
    if search_query:
        # Perform the search using the Department model's query method
        search_results = Department.query.filter(Department.name.ilike(f"%{search_query}%")).all()
        return render_template('SearchTemplates/Departmnets.html', results=search_results)
    else:
        return render_template('SearchTemplates/Departmnets.html', results=search_results)

    



@app.route('/search', methods=['POST'])
def search():
    search_query = request.form.get('search')
    if search_query:
        # Perform the search using the Student model's search_by_name method
        search_results = Student.query.filter(Student.fullname.ilike(f"%{search_query}%")).all()
        return render_template('SearchTemplates/Students.html', results=search_results)
    else:
        return render_template('SearchTemplates/Students.html', results=search_results)
    


