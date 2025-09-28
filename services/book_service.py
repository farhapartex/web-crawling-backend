from typing import Tuple, List
from bson import ObjectId
from math import ceil
from database import db_connection
from models.schemas import BookQueryParams, BookResponse, PaginationInfo, BooksListResponse, BookDetailResponse

class BookService:
    def __init__(self):
        self.collection = db_connection.get_collection("processed_books")

    def get_books(self, params: BookQueryParams) -> BooksListResponse:
        query = self._build_query(params)
        sort_field, sort_direction = self._get_sort_criteria(params.sort_by)

        skip = (params.page - 1) * params.limit

        cursor = self.collection.find(query).sort(sort_field, sort_direction).skip(skip).limit(params.limit)
        books = list(cursor)

        total = self.collection.count_documents(query)
        total_pages = ceil(total / params.limit)

        book_responses = []
        for book in books:
            book["_id"] = str(book["_id"])
            book_responses.append(BookResponse(**book))

        pagination = PaginationInfo(
            page=params.page,
            limit=params.limit,
            total=total,
            total_pages=total_pages,
            has_next=params.page < total_pages,
            has_prev=params.page > 1
        )

        return BooksListResponse(books=book_responses, pagination=pagination)

    def get_book_by_id(self, book_id: str) -> BookDetailResponse:
        if not ObjectId.is_valid(book_id):
            raise ValueError("Invalid book ID format")

        book = self.collection.find_one({"_id": ObjectId(book_id)})

        if not book:
            raise FileNotFoundError("Book not found")

        book["_id"] = str(book["_id"])
        book_response = BookResponse(**book)

        return BookDetailResponse(book=book_response)

    def _build_query(self, params: BookQueryParams) -> dict:
        query = {}

        if params.category:
            query["product_type"] = {"$regex": params.category, "$options": "i"}

        if params.min_price is not None or params.max_price is not None:
            price_query = {}
            if params.min_price is not None:
                price_query["$gte"] = params.min_price
            if params.max_price is not None:
                price_query["$lte"] = params.max_price

            query["$or"] = [
                {"price_excl_tax": {"$regex": r"£(\d+\.?\d*)", "$options": "i"}},
                {"price_incl_tax": {"$regex": r"£(\d+\.?\d*)", "$options": "i"}},
                {"price_color": {"$regex": r"£(\d+\.?\d*)", "$options": "i"}}
            ]

        if params.rating is not None:
            query["star_count"] = params.rating

        return query

    def _get_sort_criteria(self, sort_by: str) -> Tuple[str, int]:
        sort_direction = -1

        if sort_by == "rating":
            sort_field = "star_count"
        elif sort_by == "price":
            sort_field = "price_excl_tax"
        elif sort_by == "reviews":
            sort_field = "number_of_reviews"
        else:
            sort_field = "created_at"

        return sort_field, sort_direction

book_service = BookService()