from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, IntegerField, RadioField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, NumberRange

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')



#########USER-STATS##############
class UserStatsForm(FlaskForm):
    weight = FloatField('Weight (lbs)', validators=[DataRequired(), NumberRange(min=1)])
    height_feet = IntegerField('Height (feet)', validators=[DataRequired(), NumberRange(min=1)])
    height_inches = IntegerField('Height (inches)', validators=[DataRequired(), NumberRange(min=0, max=11)])
    age = IntegerField('Age', validators=[DataRequired(), NumberRange(min=1)])
    gender = RadioField('Gender', choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], validators=[DataRequired()])
    activity_level = SelectField('Activity Level', choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')], validators=[DataRequired()])
    week = IntegerField('Week', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Submit')
'''
class UserStatsForm(FlaskForm):
    weight = StringField('Weight', validators=[DataRequired()])
    height = StringField('Height', validators=[DataRequired()])
    age = StringField('Age', validators=[DataRequired()])
    gender = StringField('Gender', validators=[DataRequired()])
    activity_level = StringField('Activity Level', validators=[DataRequired()])
    submit = SubmitField('Submit')
'''