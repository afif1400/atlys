from typing import Optional
from fastapi import APIRouter, Depends
from app.services.scraper import Scraper
from app.repository.json import JSONRepository
from app.services.notifier import Notifier
from app.core.auth import authenticate

router = APIRouter()

@router.post("/scrape", dependencies=[Depends(authenticate)])
async def scrape(max_pages: int, proxy: Optional[str] = None):
    scraper = Scraper(
        base_url="https://dentalstall.com/shop",
        max_pages=max_pages,
        proxy=proxy
    )
    products = await scraper.scrape()
    print(products)
    repository = JSONRepository()
    repository.update(products)

    notifier = Notifier()
    notifier.notify(f"Scraping completed. Total products scraped: {len(products)}")
    return {"message": "Scraping complete", "count": len(products)}
