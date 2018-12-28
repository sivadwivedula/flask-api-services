from flask import Flask, jsonify
import datetime
import jwt
import db
from flask.globals import request

#returns  the auth taken 
#encode(userid) will return a token valid for 45 seconds
def encode(user_id):
   
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=45),
            'id': user_id
        }
        return jwt.encode(
            payload,
            "shiva",
            algorithm='HS256'
        )
    except Exception as e:
        return e


#decodes the auth token and return the encoded data
#decode(token) will return userid
#if expired will return False
def decode(auth_token):
    """
    Decodes the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        payload = jwt.decode(auth_token, "shiva")
        return payload['id']
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False
    
    
    
    
    
    




#making flask object
app = Flask(__name__)


#method login bound to route http://server:port/login
#POST datainput -> form [{empid:empid},{emp_password:emp_password}]
#will return token for the emp_id valid for the particular time 
@app.route('/login',methods=['POST'])
def login():
    emp_id=request.form['emp_id']
    emp_password=request.form['emp_password']
    
    row_length=db.login(emp_id,emp_password).__len__()
    if (row_length==1):
        token=encode(emp_id).decode()
        return jsonify({'token':token})
    else:
        return "false"

#method signup bound to route http://server:port/signup
#POST datainput -> form [{empid:empid},{emp_password:emp_password},{emp_name:emp_name},{emp_age:emp_age}]
#will return success if created or else will return failed    
@app.route('/signup',methods=['POST'])
def signup():
    emp_id=request.form['emp_id']
    emp_password=request.form['emp_password']
    emp_name=request.form['emp_name']
    emp_age=request.form['emp_age']
    try:
        success=db.signup(emp_id, emp_password, emp_name, emp_age)
        if success:
            return "success"
        else:
            return "failed"

    except:
        return "failed"



#method getdetails bound to route http://server:port/retrieve/emp_id
#will return employe data as json  , if no data available will return failed
@app.route('/retrieve/<emp_id>',methods=['GET'])
def getdetails(emp_id):
        details=db.query(str(emp_id))
        return jsonify({'details':details})

#method verifytoken bound to route http://server:port/verify
#POST datainput -> form [{empid:empid},{token:token}]
#will return success if token is alive , or else will return failed if token is expired    
@app.route('/verify',methods=['POST'])
def verifytoken():
    emp_id=request.form['emp_id']
    token=request.form['token']
    check=emp_id==decode(token)
    if check:
        return "success"
    else:
        return "failed"
    
if (__name__ == '__main__'):       
    app.run(debug=True)



