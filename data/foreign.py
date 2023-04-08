import sqlalchemy
from sqlalchemy import orm

from data.db_session import SqlAlchemyBase


class Foreign(SqlAlchemyBase):
    __tablename__ = 'foreign'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True, unique=True)
    quote = sqlalchemy.Column(sqlalchemy.String)
    person = sqlalchemy.Column(sqlalchemy.String)
    work = sqlalchemy.Column(sqlalchemy.String)

    def __repr__(self):
        return f"{self.quote} - {self.person}, {self.work}"