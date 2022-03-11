import uvicorn
from pony.orm import db_session
from fastapi import FastAPI

from src.config import get_config
from src.db.init_db import db, set_up_db
from src.db.db_models import Token


app = FastAPI()
config = get_config()

@app.post("/tokens/create")
async def create():
    """Создание нового уникального токена в блокчейне"""
    pass

@app.get("/tokens/total_supply")
async def total_supply():
    """Выдача информации о текущем Total supply токена"""
    pass

@app.get("/tokens/list")
async def list_():
    """Выдача списка всех обьектов модели Token"""
    pass

if __name__ == "__main__":
    set_up_db(config)
    db.generate_mapping(create_tables=True)
    uvicorn.run(app, host="0.0.0.0", port=8000)