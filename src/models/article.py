from pydantic import BaseModel, Field
from typing import Optional, Literal


class URL(BaseModel):
    source: Literal["pravdask"]
    article_url: str = Field(..., description="Full article URL serves also as Unique ID")


class Comment(URL):
    post_id: str = Field(..., description="Unique identifier of the comment")
    author: str = Field(default="Anonymous", description="Comment author")
    text: str = Field(..., description="Comment content")
    rating: str = Field(default="0", description="Comment rating")
    timestamp: str = Field(default="", description="Comment timestamp in format DD.MM.YYYY HH:MM")
    parent_id: Optional[str] = Field(default=None, description="ID of parent comment if it's a reply")

    class Config:
        json_schema_extra = {
            "example": {
                "source": "pravdask",
                "article_url": "https://spravy.pravda.sk/domace/clanok/747227-nove",
                "post_id": "12345",
                "author": "JohnDoe",
                "text": "This is a comment",
                "rating": "5",
                "timestamp": "04.04.2025 14:30",
                "parent_id": None,
            }
        }


class Article(URL):
    title: str = Field(default="", description="Article title")
    description: str = Field(default="", description="Article description")
    body: str = Field(default="", description="Article main content")

    class Config:
        json_schema_extra = {
            "example": {
                "source": "pravdask",
                "article_url": "https://spravy.pravda.sk/domace/clanok/747227-nove",
                "title": "Sample Article",
                "description": "This is a sample article description",
                "body": "This is the main content of the article...",
            }
        }
