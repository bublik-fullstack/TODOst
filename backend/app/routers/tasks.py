from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from app.database import get_db
from app.models.task import Task, PriorityEnum
from app.models.column import Column
from app.models.board import Board
from app.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate, TaskMove, TaskResponse, TaskListResponse
from app.services.task import move_task, get_next_order_position
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/api", tags=["tasks"])


async def get_task_with_ownership(
    db: AsyncSession, task_id: str, user_id: str
) -> Task | None:
    result = await db.execute(
        select(Task)
        .join(Column, Task.column_id == Column.id)
        .join(Board, Column.board_id == Board.id)
        .where(Task.id == task_id, Board.owner_id == user_id)
    )
    return result.scalar_one_or_none()


async def get_column_with_ownership(
    db: AsyncSession, column_id: str, user_id: str
) -> Column | None:
    result = await db.execute(
        select(Column)
        .join(Board, Column.board_id == Board.id)
        .where(Column.id == column_id, Board.owner_id == user_id)
    )
    return result.scalar_one_or_none()


@router.post("/columns/{column_id}/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    column_id: str,
    data: TaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    column = await get_column_with_ownership(db, column_id, current_user.id)
    if not column:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Column not found")

    next_order = await get_next_order_position(db, column_id)

    task = Task(
        title=data.title,
        description=data.description,
        column_id=column_id,
        order_position=next_order,
        priority=data.priority,
        deadline=data.deadline,
        author_id=current_user.id,
    )
    db.add(task)
    await db.flush()
    return task


@router.get("/boards/{board_id}/tasks", response_model=TaskListResponse)
async def list_board_tasks(
    board_id: str,
    search: str | None = Query(None),
    priority: PriorityEnum | None = Query(None),
    deadline_before: str | None = Query(None),
    deadline_after: str | None = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    board_result = await db.execute(
        select(Board).where(Board.id == board_id, Board.owner_id == current_user.id)
    )
    if not board_result.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Board not found")

    columns_subq = select(Column.id).where(Column.board_id == board_id).scalar_subquery()
    query = select(Task).where(Task.column_id.in_(columns_subq))

    if search:
        query = query.where(Task.title.ilike(f"%{search}%"))
    if priority:
        query = query.where(Task.priority == priority)
    if deadline_before:
        query = query.where(Task.deadline <= datetime.fromisoformat(deadline_before))
    if deadline_after:
        query = query.where(Task.deadline >= datetime.fromisoformat(deadline_after))

    total_result = await db.execute(
        select(func.count()).select_from(query.subquery())
    )
    total = total_result.scalar()

    query = query.order_by(Task.column_id, Task.order_position).offset(skip).limit(limit)

    result = await db.execute(query)
    tasks = result.scalars().all()
    return TaskListResponse(tasks=tasks, total=total)


@router.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = await get_task_with_ownership(db, task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@router.put("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: str,
    data: TaskUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = await get_task_with_ownership(db, task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    if data.title is not None:
        task.title = data.title
    if data.description is not None:
        task.description = data.description
    if data.priority is not None:
        task.priority = data.priority
    if data.deadline is not None:
        task.deadline = data.deadline

    await db.flush()
    return task


@router.patch("/tasks/{task_id}/move", response_model=TaskResponse)
async def move_task_endpoint(
    task_id: str,
    data: TaskMove,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = await move_task(db, task_id, data.column_id, data.order_position, current_user.id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = await get_task_with_ownership(db, task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    await db.delete(task)
    await db.flush()
