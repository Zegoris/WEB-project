
import sqlalchemy


from data.db_session import SqlAlchemyBase


class Russian(SqlAlchemyBase):
    __tablename__ = 'russian'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True, unique=True)
    quote = sqlalchemy.Column(sqlalchemy.String)
    person = sqlalchemy.Column(sqlalchemy.String)
    work = sqlalchemy.Column(sqlalchemy.String)

    def __repr__(self):
        return f"{self.quote} - {self.person}, {self.work}"