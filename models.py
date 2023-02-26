from typing import Optional

from pydantic impor BaseModel


class Course(BaseModel):
    id: Optional[int] = None
    title: str
    classes: int
    hours: int

