DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS refresh_tokens;
DROP TABLE IF EXISTS tasks;
DROP TABLE IF EXISTS board_users;
DROP TABLE IF EXISTS boards;

CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id TEXT UNIQUE NOT NULL,
  username TEXT UNIQUE NOT NULL,
  hashed_password TEXT NOT NULL
);

CREATE TABLE refresh_tokens (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  token TEXT UNIQUE NOT NULL,
  expires_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  revoked_at TIMESTAMP,
  user_id TEXT NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE boards (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  board_id TEXT UNIQUE NOT NULL,
  name TEXT NOT NULL,
  owner_id TEXT NOT NULL,
  FOREIGN KEY (owner_id) REFERENCES users(user_id)
);

CREATE TABLE board_users (
  user_id TEXT NOT NULL,
  board_id TEXT NOT NULL,
  role INTEGER NOT NULL,

  PRIMARY KEY (user_id, board_id),
  FOREIGN KEY (user_id) REFERENCES users(user_id),
  FOREIGN KEY (board_id) REFERENCES boards(board_id)
);

CREATE TABLE tasks (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  task_id TEXT UNIQUE NOT NULL,
  title TEXT NOT NULL,
  status INTEGER NOT NULL,
  content TEXT,
  board_id TEXT NOT NULL,
  created_by TEXT NOT NULL,
  assigned_to TEXT,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

  FOREIGN KEY (created_by) REFERENCES users(user_id),
  FOREIGN KEY (assigned_to) REFERENCES users(user_id),
  FOREIGN KEY (board_id) REFERENCES boards(board_id)
);