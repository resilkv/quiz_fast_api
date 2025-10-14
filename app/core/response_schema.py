from pydantic import BaseModel
from typing import Generic, TypeVar, Optional
from pydantic.generics import GenericModel

DataT = TypeVar("DataT") 

class ResponseSchema(GenericModel, Generic[DataT]):

    status: str
    status_code: int
    message: str
    data: Optional[DataT] = None
    error: Optional[str] = None