
from decorators import app
from routes.Allroutes import Allroutes
from routes.Auth import Auth
from decorators import api
from routes.Reports import Report
from routes.Restful_Api import AttendanceTracking


local_server = True


app.register_blueprint(Allroutes)
app.register_blueprint(Auth)
app.register_blueprint(Report)



api.add_resource(AttendanceTracking, '/api/attendance_tracking')


app.run(debug=True)

