import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Result(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'results'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    test = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("teachers.id"))
    student = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("students.id"))\

    test = orm.relation('Test')
    students = orm.relation('Student')
