from bs4 import BeautifulSoup
from fastapi import HTTPException
from httpx import AsyncClient

from app.models.headline import Headline


async def scrape_headline(url: str) -> BeautifulSoup:
    async with AsyncClient() as client:
        response = await client.get(url)
        return BeautifulSoup(response.text, "html.parser")


def parse_headline(soup: BeautifulSoup) -> Headline:
    article = soup.select_one("article")
    if article is None:
        raise HTTPException(status_code=500, detail="Not found article")
    if "e-magazine" in article["class"]:
        title = article.find("h1", {"class": "e-magazine__title"})
        if title is None:
            raise HTTPException(status_code=500, detail="Not found title")
        content_div = article.find("div", {"class": "e-magazine__body"})
        if content_div is None:
            raise HTTPException(status_code=500, detail="Not found content")
        content = [p.text.replace("\xa0", " ") for p in content_div.find_all("p")]
        return Headline(title=title.text, content="".join(content))

    title = article.find("h1", {"class": "title-page"})
    if title is None:
        raise HTTPException(status_code=500, detail="Not found title")
    content_div = article.find("div", {"class": "singular-content"})
    if content_div is None:
        raise HTTPException(status_code=500, detail="Not found content")
    content = [p.text.replace("\xa0", " ") for p in content_div.find_all("p")]
    return Headline(title=title.text, content="".join(content))
