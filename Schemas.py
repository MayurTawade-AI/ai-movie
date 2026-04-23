from dataclasses import Field

from pydantic import BaseModel , Field
from typing import Optional

class MovieCreate(BaseModel):
    title: str
    director: str
    rating: float = Field(ge=1.0, le=5.0, description="Rating must bebetween 1 and 5")
    year: int = Field(ge=1888 , le=2026 , description = "movie year must be valid")
    summary: Optional[str] = None


class MovieResponse(MovieCreate):
    id: int
    tags : str

    class Config:
        from_attributes = True