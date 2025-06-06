
from .base import CRUDBaseService
from app.repositories.article import RepositoryArticle


class ArticleService(CRUDBaseService[RepositoryArticle]):
    pass
