from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from core.configs import settings


class UserModel(settings.DBBaseModel):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    email = Column(String(255), index=True, nullable=True, unique=True)
    password = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False)
    articles = relationship(
        "ArticleModel",
        cascade="all,delete-orphan",
        back_populates="creator",
        uselist=True,
        lazy="joined"
    )
