from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse, Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import current_user_jwt_dep
from app.db.session import get_db
from app.models.comments import Comment
from app.models.enums import CommentStatus
from app.models.post import Post
from app.models.users import User
from app.schemas.comment import CommentCreate, CommentResponse, CommentUpdate

router = APIRouter()


def _can_manage_comment(current_user: User, comment: Comment) -> bool:
    return current_user.is_superuser or current_user.id == comment.user_id


@router.get("/post/{post_id}/", response_model=list[CommentResponse])
async def comments_by_post(post_id: int, db: AsyncSession = Depends(get_db)):
    post = await db.scalar(select(Post).where(Post.id == post_id))
    if not post:
        return JSONResponse(
            {"error": "Post not found"}, status_code=status.HTTP_404_NOT_FOUND
        )

    result = await db.execute(
        select(Comment)
        .where(Comment.post_id == post_id, Comment.status == CommentStatus.VISIBLE)
        .order_by(Comment.created_at)
    )
    return result.scalars().all()


@router.get("/{comment_id}/", response_model=CommentResponse)
async def comment_detail(comment_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Comment).where(Comment.id == comment_id))
    comment = result.scalar_one_or_none()
    if not comment:
        return JSONResponse(
            {"error": "Comment not found"}, status_code=status.HTTP_404_NOT_FOUND
        )
    return comment


@router.post("/", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
async def comment_create(
    body: CommentCreate,
    current_user: current_user_jwt_dep,
    db: AsyncSession = Depends(get_db),
):
    post = await db.scalar(select(Post).where(Post.id == body.post_id))
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found."
        )

    if body.parent_id is not None:
        parent = await db.scalar(
            select(Comment).where(
                Comment.id == body.parent_id, Comment.post_id == body.post_id
            )
        )
        if not parent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Parent comment not found in this post.",
            )

    comment = Comment(
        user_id=current_user.id,
        post_id=body.post_id,
        parent_id=body.parent_id,
        text=body.text,
        status=CommentStatus.VISIBLE,
    )

    db.add(comment)
    await db.commit()
    await db.refresh(comment)
    return comment


@router.put("/{comment_id}/", response_model=CommentResponse)
async def comment_update(
    comment_id: int,
    body: CommentUpdate,
    current_user: current_user_jwt_dep,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Comment).where(Comment.id == comment_id))
    comment = result.scalar_one_or_none()
    if not comment:
        return JSONResponse(
            {"error": "Comment not found"}, status_code=status.HTTP_404_NOT_FOUND
        )

    if not _can_manage_comment(current_user, comment):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions.",
        )

    update_data = body.model_dump(exclude_unset=True)

    if "status" in update_data and not (
        current_user.is_staff or current_user.is_superuser
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only staff can change comment status.",
        )

    for field, value in update_data.items():
        setattr(comment, field, value)

    db.add(comment)
    await db.commit()
    await db.refresh(comment)
    return comment


@router.delete("/{comment_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def comment_delete(
    comment_id: int,
    current_user: current_user_jwt_dep,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Comment).where(Comment.id == comment_id))
    comment = result.scalar_one_or_none()
    if not comment:
        return JSONResponse(
            {"error": "Comment not found"}, status_code=status.HTTP_404_NOT_FOUND
        )

    if not _can_manage_comment(current_user, comment):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions.",
        )

    await db.delete(comment)
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
