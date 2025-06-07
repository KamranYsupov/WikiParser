from fastapi import BackgroundTasks, APIRouter, Depends
from starlette import status
from dependency_injector.wiring import Provide, inject

from app.core.container import Container
from app.db.models import Article
from app.schemas.article import ArticleCreate, ArticleSchema
from app.services import ArticleService
from app.tasks.parser import parse_wiki_articles_task

router = APIRouter(tags=['Articles'], prefix='/articles')

@router.post('/parse', status_code=status.HTTP_200_OK)
@inject
async def parse_article(
        article_create_schema: ArticleCreate,
        background_tasks: BackgroundTasks,
) -> dict[str, str]:
    background_tasks.add_task(
        parse_wiki_articles_task,
        article_create_schema.title
    )
    return {'message': 'Парсинг запущен'}


@router.get('/{title}', status_code=status.HTTP_200_OK)
@inject
async def get_article(
        title: str,
        article_service: ArticleService = Depends(
            Provide[Container.article_service],
        )
) -> ArticleSchema:
    article: Article = await article_service.get(title=title)
    return article.serialize(schema_class=ArticleSchema, model_dump=True)


