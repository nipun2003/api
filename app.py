from crypt import methods
from flask import Flask,jsonify,request
from include import dbHandler 
import userController as usCtrl

app = Flask(__name__)
userControll = usCtrl.UserController(app)

@app.route('/')
def route():
    return "Hello World"

@app.route('/check_phone',methods =['POST'])
def checkPhone():
    req = request.args.get('phone')
    result = userControll.checkPhone(req)
    return jsonify(result)

@app.route('/verify_otp')
def verifyOtp():
    phone = request.args.get('phone')
    otp = request.args.get('otp')
    result = userControll.verifyOtp(phone=phone,otp=otp)
    return jsonify(result)

@app.route('/register',methods = ['POST'])
def registerUser():
    name = request.args.get('name')
    otp = request.args.get('otp')
    phone = request.args.get('phone')
    password = request.args.get('password')
    email = request.args.get('email')

    result = userControll.createUser(otp=otp,name=name,phone=phone,password=password,email=email)
    return jsonify(result)


if __name__=="__main__":
    app.run(debug=True, port=8000)
