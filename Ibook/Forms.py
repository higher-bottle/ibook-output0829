from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, ValidationError, Email, URL
from wtforms import StringField, SubmitField, PasswordField, BooleanField, SelectField, HiddenField, IntegerField


class SyncBooks(FlaskForm):
    """Sync Book"""
    submit = SubmitField('Sync Book')


class ExportNotes(FlaskForm):
    bookid = StringField('Book ID', validators=[DataRequired()])
    submit = SubmitField('Export Notes')