from fastapi import APIRouter

from app.models.headline import Headline, Request
from app.services.headline import parse_headline, scrape_headline

router = APIRouter()


@router.post("/")
async def get_headline(headline: Request) -> Headline:
    soup = await scrape_headline(str(headline.url))
    return parse_headline(soup)
