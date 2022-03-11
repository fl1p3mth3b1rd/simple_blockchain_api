from pydantic import BaseModel, HttpUrl


class CreateRequest(BaseModel):
    media_url: HttpUrl
    owner: str