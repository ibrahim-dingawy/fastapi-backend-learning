from enum import Enum

from pydantic import BaseModel


class VideoStatus(str, Enum):
    processing = "processing"
    indexed = "indexed"
    failed = "failed"


class VideoCreate(BaseModel):
    title: str
    description: str
    status: VideoStatus


class VideoUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: VideoStatus | None = None


class VideoReplace(BaseModel):
    title: str
    description: str
    status: VideoStatus


class VideoStatusUpdate(BaseModel):
    status: VideoStatus


class VideoResponse(BaseModel):
    id: int
    title: str
    description: str
    status: VideoStatus


class VideoSearchResponse(BaseModel):
    query: str
    total: int
    results: list[VideoResponse]


class VideoFilterResponse(BaseModel):
    total: int
    page: int
    page_size: int
    results: list[VideoResponse]


class VideoSummaryResponse(BaseModel):
    total: int
    indexed: int
    processing: int
    failed: int