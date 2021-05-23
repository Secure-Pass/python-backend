from flask_login import current_user, login_user ,login_required , logout_user
from flask import Blueprint , jsonify , Response , request , make_response
from flask_sqlalchemy import BaseQuery
from .models import User , db , CredentialDocs

auth_blue_print = Blueprint('auth',__name__)


@auth_blue_print.route("/login",methods=['POST'])
def login():
    UserQuery:BaseQuery = User.query
    if request.method == "POST" :
        if current_user.is_authenticated :

            return make_response(
                    jsonify(msg="ALREADY_LOGGED_IN"),
                200
                )
        else:
            args = request.form
            email = args['email']
            password = args['password']

            if(None in (email,password)):

                return make_response(
                        jsonify(msg="BAD_REQUEST"),
                        400
                        )

            user = UserQuery.filter_by(email=email).first()
            if user is not None and user.check_password(password):
                login_user(user)
                return make_response(
                        jsonify(msg="OK"),
                        200
                        )
            else:
                return make_response(
                        jsonify(msg="FAILED"),
                        200
                        )
    #TODO:render login screen on GET request

@auth_blue_print.route("/register",methods=["POST"])
def register():
    UserQuery:BaseQuery = User.query

    if request.method == "POST":
        args = request.form
        email = args["email"]
        password = args["password"]
        encryptedEncryptionKey = args["encryptedEncryptionKey"]

        if(None in (email,password,encryptedEncryptionKey)):
            return make_response(
                    jsonify(msg="BAD_REQUEST"),
                    400
                    )

        if UserQuery.filter_by(email=email).first():
            return make_response(
                    jsonify(msg="ACCOUNT_EXISTS"),
                    200
                    )
        else:

            user = User(email=email)
            user.set_password(password)

            creds = CredentialDocs(
                    domainname="encryptedEncryptionKey",
                    credentials = encryptedEncryptionKey,
                    owner = user
                    )

            db.session.add(user)
            db.session.add(creds)
            db.session.commit()

            return make_response(
                    jsonify(msg="OK"),
                    200
                    )
    ##TODO:Render page in get request

@auth_blue_print.route("/logout",methods=["POST"])
@login_required
def logout():
    print(logout_user())
    return make_response(
            jsonify(msg="OK"),
            200
            )
