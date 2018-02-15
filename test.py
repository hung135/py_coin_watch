from db import dbtable, dbtable_def
import logging
logging.basicConfig(level='DEBUG')
logging.getLogger().setLevel(logging.DEBUG)
x=dbtable.DbConn()

r=dbtable.RecordKeeper(x)
row=dbtable_def.CoinTbl(name="hungs",symbol="hssung")


r.add_record(row,commit=True)
r.session.add(row)
r.session.commit()

