import os
from flask import Flask, render_template

from Ibook.blueprint.admin import ibook_bp
# from Forms import

from Ibook.settings import config
from Ibook.Extension import db, csrf
from Ibook.commands import register_commands


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('Ibook')
    app.config.from_object(config[config_name])

    # 注册
    register_commands(app)  # 自定义shell命令
    register_extensions(app)  # 扩展实例初始化
    register_logging(app)  # 日志处理器
    # register_error_handler(app)  # 错误处理函数
    register_blueprint(app)  # 蓝本
    register_shell_context(app)  # shell上下文处理函数
    # register_template_context(app)  # 模版上下文处理函数
    return app


def register_blueprint(app):
    """register blueprint"""
    app.register_blueprint(ibook_bp, url_prefix='/blog')


def register_extensions(app):
    """register Flask extensions"""
    db.init_app(app)
    csrf.init_app(app)
    with app.app_context():
        db.drop_all()
        db.create_all()
        # click.echo('Initialized the database.')


def register_logging(app):
    """register logging"""
    ...


# def register_error_handler(app):
#     @app.errorhandler(404)
#     def bad_request(e):
#         return render_template('errors/404.html'), 400
#
#     @app.errorhandler(CSRFError)
#     def handle_csrf_error(e):
#         return render_template('errors/400.html', description=e.description), 400


# def register_commands(app):
#     ...


# def register_template_context(app):
#     ...
#
#     @app.context_processor
#     def make_template_context():
#         admin = Admin.query.first()
#         categories = Category.query.order_by(Category.name).all()
#         del_categories = DeleteCategory()
#         del_posts = DeletePost()
#
#         return dict(admin=admin, categories=categories, category_del_form=del_categories, post_del_form=del_posts)


def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(app=app)
