# app/models/requests.py
from pydantic import BaseModel, Field, validator
from typing import Optional

class SearchRequest(BaseModel):
    query: str = Field(
        ..., 
        min_length=1, 
        max_length=500,
        description="The search query to process"
    )
    max_results: int = Field(
        default=8, 
        ge=1, 
        le=20,
        description="Maximum number of sources to include"
    )
    include_sources: bool = Field(
        default=True,
        description="Whether to include source URLs in response"
    )
    
    @validator("query")
    def validate_query(cls, v):
        if not v.strip():
            raise ValueError("Query cannot be empty or whitespace only")
        return v.strip()

# app/models/responses.py
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class SearchResponse(BaseModel):
    query: str = Field(..., description="Original search query")
    answer: str = Field(..., description="AI-generated response")
    sources: List[str] = Field(..., description="Source URLs used")
    confidence: float = Field(
        ..., 
        ge=0.0, 
        le=1.0,
        description="Confidence score (0.0-1.0)"
    )
    processing_time: float = Field(..., description="Processing time in seconds")
    cached: bool = Field(default=False, description="Whether response was cached")
    cost_estimate: Optional[float] = Field(None, description="Estimated cost in USD")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class HealthResponse(BaseModel):
    status: str = Field(..., description="Overall system status")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    services: Dict[str, str] = Field(..., description="Individual service statuses")
    response_time_ms: Optional[float] = Field(None, description="Health check response time")

class ErrorResponse(BaseModel):
    error: str = Field(..., description="Error message")
    error_code: Optional[str] = Field(None, description="Error code")
    request_id: Optional[str] = Field(None, description="Request ID for tracking")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

# app/models/internal.py
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum

class ContentSource(str, Enum):
    NEWS = "news"
    ACADEMIC = "academic"
    SOCIAL = "social"
    ECOMMERCE = "ecommerce"
    GENERAL = "general"

class SearchResult(BaseModel):
    title: str
    url: str
    snippet: str
    source_engine: str
    relevance_score: float = Field(ge=0.0, le=1.0)

class ContentData(BaseModel):
    url: str
    title: str
    content: str
    word_count: int
    source_type: ContentSource = ContentSource.GENERAL
    extraction_method: str = "default"
    confidence_score: float = Field(default=1.0, ge=0.0, le=1.0)
    fetch_time: float = 0.0

class QueryEnhancement(BaseModel):
    original_query: str
    enhanced_queries: List[str]
    enhancement_method: str
    processing_time: float = 0.0
