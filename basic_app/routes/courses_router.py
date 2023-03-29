from fastapi import APIRouter

router = APIRouter()

@router.get('/api/v1/courses')
async def get_courses():
    return {"info": "All Courses"}
