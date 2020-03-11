DEBUG = True
#dialect+driver://root:1q2w3e4r5t@127.0.0.1:3306/
DIALECT = 'mysql'
DRIVER='pymysql'
USERNAME = 'root'
PASSWORD = '123456'
HOST = '127.0.0.1'
PORT = 3306
DATABASE = 'ffunds'

SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format('mysql','pymysql','root','123456','127.0.0.1','3306','ffunds')
SQLALCHEMY_TRACK_MODIFICATIONS = False
# print(SQLALCHEMY_DATABASE_URI)