from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class AddUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    role = SelectField('Role', choices=[('parent', 'Parent'), ('teacher', 'Teacher'), ('student', 'Student')],
                       validators=[DataRequired()])
    submit = SubmitField('Add User')


class ChangePasswordForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    submit = SubmitField('Change Password')
