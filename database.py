from pymongo import MongoClient
from pymongo.database import Database
from config import Settings


setting =Settings()

host =setting.HOST
database=  setting.DATABASE
user = setting.USER
password = setting.PASSWORD
port= setting.PORT
# Database connection details
db_params = {
    'host': host,
    'database': database,
    'user': user,
    'password': password,
    'port':port
}


db : Database = MongoClient("mongodb+srv://fedislimen98:969xZIC88sT0q13R@cluster0.hxwzais.mongodb.net/")["API1"]