from include import dbconnector as dbc,pass_hash as ph,constants
from flask import jsonify
import random
from datetime import datetime
import requests


class DbHandler:
    __conn = 1

    def __init__(self, app) -> None:
        db = dbc.DBConnect(app)
        self.__conn = db.connect()

# -------------------------------------------- User related query ----------------------------------------- #

    def checkPhone(self, phone):
        """The method return true if user is already exist in database otherwise false """
        cur = self.__conn.connection.cursor()
        result = cur.execute(f"SELECT id from users WHERE phone = {phone} ")
        return result > 0

    def createNewSecret(self, phone, a):
        """The method add the otp in database and also send otp to the user phone by calling the sendotp function"""
        cur = self.__conn.connection.cursor()
        otp = random.randint(100000, 999999)
        now = datetime.now()
        date = str(now.strftime("%Y-%m-%d %H:%M:%S"))
        cur.execute(f"""DELETE FROM secret WHERE phone = {phone}""")
        cur.execute(
            """INSERT INTO secret(phone, otp, date, type) values(%s,%s,%s,%s)""", (phone, otp, date, a))
        return self.__sendOtp(phone=phone, otp=otp)

    def createUser(self,name,phone,password,email):
        """
            function for creating new user
        """
        hashMethod = ph.PassHash()
        cur = self.__conn.connection.cursor()
        print(type(phone))
        if(self.__isEmailExist(email=email)):
            return constants.USER_ALREADY_EXISTED
        else:
            passwordHash = hashMethod.hash(password=password)
            print(f"{passwordHash} type is {type(passwordHash)}")
            apiKey = hashMethod.generateApiKey()
            username = self.__createUserName(name=name)
            res = cur.execute("""INSERT INTO users(name, phone, password_hash, email, username, api_key, status) values(%s,%s,%s,%s,%s,%s,%s""",(name,phone,str(passwordHash),email,username,apiKey,1))

            if(res):
                return constants.USER_CREATED_SUCCESSFULLY
            else :
                return constants.USER_CREATE_FAILED



    
    def __createUserName(self,name):
        cur = self.__conn.connection.cursor()
        cur.execute("SELECT COUNT(*) as counts from users")
        res = cur.fetchall()
        userCount = 0
        for item in res:
            userCount = item[0]
        name = name.split(" ")[0]
        return name+str(userCount)
    



    def __isEmailExist(self,email):
        cur = self.__conn.connection.cursor()
        print(email)
        res = cur.execute("""SELECT id FROM users WHERE email = %s""",(email))
        return res>0


# --------------------------------------- Sending the otp --------------------------------------#

    def __sendOtp(self, phone, otp):
        """This function is made for sending the otp to the user phone"""
        url = "http://mysms.sms7.biz/rest/services/sendSMS/sendGroupSms"
        params = {
            "AUTH_KEY": "4ae9995144e1811ffe5b63103151847a",
            "message": f"{otp} is the OTP for ExamHelper. Valid for 15 minutes.\nMsgId: lzrRoj3hcEz",
            "senderId": "EXMHLP",
            "routeId": '8',
            "mobileNos": phone,
            "smsContentType": 'english'
        }
        res = requests.get(url=url, params=params)
        result = res.json()
        # Status code == 3001 mean otp successfully send
        return result['responseCode'] == '3001'

    def verifyOtp(self, phone, otp):
        cur = self.__conn.connection.cursor()
        res = cur.execute(
            f"""SELECT * FROM secret WHERE phone = {phone} AND otp = {otp}""")
        print(res)
        if(res > 0):
            detail = cur.fetchall()
            for item in detail:
                dataOtp = item[2]
                print(dataOtp)
                print(otp)
                if(otp == dataOtp):
                    now = datetime.now().timestamp()
                    sendTime = item[3]
                    sendTimeInFloat = datetime.strptime(
                        sendTime, "%Y-%m-%d %H:%M:%S").timestamp()
                    validTime = 900.0
                    if((now - sendTimeInFloat)) > validTime:
                        return 1
                    else:
                        cur.execute(
                            f"""DELETE FROM secret WHERE phone = {phone}""")
                        return 0
                else:
                    return 2
        else:
            return 2
        
    def getVideos(self):
        cur = self.__conn.connection.cursor()
        resultValue = cur.execute("SELECT * FROM videos")
        if(resultValue > 0):
            userDetails = cur.fetchall()
            user = []
            for item in userDetails:
                row = {"id": item[0], "title": item[3]}
                user.append(row)
            return jsonify(user)
