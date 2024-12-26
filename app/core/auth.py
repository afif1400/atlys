from fastapi import HTTPException, Header
from app.config import Settings

async def authenticate(token: str = Header(...)):
    settings = Settings()
    if token != settings.API_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")
        # raise HTTPException(status_code=401, detail="Unauthorized")
