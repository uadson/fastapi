from typing import List

from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from models.course_model import CourseModel
from core.deps import get_session

# Bypass warning SQLModel select
from sqlmodel.sql.expression import Select, SelectOfScalar

SelectOfScalar.inherit_cache = True # type: ignore
Select.inherit_cache = True # type: ignore
# End bypass

router = APIRouter()

# POST
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=CourseModel)
async def post_course(course: CourseModel, db: AsyncSession = Depends(get_session)):
    new_course = CourseModel(
        title=course.title,
        lessons=course.lessons,
        duration=course.duration
    )
    db.add(new_course)
    await db.commit()

    return new_course


# GET
@router.get('/', response_model=List[CourseModel])
async def get_courses(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CourseModel)
        result = await session.execute(query)
        courses: List[CourseModel] = result.scalars().all()

        return courses


# GET Course
@router.get('/{course_id}', response_model=CourseModel, status_code=status.HTTP_200_OK)
async def get_course(course_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CourseModel).filter(CourseModel.id == course_id)
        result = await session.execute(query)
        course = result.scalar_one_or_none()

        if course:
            return course
        else:
            raise HTTPException(detail="Course not found", status_code=status.HTTP_404_NOT_FOUND)
        

# PUT Course
@router.put('/{course_id}', response_model=CourseModel, status_code=status.HTTP_202_ACCEPTED)
async def put_course(course_id: int, course: CourseModel, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CourseModel).filter(CourseModel.id == course_id)
        result = await session.execute(query)
        course_up = result.scalar_one_or_none()

        if course_up:
            course_up.title = course.title
            course_up.lessons = course.lessons
            course_up.duration = course.duration

            await session.commit()

            return course_up
        else:
            raise HTTPException(detail="Course not found", status_code=status.HTTP_404_NOT_FOUND)


# DELETE Course
@router.delete('/{course_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(course_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CourseModel).filter(CourseModel.id == course_id)
        result = await session.execute(query)
        course_del = result.scalar_one_or_none()

        if course_del:
            await session.delete(course_del)
            await session.commit()

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail="Course not found", status_code=status.HTTP_404_NOT_FOUND)
