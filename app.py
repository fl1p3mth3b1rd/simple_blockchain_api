from typing import List

import uvicorn
from fastapi import FastAPI, HTTPException

from src.config import get_config
from src.contract.rinkeby_testnet_api import (
    connect_to_node,
    connect_to_contract,
    contract_mint,
    contract_total_supply
)
from src.contract.unique_hash import generate_hash
from src.db.db_api import read_all_tokens, write_token
from src.db.init_db import db, set_up_db
from src.models import CreateRequest, TokenResponse, TotalSupply


app = FastAPI()
config = get_config()

@app.post("/tokens/create", response_model=TokenResponse)
async def create(req_params: CreateRequest):
    """Создание нового уникального токена в блокчейне"""
    media_url = req_params.media_url
    owner = req_params.owner
    # создание подключения к блокчейн-провайдеру:
    conn = connect_to_node(config["etherium"])
    if conn["message"] != "ok":
        raise HTTPException(status_code=500, detail=conn["message"])
    connection = conn["connection"]
    # создание подключения к контракту:
    contr = connect_to_contract(config["etherium"], connection)
    if contr["message"] != "ok":
        raise HTTPException(status_code=500, detail=contr["message"])
    contract = contr["contract"]
    unique_hash = generate_hash()
    # взаимодействие с методом mint контракта:
    res = contract_mint(
        connection=connection,
        contract=contract,
        owner=owner,
        unique_hash=unique_hash,
        media_url=media_url,
        config=config["etherium"]
    )
    if res["message"] != "ok":
        raise HTTPException(status_code=500, detail=res["message"])
    tx_hash = res["tx_hash"]
    # сохранение в бд:
    token = write_token(
        unique_hash=unique_hash,
        tx_hash=tx_hash,
        media_url=media_url,
        owner=owner
    )
    return token.to_dict()

@app.get("/tokens/total_supply", response_model=TotalSupply)
async def total_supply():
    """Выдача информации о текущем Total supply токена"""
    # создание подключения к блокчейн-провайдеру:
    conn = connect_to_node(config["etherium"])
    if conn["message"] != "ok":
        raise HTTPException(status_code=500, detail=conn["message"])
    connection = conn["connection"]
    # создание подключения к контракту:
    contr = connect_to_contract(config["etherium"], connection)
    if contr["message"] != "ok":
        raise HTTPException(status_code=500, detail=contr["message"])
    contract = contr["contract"]
    # взаимодействие с методом total supply контракта:
    ts = contract_total_supply(contract)
    if ts["message"] != "ok":
        raise HTTPException(status_code=500, detail=ts["message"])
    return {"total_supply": ts["total_supply"]}

@app.get("/tokens/list", response_model=List[TokenResponse])
async def all_tokens_in_db():
    """Выдача списка всех обьектов модели Token"""
    tokens = read_all_tokens()
    return [token.to_dict() for token in tokens]

if __name__ == "__main__":
    set_up_db(config)
    db.generate_mapping(create_tables=True)
    uvicorn.run(app, host="0.0.0.0", port=8000)