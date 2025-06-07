from uuid import UUID
from typing import (
    Generic,
    Sequence,
    TypeVar,
    Type,
    Optional,
)

from app.repositories.base import ModelType

RepositoryType = TypeVar('RepositoryType')


class CRUDBaseService(Generic[RepositoryType, ]):
    """Класс с базовым CRUD для сервисов"""

    def __init__(
            self,
            repository: Type[RepositoryType],
    ):
        self._repository = repository

    async def get(self, **kwargs) -> ModelType:
        return await self._repository.get(**kwargs)

    async def create(self, obj_in) -> ModelType:
        return await self._repository.create(
            insert_data=dict(obj_in),
        )

    async def update(self, *, obj_id: UUID, obj_in) -> ModelType:
        return await self._repository.update(
            obj_id=obj_id,
            insert_data=dict(obj_in),
        )

    async def list(
            self,
            *args,
            skip: Optional[int] = None,
            limit: Optional[int] = None,
            **kwargs
    ) -> list[ModelType]:
        return await self._repository.list(
            *args,
            skip=skip,
            limit=limit,
            **kwargs
        )

    async def delete(self, obj_id: UUID) -> None:
        return await self._repository.delete(obj_id=obj_id)

    async def exists(self, *args, **kwargs) -> Optional[ModelType]:
        return await self._repository.exists(*args, **kwargs)



