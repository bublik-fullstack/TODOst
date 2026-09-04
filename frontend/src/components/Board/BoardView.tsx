import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  DndContext,
  DragOverlay,
  closestCorners,
  KeyboardSensor,
  PointerSensor,
  useSensor,
  useSensors,
  DragStartEvent,
  DragEndEvent,
} from '@dnd-kit/core';
import { sortableKeyboardCoordinates } from '@dnd-kit/sortable';
import api from '../../api/axios';
import { Board, Column as ColumnType, Task } from '../../types';
import { Column } from './Column';
import { TaskCard } from './TaskCard';
import { TaskModal } from '../Task/TaskModal';
import { useAuth } from '../../hooks/useAuth';

export function BoardView() {
  const { boardId } = useParams<{ boardId: string }>();
  const navigate = useNavigate();
  const { logout } = useAuth();
  const [board, setBoard] = useState<Board | null>(null);
  const [columns, setColumns] = useState<ColumnType[]>([]);
  const [tasks, setTasks] = useState<Task[]>([]);
  const [activeTask, setActiveTask] = useState<Task | null>(null);
  const [selectedTask, setSelectedTask] = useState<Task | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const sensors = useSensors(
    useSensor(PointerSensor, { activationConstraint: { distance: 5 } }),
    useSensor(KeyboardSensor, { coordinateGetter: sortableKeyboardCoordinates })
  );

  useEffect(() => {
    if (!boardId) return;
    fetchBoardData();
  }, [boardId]);

  const fetchBoardData = async () => {
    try {
      const [boardRes, columnsRes, tasksRes] = await Promise.all([
        api.get(`/boards/${boardId}`),
        api.get(`/boards/${boardId}/columns`),
        api.get(`/boards/${boardId}/tasks`),
      ]);
      setBoard(boardRes.data);
      setColumns(columnsRes.data);
      setTasks(tasksRes.data.tasks);
    } catch (error) {
      console.error('Failed to fetch board data:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDragStart = (event: DragStartEvent) => {
    const { active } = event;
    const task = tasks.find((t) => t.id === active.id);
    if (task) setActiveTask(task);
  };

  const handleDragEnd = async (event: DragEndEvent) => {
    const { active, over } = event;
    setActiveTask(null);

    if (!over) return;

    const activeId = active.id as string;
    const overId = over.id as string;

    const activeTask = tasks.find((t) => t.id === activeId);
    if (!activeTask) return;

    let targetColumnId: string;
    let newOrder: number;

    const overTask = tasks.find((t) => t.id === overId);
    if (overTask) {
      targetColumnId = overTask.column_id;
      const columnTasks = tasks.filter((t) => t.column_id === targetColumnId && t.id !== activeId);
      newOrder = columnTasks.findIndex((t) => t.id === overId);
      if (newOrder === -1) newOrder = columnTasks.length;
    } else {
      targetColumnId = overId;
      const columnTasks = tasks.filter((t) => t.column_id === targetColumnId && t.id !== activeId);
      newOrder = columnTasks.length;
    }

    try {
      await api.patch(`/tasks/${activeId}/move`, {
        column_id: targetColumnId,
        order_position: newOrder,
      });
      await fetchBoardData();
    } catch (error) {
      console.error('Failed to move task:', error);
    }
  };

  const handleAddTask = async (columnId: string, title: string) => {
    try {
      await api.post(`/columns/${columnId}/tasks`, {
        title,
        column_id: columnId,
        priority: 'medium',
      });
      await fetchBoardData();
    } catch (error) {
      console.error('Failed to create task:', error);
    }
  };

  const handleDeleteColumn = async (columnId: string) => {
    if (!confirm('Delete this column and all its tasks?')) return;
    try {
      await api.delete(`/columns/${columnId}`);
      await fetchBoardData();
    } catch (error) {
      console.error('Failed to delete column:', error);
    }
  };

  const handleUpdateTask = async (taskId: string, data: Partial<Task>) => {
    try {
      await api.put(`/tasks/${taskId}`, data);
      await fetchBoardData();
      setSelectedTask(null);
    } catch (error) {
      console.error('Failed to update task:', error);
    }
  };

  const handleDeleteTask = async (taskId: string) => {
    try {
      await api.delete(`/tasks/${taskId}`);
      await fetchBoardData();
      setSelectedTask(null);
    } catch (error) {
      console.error('Failed to delete task:', error);
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-100">
        <div className="text-gray-500">Loading...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-blue-600">
      <header className="bg-blue-700 text-white px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <button onClick={() => navigate('/')} className="hover:bg-blue-600 px-3 py-1 rounded">
            Boards
          </button>
          <h1 className="text-xl font-bold">{board?.title || 'Board'}</h1>
        </div>
        <button onClick={logout} className="hover:bg-blue-600 px-3 py-1 rounded">
          Logout
        </button>
      </header>

      <div className="p-6 overflow-x-auto">
        <DndContext
          sensors={sensors}
          collisionDetection={closestCorners}
          onDragStart={handleDragStart}
          onDragEnd={handleDragEnd}
        >
          <div className="flex gap-4">
            {columns.map((column) => (
              <Column
                key={column.id}
                column={column}
                tasks={tasks.filter((t) => t.column_id === column.id)}
                onTaskClick={setSelectedTask}
                onAddTask={handleAddTask}
                onDeleteColumn={handleDeleteColumn}
              />
            ))}
          </div>

          <DragOverlay>
            {activeTask && <TaskCard task={activeTask} onClick={() => {}} />}
          </DragOverlay>
        </DndContext>
      </div>

      {selectedTask && (
        <TaskModal
          task={selectedTask}
          onClose={() => setSelectedTask(null)}
          onUpdate={handleUpdateTask}
          onDelete={handleDeleteTask}
        />
      )}
    </div>
  );
}
