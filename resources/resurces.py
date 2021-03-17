from flask import jsonify
from flask_restful import reqparse, abort, Resource

from data import db_session
from data.__all_models import Users as User
from data.__all_models import Roles as Role
from data.__all_models import Groups as Group
from data.__all_models import TeacherGroups
from data.__all_models import GroupStudents
from data.__all_models import Test
from data.__all_models import Questions as Question
from data.__all_models import TestQuestions
from data.__all_models import TestResults


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")


def abort_if_login_not_unique(login):
    session = db_session.create_session()
    user = session.query(User).filter(User.login == login).first()
    if user:
        abort(400, message=f"User with nickname '{login}' already exists")


class UsersResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify({'user': user.to_dict(
            only=('id', 'login', 'surname', 'role_id'))})

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, user_id):
        abort_if_user_not_found(user_id)
        parser = reqparse.RequestParser()
        parser.add_argument('login', required=False)
        parser.add_argument('surname', required=False)
        parser.add_argument('name', required=False)
        parser.add_argument('role_id', required=False, type=int)
        parser.add_argument('hashed_password', required=False)
        args = parser.parse_args()

        session = db_session.create_session()
        user = session.query(User).get(user_id)

        abort_if_login_not_unique(args['login'])
        if args['login']:
            user.login = args['login']
        if args['surname']:
            user.surname = args['surname']
        if args['name']:
            user.name = args['name']
        if args['role_id']:
            user.role_id = args['role_id']
        if args['hashed_password']:
            user.set_password(args['password'])

        session.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({'roles': [item.to_dict(
            only=('id', 'login', 'surname', 'role_id')) for item in users]})

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('login', required=True)
        parser.add_argument('surname', required=False)
        parser.add_argument('name', required=False)
        parser.add_argument('role_id', required=False, type=int)
        parser.add_argument('hashed_password', required=True)
        args = parser.parse_args()

        abort_if_login_not_unique(args['login'])

        session = db_session.create_session()
        user = User(
            login=args['login'],
            surname=args['surname'],
            name=args['name'],
            role_id=args['role_id']
        )
        user.set_password(args['hashed_password'])
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})


def abort_if_role_not_found(role_id):
    session = db_session.create_session()
    role = session.query(Role).get(role_id)
    if not role:
        abort(404, message=f"Role {role_id} not found")


class RolesResource(Resource):
    def get(self, role_id):
        abort_if_user_not_found(role_id)
        session = db_session.create_session()
        role = session.query(Role).get(role_id)
        return jsonify({'role': role.to_dict(
            only=('name', 'can_view_teachers', 'can_view_tests',
                  'can_add_users', 'can_add_tests', 'can_complete_tests'))})

    def delete(self, role_id):
        abort_if_role_not_found(role_id)
        session = db_session.create_session()
        role = session.query(Role).get(role_id)
        session.delete(role)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, role_id):
        abort_if_role_not_found(role_id)
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=False)
        parser.add_argument('can_view_teachers', required=False)
        parser.add_argument('can_view_tests', required=False)
        parser.add_argument('can_add_users', required=False)
        parser.add_argument('can_add_tests', required=False)
        parser.add_argument('can_complete_tests', required=False)

        args = parser.parse_args()

        session = db_session.create_session()
        role = session.query(Role).get(role_id)

        if args['name']:
            role.login = args['name']
        if args['can_view_teachers']:
            role.surname = args['can_view_teachers']
        if args['can_view_tests']:
            role.name = args['can_view_tests']
        if args['can_add_users']:
            role.role_id = args['can_add_users']
        if args['can_add_tests']:
            role.role_id = args['can_add_tests']
        if args['can_complete_tests']:
            role.set_password(args['can_complete_tests'])

        session.commit()
        return jsonify({'success': 'OK'})


class RolesListResource(Resource):
    def get(self):
        session = db_session.create_session()
        roles = session.query(Role).all()
        return jsonify({'roles': [item.to_dict(
            only=('name', 'can_view_teachers', 'can_view_tests',
                  'can_add_users', 'can_add_tests',
                  'can_complete_tests')) for item in roles]})

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True)
        parser.add_argument('can_view_teachers', required=False)
        parser.add_argument('can_view_tests', required=False)
        parser.add_argument('can_add_users', required=False)
        parser.add_argument('can_add_tests', required=True)
        parser.add_argument('can_complete_tests', required=True)
        args = parser.parse_args()

        session = db_session.create_session()
        role = Role(
            name=args['name'],
            can_view_teachers=args['can_view_teachers'],
            can_view_tests=args['can_view_tests'],
            can_add_users=args['can_add_users'],
            can_add_tests=args['can_add_tests'],
            can_complete_tests=args['can_complete_tests']
        )
        session.add(role)
        session.commit()
        return jsonify({'success': 'OK'})


def abort_if_group_not_found(group_id):
    session = db_session.create_session()
    group = session.query(Group).get(group_id)
    if not group:
        abort(404, message=f"Group {group_id} not found")


class GroupsResource(Resource):
    def get(self, group_id):
        abort_if_group_not_found(group_id)
        session = db_session.create_session()
        group = session.query(Group).get(group_id)
        return jsonify({'group': group.to_dict(
            only=('name'))})

    def delete(self, group_id):
        abort_if_group_not_found(group_id)
        session = db_session.create_session()
        group = session.query(Group).get(group_id)
        session.delete(group)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, group_id):
        abort_if_group_not_found(group_id)
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=False)

        args = parser.parse_args()

        session = db_session.create_session()
        group = session.query(Group).get(group_id)

        if args['name']:
            group.login = args['name']

        session.commit()
        return jsonify({'success': 'OK'})


class GroupsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        roles = session.query(Group).all()
        return jsonify({'groups': [item.to_dict(
            only=('name')) for item in roles]})

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True)
        args = parser.parse_args()

        session = db_session.create_session()
        role = Group(
            name=args['name']
        )
        session.add(role)
        session.commit()
        return jsonify({'success': 'OK'})


def abort_if_teachersgroup_not_found(tg_id):
    session = db_session.create_session()
    teachgroup = session.query(TeacherGroups).get(tg_id)
    if not teachgroup:
        abort(404, message=f"TeacherGroup {tg_id} not found")


class TeacherGroupsResource(Resource):
    def get(self, tg_id):
        abort_if_teachersgroup_not_found(tg_id)
        session = db_session.create_session()
        teachgroup = session.query(TeacherGroups).get(tg_id)
        return jsonify({'teachergroups': teachgroup.to_dict(
            only=('teacher_id', 'group_id'))})

    def delete(self, tg_id):
        abort_if_teachersgroup_not_found(tg_id)
        session = db_session.create_session()
        teachgroup = session.query(TeacherGroups).get(tg_id)
        session.delete(teachgroup)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, tg_id):
        abort_if_teachersgroup_not_found(tg_id)
        parser = reqparse.RequestParser()
        parser.add_argument('teacher_id', required=False)
        parser.add_argument('group_id', required=False)

        args = parser.parse_args()

        session = db_session.create_session()
        teachgroup = session.query(TeacherGroups).get(tg_id)

        if args['teacher_id']:
            teachgroup.login = args['teacher_id']
        if args['group_id']:
            teachgroup.login = args['group_id']

        session.commit()
        return jsonify({'success': 'OK'})


class TeacherGroupsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        teachgroup = session.query(TeacherGroups).all()
        return jsonify({'teachergroups': [item.to_dict(
            only=('teacher_id', 'group_id')) for item in teachgroup]})

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('teacher_id', required=True)
        parser.add_argument('group_id', required=True)
        args = parser.parse_args()

        session = db_session.create_session()
        teachgroup = TeacherGroups(
            group_id=args['group_id'],
            teacher_id=args['teacher_id']
        )
        session.add(teachgroup)
        session.commit()
        return jsonify({'success': 'OK'})


def abort_if_groupstudents_not_found(gs_id):
    session = db_session.create_session()
    groupstudents = session.query(GroupStudents).get(gs_id)
    if not groupstudents:
        abort(404, message=f"GroupStudents {gs_id} not found")


class GroupStudentsResource(Resource):
    def get(self, gs_id):
        abort_if_groupstudents_not_found(gs_id)
        session = db_session.create_session()
        groupstudents = session.query(GroupStudents).get(gs_id)
        return jsonify({'groupstudents': groupstudents.to_dict(
            only=('student_id', 'group_id'))})

    def delete(self, gs_id):
        abort_if_groupstudents_not_found(gs_id)
        session = db_session.create_session()
        groupstudents = session.query(GroupStudents).get(gs_id)
        session.delete(groupstudents)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, gs_id):
        abort_if_groupstudents_not_found(gs_id)
        parser = reqparse.RequestParser()
        parser.add_argument('student_id', required=False)
        parser.add_argument('group_id', required=False)

        args = parser.parse_args()

        session = db_session.create_session()
        groupstudents = session.query(GroupStudents).get(gs_id)

        if args['student_id']:
            groupstudents.login = args['student_id']
        if args['group_id']:
            groupstudents.login = args['group_id']

        session.commit()
        return jsonify({'success': 'OK'})


class GroupStudentsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        groupstudents = session.query(GroupStudents).all()
        return jsonify({'groupstudents': [item.to_dict(
            only=('student_id', 'group_id')) for item in groupstudents]})

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('student_id', required=True)
        parser.add_argument('group_id', required=True)
        args = parser.parse_args()

        session = db_session.create_session()
        groupstudents = GroupStudents(
            group_id=args['group_id'],
            student_id=args['student_id']
        )
        session.add(groupstudents)
        session.commit()
        return jsonify({'success': 'OK'})


def abort_if_test_not_found(test_id):
    session = db_session.create_session()
    test = session.query(Test).get(test_id)
    if not test:
        abort(404, message=f"Test {test_id} not found")


class TestResource(Resource):
    def get(self, test_id):
        abort_if_test_not_found(test_id)
        session = db_session.create_session()
        test = session.query(Test).get(test_id)
        return jsonify({'tests': test.to_dict(
            only=('teacher_id', 'group_id', 'start_date'))})

    def delete(self, test_id):
        abort_if_test_not_found(test_id)
        session = db_session.create_session()
        test = session.query(Test).get(test_id)
        session.delete(test)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, test_id):
        abort_if_test_not_found(test_id)
        parser = reqparse.RequestParser()
        parser.add_argument('teacher_id', required=False)
        parser.add_argument('group_id', required=False)
        parser.add_argument('start_date', required=False)

        args = parser.parse_args()

        session = db_session.create_session()
        test = session.query(Test).get(test_id)

        if args['teacher_id']:
            test.login = args['teacher_id']
        if args['group_id']:
            test.login = args['group_id']

        session.commit()
        return jsonify({'success': 'OK'})


class TestListResource(Resource):
    def get(self):
        session = db_session.create_session()
        test = session.query(Test).all()
        return jsonify({'tests': [item.to_dict(
            only=('teacher_id', 'group_id', 'start_date')) for item in test]})

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('teacher_id', required=True)
        parser.add_argument('group_id', required=True)
        parser.add_argument('start_date', required=True)
        args = parser.parse_args()

        session = db_session.create_session()
        tests = Test(
            group_id=args['group_id'],
            teacher_id=args['teacher_id'],
            start_date=args['start_date']
        )
        session.add(tests)
        session.commit()
        return jsonify({'success': 'OK'})


def abort_if_question_not_found(question_id):
    session = db_session.create_session()
    question = session.query(Question).get(question_id)
    if not question:
        abort(404, message=f"Question {question} not found")


class QuestionsResource(Resource):
    def get(self, question_id):
        abort_if_question_not_found(question_id)
        session = db_session.create_session()
        question = session.query(Question).get(question_id)
        return jsonify({'question': question.to_dict(
            only=('teacher_id', 'module', 'description', 'correct_answer',
                  'wrong_answer1', 'wrong_answer2', 'wrong_answer3'))})

    def delete(self, question_id):
        abort_if_question_not_found(question_id)
        session = db_session.create_session()
        question = session.query(Question).get(question_id)
        session.delete(question)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, question_id):
        abort_if_test_not_found(question_id)
        parser = reqparse.RequestParser()
        parser.add_argument('teacher_id', required=False)
        parser.add_argument('module', required=False)
        parser.add_argument('description', required=False)
        parser.add_argument('correct_answer', required=False)
        parser.add_argument('wrong_answer1', required=False)
        parser.add_argument('wrong_answer2', required=False)
        parser.add_argument('wrong_answer3', required=False)

        args = parser.parse_args()

        session = db_session.create_session()
        question = session.query(Question).get(question_id)

        if args['teacher_id']:
            question.login = args['teacher_id']
        if args['module']:
            question.login = args['module']
        if args['description']:
            question.login = args['description']
        if args['wrong_answer1']:
            question.login = args['wrong_answer1']
        if args['wrong_answer2']:
            question.login = args['wrong_answer2']
        if args['wrong_answer3']:
            question.login = args['wrong_answer3']

        session.commit()
        return jsonify({'success': 'OK'})


class QuestionsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        question = session.query(Question).all()
        return jsonify({'questions': [item.to_dict(
            only=('teacher_id', 'module', 'description', 'correct_answer',
                  'wrong_answer1', 'wrong_answer2', 'wrong_answer3')) for item in question]})

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('teacher_id', required=True)
        parser.add_argument('module', required=True)
        parser.add_argument('description', required=True)
        parser.add_argument('correct_answer', required=True)
        parser.add_argument('wrong_answer1', required=True)
        parser.add_argument('wrong_answer2', required=True)
        parser.add_argument('wrong_answer3', required=True)

        args = parser.parse_args()

        session = db_session.create_session()
        question = Question(
            group_id=args['module'],
            teacher_id=args['teacher_id'],
            description=args['description'],
            correct_answer=args['correct_answer'],
            wrong_answer1=args['wrong_answer1'],
            wrong_answer2=args['wrong_answer2'],
            wrong_answer3=args['wrong_answer3']

        )
        session.add(question)
        session.commit()
        return jsonify({'success': 'OK'})


def abort_if_testquestions_not_found(tq_id):
    session = db_session.create_session()
    tq = session.query(Question).get(tq_id)
    if not tq:
        abort(404, message=f"TestQuestions {tq} not found")


class TestQuestionsResource(Resource):
    def get(self, tq_id):
        abort_if_question_not_found(tq_id)
        session = db_session.create_session()
        tq = session.query(TestQuestions).get(tq_id)
        return jsonify({'testquestion': tq.to_dict(
            only=('question_id', 'test_id'))})

    def delete(self, tq_id):
        abort_if_question_not_found(tq_id)
        session = db_session.create_session()
        question = session.query(TestQuestions).get(tq_id)
        session.delete(question)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, tq_id):
        abort_if_test_not_found(tq_id)
        parser = reqparse.RequestParser()
        parser.add_argument('test_id', required=False)
        parser.add_argument('question_id', required=False)

        args = parser.parse_args()

        session = db_session.create_session()
        tq = session.query(TestQuestions).get(tq_id)

        if args['question_id']:
            tq.login = args['question_id']
        if args['test_id']:
            tq.login = args['test_id']

        session.commit()
        return jsonify({'success': 'OK'})


class TestQuestionsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        tq = session.query(TestQuestions).all()
        return jsonify({'testquestions': [item.to_dict(
            only=('question_id', 'test_id')) for item in tq]})

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('question_id', required=True)
        parser.add_argument('test_id', required=True)

        args = parser.parse_args()

        session = db_session.create_session()
        tq = TestQuestions(
            question_id=args['question_id'],
            test_id=args['test_id'],

        )
        session.add(tq)
        session.commit()
        return jsonify({'success': 'OK'})


def abort_if_testquestions_not_found(tq_id):
    session = db_session.create_session()
    tq = session.query(Question).get(tq_id)
    if not tq:
        abort(404, message=f"TestQuestions {tq} not found")


class TestResultsResource(Resource):
    def get(self, tr_id):
        abort_if_question_not_found(tr_id)
        session = db_session.create_session()
        tr = session.query(TestResults).get(tr_id)
        return jsonify({'testresults': tr.to_dict(
            only=('student_id', 'test_id', 'mark', 'result'))})

    def delete(self, tr_id):
        abort_if_question_not_found(tr_id)
        session = db_session.create_session()
        tr = session.query(TestResults).get(tr_id)
        session.delete(tr)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, tr_id):
        abort_if_test_not_found(tr_id)
        parser = reqparse.RequestParser()
        parser.add_argument('test_id', required=False)
        parser.add_argument('student_id', required=False)
        parser.add_argument('mark', required=False)
        parser.add_argument('result', required=False)

        args = parser.parse_args()

        session = db_session.create_session()
        tr = session.query(TestQuestions).get(tr_id)

        if args['student_id']:
            tr.login = args['student_id']
        if args['test_id']:
            tr.login = args['test_id']
        if args['mark']:
            tr.login = args['mark']
        if args['result']:
            tr.login = args['result']

        session.commit()
        return jsonify({'success': 'OK'})


class TestResultsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        tr = session.query(TestQuestions).all()
        return jsonify({'testresults': [item.to_dict(
            only=('student_id', 'test_id', 'mark', 'result')) for item in tr]})

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('student_id', required=True)
        parser.add_argument('test_id', required=True)
        parser.add_argument('mark', required=True)
        parser.add_argument('result', required=True)

        args = parser.parse_args()

        session = db_session.create_session()
        tr = TestQuestions(
            question_id=args['student_id'],
            test_id=args['test_id'],
            mark=args['mark'],
            result=args['result'],

        )
        session.add(tr)
        session.commit()
        return jsonify({'success': 'OK'})