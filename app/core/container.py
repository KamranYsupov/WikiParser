from dependency_injector import containers, providers
from openai import OpenAI

from app.db import DataBaseManager
from app.core.config import settings


class Container(containers.DeclarativeContainer):
    db_manager = providers.Singleton(DataBaseManager, db_url=settings.db_url)
    session = providers.Resource(db_manager().get_async_session)

    openai_client = providers.Singleton(
        OpenAI,
        base_url=settings.base_url,
        api_key=settings.api_key
    )
