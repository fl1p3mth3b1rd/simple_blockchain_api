from typing import List

from pony.orm import db_session, select, desc

from src.db.db_models import Token


def write_token(
    unique_hash: str,
    tx_hash: str,
    media_url: str,
    owner: str
    ) -> Token:
    """Запись токена в базу данных"""
    with db_session:
        t = Token(
            unique_hash = unique_hash,
            tx_hash = tx_hash,
            media_url = media_url,
            owner = owner
        )
        return t


def read_all_tokens() -> List[Token]:
    """Получение всех токенов из базы данных"""
    with db_session:
        return list(select(t for t in Token).order_by(lambda t: desc(t.id)))