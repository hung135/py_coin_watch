import logging
import pprint
from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import CreateSchema

from .dbtable_def import CoinTbl, MetaBase, ErrorLogTbl

class DbConn():
    def __init__(self):
        self._userid='postgres'
        self._password='tester'
        self._host='192.168.99.100' #vagrant macine ip
        self._port=5432
        self._database_name='postgres'
        self._schema='coin_watch'
    def get_conn_url(self):
        url = 'postgresql://{}:{}@{}:{}/{}'
        url = url.format(self._userid, self._password, self._host, self._port, self._database_name)
        return url

class RecordKeeper():
    db_url = None
    table = None

    def __init__(self, dbconn, table_def=None, DbSchema_overide=None):
        assert isinstance(dbconn,DbConn)
        if table_def is None:
            self.table = CoinTbl
        else:
            self.table = table_def

        if DbSchema_overide is not None:
            # pprint.pprint((self.table.__dict__))
            self.table.DbSchema = DbSchema_overide
            self.table.__table_args__['schema'] = self.table.DbSchema

        self.engine = create_engine(dbconn.get_conn_url())
        try:
            self.engine.execute(CreateSchema(self.table.DbSchema))
            logging.debug("Creating Database Schema: {}".format(self.table.DbSchema))
        except:
            # logging.debug("Schema Already Exists No need to create:")
            pass

        # create tables
        MetaBase.metadata.create_all(bind=self.engine)

        # create session
        Session = sessionmaker()
        Session.configure(bind=self.engine)
        self.session = Session()

        # reflecting whole schema
        self.metadata = MetaData()
        self.metadata.reflect(bind=self.engine)

    def add_record(self, table, commit=False):

        # add row to database

        self.session.add(table)

        if commit:
            try:
                self.commit()

            except Exception as e:
                logging.error(e)
                print(e)
                self.session.rollback()

    def print_row(self, row):
        print(type(row), dir(row))
        for i in row.keys:
            print(i)

    def get_record(self, *row):
        # update row to database
        row = self.session.query(CoinTbl).filter(*row).order_by(CoinTbl.id.desc()).first()

        return row

    def commit(self):
        try:
            self.session.commit()
        except:
            self.session.rollback()

    def __del__(self):
        try:
            self.session.close()
            logging.debug("Closing dbtable.py Session")
        except:
            logging.error("Error Occured Closing dbtable.py Session")
