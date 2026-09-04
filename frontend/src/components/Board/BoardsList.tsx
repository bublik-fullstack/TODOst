import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '../../store/authStore';
import api from '../../api/axios';
import { Board } from '../../types';

export function BoardsList() {
  const [boards, setBoards] = useState<Board[]>([]);
  const [newTitle, setNewTitle] = useState('');
  const [showForm, setShowForm] = useState(false);
  const { logout } = useAuthStore();
  const navigate = useNavigate();

  useEffect(() => {
    fetchBoards();
  }, []);

  const fetchBoards = async () => {
    try {
      const response = await api.get('/boards');
      setBoards(response.data.boards);
    } catch (error) {
      console.error('Failed to fetch boards:', error);
    }
  };

  const handleCreate = async () => {
    if (!newTitle.trim()) return;
    try {
      await api.post('/boards', { title: newTitle.trim() });
      setNewTitle('');
      setShowForm(false);
      fetchBoards();
    } catch (error) {
      console.error('Failed to create board:', error);
    }
  };

  const handleDelete = async (boardId: string) => {
    if (!confirm('Delete this board?')) return;
    try {
      await api.delete(`/boards/${boardId}`);
      fetchBoards();
    } catch (error) {
      console.error('Failed to delete board:', error);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-white shadow px-6 py-4 flex items-center justify-between">
        <h1 className="text-xl font-bold text-gray-800">My Boards</h1>
        <div className="flex gap-4">
          <button
            onClick={() => setShowForm(true)}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
          >
            + New Board
          </button>
          <button onClick={logout} className="text-gray-600 hover:text-gray-800">
            Logout
          </button>
        </div>
      </header>

      <div className="p-6">
        {showForm && (
          <div className="mb-6 bg-white p-4 rounded-lg shadow inline-flex gap-2">
            <input
              type="text"
              value={newTitle}
              onChange={(e) => setNewTitle(e.target.value)}
              placeholder="Board title"
              className="px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              onKeyDown={(e) => e.key === 'Enter' && handleCreate()}
              autoFocus
            />
            <button
              onClick={handleCreate}
              className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
            >
              Create
            </button>
            <button
              onClick={() => setShowForm(false)}
              className="text-gray-600 hover:text-gray-800 px-4 py-2"
            >
              Cancel
            </button>
          </div>
        )}

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {boards.map((board) => (
            <div
              key={board.id}
              className="bg-white p-4 rounded-lg shadow hover:shadow-md transition-shadow cursor-pointer"
              onClick={() => navigate(`/boards/${board.id}`)}
            >
              <div className="flex justify-between items-start">
                <h3 className="font-semibold text-gray-800">{board.title}</h3>
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    handleDelete(board.id);
                  }}
                  className="text-gray-400 hover:text-red-500"
                >
                  x
                </button>
              </div>
              {board.description && (
                <p className="text-sm text-gray-500 mt-2">{board.description}</p>
              )}
              <p className="text-xs text-gray-400 mt-3">
                Created: {new Date(board.created_at).toLocaleDateString()}
              </p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
