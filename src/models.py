from pydantic import BaseModel, HttpUrl


class CreateRequest(BaseModel):
    media_url: HttpUrl
    owner: str

class TokenResponse(BaseModel):
    id: int
    unique_hash: str
    tx_hash: str
    media_url: str
    owner: str

class TotalSupply(BaseModel):
    total_supply: str