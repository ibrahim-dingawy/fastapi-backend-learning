from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    File,
    HTTPException,
    Query,
    UploadFile,
    status,
)

from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.video import (
    VideoCreate,
    VideoFilterResponse,
    VideoReplace,
    VideoResponse,
    VideoSearchResponse,
    VideoStatus,
    VideoStatusUpdate,
    VideoSummaryResponse,
    VideoUpdate,
)
from app.services.user_service import (
    get_current_user,
)
from app.services.video_service import (
    change_video_status_orm,
    create_video_orm,
    delete_video_orm,
    filter_videos_orm,
    get_all_videos_orm,
    get_limited_videos_by_status_orm,
    get_video_orm,
    get_video_summary_orm,
    get_videos_by_status_orm,
    handle_video_upload_orm,
    process_uploaded_video_orm,
    replace_video_orm,
    reset_all_failed_videos_orm,
    retry_all_failed_videos_orm,
    retry_single_video_orm,
    search_videos_orm,
    update_video_orm,
    user_can_access_video,
)

router = APIRouter(
    prefix="/videos",
    tags=["Videos"],
)


def raise_video_not_found():
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Video not found",
    )

from app.services.user_service import (
    get_current_user,
    require_admin,
)

# =========================================================
# Static routes
# Keep these before /{video_id}
# =========================================================

@router.get(
    "",
    response_model=list[VideoResponse],
)
def get_videos(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return get_all_videos_orm(db)


@router.get(
    "/filter",
    response_model=VideoFilterResponse,
)
def filter_videos(
    status_filter: VideoStatus | None = Query(
        default=None,
        alias="status",
    ),
    title: str | None = None,
    sort_by: str | None = None,
    sort_order: str = "asc",
    page: int = Query(
        default=1,
        ge=1,
    ),
    page_size: int = Query(
        default=10,
        ge=1,
        le=100,
    ),
    db: Session = Depends(get_db),
):
    try:
        return filter_videos_orm(
            db=db,
            status_filter=status_filter,
            title=title,
            sort_by=sort_by,
            sort_order=sort_order,
            page=page,
            page_size=page_size,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )


@router.get(
    "/search",
    response_model=VideoSearchResponse,
)
def search_by_word(
    word: str = Query(
        alias="q",
        min_length=1,
    ),
    db: Session = Depends(get_db),
):
    matched_videos = search_videos_orm(
        db=db,
        word=word,
    )

    return {
        "query": word,
        "total": len(matched_videos),
        "results": matched_videos,
    }


@router.get(
    "/summary",
    response_model=VideoSummaryResponse,
)
def get_videos_summary(
    db: Session = Depends(get_db),
):
    return get_video_summary_orm(db)


@router.get(
    "/status/{video_status}",
    response_model=list[VideoResponse],
)
def get_videos_by_status(
    video_status: VideoStatus,
    db: Session = Depends(get_db),
):
    return get_videos_by_status_orm(
        db=db,
        video_status=video_status,
    )


@router.get(
    "/status/{status_name}/limited",
    response_model=list[VideoResponse],
)
def get_limited_videos_by_status(
    status_name: VideoStatus,
    limit: int | None = Query(
        default=None,
        ge=1,
    ),
    db: Session = Depends(get_db),
):
    return get_limited_videos_by_status_orm(
        db=db,
        status_value=status_name,
        limit=limit,
    )


@router.post(
    "/upload",
    status_code=status.HTTP_202_ACCEPTED,
)
async def upload_video(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    new_video, file_path = (
        await handle_video_upload_orm(
            db=db,
            file=file,
        )
    )

    background_tasks.add_task(
        process_uploaded_video_orm,
        new_video.id,
        file_path,
    )

    return {
        "message": (
            "Video uploaded and processing started"
        ),
        "video": new_video,
    }


@router.patch("/retry-failed")
def retry_failed_videos(
    db: Session = Depends(get_db),
):
    updated_count = (
        retry_all_failed_videos_orm(db)
    )

    if updated_count == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No failed videos found",
        )

    return {
        "updated_videos": updated_count,
        "message": "Retry started successfully",
    }


@router.patch("/reset-failed")
def reset_failed_videos(
    db: Session = Depends(get_db),
):
    reset_count = (
        reset_all_failed_videos_orm(db)
    )

    if reset_count == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No failed videos found",
        )

    return {
        "reset_videos": reset_count,
        "message": "Failed videos reset successfully",
    }


# =========================================================
# Dynamic routes
# =========================================================

@router.get(
    "/{video_id}",
    response_model=VideoResponse,
)
def get_video(
    video_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    video = get_video_orm(
        db=db,
        video_id=video_id,
    )

    if video is None:
        raise_video_not_found()

    if not user_can_access_video(
        video=video,
        current_user=current_user,
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this video",
        )

    return video


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=VideoResponse,
)
def create_video(
    video: VideoCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return create_video_orm(
        db=db,
        title=video.title,
        description=video.description,
        status_value=video.status.value,
        user_id=current_user.id,
    )


@router.patch(
    "/{video_id}",
    response_model=VideoResponse,
)
def update_video(
    video_id: int,
    video_update: VideoUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    video = get_video_orm(
        db=db,
        video_id=video_id,
    )

    if video is None:
        raise_video_not_found()

    if not user_can_access_video(
        video=video,
        current_user=current_user,
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this video",
        )

    updated_video = update_video_orm(
        db=db,
        video_id=video_id,
        title=video_update.title,
        description=video_update.description,
        status_value=(
            video_update.status.value
            if video_update.status is not None
            else None
        ),
    )

    return updated_video


@router.put(
    "/{video_id}",
    response_model=VideoResponse,
)
def replace_video(
    video_id: int,
    video_data: VideoReplace,
    db: Session = Depends(get_db),
):
    replaced_video = replace_video_orm(
        db=db,
        video_id=video_id,
        title=video_data.title,
        description=video_data.description,
        status_value=video_data.status.value,
    )

    if replaced_video is None:
        raise_video_not_found()

    return replaced_video


@router.delete("/{video_id}")
def delete_video(
    video_id: int,
    db: Session = Depends(get_db),
    current_admin=Depends(require_admin),
):
    deleted_video = delete_video_orm(
        db=db,
        video_id=video_id,
    )

    if deleted_video is None:
        raise_video_not_found()

    return {
        "message": "Video deleted successfully",
        "deleted_video": deleted_video,
    }


@router.patch(
    "/{video_id}/retry",
    response_model=VideoResponse,
)
def retry_video(
    video_id: int,
    db: Session = Depends(get_db),
):
    try:
        video = retry_single_video_orm(
            db=db,
            video_id=video_id,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )

    if video is None:
        raise_video_not_found()

    return video


@router.patch(
    "/{video_id}/status",
    response_model=VideoResponse,
)
def change_video_status(
    video_id: int,
    status_data: VideoStatusUpdate,
    force: bool = False,
    db: Session = Depends(get_db),
):
    try:
        video = change_video_status_orm(
            db=db,
            video_id=video_id,
            new_status=status_data.status,
            force=force,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )

    if video is None:
        raise_video_not_found()

    return video