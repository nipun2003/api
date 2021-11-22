import yaml
from flask_mysqldb import MySQL
from flask import Flask


class DBConnect:

    __database = 1

    def __init__(self, app):
        db = yaml.load(open('./include/config.yaml'),
                       Loader=yaml.FullLoader)
        app.config['MYSQL_HOST'] = db['mysql_host']
        app.config['MYSQL_USER'] = db['mysql_user']
        app.config['MYSQL_PASSWORD'] = db['mysql_password']
        app.config['MYSQL_DB'] = db['mysql_db']
        self.__database = MySQL(app)

    def connect(self):
        return self.__database
