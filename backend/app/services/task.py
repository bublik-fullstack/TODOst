from sqlalchemy import select, update, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.task import Task
from app.models.column import Column
from app.models.board import Board


async def move_task(
    db: AsyncSession,
    task_id: str,
    new_column_id: str,
    new_order_position: int,
    user_id: str,
) -> Task | None:
    result = await db.execute(
        select(Task)
        .join(Column, Task.column_id == Column.id)
        .join(Board, Column.board_id == Board.id)
        .where(Task.id == task_id, Board.owner_id == user_id)
    )
    task = result.scalar_one_or_none()
    if not task:
        return None

    old_column_id = task.column_id
    old_order_position = task.order_position

    if old_column_id == new_column_id:
        if old_order_position < new_order_position:
            await db.execute(
                update(Task)
                .where(
                    Task.column_id == old_column_id,
                    Task.order_position > old_order_position,
                    Task.order_position <= new_order_position,
                    Task.id != task_id,
                )
                .values(order_position=Task.order_position - 1)
            )
        elif old_order_position > new_order_position:
            await db.execute(
                update(Task)
                .where(
                    Task.column_id == old_column_id,
                    Task.order_position >= new_order_position,
                    Task.order_position < old_order_position,
                    Task.id != task_id,
                )
                .values(order_position=Task.order_position + 1)
            )
    else:
        await db.execute(
            update(Task)
            .where(
                Task.column_id == old_column_id,
                Task.order_position > old_order_position,
            )
            .values(order_position=Task.order_position - 1)
        )
        await db.execute(
            update(Task)
            .where(
                Task.column_id == new_column_id,
                Task.order_position >= new_order_position,
            )
            .values(order_position=Task.order_position + 1)
        )

    task.column_id = new_column_id
    task.order_position = new_order_position
    await db.flush()
    return task


async def get_next_order_position(db: AsyncSession, column_id: str) -> int:
    result = await db.execute(
        select(func.coalesce(func.max(Task.order_position), -1) + 1).where(Task.column_id == column_id)
    )
    return result.scalar()
