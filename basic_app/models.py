from typing import Optional

from pydantic import BaseModel, validator


class Course(BaseModel):
    id: Optional[int] = None # ID is optional
    title: str
    lessons: int
    duration: int

    # Example validation
    @validator('title')
    def validate_title(cls, value: str):
        words = value.split(' ')
        if len(words) < 2:
            raise ValueError('The title must be almost 2 words')
        
        if value.islower():
            raise ValueError('The title must be upper')
        return value 

courses = [
    Course(
        id=1,
        title="Python Full",
        lessons=100,
        duration=80
    ),

    Course(
        id=2,
        title="Django Framework",
        lessons=200,
        duration=100
    ),

    Course(
        id=3,
        title="Django Rest",
        lessons=70,
        duration=60
    ),

    Course(
        id=4,
        title="FastAPI Framework",
        lessons=80,
        duration=70
    )
    
]
