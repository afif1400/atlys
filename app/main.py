from fastapi import FastAPI
from app.api import scraping

app = FastAPI()

app.include_router(scraping.router)
