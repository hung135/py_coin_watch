from sqlalchemy.schema import Column, UniqueConstraint
import sqlalchemy.types as c

from sqlalchemy.ext.declarative import declarative_base


MetaBase = declarative_base()


class CoinTbl(MetaBase):
    DbSchema = 'coin_watch'
    __tablename__ = 'coin'

    __table_args__ = (UniqueConstraint('name', name='coin_name'), {"schema": DbSchema})
    id = Column(c.Integer, primary_key=True)
    name = Column(c.String, nullable=False)
    symbol = Column(c.String, nullable=False)
    last_sms_msg_sent = Column(c.String, nullable=True)
    process_start_dtm = Column(c.DateTime, default=None)
    process_end_dtm = Column(c.DateTime, default=None)


class ErrorLogTbl(MetaBase):
    DbSchema = 'logging'
    __tablename__ = 'error_log'
    __table_args__ = {"schema": DbSchema}
    id = Column(c.Integer, primary_key=True)

    error_code = Column(c.String)
    error_log_id = Column(c.String)
    error_message = Column(c.String)
    error_timestamp = Column(c.DateTime)
    user_name = Column(c.String)
    program_unit = Column(c.String)
    sql_statement = Column(c.String)


