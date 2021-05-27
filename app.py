from flask import Flask ,jsonify , Response , request , make_response
from flask_migrate import Migrate
from flask_login import current_user, login_user ,login_required , logout_user
from flask_cors import CORS

from models import db,login_manager,User
from auth import auth_blue_print as auth_app
from userDocs import userDocsBluePrint as userDocs_app
import os

app = Flask(__name__)

#app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///students.sqlite3"
#app.config["SECRET_KEY"] = "gMn55Y6kT79N4mwcFhwu7"

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL").replace("postgres://","postgresql://")
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]

db.init_app(app)
login_manager.init_app(app)
migrate = Migrate(app, db,compare_type=True)
#CORS(app,resources={r'/*':{'origins':"*"}})

#======================ATTACHING BLUEPRINTS==================
##AUTH HANDLER
app.register_blueprint(blueprint=auth_app,url_prefix="/auth")
##Credentials Manager
app.register_blueprint(blueprint=userDocs_app,url_prefix="/userDocs")

@app.route("/")
def hello():
    return "Website version Not yet developed"

if __name__=="__main__":
    app.run(host="0.0.0.0")

