from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.board import Board
from app.models.column import Column
from app.models.user import User
from app.schemas.board import BoardCreate, BoardUpdate, BoardResponse, BoardListResponse
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/api/boards", tags=["boards"])

DEFAULT_COLUMNS = ["To Do", "In Progress", "Done"]


@router.get("", response_model=BoardListResponse)
async def list_boards(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    total_result = await db.execute(
        select(func.count()).select_from(
            select(Board).where(Board.owner_id == current_user.id).subquery()
        )
    )
    total = total_result.scalar()

    result = await db.execute(
        select(Board)
        .where(Board.owner_id == current_user.id)
        .order_by(Board.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    boards = result.scalars().all()
    return BoardListResponse(boards=boards, total=total)


@router.post("", response_model=BoardResponse, status_code=status.HTTP_201_CREATED)
async def create_board(
    data: BoardCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    board = Board(title=data.title, description=data.description, owner_id=current_user.id)
    db.add(board)
    await db.flush()

    for i, col_title in enumerate(DEFAULT_COLUMNS):
        column = Column(title=col_title, board_id=board.id, order_position=i)
        db.add(column)

    await db.flush()
    return board


@router.get("/{board_id}", response_model=BoardResponse)
async def get_board(
    board_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Board).where(Board.id == board_id, Board.owner_id == current_user.id)
    )
    board = result.scalar_one_or_none()
    if not board:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Board not found")
    return board


@router.put("/{board_id}", response_model=BoardResponse)
async def update_board(
    board_id: str,
    data: BoardUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Board).where(Board.id == board_id, Board.owner_id == current_user.id)
    )
    board = result.scalar_one_or_none()
    if not board:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Board not found")

    if data.title is not None:
        board.title = data.title
    if data.description is not None:
        board.description = data.description

    await db.flush()
    return board


@router.delete("/{board_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_board(
    board_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Board).where(Board.id == board_id, Board.owner_id == current_user.id)
    )
    board = result.scalar_one_or_none()
    if not board:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Board not found")

    await db.delete(board)
    await db.flush()
