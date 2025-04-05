from typing import List

from fastapi import APIRouter, HTTPException
from src.services.pravda.pravdask import PravdaSK
from src.models.article import Comment, Article

router = APIRouter(
    prefix="/pravda",
    tags=["pravda"],
    responses={404: {"description": "Not found"}},
)


@router.get("/article", response_model=Article)
async def get_article(url: str):
    """
    Extract article title, description and body from a pravda.sk article
    """
    try:
        pravda = PravdaSK(url)
        article_data = pravda.parse_article()
        return article_data
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")


@router.get("/comments", response_model=List[Comment])
async def get_article_comments(url: str):
    """
    Extract all comments from a pravda.sk article
    """
    try:
        pravda = PravdaSK(url)
        comments = pravda.scrape_comments()
        return comments
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")
