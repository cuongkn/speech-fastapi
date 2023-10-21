from fastapi import APIRouter

from app.api import audio, headline

router = APIRouter()
router.include_router(headline.router, tags=["Headline"], prefix="/headline")
router.include_router(audio.router, tags=["Audio"], prefix="/audio")
