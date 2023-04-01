from typing import Optional

from pydantic import BaseModel as SCBaseModel, HttpUrl


class ArticleSchema(SCBaseModel):
    id: Optional[int] = None
    title: str
    description: str
    url_font: HttpUrl
    user_id: Optional[int]
    
    class Config:
        orm_mode = True
