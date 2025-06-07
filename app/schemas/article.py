import uuid
from typing import Optional

from pydantic import BaseModel


class ArticleCreate(BaseModel):
    title: str

class ArticleSchema(BaseModel):
    id: uuid.UUID
    title: str
    summary: Optional[str] = None