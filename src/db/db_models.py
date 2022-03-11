from pony.orm import Required, PrimaryKey

from src.db.init_db import db


class Token(db.Entity):
    _table_ = "tokens_table"
    id = PrimaryKey(int, auto=True)
    unique_hash = Required(str, max_len=20)
    tx_hash = Required(str)
    media_url = Required(str)
    owner = Required(str)
