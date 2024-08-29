"""为不同的使用场景设置了不同的database"""
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    load_dotenv()
    # SECRET_KEY = os.environ.get('SECRET_KEY')
    SECRET_KEY = os.urandom(32)
    # # SQLALCHEMY_TRACK_MODIFICATIONS决定是否追踪对象的修改
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    #
    # MAIL_SERVER = os.environ.get('MAIL_SERVER')
    # MAIL_PORT = int(os.environ.get('MAIL_PORT'))
    # MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    # MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
    # MAIL_USE_TLS = True
    #
    # BLOG_EMAIL = os.environ.get('BLOG_EMAIL')
    # BLOG_POSTS_PER_PAGE = os.environ.get('BLOG_POSTS_PER_PAGE')
    # BLOG_MANAGE_POSTS_PER_PAGE = os.environ.get('BLOG_MANAGE_POSTS_PER_PAGE')
    # BLOG_COMMENTS_PER_PAGE = os.environ.get('BLOG_COMMENTS_PER_PAGE')


class DevelopmentConfig(BaseConfig):
    FLASK_DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-dev.db')


class TestingConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'data.db'))


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
