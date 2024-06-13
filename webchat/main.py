from fastapi import FastAPI

from configs import settings

import endpoints
import uvicorn

app = FastAPI()

app.mount('/static', settings.STATICFILES, name='static')
app.include_router(endpoints.router)

if __name__ == '__main__':
    uvicorn.run(app='main:app', host='0.0.0.0', port=8000, reload=True, log_level='info')
