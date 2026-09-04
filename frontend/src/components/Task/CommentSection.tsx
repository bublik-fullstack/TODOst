import React, { useState } from 'react';
import api from '../../api/axios';
import { Comment } from '../../types';
import { Button } from '../UI/Button';

interface CommentSectionProps {
  taskId: string;
  comments: Comment[];
  onUpdate: () => void;
}

export function CommentSection({ taskId, comments, onUpdate }: CommentSectionProps) {
  const [newComment, setNewComment] = useState('');

  const handleAddComment = async () => {
    if (!newComment.trim()) return;
    try {
      await api.post(`/tasks/${taskId}/comments`, { content: newComment.trim() });
      setNewComment('');
      onUpdate();
    } catch (error) {
      console.error('Failed to add comment:', error);
    }
  };

  const handleDeleteComment = async (commentId: string) => {
    try {
      await api.delete(`/tasks/${taskId}/comments/${commentId}`);
      onUpdate();
    } catch (error) {
      console.error('Failed to delete comment:', error);
    }
  };

  return (
    <div>
      <h3 className="font-semibold text-gray-700 mb-3">Comments</h3>

      <div className="space-y-3 mb-4">
        {comments.length === 0 ? (
          <p className="text-gray-500 text-sm">No comments yet.</p>
        ) : (
          comments.map((comment) => (
            <div key={comment.id} className="bg-gray-50 p-3 rounded-lg">
              <div className="flex justify-between items-start">
                <p className="text-gray-800">{comment.content}</p>
                <button
                  onClick={() => handleDeleteComment(comment.id)}
                  className="text-gray-400 hover:text-red-500 text-sm ml-2"
                >
                  x
                </button>
              </div>
              <p className="text-xs text-gray-400 mt-1">
                {new Date(comment.created_at).toLocaleString()}
              </p>
            </div>
          ))
        )}
      </div>

      <div className="flex gap-2">
        <input
          type="text"
          value={newComment}
          onChange={(e) => setNewComment(e.target.value)}
          placeholder="Add a comment..."
          className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          onKeyDown={(e) => e.key === 'Enter' && handleAddComment()}
        />
        <Button onClick={handleAddComment} disabled={!newComment.trim()}>
          Add
        </Button>
      </div>
    </div>
  );
}
