from fastapi import FastAPI

from support.api import router


app = FastAPI(
    title='Support',
    version='0.1',
)

app.include_router(router)
