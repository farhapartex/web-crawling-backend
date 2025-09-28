from fastapi import APIRouter, Query, HTTPException, status, Depends
from typing import Optional
from models.schemas import BooksListResponse, BookDetailResponse, BookQueryParams
from services.book_service import book_service

router = APIRouter()

def get_book_query_params(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    category: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),
    rating: Optional[int] = Query(None, ge=0, le=5),
    sort_by: str = Query("created_at", regex="^(rating|price|reviews|created_at)$")
) -> BookQueryParams:
    return BookQueryParams(
        page=page,
        limit=limit,
        category=category,
        min_price=min_price,
        max_price=max_price,
        rating=rating,
        sort_by=sort_by
    )

@router.get("/books", response_model=BooksListResponse)
async def get_books(params: BookQueryParams = Depends(get_book_query_params)):
    try:
        return book_service.get_books(params)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/books/{book_id}", response_model=BookDetailResponse)
async def get_book_detail(book_id: str):
    try:
        return book_service.get_book_by_id(book_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )