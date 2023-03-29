from time import sleep

from typing import Optional, Any, Dict, List

import uvicorn

from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import status
# from fastapi.responses import JSONResponse
from fastapi import Response

# Path Parameters
from fastapi import Path

# Query Parameters
from fastapi import Query

# Header Parameters
from fastapi import Header

# Depends
from fastapi import Depends

# Data
from models import Course, courses

# Routers
from routes import courses_router
from routes import users_router

##### MAIN APP OBJECT #####
app = FastAPI(
	# Docs
	title='FastAPI Course - Geek University',
	version='0.1.0',
	description='A api to study'
)

# Routers
app.include_router(courses_router.router, tags=['courses'])
app.include_router(users_router.router, tags=['users'])

##### DB SIMULATION #####
def fake_db():
	try:
		print("Open connection")
		sleep(1)
	finally:
		print("Closing connection")
		sleep(1)


##### GET #####
@app.get('/courses', 
	 description="Return a courses list", 
	 summary="Return all courses",
	 # response_model=Dict[int, Course])
	 response_model=List[Course],
	 response_description="Courses finded successfully! ")

async def courses_list(db: Any = Depends(fake_db)):
	return courses


##### GET A ELEMENT #####
@app.get('/courses/{course_id}')
async def course_retrieve(course_id: int = Path(
	default=None, 
	title='Course ID', 
	description='Must be between 1 and 2', 
	gt=0, lt=3),# gt -> maior que lt -> menor que -> Path Parameters
	db: Any = Depends(fake_db)): 
	
	try:
		course = courses[course_id]
		return course
	except KeyError:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Course not found. :(')
	

##### POST #####
@app.post('/courses', 
	  status_code=status.HTTP_201_CREATED,
	  response_model=Course)

async def course_add(
	course: Course):

	next_id: int = len(courses) + 1
	course.id = next_id
	courses.append(course)
	return course


##### PUT #####
@app.put('/courses/{course_id}')
async def course_update(
	course_id: int, 
	course: Course,
	db: Any = Depends(fake_db)):

	if course_id in courses:
		courses[course_id] = course
		# course.id = course_id
		del course.id
		return course
	else:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Course not found. :(')
	

##### DELETE #####
@app.delete('/courses/{course_id}')
async def course_delete(
	course_id: int,
	db: Any = Depends(fake_db)):

	if course_id in courses_router:
		del courses[course_id]
		# return JSONResponse(content="", status_code=status.HTTP_204_NO_CONTENT)
		return Response(status_code=status.HTTP_204_NO_CONTENT)
	else:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Course not found. :(')



##### Query Parameters #####
@app.get('/calc')
async def calc(
	a: int = Query(default=None, gt=5), 
	b: int = Query(default=None, gt=10), 
	x_geek: str = Header(default=None), # Header Parameter
	c: Optional[int] = None,
	db: Any = Depends(fake_db)): # valor de c é opcional
	
	sum = a + b
	if c:
		sum = sum + c
	
	print(f'X-GEEK: {x_geek}')
	return {"result": sum}


if __name__ == '__main__':
	uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
