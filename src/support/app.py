from fastapi import FastAPI

from support.api import router


app = FastAPI()

app.include_router(router)
