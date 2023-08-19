from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, PasswordField, SubmitField, RadioField, MultipleFileField, SelectField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired, Email, NumberRange, Regexp

class AdminLoginForm(FlaskForm):
    userName = StringField("User name", validators=[DataRequired()], render_kw={'placeholder': 'User name'})
    password = PasswordField("Password", validators=[DataRequired()], render_kw={'placeholder': 'Password'})
    submit = SubmitField("Login")

class UserProfileForm(FlaskForm):
    img = FileField('Upload image', validators=[FileRequired(), FileAllowed(['jpg','png', 'jpeg'])])
    userName = StringField('User name', validators=[DataRequired()])
    realName = StringField('Real name', validators=[DataRequired()])
    phoneNumber = IntegerField('Phone number', validators=[DataRequired()])
    gender = RadioField('Gender', choices=['male', 'female'])
    submit = SubmitField('Confirm')

class CommentForm(FlaskForm):
    imgs = MultipleFileField('Upload images')
    anonymous = SelectField('Anonymous', validators=[DataRequired()])
    score = RadioField('Score', choices=['⭐', '⭐⭐', '⭐⭐⭐', '⭐⭐⭐⭐', '⭐⭐⭐⭐⭐'], validators=[DataRequired()])
    submit = SubmitField("Confirm")

class LocationForm(FlaskForm):
    name = StringField('Receiver Name', validators=[DataRequired()])
    phoneNumber = IntegerField('Phone number', validators=[DataRequired()])
    Province = StringField('Province', validators=[DataRequired()])
    City = StringField('City', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])

class RegisterForm(FlaskForm):
    fullName = StringField("Full name", validators=[DataRequired()], render_kw={'placeholder':'Full name'})

    # this should be a password field and will be update later
    password = PasswordField("Password", validators=[DataRequired()], render_kw={'placeholder':'Password'})
    passwordCheck = PasswordField('Confirm password', validators=[DataRequired()], render_kw={'placeholder':'Password confirm'})
    phoneNumber = IntegerField("Phone number", validators=[DataRequired()], render_kw={'placeholder':'Phone number'})
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    phoneNumber = IntegerField("Phone number", validators=[DataRequired()], render_kw={'placeholder':'Phone number'})
    # this should be a password field and will be update later
    password = PasswordField("Password", validators=[DataRequired()], render_kw={'placeholder':'Password'})
    submit = SubmitField('Login')

class indexSearchForm(FlaskForm):
    query = StringField("Search", validators=[DataRequired()])
    submit = SubmitField("Search")


