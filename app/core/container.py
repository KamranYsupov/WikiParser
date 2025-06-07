from dependency_injector import containers, providers
from openai import OpenAI

from app.db import DataBaseManager
from app.core.config import settings
from app.db.models import Article
from app.repositories import (
    RepositoryArticle,
)
from app.services import (
    ArticleService,
    WikiParserService,
)

class Container(containers.DeclarativeContainer):
    openai_client = providers.Singleton(
        OpenAI,
        base_url=settings.openai_base_url,
        api_key=settings.openai_api_key
    )

    # region репозитории
    repository_article = providers.Singleton(
        RepositoryArticle,
        model=Article,
    )
    # endregion

    # region сервисы
    article_service = providers.Singleton(
        ArticleService,
        repository=repository_article
    )
    wiki_parser_service = providers.Singleton(
        WikiParserService,
        repository_article=repository_article,
    )
    # endregion

