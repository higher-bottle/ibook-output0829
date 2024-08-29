from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
# from flask_sslify import SSLify

db = SQLAlchemy()
csrf = CSRFProtect()
# sslify = SSLify()