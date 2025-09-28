from datetime import datetime
from enum import Enum
from typing import Optional, List, Any, Dict, Annotated
from pydantic import BaseModel, Field, ConfigDict, BeforeValidator
from bson import ObjectId


def validate_object_id(v: Any) -> ObjectId:
    if isinstance(v, ObjectId):
        return v
    if isinstance(v, str) and ObjectId.is_valid(v):
        return ObjectId(v)
    raise ValueError("Invalid ObjectId")


PyObjectId = Annotated[ObjectId, BeforeValidator(validate_object_id)]


class JobStatus(str, Enum):
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class SyncJob(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    url: str
    status: JobStatus = JobStatus.IN_PROGRESS
    created_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    total_pages_scraped: int = 0
    total_books_found: int = 0

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )


class RawData(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    sync_job_id: PyObjectId
    page_url: str
    book_title: str
    book_url: str
    image_url: str
    price: str
    stock_status: str
    rating: str
    is_data_processed: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    processed_at: Optional[datetime] = None

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )


class ProcessedBook(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    sync_job_id: PyObjectId
    raw_data_id: PyObjectId
    title: str
    image_url: str
    price_excl_tax: Optional[str] = None
    price_incl_tax: Optional[str] = None
    stock_status: str
    star_count: int = 0
    description: Optional[str] = None
    product_type: Optional[str] = None
    availability: Optional[str] = None
    upc: Optional[str] = None
    tax: Optional[str] = None
    number_of_reviews: Optional[str] = None
    price_color: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )


class ScrapingMetrics(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    sync_job_id: PyObjectId
    total_pages: int = 0
    successful_pages: int = 0
    failed_pages: int = 0
    total_books_raw: int = 0
    total_books_processed: int = 0
    start_time: datetime = Field(default_factory=datetime.utcnow)
    end_time: Optional[datetime] = None
    duration_seconds: Optional[float] = None

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )


class PaginationInfo(BaseModel):
    page: int
    limit: int
    total: int
    total_pages: int
    has_next: bool
    has_prev: bool


class BookResponse(BaseModel):
    id: str = Field(alias="_id")
    title: str
    image_url: str
    price_excl_tax: Optional[str] = None
    price_incl_tax: Optional[str] = None
    stock_status: str
    star_count: int = 0
    description: Optional[str] = None
    product_type: Optional[str] = None
    availability: Optional[str] = None
    upc: Optional[str] = None
    tax: Optional[str] = None
    number_of_reviews: Optional[str] = None
    price_color: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={ObjectId: str}
    )


class BooksListResponse(BaseModel):
    books: List[BookResponse]
    pagination: PaginationInfo


class BookDetailResponse(BaseModel):
    book: BookResponse


class BookQueryParams(BaseModel):
    page: int = 1
    limit: int = 10
    category: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    rating: Optional[int] = None
    sort_by: str = "created_at"

    model_config = ConfigDict(
        validate_assignment=True
    )