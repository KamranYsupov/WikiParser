from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession
)

from app.core.config import settings


class DataBaseManager:
    """Менеджер для работы с базой данных"""

    def __init__(self, db_url: str):
        self.engine = create_async_engine(url=db_url)
        self.AsyncSessionLocal = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def get_async_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.AsyncSessionLocal() as session:
            yield session

    async def dispose(self):
        await self.engine.dispose()


db_manager = DataBaseManager(db_url=settings.db_url)



def provide_session(func):
    async def wrapper(*args, **kwargs):
        async with db_manager.AsyncSessionLocal() as session:
            try:
                return await func(*args, session=session, **kwargs)
            except Exception as e:
                await session.rollback()
                raise e
            finally:
                await session.close()

    return wrapper