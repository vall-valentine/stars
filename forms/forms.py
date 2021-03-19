from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, IntegerField, DateField, RadioField
from wtforms.validators import DataRequired


class UserRegisterForm(FlaskForm):
    login = StringField('Login', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    role_id = RadioField('Role', validators=[DataRequired()])


class GroupRegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    teacher = StringField('Teacher', validators=[DataRequired()])
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
    answer0 = StringField('Answer', validators=[DataRequired()])
    answer1 = StringField('Answer', validators=[DataRequired()])
    answer2 = StringField('Answer', validators=[DataRequired()])
    answer3 = StringField('Answer', validators=[DataRequired()])
    answer4 = StringField('Answer', validators=[DataRequired()])
    answer5 = StringField('Answer', validators=[DataRequired()])
    answer6 = StringField('Answer', validators=[DataRequired()])
    answer7 = StringField('Answer', validators=[DataRequired()])
    answer8 = StringField('Answer', validators=[DataRequired()])
    answer9 = StringField('Answer', validators=[DataRequired()])
    answer10 = StringField('Answer', validators=[DataRequired()])
    answer11 = StringField('Answer', validators=[DataRequired()])
    answer12 = StringField('Answer', validators=[DataRequired()])
    answer13 = StringField('Answer', validators=[DataRequired()])
    answer14 = StringField('Answer', validators=[DataRequired()])
    answer15 = StringField('Answer', validators=[DataRequired()])


class LoginForm(FlaskForm):
    login = StringField("Login: ", validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
