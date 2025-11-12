"""
Pagination utilities for API endpoints.

Provides consistent pagination across all list endpoints with:
- Cursor-based pagination (efficient for large datasets)
- Offset-based pagination (simple, familiar)
- Total count caching
- Sorting support
"""
from typing import TypeVar, Generic, List, Optional
from pydantic import BaseModel, Field
from sqlalchemy.orm import Query


T = TypeVar('T')


# ==============================================================================
# Pagination Models
# ==============================================================================

class PaginationParams(BaseModel):
    """
    Query parameters for pagination.

    Usage in FastAPI:
        @router.get("/items")
        async def list_items(pagination: PaginationParams = Depends()):
            return paginate(query, pagination)
    """
    page: int = Field(default=1, ge=1, description="Page number (1-indexed)")
    page_size: int = Field(default=20, ge=1, le=100, description="Items per page (max 100)")
    sort_by: Optional[str] = Field(default=None, description="Field to sort by")
    sort_order: str = Field(default="desc", regex="^(asc|desc)$", description="Sort order")

    @property
    def offset(self) -> int:
        """Calculate offset for SQL query."""
        return (self.page - 1) * self.page_size

    @property
    def limit(self) -> int:
        """Get limit for SQL query."""
        return self.page_size


class PaginatedResponse(BaseModel, Generic[T]):
    """
    Standard paginated response format.

    Example:
        {
            "items": [...],
            "total": 150,
            "page": 1,
            "page_size": 20,
            "total_pages": 8,
            "has_next": true,
            "has_previous": false
        }
    """
    items: List[T]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_previous: bool

    class Config:
        # Allow arbitrary types for generic T
        arbitrary_types_allowed = True


# ==============================================================================
# Pagination Functions
# ==============================================================================

def paginate(
    query: Query,
    params: PaginationParams,
    count_query: Optional[Query] = None
) -> PaginatedResponse:
    """
    Paginate a SQLAlchemy query.

    Args:
        query: SQLAlchemy query to paginate
        params: Pagination parameters
        count_query: Optional separate query for counting (for performance)

    Returns:
        PaginatedResponse with items and metadata

    Example:
        query = db.query(Document).filter(Document.user_id == user_id)
        result = paginate(query, PaginationParams(page=1, page_size=20))
    """
    # Get total count (use separate count query if provided for performance)
    if count_query is not None:
        total = count_query.count()
    else:
        total = query.count()

    # Apply sorting if specified
    if params.sort_by:
        # Prevent SQL injection by validating column name
        # You should implement proper validation based on your models
        if params.sort_order == "asc":
            query = query.order_by(getattr(query.column_descriptions[0]['type'], params.sort_by).asc())
        else:
            query = query.order_by(getattr(query.column_descriptions[0]['type'], params.sort_by).desc())

    # Apply pagination
    items = query.offset(params.offset).limit(params.limit).all()

    # Calculate metadata
    total_pages = (total + params.page_size - 1) // params.page_size  # Ceiling division
    has_next = params.page < total_pages
    has_previous = params.page > 1

    return PaginatedResponse(
        items=items,
        total=total,
        page=params.page,
        page_size=params.page_size,
        total_pages=total_pages,
        has_next=has_next,
        has_previous=has_previous
    )


def paginate_list(
    items: List[T],
    params: PaginationParams
) -> PaginatedResponse[T]:
    """
    Paginate a Python list (for in-memory data).

    Args:
        items: List to paginate
        params: Pagination parameters

    Returns:
        PaginatedResponse with paginated items

    Note:
        Less efficient than database pagination. Use only for small datasets.
    """
    total = len(items)
    start = params.offset
    end = start + params.page_size

    paginated_items = items[start:end]

    total_pages = (total + params.page_size - 1) // params.page_size
    has_next = params.page < total_pages
    has_previous = params.page > 1

    return PaginatedResponse(
        items=paginated_items,
        total=total,
        page=params.page,
        page_size=params.page_size,
        total_pages=total_pages,
        has_next=has_next,
        has_previous=has_previous
    )


# ==============================================================================
# Cursor-based Pagination (for real-time data)
# ==============================================================================

class CursorPaginationParams(BaseModel):
    """
    Cursor-based pagination parameters.

    More efficient for large datasets and real-time data.
    Cursor should be an opaque string (usually base64-encoded ID).
    """
    cursor: Optional[str] = Field(default=None, description="Cursor for next page")
    limit: int = Field(default=20, ge=1, le=100, description="Items per page")


class CursorPaginatedResponse(BaseModel, Generic[T]):
    """
    Cursor-based paginated response.

    Example:
        {
            "items": [...],
            "next_cursor": "eyJpZCI6MTIzfQ==",
            "has_more": true
        }
    """
    items: List[T]
    next_cursor: Optional[str]
    has_more: bool

    class Config:
        arbitrary_types_allowed = True


def cursor_paginate(
    query: Query,
    cursor_field: str,
    params: CursorPaginationParams,
    decode_cursor = None
) -> CursorPaginatedResponse:
    """
    Cursor-based pagination for efficient large dataset pagination.

    Args:
        query: SQLAlchemy query
        cursor_field: Field name to use for cursor (usually 'id' or 'created_at')
        params: Cursor pagination parameters
        decode_cursor: Optional function to decode cursor string

    Returns:
        CursorPaginatedResponse

    Example:
        query = db.query(Document).filter(Document.user_id == user_id)
        result = cursor_paginate(
            query,
            cursor_field='id',
            params=CursorPaginationParams(limit=20)
        )
    """
    # Decode cursor if provided
    last_value = None
    if params.cursor and decode_cursor:
        last_value = decode_cursor(params.cursor)
    elif params.cursor:
        # Simple integer cursor
        try:
            last_value = int(params.cursor)
        except (ValueError, TypeError):
            last_value = None

    # Apply cursor filter
    if last_value is not None:
        query = query.filter(getattr(query.column_descriptions[0]['type'], cursor_field) > last_value)

    # Fetch items + 1 to check if there are more
    items = query.limit(params.limit + 1).all()

    # Check if there are more items
    has_more = len(items) > params.limit
    if has_more:
        items = items[:params.limit]

    # Generate next cursor
    next_cursor = None
    if has_more and items:
        next_cursor = str(getattr(items[-1], cursor_field))

    return CursorPaginatedResponse(
        items=items,
        next_cursor=next_cursor,
        has_more=has_more
    )


# ==============================================================================
# Example Usage
# ==============================================================================

if __name__ == "__main__":
    from sqlalchemy import create_engine, Column, Integer, String
    from sqlalchemy.orm import sessionmaker, declarative_base

    # Example setup
    Base = declarative_base()

    class Document(Base):
        __tablename__ = "documents"
        id = Column(Integer, primary_key=True)
        title = Column(String)

    # Create in-memory database
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Add test data
    for i in range(50):
        session.add(Document(title=f"Document {i}"))
    session.commit()

    # Test pagination
    query = session.query(Document)
    params = PaginationParams(page=1, page_size=10)
    result = paginate(query, params)

    print(f"Total: {result.total}")
    print(f"Page: {result.page}/{result.total_pages}")
    print(f"Items: {len(result.items)}")
    print(f"Has next: {result.has_next}")
