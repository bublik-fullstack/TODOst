from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.column import Column
from app.models.board import Board
from app.models.user import User
from app.schemas.column import ColumnCreate, ColumnUpdate, ColumnResponse
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/api", tags=["columns"])


@router.get("/boards/{board_id}/columns", response_model=list[ColumnResponse])
async def list_columns(
    board_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    board_result = await db.execute(
        select(Board).where(Board.id == board_id, Board.owner_id == current_user.id)
    )
    if not board_result.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Board not found")

    result = await db.execute(
        select(Column)
        .where(Column.board_id == board_id)
        .order_by(Column.order_position)
    )
    return result.scalars().all()


@router.post("/boards/{board_id}/columns", response_model=ColumnResponse, status_code=status.HTTP_201_CREATED)
async def create_column(
    board_id: str,
    data: ColumnCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    board_result = await db.execute(
        select(Board).where(Board.id == board_id, Board.owner_id == current_user.id)
    )
    if not board_result.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Board not found")

    max_order_result = await db.execute(
        select(Column.order_position)
        .where(Column.board_id == board_id)
        .order_by(Column.order_position.desc())
        .limit(1)
    )
    max_order = max_order_result.scalar()
    next_order = (max_order + 1) if max_order is not None else 0

    column = Column(
        title=data.title,
        board_id=board_id,
        order_position=data.order_position if data.order_position is not None else next_order,
    )
    db.add(column)
    await db.flush()
    return column


@router.put("/columns/{column_id}", response_model=ColumnResponse)
async def update_column(
    column_id: str,
    data: ColumnUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Column)
        .join(Board, Column.board_id == Board.id)
        .where(Column.id == column_id, Board.owner_id == current_user.id)
    )
    column = result.scalar_one_or_none()
    if not column:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Column not found")

    if data.title is not None:
        column.title = data.title
    if data.order_position is not None:
        column.order_position = data.order_position

    await db.flush()
    return column


@router.delete("/columns/{column_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_column(
    column_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Column)
        .join(Board, Column.board_id == Board.id)
        .where(Column.id == column_id, Board.owner_id == current_user.id)
    )
    column = result.scalar_one_or_none()
    if not column:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Column not found")

    await db.delete(column)
    await db.flush()
