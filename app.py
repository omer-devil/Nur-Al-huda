# =========================================================================== #
# Author: Omer Kemal                                                          #
# Social Media:                                                               #
#   - Facebook: https://web.facebook.com/omer.kemal.7                         #
#   - GitHub: https://github.com/omer-devil                                   #
# =========================================================================== #
from flask import Flask

from admin.Admin import Admin
from login.login import Login
from student.Student import Student
from teacher.Teacher import Teachters
from public.public import public
from event.event import event
from database.manage_db import var


app = Flask(__name__)
var.setting_var()

app.secret_key = var.SECRAT_KEY

app.register_blueprint(public)
app.register_blueprint(event)
app.register_blueprint(Teachters)
app.register_blueprint(Admin)
app.register_blueprint(Student)
app.register_blueprint(Login)


if __name__ == '__main__':
    app.run(debug=True)
