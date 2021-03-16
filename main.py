from flask import Flask, render_template
from data import db_session

app = Flask(__name__)


# страница входа
@app.route('/', methods=['GET'])
@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


# страница ученика
@app.route('/student', methods=['GET'])
def start_student():
    return render_template('student.html')


# все тесты ученика
@app.route('/student/tests', methods=['GET'])
def student_tests():
    return render_template('student_tests.html')


# определенный тест ученика
@app.route('/student/tests/<test_name>', methods=['GET', 'POST'])
def student_certain_test():
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
