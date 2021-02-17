import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Group(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'groups'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    teacher = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("teachers.id"))
    student = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    teachers = orm.relation("Teacher")
    students = orm.relation("Student", back_populates='group')

    tests = orm.relation("Test", back_populates='group')
