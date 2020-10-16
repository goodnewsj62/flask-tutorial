from flask_wtf import FlaskForm
from flask1.models import User
from wtforms import StringField,SubmitField,TextAreaField,PasswordField,BooleanField
from wtforms.validators import  Email,ValidationError,DataRequired,Length,EqualTo


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),Length(min = 6, max = 20)])
    email = StringField('Email', validators=[DataRequired(),Length(min = 6)])
    password = PasswordField('Password',validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('User with username already exists choose another')

    def validate_email(self,email):
        email = User.query.filter_by(email= email.data).first()
        if self.email.data[-4] == '.' and '@' in self.email.data:
            if email:
                raise ValidationError('Email already exists')
        else:
            raise ValidationError('must be a valid email')


class Loginform(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(min=6)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('remember me')
    submit = SubmitField('Sign Up')

class UpdateForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=3)])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Update')

class CreateForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=3)])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Create')

