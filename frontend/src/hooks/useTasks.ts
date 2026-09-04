import { useState, useEffect, useCallback } from 'react';
import api from '../api/axios';
import { Task, Column } from '../types';

export function useTasks(boardId: string | undefined) {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [columns, setColumns] = useState<Column[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  const fetchBoardData = useCallback(async () => {
    if (!boardId) return;
    try {
      const [tasksRes, columnsRes] = await Promise.all([
        api.get(`/boards/${boardId}/tasks`),
        api.get(`/boards/${boardId}`),
      ]);
      setTasks(tasksRes.data.tasks);
    } catch (error) {
      console.error('Failed to fetch board data:', error);
    } finally {
      setIsLoading(false);
    }
  }, [boardId]);

  useEffect(() => {
    fetchBoardData();
  }, [fetchBoardData]);

  const createTask = async (columnId: string, title: string, description?: string, priority?: string, deadline?: string) => {
    const response = await api.post(`/columns/${columnId}/tasks`, {
      title,
      description,
      column_id: columnId,
      priority: priority || 'medium',
      deadline,
    });
    setTasks((prev) => [...prev, response.data]);
    return response.data;
  };

  const updateTask = async (taskId: string, data: Partial<Task>) => {
    const response = await api.put(`/tasks/${taskId}`, data);
    setTasks((prev) => prev.map((t) => (t.id === taskId ? response.data : t)));
    return response.data;
  };

  const deleteTask = async (taskId: string) => {
    await api.delete(`/tasks/${taskId}`);
    setTasks((prev) => prev.filter((t) => t.id !== taskId));
  };

  const moveTask = async (taskId: string, newColumnId: string, newOrder: number) => {
    const response = await api.patch(`/tasks/${taskId}/move`, {
      column_id: newColumnId,
      order_position: newOrder,
    });
    setTasks((prev) => prev.map((t) => (t.id === taskId ? response.data : t)));
    return response.data;
  };

  return {
    tasks,
    columns,
    isLoading,
    createTask,
    updateTask,
    deleteTask,
    moveTask,
    refetch: fetchBoardData,
  };
}
