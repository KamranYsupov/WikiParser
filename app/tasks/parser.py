from typing import Set

import aiohttp
from dependency_injector.wiring import Provide, inject
from openai import OpenAI

from app.core.container import Container
from app.db.models import Article
from app.services import WikiParserService, ArticleService
from app.utils.ai import get_content_summary


@inject
async def parse_wiki_articles_task(
        title: str,
        visited: Set[str] = set(),
        max_depth: int = 5,
        current_depth: int = 1,
        article_service: ArticleService = Provide[
            Container.article_service
        ],
        wiki_parser_service: WikiParserService = Provide[
            Container.wiki_parser_service
        ]
):
    async with aiohttp.ClientSession() as session:
        root_article: Article = await wiki_parser_service.parse_article_recursive(
            session=session,
            title=title,
            visited=visited,
            max_depth=max_depth,
            current_depth=current_depth,
        )

        if root_article:
            summary = get_content_summary(content=root_article.content)
            await article_service.update(
                obj_id=root_article.id,
                obj_in={'summary': summary}
            )