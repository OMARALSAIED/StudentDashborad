
from decorators import app
from routes.Dashboard import Dashboard
from routes.Auth import Auth
from decorators import api
from routes.Reports import Report
from routes.DetalsRoutes import DetalsRoutes
from routes.Restful_Api import GetCourseNametest
from routes.Addfun import Addfun
from routes.Editfun import Editfun
from routes.Deletefun import Deletefun
local_server = True


app.register_blueprint(Dashboard)
app.register_blueprint(Auth)
app.register_blueprint(Report)
app.register_blueprint(DetalsRoutes)
app.register_blueprint(Addfun)
app.register_blueprint(Editfun)
app.register_blueprint(Deletefun)


api.add_resource(GetCourseNametest,'/get_course_name_test')

app.run(debug=True)

