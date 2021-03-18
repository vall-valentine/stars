from flask import Flask, abort
from flask import redirect
from flask import render_template
from flask_login import LoginManager, login_user, logout_user
from flask_login import login_required, current_user
from requests import get, post, put, delete

from data import db_session
from data.__all_models import Users, Roles, Groups, TeacherGroups, GroupStudents, Tests, \
    Questions, TestQuestions, TestResults
from forms.forms import UserRegisterForm, GroupRegisterForm, QuestionRegisterForm,\
    TestRegisterForm, QuestionForm, LoginForm

from flask_user import roles_required

from conf.routes import generate_routes

app = Flask(__name__)
app.config['SECRET_KEY'] = 'solnyshki_vperyod'

login_manager = LoginManager(app)
login_manager.init_app(app)

generate_routes(app)


# вход юзера
@login_manager.user_loader
def load_user(user_id):
    db_session.global_init("db/database.sqlite")
    session = db_session.create_session()
    return session.query(Users).get(user_id)


# страница входа
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.role_id == 1:
            return render_template('system_admin.html')
        if current_user.role_id == 2:
            return render_template('ed_process_admin.html')
        if current_user.role_id == 3:
            return render_template('teacher.html')
        if current_user.role_id == 1:
            return render_template('student.html')

    if get('http://127.0.0.1:8080//api/users/1').status_code == 404:
        post('http://127.0.0.1:8080//api/roles', json={"name": "SysAdmin", "can_view_teachers": 1,
                                                       "can_view_tests": 1, "can_add_users": 1,
                                                       "can_add_tests": 1, "can_complete_tests": 1})

        post('http://127.0.0.1:8080//api/roles', json={'name': 'EduAdmin', 'can_view_teachers': 1,
                                                       'can_view_tests': 1, 'can_add_users': 0,
                                                       'can_add_tests': 0, 'can_complete_tests': 0})

        post('http://127.0.0.1:8080//api/roles', json={'name': 'Teacher', 'can_view_teachers': 0,
                                                       'can_view_tests': 1, 'can_add_users': 0,
                                                       'can_add_tests': 0, 'can_complete_tests': 0})

        post('http://127.0.0.1:8080//api/roles', json={'name': 'Student', 'can_view_teachers': 0,
                                                       'can_view_tests': 1, 'can_add_users': 0,
                                                       'can_add_tests': 1, 'can_complete_tests': 0})

        post('http://127.0.0.1:8080//api/users', json={'login': "admin", 'surname': 'Админов',
                                                       'role_id': 1, 'name': 'Админ', 'hashed_password': '111'})

    form_log = LoginForm()

    # если форма заполнена и отправлена
    if form_log.validate_on_submit():
        db_session.global_init("db/database.sqlite")
        session = db_session.create_session()
        user = session.query(Users).filter(Users.login ==
                                           form_log.login.data).first()

        # если пароль введён верный
        if user and user.check_password(form_log.password.data):
            # выполняется вход пользователя
            login_user(user, remember=True)
            if current_user.role_id == 1:
                return render_template('system_admin.html')
            if current_user.role_id == 2:
                return render_template('ed_process_admin.html')
            if current_user.role_id == 3:
                return render_template('teacher.html')
            if current_user.role_id == 1:
                return render_template('student.html')
        return render_template('login.html',
                               error="Неправильный логин или пароль",
                               form_log=form_log)
    return render_template('login.html', form_log=form_log)


# выход из системы
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


# перенаправление неавторизированных
@login_manager.unauthorized_handler
def unauthorized():
    return redirect('/login')


# страница ученика
@app.route('/student', methods=['GET'])
@roles_required('Student')
def start_student():
    return render_template('student.html')


# все тесты ученика
@app.route('/student/tests', methods=['GET'])
def student_tests():
    return render_template('student_tests.html')


# определенный тест ученика
@app.route('/student/tests/<test_name>', methods=['GET', 'POST'])
def student_certain_test(test_name):
    return


# результаты ученика
@app.route('/student/results', methods=['GET'])
def student_results():
    return render_template('student_results.html')


# страница учителя
@app.route('/teacher', methods=['GET'])
def start_teacher():
    return render_template('teacher.html')


# группы учителя
@app.route('/teacher/groups', methods=['GET'])
def teacher_groups():
    return render_template('teacher_groups.html')


# список учеников опрделенной группы учителя
@app.route('/teacher/groups/<group>', methods=['GET'])
def teacher_groups_students(group):
    return


# список результатов учеников определенной группы учителя
@app.route('/teacher/groups/<group>/results', methods=['GET'])
def teacher_students_results(group):
    return


# добавление вопросов учителем
@app.route('/teacher/add_question', methods=['GET'])
def teacher_add_question():
    return render_template('teacher_add_question.html')


# задание параметров теста учителем
@app.route('/teacher/test_options', methods=['GET'])
def teacher_test_options():
    return render_template('teacher_test_options.html')


# страница системного администратора
@app.route('/system_admin', methods=['GET'])
def start_system_admin():
    return render_template('system_admin.html')


# создание группы учеников системным администратором
@app.route('/system_admin/new_group', methods=['GET'])
def system_admin_new_group():
    return render_template('system_admin_newgroup.html')


# регистрация нового пользователя системным администратором
@app.route('/system_admin/new_user', methods=['GET'])
def system_admin_new_user():
    return render_template('system_admin_newuser.html')


# страница администратора учебного процесса
@app.route('/ed_process_admin', methods=['GET'])
def start_ed_process_admin():
    return render_template('ed_process_admin.html')


# просмотр учителей администратором учебного процесса
@app.route('/ed_process_admin/teachers', methods=['GET'])
def ed_process_admin_teachers():
    return render_template('ed_process_admin_teachers.html')


# просмотр группы учителя администратором учебного процесса
@app.route('/ed_process_admin/teachers/<group>', methods=['GET'])
def ed_process_admin_teachergroup(group):
    return render_template('ed_process_admin_teachergroup.html')


# просмотр запланированных тестов администратором учебного процесса
@app.route('/ed_process_admin/planned_tests', methods=['GET'])
def ed_process_admin_planned_tests():
    return render_template('ed_process_admin_plannedtests.html')


# просмотр проведенных тестов администратором учебного процесса
@app.route('/ed_process_admin/finished_tests', methods=['GET'])
def ed_process_admin_finished_tests():
    return render_template('ed_process_admin_finishedtests.html')


# просмотр результатов проведенных тестов администратором учебного процесса
@app.route('/ed_process_admin/finished_tests/<test>', methods=['GET'])
def ed_process_admin_results(test):
    return render_template('ed_process_admin_results.html')


# просмотр заданий администратором учебного процесса
@app.route('/ed_process_admin/questions', methods=['GET'])
def ed_process_admin_questions():
    return render_template('ed_process_admin_questions.html')


if __name__ == '__main__':
    db_session.global_init("db/database.sqlite")
    app.run(port=8080, host='127.0.0.1')

    # can_view_teachers значит и тесты видит, и учеников препода, и вопросы загруженные
    # can_view_tests значит видит тесты запланнированные и оценки
    # can_add_users значит и добавлять группы и студентов в них
    # can_add_tests
    # can_complete_tests значит и видеть оценку


