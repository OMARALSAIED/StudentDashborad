
from api.Restful_api import AttendanceList,FindConflictingCourseResource
from Serach.Searchfun import Search
from api.User_Auth import LoginResource, StudentResource, User_Auth
from decorators import  app
from routes.Dashboard import Dashboard
from routes.Auth import Auth
from decorators import api
from routes.Reports import Report
from routes.DetalsRoutes import DetalsRoutes
from routes.Addfun import Addfun
from routes.Editfun import Editfun
from routes.Deletefun import Deletefun
local_server = True

app.register_blueprint(User_Auth)
app.register_blueprint(Dashboard)
app.register_blueprint(Auth)
app.register_blueprint(Report)
app.register_blueprint(DetalsRoutes)
app.register_blueprint(Addfun)
app.register_blueprint(Editfun)
app.register_blueprint(Deletefun)
app.register_blueprint(Search)
api.add_resource(AttendanceList, '/attendance')
api.add_resource(FindConflictingCourseResource, '/find_conflicting_course')
api.add_resource(StudentResource, '/api/student', '/api/student/<int:student_id>')
api.add_resource(LoginResource, '/api/login')




app.run(debug=True)

