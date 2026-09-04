from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.comment import Comment
from app.models.task import Task
from app.models.column import Column
from app.models.board import Board
from app.models.user import User
from app.schemas.comment import CommentCreate, CommentUpdate, CommentResponse
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/api/tasks/{task_id}/comments", tags=["comments"])


async def verify_task_ownership(
    db: AsyncSession, task_id: str, user_id: str
) -> Task | None:
    result = await db.execute(
        select(Task)
        .join(Column, Task.column_id == Column.id)
        .join(Board, Column.board_id == Board.id)
        .where(Task.id == task_id, Board.owner_id == user_id)
    )
    return result.scalar_one_or_none()


@router.get("", response_model=list[CommentResponse])
async def list_comments(
    task_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = await verify_task_ownership(db, task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    result = await db.execute(
        select(Comment)
        .where(Comment.task_id == task_id)
        .order_by(Comment.created_at)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


@router.post("", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
async def create_comment(
    task_id: str,
    data: CommentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = await verify_task_ownership(db, task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    comment = Comment(content=data.content, task_id=task_id, author_id=current_user.id)
    db.add(comment)
    await db.flush()
    return comment


@router.put("/{comment_id}", response_model=CommentResponse)
async def update_comment(
    task_id: str,
    comment_id: str,
    data: CommentUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = await verify_task_ownership(db, task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    result = await db.execute(
        select(Comment).where(Comment.id == comment_id, Comment.task_id == task_id)
    )
    comment = result.scalar_one_or_none()
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")

    if comment.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your comment")

    comment.content = data.content
    await db.flush()
    return comment


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    task_id: str,
    comment_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = await verify_task_ownership(db, task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    result = await db.execute(
        select(Comment).where(Comment.id == comment_id, Comment.task_id == task_id)
    )
    comment = result.scalar_one_or_none()
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")

    if comment.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your comment")

    await db.delete(comment)
    await db.flush()
