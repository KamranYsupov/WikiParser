import uuid

from pydantic import BaseModel, HttpUrl


class ArticleCreate(BaseModel):
    title: str

class ArticleSchema(BaseModel):
    id: uuid.UUID
    title: str
    summary: str