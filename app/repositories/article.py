from app.db.models import Article
from app.repositories.base import RepositoryBase


class RepositoryArticle(RepositoryBase[Article]):
    """Репозиторий модели Article"""
    pass