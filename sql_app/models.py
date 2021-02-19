from sqlalchemy import Column
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import DateTime, Integer

from .database import Base


class AccessLog(Base):
    __tablename__ = 'accesslogs'

    student_id = Column(Integer, primary_key=True)
    entered_at = Column(DateTime, primary_key=True, index=True)
    exited_at = Column(DateTime, default=None, index=True)


class InRoomUser(Base):
    __tablename__ = 'inroomusers'

    id = Column(Integer, primary_key=True, autoincrement=False)
    entered_at = Column(DateTime, server_default=text('CURRENT_TIMESTAMP()'))
