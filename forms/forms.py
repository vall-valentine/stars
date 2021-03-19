from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, IntegerField, DateField, BooleanField, RadioField
from wtforms.validators import DataRequired


class UserRegisterForm(FlaskForm):
    login = StringField('Login', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    role_id = RadioField('Role', validators=[DataRequired()])


class GroupRegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    teacher = IntegerField('Teacher ID', validators=[DataRequired()])
    students = TextAreaField('Students', validators=[DataRequired()])


class QuestionRegisterForm(FlaskForm):
    module = StringField('Module', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    correct_answer = StringField('Correct answer', validators=[DataRequired()])
    wrong_answer1 = StringField('Wrong answer 1', validators=[DataRequired()])
    wrong_answer2 = StringField('Wrong answer 2', validators=[DataRequired()])
    wrong_answer3 = StringField('Wrong answer 3', validators=[DataRequired()])


class TestRegisterForm(FlaskForm):
    group_id = IntegerField('Group', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    num_questions = TextAreaField('Number of questions', validators=[DataRequired()])
    num_modules = TextAreaField('Number of modules', validators=[DataRequired()])
    num_module_questions = TextAreaField('Number of question in module', validators=[DataRequired()])


class QuestionForm(FlaskForm):
    answer1 = BooleanField('Answer', validators=[DataRequired()])
    answer2 = BooleanField('Answer', validators=[DataRequired()])
    answer3 = BooleanField('Answer', validators=[DataRequired()])
    answer4 = BooleanField('Answer', validators=[DataRequired()])


class LoginForm(FlaskForm):
    login = StringField("Login: ", validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
