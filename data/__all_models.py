import sqlalchemy
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Users(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    login = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    role_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("roles.id"))

    roles = orm.relation('Role')

    teachergroups = orm.relation("TeacherGroups", back_populates='teachers')
    groupstudents = orm.relation("GroupsStudents", back_populates='students')
    testresults = orm.relation("TestResults", back_populates='students')
    tests = orm.relation("Tests", back_populates='tests')


class Roles(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'roles'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    can_view_teachers = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
    can__view_tests = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
    can_add_users = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
    can_add_tests = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
    can_complete_tests = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)

    user = orm.relation("Users", back_populates='roles')


class Groups(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'groups'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    teachergroups = orm.relation("TeacherGroups", back_populates='groups')
    tests = orm.relation("Tests", back_populates='groups')


class TeacherGroups(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'teachergroups'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    teacher_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    group_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("groups.id"))

    teachers = orm.relation('Users')
    groups = orm.relation('Groups')


class GroupStudents(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'groupstudents'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    group_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("groups.id"))
    student_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))

    students = orm.relation('Users')
    groups = orm.relation('Groups')


class Test(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'tests'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    group_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("groups.id"))
    teacher_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))

    teachers = orm.relation('Users')
    groups = orm.relation('Groups')

    testquestions = orm.relation("TestQuestions", back_populates='tests')


class Questions(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'questions'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    group_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("groups.id"))
    teacher_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))

    teachers = orm.relation('Users')
    groups = orm.relation('Groups')

    testquestions = orm.relation("TestQuestions", back_populates='questions')


class TestQuestions(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'testquestions'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    test_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("tests.id"))
    question_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("questions.id"))

    tests = orm.relation('Tests')
    Questions = orm.relation('Questions')


class TestResults(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'testresults'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    test_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("tests.id"))
    student_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))

    result = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    mark = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    tests = orm.relation('Tests')
    students = orm.relation('Users')
