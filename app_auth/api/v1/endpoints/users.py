from typing import List, Optional, Any

from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.user_model import UserModel
from schemas.user_schema import (
    UserSchemaBase, UserSchemaCreate, UserSchemaUpdate, UserSchemaArticles
)

from core.deps import get_session, get_current_user
from core.security import generate_hash_passwd
from core.auth import authenticate, create_token_access

router = APIRouter()


# POST logon
@router.post('/login')
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: AsyncSession = Depends(get_session)):
    
    user = await authenticate(
        email=form_data.username, 
        password=form_data.password,
        db=db)
    
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid access data")
    
    return JSONResponse(
        content={"access_token": create_token_access(sub=user.id),
                 "token_type": "bearer"},
                 status_code=status.HTTP_200_OK)


# GET Logged
@router.get('/logged', response_model=UserSchemaBase)
def get_logged(user_logged: UserModel = Depends(get_current_user)):
    return user_logged


# POST SignUp
@router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=UserSchemaBase)
async def post_user(user: UserSchemaCreate, db: AsyncSession = Depends(get_session)):
    new_user: UserModel = UserModel(
        first_name = user.first_name,
        last_name = user.last_name,
        email = user.email,
        password = generate_hash_passwd(user.password),
        is_admin = user.is_admin
    )

    async with db as session:
        session.add(new_user)
        await session.commit()
        return new_user


# GET
@router.get('/', response_model=List[UserSchemaBase])
async def get_users(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UserModel)
        result = await session.execute(query)
        users: List[UserModel] = result.scalars().unique().all()

        return users
    

# GET User
@router.get('/{user_id}', response_model=UserSchemaArticles, status_code=status.HTTP_200_OK)
async def get_user(user_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UserModel).filter(UserModel.id == user_id)
        result = await session.execute(query)
        user: UserSchemaArticles = result.scalars().unique().one_or_none()

        if user:
            return user
        else:
            raise HTTPException(detail="User not found", status_code=status.HTTP_404_NOT_FOUND)


# PUT Article
@router.put('/{user_id}', response_model=UserSchemaBase, status_code=status.HTTP_202_ACCEPTED)
async def put_user(
    user_id: int, 
    user: UserSchemaUpdate, 
    db: AsyncSession = Depends(get_session)):

    async with db as session:
        query = select(UserModel).filter(UserModel.id == user_id)
        result = await session.execute(query)
        user_up: UserSchemaBase = result.scalars().unique().one_or_none()

        if user_up:
            if user.first_name:
                user_up.first_name = user.first_name
            if user.last_name:
                user_up.last_name = user.last_name
            if user.email:
                user_up.email = user.email
            if user.is_admin:
                user_up.is_admin = user.is_admin
            if user.password:
                user_up.password = generate_hash_passwd(user.password)

            await session.commit()
            return user_up
        else:
            raise HTTPException(detail="User not found", status_code=status.HTTP_404_NOT_FOUND)


# DELETE Course
@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_session)):

    async with db as session:
        query = select(UserModel).filter(UserModel.id == user_id)
        result = await session.execute(query)
        user_del: UserSchemaArticles = result.scalars().unique().one_or_none()

        if user_del:
            await session.delete_user(user_del)
            await session.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail="User not found", status_code=status.HTTP_404_NOT_FOUND)
