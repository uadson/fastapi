from typing import Optional, List

from pydantic import BaseModel as SCBaseModel, EmailStr

from schemas.article_schema import ArticleSchema


class UserSchemaBase(SCBaseModel):
    id: Optional[int] = None
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    is_admin: bool = False

    class Config:
        orm_mode = True


class UserSchemaCreate(UserSchemaBase):
    password: str


class UserSchemaArticles(UserSchemaBase):
    articles: Optional[List[ArticleSchema]]


class UserSchemaUpdate(UserSchemaBase):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]
    is_admin: Optional[bool]
