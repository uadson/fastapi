from core.configs import settings

from sqlalchemy import Column, Integer, String


class CourseModel(settings.DBBaseModel):
    __tablename__ = 'courses'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    title: str = Column(String(100))
    lessons: int = Column(Integer)
    duration: int = Column(Integer)
