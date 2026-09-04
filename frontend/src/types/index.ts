export interface User {
  id: string;
  email: string;
  username: string;
  created_at: string;
}

export interface Board {
  id: string;
  title: string;
  description: string | null;
  owner_id: string;
  created_at: string;
  updated_at: string;
}

export interface Column {
  id: string;
  title: string;
  board_id: string;
  order_position: number;
  created_at: string;
  updated_at: string;
}

export interface Task {
  id: string;
  title: string;
  description: string | null;
  column_id: string;
  order_position: number;
  priority: 'low' | 'medium' | 'high';
  deadline: string | null;
  author_id: string;
  created_at: string;
  updated_at: string;
}

export interface Comment {
  id: string;
  content: string;
  task_id: string;
  author_id: string;
  created_at: string;
  updated_at: string;
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
}
