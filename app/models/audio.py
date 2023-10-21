from pydantic import BaseModel


class AudioMeta(BaseModel):
    sample_rate: float
    duration: float
