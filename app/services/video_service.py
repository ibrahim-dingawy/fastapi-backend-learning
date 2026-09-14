import time
from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.core.config import (
    ALLOWED_VIDEO_TYPES,
    MAX_FILE_SIZE,
    UPLOAD_DIRECTORY,
)
from app.database import SessionLocal
from app.models.user import User
from app.models.video import Video
from app.schemas.video import VideoStatus

# =========================================================
# Basic CRUD
# =========================================================


def user_can_access_video(
    video: Video,
    current_user: User,
) -> bool:
    if current_user.role == "admin":
        return True

    return video.user_id == current_user.id


def get_all_videos_orm(
    db: Session,
):
    return db.query(Video).all()


def get_video_orm(
    db: Session,
    video_id: int,
):
    return (
        db.query(Video)
        .filter(Video.id == video_id)
        .first()
    )



def create_video_orm(
    db: Session,
    title: str,
    description: str,
    status_value: str,
    user_id: int,
):
    video = Video(
        title=title,
        description=description,
        status=status_value,
        user_id=user_id,
    )

    db.add(video)
    db.commit()
    db.refresh(video)

    return video



def update_video_orm(
    db: Session,
    video_id: int,
    title: str | None = None,
    description: str | None = None,
    status_value: str | None = None,
):
    video = get_video_orm(
        db=db,
        video_id=video_id,
    )

    if video is None:
        return None

    if title is not None:
        video.title = title

    if description is not None:
        video.description = description

    if status_value is not None:
        video.status = status_value

    db.commit()
    db.refresh(video)

    return video


def replace_video_orm(
    db: Session,
    video_id: int,
    title: str,
    description: str,
    status_value: str,
):
    video = get_video_orm(
        db=db,
        video_id=video_id,
    )

    if video is None:
        return None

    video.title = title
    video.description = description
    video.status = status_value

    db.commit()
    db.refresh(video)

    return video


def delete_video_orm(
    db: Session,
    video_id: int,
):
    video = get_video_orm(
        db=db,
        video_id=video_id,
    )

    if video is None:
        return None

    db.delete(video)
    db.commit()

    return video


# =========================================================
# Search / Filter / Summary
# =========================================================

def search_videos_orm(
    db: Session,
    word: str,
):
    search_value = f"%{word}%"

    return (
        db.query(Video)
        .filter(
            (Video.title.ilike(search_value))
            |
            (Video.description.ilike(search_value))
        )
        .all()
    )


def get_videos_by_status_orm(
    db: Session,
    video_status: VideoStatus,
):
    return (
        db.query(Video)
        .filter(
            Video.status == video_status.value
        )
        .all()
    )


def get_limited_videos_by_status_orm(
    db: Session,
    status_value: VideoStatus,
    limit: int | None = None,
):
    query = (
        db.query(Video)
        .filter(
            Video.status == status_value.value
        )
    )

    if limit is not None:
        query = query.limit(limit)

    return query.all()


def get_video_summary_orm(
    db: Session,
):
    total = db.query(Video).count()

    indexed = (
        db.query(Video)
        .filter(
            Video.status
            == VideoStatus.indexed.value
        )
        .count()
    )

    processing = (
        db.query(Video)
        .filter(
            Video.status
            == VideoStatus.processing.value
        )
        .count()
    )

    failed = (
        db.query(Video)
        .filter(
            Video.status
            == VideoStatus.failed.value
        )
        .count()
    )

    return {
        "total": total,
        "indexed": indexed,
        "processing": processing,
        "failed": failed,
    }


def filter_videos_orm(
    db: Session,
    status_filter: VideoStatus | None = None,
    title: str | None = None,
    sort_by: str | None = None,
    sort_order: str = "asc",
    page: int = 1,
    page_size: int = 10,
):
    query = db.query(Video)

    if status_filter is not None:
        query = query.filter(
            Video.status == status_filter.value
        )

    if title is not None:
        query = query.filter(
            Video.title.ilike(f"%{title}%")
        )

    # Count after filtering but before pagination.
    total = query.count()

    allowed_sort_fields = {
        "id": Video.id,
        "title": Video.title,
        "status": Video.status,
    }

    if sort_by is not None:
        if sort_by not in allowed_sort_fields:
            raise ValueError(
                "Invalid sort field"
            )

        sort_column = allowed_sort_fields[
            sort_by
        ]

        if sort_order.lower() == "asc":
            query = query.order_by(
                sort_column.asc()
            )

        elif sort_order.lower() == "desc":
            query = query.order_by(
                sort_column.desc()
            )

        else:
            raise ValueError(
                "Invalid sort order"
            )

    offset = (page - 1) * page_size

    results = (
        query
        .offset(offset)
        .limit(page_size)
        .all()
    )

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "results": results,
    }


# =========================================================
# Retry / Reset / Status
# =========================================================

def retry_single_video_orm(
    db: Session,
    video_id: int,
):
    video = get_video_orm(
        db=db,
        video_id=video_id,
    )

    if video is None:
        return None

    if video.status != VideoStatus.failed.value:
        raise ValueError(
            "Only failed videos can be retried"
        )

    video.status = VideoStatus.processing.value

    db.commit()
    db.refresh(video)

    return video


def retry_all_failed_videos_orm(
    db: Session,
):
    failed_videos = (
        db.query(Video)
        .filter(
            Video.status
            == VideoStatus.failed.value
        )
        .all()
    )

    for video in failed_videos:
        video.status = VideoStatus.processing.value

    db.commit()

    return len(failed_videos)


def reset_all_failed_videos_orm(
    db: Session,
):
    failed_videos = (
        db.query(Video)
        .filter(
            Video.status
            == VideoStatus.failed.value
        )
        .all()
    )

    for video in failed_videos:
        video.status = VideoStatus.indexed.value

    db.commit()

    return len(failed_videos)


def change_video_status_orm(
    db: Session,
    video_id: int,
    new_status: VideoStatus,
    force: bool,
):
    video = get_video_orm(
        db=db,
        video_id=video_id,
    )

    if video is None:
        return None

    if (
        video.status == VideoStatus.indexed.value
        and new_status == VideoStatus.processing
        and force is False
    ):
        raise ValueError(
            "Changing indexed video back to processing "
            "requires force=true"
        )

    video.status = new_status.value

    db.commit()
    db.refresh(video)

    return video


# =========================================================
# File Upload
# =========================================================

async def handle_video_upload_orm(
    db: Session,
    file: UploadFile,
):
    if file.content_type not in ALLOWED_VIDEO_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported video type",
        )

    file_content = await file.read()

    if len(file_content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size exceeds 10 MB",
        )

    original_filename = (
        file.filename or "uploaded_video"
    )

    file_extension = Path(
        original_filename
    ).suffix

    stored_filename = (
        f"{uuid4()}{file_extension}"
    )

    file_path = (
        UPLOAD_DIRECTORY / stored_filename
    )

    file_path.write_bytes(file_content)

    video = Video(
        title=original_filename,
        description=(
            "Uploaded video waiting for processing"
        ),
        status=VideoStatus.processing.value,
    )

    db.add(video)
    db.commit()
    db.refresh(video)

    return video, file_path


def process_uploaded_video_orm(
    video_id: int,
    file_path: Path,
):
    db = SessionLocal()

    try:
        print(
            f"Processing started for video {video_id}"
        )

        # Simulates a long processing operation.
        time.sleep(5)

        video = get_video_orm(
            db=db,
            video_id=video_id,
        )

        if video is None:
            print(
                f"Video {video_id} was not found"
            )
            return

        video.status = VideoStatus.indexed.value

        db.commit()

        print(
            f"Processing finished for video "
            f"{video_id}. File: {file_path}"
        )

    finally:
        db.close()