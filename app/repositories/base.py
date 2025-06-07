from uuid import UUID
from typing import (
    Generic,
    Optional,
    Type,
    TypeVar,
    List,
    Tuple
)

from sqlalchemy import select, update, delete, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.manager import db_manager, provide_session

ModelType = TypeVar("ModelType")


class RepositoryBase(Generic[ModelType,]):
    """Репозиторий с базовым CRUD"""

    def __init__(
            self,
            model: Type[ModelType],
    ) -> None:
        self.model = model

    @provide_session
    async def create(
            self,
            insert_data: dict,
            session: Optional[AsyncSession] = None,
    ) -> ModelType:
        db_obj = self.model(**insert_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)

        return db_obj

    @provide_session
    async def get(
            self,
            options: List = [],
            session: Optional[AsyncSession] = None,
            **kwargs
    ) -> Optional[ModelType]:
        statement = select(self.model).options(*options).filter_by(**kwargs)
        result = await session.execute(statement)
        return result.scalars().first()

    @provide_session
    async def update(
            self,
            *,
            obj_id: UUID,
            insert_data: dict,
            session: Optional[AsyncSession] = None,
    ) -> ModelType:
        statement = (
            update(self.model).
            where(self.model.id == obj_id).
            values(**insert_data)
        )
        await session.execute(statement)
        await session.commit()

        return await session.get(self.model, obj_id)

    @provide_session
    async def list(
            self,
            *args,
            options: List = [],
            limit: Optional[int] = None,
            skip: Optional[int] = None,
            session: Optional[AsyncSession] = None,
            **kwargs
    ):
        statement = (
            select(self.model)
            .options(*options)
            .filter(*args)
            .filter_by(**kwargs)
            .offset(skip)
            .limit(limit)
        )
        result = await session.execute(statement)
        return result.scalars().all()

    @provide_session
    async def delete(self, *args, session: Optional[AsyncSession] = None, **kwargs) -> None:
        statement = delete(self.model).filter(*args).filter_by(**kwargs)
        await session.execute(statement)

    @provide_session
    async def exists(
            self,
            *args,
            session: Optional[AsyncSession] = None,
            **kwargs,
    ) -> Optional[ModelType]:
        statement = select(self.model).filter(or_(*args)).filter_by(**kwargs)
        result = await session.execute(statement)
        return result.scalars().first()