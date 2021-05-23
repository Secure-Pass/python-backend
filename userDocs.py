from flask_login import current_user, login_user ,login_required , logout_user
from flask import Blueprint , jsonify , Response , request , make_response
from flask_sqlalchemy import BaseQuery
from .models import db , CredentialDocs , User
from sys import stdout
from datetime import datetime

userDocsBluePrint = Blueprint('userDocs',__name__)

@userDocsBluePrint.route("/addOrUpdateDoc",methods=["POST"])
@login_required
def addDoc():
    CredentialDocsQuery:BaseQuery = CredentialDocs.query
    args = request.form
    domainname = args["domainname"]
    credentials = args["credentials"]
    
    if(None in (domainname,credentials)):
        return make_response(
                jsonify(
                    msg="BAD_REQUEST"
                    ),
                400
                )
    doc:CredentialDocs = CredentialDocsQuery.filter_by(owner=current_user,domainname=domainname).first()

    if (doc):#Update
        doc.credentials = credentials
        doc.lastUpdateTimeStamp =datetime.utcnow().timestamp()
        db.session.commit()

    else:#Insert
        credential = CredentialDocs(
                domainname=domainname,
                credentials=credentials,
                owner=current_user,
                lastUpdateTimeStamp = datetime.utcnow().timestamp()
                )
        db.session.add(credential)
        db.session.commit()

    return make_response(
        jsonify(
            msg="OK"
        ),
        200
    )

@userDocsBluePrint.route("/newDocsSince/<int:lastUpdate>",methods=["POST"])
@login_required
def listDocs(lastUpdate:int=0):
    CredentialDocsQuery:BaseQuery = CredentialDocs.query
    results = list(
                CredentialDocsQuery.filter_by(
                    owner=current_user
                ).filter(
                    CredentialDocs.lastUpdateTimeStamp > lastUpdate
                ).with_entities(
                    CredentialDocs.domainname,
                    CredentialDocs.lastUpdateTimeStamp,
                    CredentialDocs.credentials
                ).all()
               )

    out = [
            {
                "domainname":x.domainname,
                "doc":x.credentials,
                "lastUpdateTimeStamp":int(x.lastUpdateTimeStamp)
            }
            for x in results
        ]
    return make_response(
            jsonify(
                msg="OK",
                body=out
                ),
            200
            )

@userDocsBluePrint.route("/",methods=["GET"])
def userDocsPage():
    #TODO:To render page here
    return "Under Construction"
