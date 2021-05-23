from flask import Flask ,jsonify , Response , request , make_response
from flask_migrate import Migrate
from flask_login import current_user, login_user ,login_required , logout_user


from .models import db,login_manager,User
from .auth import auth_blue_print as auth_app
from .userDocs import userDocsBluePrint as userDocs_app

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///students.sqlite3"
app.config["SECRET_KEY"] = "gMn55Y6kT79N4mwcFhwu7"

db.init_app(app)
login_manager.init_app(app)
migrate = Migrate(app, db)


#======================ATTACHING BLUEPRINTS==================
##AUTH HANDLER
app.register_blueprint(blueprint=auth_app,url_prefix="/auth")
##Credentials Manager
app.register_blueprint(blueprint=userDocs_app,url_prefix="/userDocs")

if __name__=="__main__":
    app.run(debug=True)

