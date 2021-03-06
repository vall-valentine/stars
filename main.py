from flask import Flask
from flask import render_template, redirect
from flask_login import LoginManager, login_user, logout_user
from flask_login import login_required, current_user
from requests import get, post

from data import db_session
from data.__all_models import Users, Roles, Groups, TeacherGroups, GroupStudents, Tests, \
    Questions, TestQuestions, TestResults
from forms.forms import UserRegisterForm, GroupRegisterForm, QuestionRegisterForm,\
    TestRegisterForm, QuestionForm, LoginForm

from random import shuffle

from conf.routes import generate_routes

import os

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'solnyshki_vperyod'
file_path = os.path.abspath(os.getcwd()) + "\database.db"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + file_path

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
            return redirect('/system_admin')
        if current_user.role_id == 2:
            return redirect('/ed_process_admin')
        if current_user.role_id == 3:
            return redirect('/teacher')
        if current_user.role_id == 4:
            return redirect('/student')

    if get('https://ssstarsss.herokuapp.com/api/users/1').status_code == 404:
        post('https://ssstarsss.herokuapp.com/api/roles', json={"name": "SysAdmin", "can_view_teachers": 1,
                                                       "can_view_tests": 1, "can_add_users": 1,
                                                       "can_add_tests": 1, "can_complete_tests": 1})

        post('https://ssstarsss.herokuapp.com/api/roles', json={'name': 'EduAdmin', 'can_view_teachers': 1,
                                                       'can_view_tests': 1, 'can_add_users': 0,
                                                       'can_add_tests': 0, 'can_complete_tests': 0})

        post('https://ssstarsss.herokuapp.com/api/roles', json={'name': 'Teacher', 'can_view_teachers': 0,
                                                       'can_view_tests': 1, 'can_add_users': 0,
                                                       'can_add_tests': 0, 'can_complete_tests': 0})

        post('https://ssstarsss.herokuapp.com/api/roles', json={'name': 'Student', 'can_view_teachers': 0,
                                                       'can_view_tests': 1, 'can_add_users': 0,
                                                       'can_add_tests': 1, 'can_complete_tests': 0})

        post('https://ssstarsss.herokuapp.com/api/users', json={'login': "admin", 'surname': 'Админов',
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
                return redirect('/system_admin')
            if current_user.role_id == 2:
                return redirect('/ed_process_admin')
            if current_user.role_id == 3:
                return redirect('/teacher')
            if current_user.role_id == 4:
                return redirect('/student')
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
def start_student():
    return render_template('student.html')


# все тесты ученика
@app.route('/student/tests', methods=['GET'])
def student_tests():
    db_session.global_init("db/database.sqlite")
    session = db_session.create_session()
    group = session.query(GroupStudents).filter(GroupStudents.student_id == current_user.id).first()
    tests = session.query(Tests).filter(Tests.group_id == group.id).all()
    return render_template('student_tests.html', tests=tests)


# определенный тест ученика
@app.route('/student/tests/<test_id>', methods=['GET', 'POST'])
def student_certain_test(test_id):
    form = QuestionForm()
    db_session.global_init("db/database.sqlite")
    session = db_session.create_session()
    test = session.query(Tests).filter(Tests.id == test_id).first()
    testquestions = session.query(TestQuestions).filter(TestQuestions.test_id == test_id).all()
    questions = []
    for q in testquestions:
        questions.append(session.query(Questions).filter(Questions.id == q.id).first())
    len_q = len(questions)

    if form.is_submitted():
        answers = []
        for i in range(len_q):
            exec(f'answers.append(form.answer{i}.data)')

        correct_answers = []
        for question in questions:
            correct_answers.append(question.correct_answer)

        result = 0
        for count in range(len_q):
            if answers[count] == correct_answers[count]:
                result += 1

        if len_q != 0:
            if result // len_q * 100 > 85:
                mark = 5
            elif result // len_q * 100 > 70:
                mark = 4
            elif result // len_q * 100 > 50:
                mark = 3
            else:
                mark = 2

            post('https://ssstarsss.herokuapp.com/api/testresults', json={"test_id": test.id, "student_id": current_user.id,
                                                             "result": result, "mark": mark})
        return redirect('/student/results')

    return render_template('test.html', test=test, questions=questions, shuffle=shuffle, len_q=len_q, form=form)


# результаты ученика
@app.route('/student/results', methods=['GET'])
def student_results():
    db_session.global_init("db/database.sqlite")
    session = db_session.create_session()
    results = session.query(TestResults).filter(TestResults.student_id == current_user.id).all()
    return render_template('student_tests_results.html', results=results)


# страница учителя
@app.route('/teacher', methods=['GET'])
def start_teacher():
    return render_template('teacher.html')


# группы учителя
@app.route('/teacher/groups', methods=['GET'])
def teacher_groups():
    db_session.global_init("db/database.sqlite")
    session = db_session.create_session()
    teachgroups = session.query(TeacherGroups).filter(TeacherGroups.teacher_id == current_user.id).all()
    groups = []
    for tg in teachgroups:
        groups.append(session.query(Groups).filter(Groups.id == tg.group_id).first())

    return render_template('teacher_groups.html', groups=groups)


# список учеников опрделенной группы учителя
@app.route('/teacher/groups/<int:group_id>', methods=['GET'])
def teacher_groups_students(group_id):
    db_session.global_init("db/database.sqlite")
    session = db_session.create_session()
    grstudents = session.query(GroupStudents).filter(GroupStudents.group_id == group_id).all()

    students = []
    for grs in grstudents:
        students.append(session.query(Users).filter(Users.id == grs.student_id).first())

    return render_template('teacher_students_group.html', students=students, group_id=group_id)


# список результатов учеников определенной группы учителя
@app.route('/teacher/groups/<int:group_id>/results', methods=['GET'])
def teacher_students_results(group_id):
    db_session.global_init("db/database.sqlite")
    session = db_session.create_session()

    group = session.query(Groups).filter(Groups.id == group_id).all()

    tests = session.query(Tests).filter(Tests.group_id == group_id).all()

    results = []
    for test in tests:
        res = session.query(TestResults).filter(TestResults.test_id == test.id).all()
        for r in res:
            student = session.query(Users).filter(Users.id == r.student_id).first()
            results.append([r, student])

    return render_template('test_results.html', results=results, group=group)


# добавление вопросов учителем
@app.route('/teacher/add_question', methods=['GET', 'POST'])
def teacher_add_question():
    form_reg = QuestionRegisterForm()
    if form_reg.validate_on_submit():
        post('https://ssstarsss.herokuapp.com/api/questions', json={"module": form_reg.module.data, "teacher_id": current_user.id,
                                                           "description": form_reg.description.data,
                                                           "correct_answer": form_reg.correct_answer.data,
                                                           "wrong_answer1": form_reg.wrong_answer1.data,
                                                           "wrong_answer2": form_reg.wrong_answer2.data,
                                                           "wrong_answer3": form_reg.wrong_answer3.data})
        return redirect('/')
    return render_template('teacher_add_question.html', form_reg=form_reg)


# задание параметров теста учителем
@app.route('/teacher/test_options', methods=['GET', 'POST'])
def teacher_test_options():
    form = TestRegisterForm()
    if form.validate_on_submit():
        module = int(form.num_modules.data)
        num_q_m = int(form.num_module_questions.data)
        num_q = int(form.num_questions.data)

        db_session.global_init("db/database.sqlite")
        session = db_session.create_session()

        tests = Tests(
            group_id=int(form.group_id.data),
            teacher_id=current_user.id,
            start_date=form.date.data
        )
        session.add(tests)
        session.commit()

        questions = []
        for m in range(1, int(module) + 1):
            qu = session.query(Questions).filter(Questions.module == m).all()
            shuffle(qu)
            questions.extend(qu[:num_q_m])
        questions = questions[:num_q]

        test = session.query(Tests).filter(Tests.teacher_id == current_user.id).all()[-1]

        for q in questions:
            print(test.id)
            post('https://ssstarsss.herokuapp.com//api/testquestions', json={'test_id': test.id,
                                                                   'question_id': q.id})
        return redirect('/')

    return render_template('test_options.html', form=form)


# страница системного администратора
@app.route('/system_admin', methods=['GET', 'POST'])
def start_system_admin():
    return render_template('system_admin.html')


# создание группы учеников системным администратором
@app.route('/system_admin/new_group', methods=['GET', 'POST'])
def system_admin_new_group():
    form_reg = GroupRegisterForm()

    if form_reg.is_submitted():
        db_session.global_init("db/database.sqlite")
        session = db_session.create_session()

        post('https://ssstarsss.herokuapp.com//api/groups', json={"name": form_reg.name.data})

        group = session.query(Groups)[-1]

        teacher = session.query(Users).filter(Users.login == form_reg.teacher.data).first()

        post('https://ssstarsss.herokuapp.com/api/teachergroups', json={"teacher_id": teacher.id,
                                                               "group_id": group.id})

        students = form_reg.students.data.split()
        for student in students:
            st = session.query(Users).filter(Users.login == student).first()
            post('https://ssstarsss.herokuapp.com/api/groupstudents', json={"group_id": group.id,
                                                                   "student_id": st.id})

        return redirect('/')

    return render_template('system_admin_newgroup.html', form_reg=form_reg)


# регистрация нового пользователя системным администратором
@app.route('/system_admin/new_user', methods=['GET', 'POST'])
def system_admin_new_user():
    form_reg = UserRegisterForm()

    if form_reg.is_submitted():
        db_session.global_init("db/database.sqlite")
        session = db_session.create_session()

        if session.query(Users).filter(Users.login ==
                                       form_reg.login.data).first():
            return render_template('system_admin_newuser.html', form_reg=form_reg, error="Логин существует")
        post('https://ssstarsss.herokuapp.com/api/users', json={"name": form_reg.name.data, "login": form_reg.login.data,
                                                       "surname": form_reg.surname.data,
                                                       "role_id": form_reg.role_id.data,
                                                       "hashed_password": form_reg.password.data})

        return redirect('/')
    return render_template('system_admin_newuser.html', form_reg=form_reg)


# страница администратора учебного процесса
@app.route('/ed_process_admin', methods=['GET', 'POST'])
def start_ed_process_admin():
    return render_template('ed_process_admin.html')


# просмотр учителей администратором учебного процесса
@app.route('/ed_process_admin/teachers', methods=['GET'])
def ed_process_admin_teachers():
    db_session.global_init("db/database.sqlite")
    session = db_session.create_session()

    teachers = session.query(Users).filter(Users.role_id == 3).all()
    return render_template('ed_process_admin_teachers.html', teachers=teachers)


# просмотр группы учителя администратором учебного процесса
@app.route('/ed_process_admin/teachers/<int:teacher_id>', methods=['GET'])
def ed_process_admin_teachergroup(teacher_id):
    db_session.global_init("db/database.sqlite")
    session = db_session.create_session()
    teachgroups = session.query(TeacherGroups).filter(TeacherGroups.teacher_id == teacher_id).all()
    groups = []
    for tg in teachgroups:
        groups.append(session.query(Groups).filter(Groups.id == tg.group_id).first())

    return render_template('ed_process_admin_teachergroup.html', groups=groups, teacher_id=teacher_id)


# просмотр группы учителя администратором учебного процесса
@app.route('/ed_process_admin/teachers/<int:teacher_id>/groups/<int:group_id>', methods=['GET'])
def ed_process_admin_one_teachergroup(teacher_id, group_id):
    db_session.global_init("db/database.sqlite")
    session = db_session.create_session()
    grstudents = session.query(GroupStudents).filter(GroupStudents.group_id == group_id).all()

    students = []
    for grs in grstudents:
        students.append(session.query(Users).filter(Users.id == grs.student_id).first())

    return render_template('ed_process_admin_one_teachergroup.html', students=students, group_id=group_id)


# просмотр группы учителя администратором учебного процесса
@app.route('/ed_process_admin/teachers/<int:teacher_id>/groups/<int:group_id>/results', methods=['GET'])
def ed_process_admin_one_teachergroup_result(teacher_id, group_id):
    db_session.global_init("db/database.sqlite")
    session = db_session.create_session()

    group = session.query(Groups).filter(Groups.id == group_id).all()

    tests = session.query(Tests).filter(Tests.group_id == group_id).all()

    results = []
    for test in tests:
        res = session.query(TestResults).filter(TestResults.test_id == test.id).all()
        for r in res:
            student = session.query(Users).filter(Users.id == r.student_id).first()
            results.append([r, student])

    return render_template('ed_process_admin_one_teachergroup_results.html', results=results, group=group)


# просмотр запланированных тестов администратором учебного процесса
@app.route('/ed_process_admin/tests', methods=['GET'])
def ed_process_admin_planned_tests():
    db_session.global_init("db/database.sqlite")
    session = db_session.create_session()

    tests = session.query(Tests).all()
    return render_template('ed_process_admin_tests.html', tests=tests)


# просмотр заданий администратором учебного процесса
@app.route('/ed_process_admin/questions', methods=['GET'])
def ed_process_admin_questions():
    db_session.global_init("db/database.sqlite")
    session = db_session.create_session()

    questions = session.query(Questions).all()
    return render_template('ed_process_admin_questions.html', questions=questions)


if __name__ == '__main__':
    # Для Heroku
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

    # Для локального тестирования
    # app.run(port=8080, host='127.0.0.1')

    # can_view_teachers значит и тесты видит, и учеников препода, и вопросы загруженные
    # can_view_tests значит видит тесты запланнированные и оценки
    # can_add_users значит и добавлять группы и студентов в них
    # can_add_tests
    # can_complete_tests значит и видеть оценку


