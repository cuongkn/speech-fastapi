from typing import Optional

from pydantic import BaseModel, HttpUrl


class Request(BaseModel):
    url: HttpUrl


class Headline(BaseModel):
    title: Optional[str]
    content: Optional[str]
