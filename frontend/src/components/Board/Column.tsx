import React, { useState } from 'react';
import { useDroppable } from '@dnd-kit/core';
import { SortableContext, verticalListSortingStrategy } from '@dnd-kit/sortable';
import { Column as ColumnType, Task } from '../../types';
import { TaskCard } from './TaskCard';
import { Button } from '../UI/Button';
import { Input } from '../UI/Input';

interface ColumnProps {
  column: ColumnType;
  tasks: Task[];
  onTaskClick: (task: Task) => void;
  onAddTask: (columnId: string, title: string) => void;
  onDeleteColumn: (columnId: string) => void;
}

export function Column({ column, tasks, onTaskClick, onAddTask, onDeleteColumn }: ColumnProps) {
  const [isAdding, setIsAdding] = useState(false);
  const [newTaskTitle, setNewTaskTitle] = useState('');

  const { setNodeRef, isOver } = useDroppable({
    id: column.id,
    data: { type: 'column', column },
  });

  const handleAddTask = () => {
    if (newTaskTitle.trim()) {
      onAddTask(column.id, newTaskTitle.trim());
      setNewTaskTitle('');
      setIsAdding(false);
    }
  };

  return (
    <div
      ref={setNodeRef}
      className={`bg-gray-100 rounded-lg p-3 min-w-[300px] max-w-[300px] ${isOver ? 'ring-2 ring-blue-500' : ''}`}
    >
      <div className="flex items-center justify-between mb-3">
        <h3 className="font-semibold text-gray-700">{column.title}</h3>
        <div className="flex gap-2">
          <button
            onClick={() => setIsAdding(true)}
            className="text-gray-500 hover:text-gray-700 text-xl"
          >
            +
          </button>
          <button
            onClick={() => onDeleteColumn(column.id)}
            className="text-gray-500 hover:text-red-500 text-sm"
          >
            x
          </button>
        </div>
      </div>

      {isAdding && (
        <div className="mb-3">
          <Input
            value={newTaskTitle}
            onChange={(e) => setNewTaskTitle(e.target.value)}
            placeholder="Task title"
            onKeyDown={(e) => e.key === 'Enter' && handleAddTask()}
          />
          <div className="flex gap-2 mt-2">
            <Button size="sm" onClick={handleAddTask}>
              Add
            </Button>
            <Button size="sm" variant="secondary" onClick={() => setIsAdding(false)}>
              Cancel
            </Button>
          </div>
        </div>
      )}

      <SortableContext items={tasks.map((t) => t.id)} strategy={verticalListSortingStrategy}>
        <div className="space-y-2">
          {tasks.map((task) => (
            <TaskCard key={task.id} task={task} onClick={onTaskClick} />
          ))}
        </div>
      </SortableContext>
    </div>
  );
}
