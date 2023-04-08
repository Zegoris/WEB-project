import sqlalchemy

from data.db_session import SqlAlchemyBase


class Mixed(SqlAlchemyBase):
    __tablename__ = 'mixed'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True, unique=True)
    quote = sqlalchemy.Column(sqlalchemy.String)
    person = sqlalchemy.Column(sqlalchemy.String)
    work = sqlalchemy.Column(sqlalchemy.String)

    def __repr__(self):
        return f"{self.quote} - {self.person}, {self.work}"