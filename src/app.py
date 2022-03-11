from fastapi import FastAPI


app = FastAPI()

@app.post("/tokens/create")
async def create():
    """Создавание нового уникального токена в блокчейне"""
    pass

@app.get("/tokens/total_supply")
async def total_supply():
    """Выдача информации о текущем Total supply токена"""
    pass

@app.get("/tokens/list")
async def list_():
    """Выдача списка всех обьектов модели Token"""
    pass