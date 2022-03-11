from pony.orm import Database

db = Database()

def set_up_db(config: dict) -> None:
    db.bind(**config['postgres'])