import asyncio
from typing import List, Set

import aiohttp
from fastapi import HTTPException
import loguru

from app.core.config import settings
from app.db.models import Article
from app.repositories.article import RepositoryArticle


class WikiParserService:
    """Сервис для парсинга википедии"""
    def __init__(
            self,
            repository_article: RepositoryArticle,
            api_url: str = settings.wiki_api_url,
    ):
        self._repository_article = repository_article
        self.api_url = api_url

    async def fetch_wiki_article(
            self,
            session: aiohttp.ClientSession,
            title: str
    ) -> dict:
        params = {
            'action': 'parse',
            'page': title,
            'format': 'json',
        }
        async with session.get(self.api_url, params=params) as resp:
            if resp.status != 200:
                raise HTTPException(status_code=resp.status, detail=f'Wiki API error for {title}')
            data = await resp.json()
            if 'error' in data:
                raise HTTPException(status_code=404, detail=f'Article {title} not found')

            return data['parse']


    @staticmethod
    def extract_links(parse_text: dict) -> List[str]:
        links = parse_text.get('links', [])
        titles = []
        for link in links:
            if link.get('ns') == 0 and not link.get('exists') is False:
                link_title = link.get('*')
                if link_title and not any(link_title.startswith(prefix) for prefix in
                                          ['File:', 'Help:', 'Special:', 'Category:', 'Template:']):
                    titles.append(link_title)
        return titles

    async def parse_article_recursive(
            self,
            session: aiohttp.ClientSession,
            title: str,
            visited: Set[str] = set(),
            max_depth: int = 5,
            current_depth: int = 1
    ):
        loguru.logger.info(title)
        if current_depth > max_depth or title in visited:
            return

        visited.add(title)
        parse_data = await self.fetch_wiki_article(session, title)

        content_html = parse_data.get('text', {}).get('*', )
        corrected_title = title.replace(' ', '_')
        url = f'{settings.wiki_base_url}/wiki/{corrected_title}'


        article = await self._repository_article.exists(
            Article.title == title,
            Article.url == url
        )
        if not article:
            article = await self._repository_article.create(
                dict(title=title, url=url, content=content_html)
            )

        links = self.extract_links(parse_data)

        links_to_parse = links[:10] # Ограничение первые 10 ссылок

        tasks = []
        for link_title in links_to_parse:
            task = self.parse_article_recursive(
                session=session,
                title=link_title,
                visited=visited,
                max_depth=max_depth,
                current_depth=current_depth + 1
            )

            tasks.append(task)

        await asyncio.gather(*tasks)


        return article


