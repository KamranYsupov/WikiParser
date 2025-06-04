import copy
from typing import Dict, Sequence, TypeVar, Optional, Union

from sqlalchemy import func, MetaData
from sqlalchemy.orm import DeclarativeBase, declared_attr

from app.core.config import settings

SchemaType = TypeVar('SchemaType')


class Base(DeclarativeBase):
    __abstract__ = True

    metadata = MetaData(
        naming_convention=settings.metadata_naming_convention
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f'{cls.__name__.lower()}s'

    def serialize(
            self,
            schema_class,
            model_dump: bool = False,
            exclude_fields: Sequence[str] = [],
    ) -> Optional[Union[Dict, SchemaType]]:
        serialized_data = {}
        schema_fields = schema_class.model_fields.keys()
        data = copy.deepcopy(self.__dict__)

        for field in schema_fields:
            serialized_data[field] = data.get(field)

        if not exclude_fields:
            return serialized_data

        for field in exclude_fields:
            serialized_data.pop(field)

        if model_dump:
            return serialized_data

        return schema_class(**serialized_data)