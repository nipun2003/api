from include import dbHandler
from include.constants import *

class UserController:
    __dbHandler = None
    def __init__(self,app) -> None:
        self.__dbHandler = dbHandler.DbHandler(app)

    def checkPhone(self,phone):
        """This method is used to check phone number ,
            if phone number is already present than it will return user already exists
            and if phone number is not present than function send otp in the phone number
            for registering the new phone number.
        """
        db = self.__dbHandler
        response = []
        userExist = db.checkPhone(phone)
        if(userExist):
            result = {
                "error" : False,
                "navigation_code" : 2,
                "navigation_type" : "login",
                "message" : "Phone number alrady exist, Proceed to login."
            }
            response.append(result)
        else :
            res = db.createNewSecret(phone,1)
            result = {}
            if(res):
                result ={
                    'error' : False,
                    'navigation_code' : 2,
                    'navigation_type' : 'register',
                    'message' : "An OTP has been sent to your mobile, Proceed to register."
                }
            else :
                result ={
                    'error' : True,
                    'message' : "Oops! An error occurred while sending OTP"
                }
            response.append(result)
        return response

    def loginUser(self,phone,password):
        """
            This method is simply take the phone number and password and check in database
            if phone number and password is matched which is stored in databases than user can login 
            otherwise user will get an error
        """
        db = self.__dbHandler
        pass
    
    def createUser(self,otp,name,phone,password,email):
        """Method for creating new user"""
        response = []
        db = self.__dbHandler
        otpRes = self.verifyOtp(otp=otp,phone=phone)
        if(otpRes[0]['error']):
            return otpRes
        res = db.createUser(name=name,phone=phone,password=password,email=email)
        if(res == USER_CREATED_SUCCESSFULLY):
            result = {
                'error' : False,
                'message' : "You are successfully registered" 
            }
        else :
            result = {
                'error' : False,
                'message' : "You are successfully registered" 
            }
        return response.append(result)

    def verifyOtp(self,otp,phone):
        db = self.__dbHandler
        response = []
        try:
            res = db.verifyOtp(phone=phone,otp=int(otp))
            if(res == 0):
                result = {
                    'error' : False,
                    'message' : 'Otp verified successfull'
                }
                response.append(result)
            elif (res == 1):
                result = {
                    'error' : True,
                    'message' : "Otp is expired",
                    'server_diff' : res
                }
                response.append(result)
            elif(res == 2) :
                result = {
                    'error' : True,
                    'message' : 'Invalid otp'
                }
                response.append(result)
        except:
            result = {
                    'error' : True,
                    'message' : 'Otp format is bad'
                }
            response.append(result)
        return response

    