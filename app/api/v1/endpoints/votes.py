from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import current_user_jwt_dep
from app.db.session import get_db
from app.models.comments import Comment
from app.models.enums import NotificationType
from app.models.post import Post
from app.models.votes import CommentVote, PostVote
from app.schemas.vote import CommentVoteResponse, PostVoteResponse, VoteCreate
from app.services.notifications import create_notification

router = APIRouter()


@router.post(
    "/posts/{post_id}/",
    response_model=PostVoteResponse,
    status_code=status.HTTP_201_CREATED,
)
async def post_vote_create(
    post_id: int,
    body: VoteCreate,
    current_user: current_user_jwt_dep,
    db: AsyncSession = Depends(get_db),
):
    post = await db.scalar(select(Post).where(Post.id == post_id))
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found."
        )

    existing = await db.scalar(
        select(PostVote).where(
            PostVote.post_id == post_id, PostVote.user_id == current_user.id
        )
    )

    if existing:
        if existing.value == body.value:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="You already voted this way.",
            )
        existing.value = body.value
        db.add(existing)
        await db.commit()
        await db.refresh(existing)
        return existing

    vote = PostVote(post_id=post_id, user_id=current_user.id, value=body.value)
    db.add(vote)
    await db.flush()

    if post.user_id:
        await create_notification(
            db,
            recipient_user_id=post.user_id,
            actor_user_id=current_user.id,
            type=NotificationType.POST_VOTED,
            payload={"post_id": post_id, "value": body.value},
        )

    await db.commit()
    await db.refresh(vote)
    return vote


@router.delete("/posts/{post_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def post_vote_delete(
    post_id: int,
    current_user: current_user_jwt_dep,
    db: AsyncSession = Depends(get_db),
):
    existing = await db.scalar(
        select(PostVote).where(
            PostVote.post_id == post_id, PostVote.user_id == current_user.id
        )
    )
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Vote not found."
        )

    await db.delete(existing)
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post(
    "/comments/{comment_id}/",
    response_model=CommentVoteResponse,
    status_code=status.HTTP_201_CREATED,
)
async def comment_vote_create(
    comment_id: int,
    body: VoteCreate,
    current_user: current_user_jwt_dep,
    db: AsyncSession = Depends(get_db),
):
    comment = await db.scalar(select(Comment).where(Comment.id == comment_id))
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found."
        )

    existing = await db.scalar(
        select(CommentVote).where(
            CommentVote.comment_id == comment_id,
            CommentVote.user_id == current_user.id,
        )
    )

    if existing:
        if existing.value == body.value:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="You already voted this way.",
            )
        existing.value = body.value
        db.add(existing)
        await db.commit()
        await db.refresh(existing)
        return existing

    vote = CommentVote(
        comment_id=comment_id, user_id=current_user.id, value=body.value
    )
    db.add(vote)
    await db.commit()
    await db.refresh(vote)
    return vote


@router.delete("/comments/{comment_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def comment_vote_delete(
    comment_id: int,
    current_user: current_user_jwt_dep,
    db: AsyncSession = Depends(get_db),
):
    existing = await db.scalar(
        select(CommentVote).where(
            CommentVote.comment_id == comment_id,
            CommentVote.user_id == current_user.id,
        )
    )
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Vote not found."
        )

    await db.delete(existing)
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
