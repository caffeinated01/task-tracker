# API Specification

## Schemas

### Data Models

#### `User`

```json
{
  "id": "integer",
  "username": "string"
}
```

#### `Board`

```json
{
  "id": "integer",
  "name": "string",
  "role": "string"
}
```

#### `Task`

```json
{
  "id": "integer",
  "title": "string",
  "status": "string",
  "content": "string",
  "importance": "string",
  "board_id": "integer",
  "created_by": "integer",
  "assigned_to": "integer | null"
}
```

#### `BoardUser`

```json
{
  "id": "integer",
  "username": "string",
  "role": "string"
}
```

### Response Models

#### `ResponseMessage`

```json
{
  "message": "string"
}
```

#### `LoginResponse`

```json
{
  "message": "string",
  "user": "User"
}
```

#### `RefreshResponse`

```json
{
  "access_token": "string"
}
```

---

## `/api/auth`

Authentication route group

### POST `/api/auth/signup`

- **request**
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
- **response**
  - **201** - Signup successful
    - `ResponseMessage`
  - **400** - Missing username or password
    - `ResponseMessage`
  - **409** - Username already exists
    - `ResponseMessage`

### POST `/api/auth/login`

- **request**
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
- **response**
  - **200** - OK
    - `LoginResponse`
    - **cookies**: `access_token`, `refresh_token`
  - **400** - Missing username or password
    - `ResponseMessage`
  - **401** - Incorrect username or password
    - `ResponseMessage`

### POST `/api/auth/refresh`

- **request**
  - **cookies**: `refresh_token`
- **response**
  - **200** - OK
    - `RefreshResponse`
    - **cookies**: `access_token`, `refresh_token`
  - **401** - Invalid refresh token
    - `ResponseMessage`

### GET `/api/auth/logout`

- **request**
  - **cookies**: `refresh_token`
- **response**
  - **200** - OK
    - `ResponseMessage`

---

## `/api/boards`

Board route group. **ALL** routes require a valid `access_token` cookie.

### GET `/api/boards/`

- **response**
  - **200** - OK
    - ```json
      {
        "boards": [Board],
        "user": {
          "username": "string",
          "user_id": "user_id"
        }
      }
      ```

### POST `/api/boards/`

- **request**
  ```json
  {
    "name": "string"
  }
  ```
- **response**
  - **201** - Board created
    ```json
    {
      "id": "integer",
      "name": "string"
    }
    ```
  - **400** - Missing name
    - `ResponseMessage`

### GET `/api/boards/<int:id>`

- **response**
  - **200** - OK
    - ```json
      {
        "board": Board,
        "user": {
          "username": "string",
          "user_id": "user_id"
        }
      }
      ```
  - **404** - Board not found
    - `ResponseMessage`

### PATCH `/api/boards/<int:id>`

- **request**
  ```json
  {
    "name": "string"
  }
  ```
- **response**
  - **200** - Board updated
    - `ResponseMessage`
  - **400** - Missing name
    - `ResponseMessage`
  - **403** - User is not the owner
    - `ResponseMessage`
  - **404** - Board not found
    - `ResponseMessage`

### DELETE `/api/boards/<int:id>`

- **response**
  - **200** - Board deleted
    - `ResponseMessage`
  - **403** - User is not the owner
    - `ResponseMessage`
  - **404** - Board not found
    - `ResponseMessage`

### GET `/api/boards/<int:id>/tasks`

- **response**
  - **200** - OK
    - `[Task]`

### POST `/api/boards/<int:id>/tasks`

- **request**
  ```json
  {
    "title": "string",
    "status": "string",
    "content": "string",
    "importance": "string",
    "assigned_to": "integer"
  }
  ```
- **response**
  - **201** - Task created
    - `Task`
  - **400** - Missing required fields
    - `ResponseMessage`
  - **403** - User does not have access to the board
    - `ResponseMessage`

### GET `/api/boards/<int:id>/users`

- **response**
  - **200** - OK
    - `[BoardUser]`
  - **403** - User does not have access to the board
    - `ResponseMessage`

### POST `/api/boards/<int:id>/users`

- **description**: Share a board with another user.
- **request**
  ```json
  {
    "username": "string"
  }
  ```
- **response**
  - **200** - Board shared
    - `ResponseMessage`
  - **400** - Missing username or trying to share with self
    - `ResponseMessage`
  - **403** - User is not the owner
    - `ResponseMessage`
  - **404** - Board or user not found
    - `ResponseMessage`
  - **409** - Board already shared with user
    - `ResponseMessage`

### DELETE `/api/boards/<int:id>/users/<int:user_id>`

- **description**: Revoke a user's access to a board.
- **response**
  - **200** - Access revoked
    - `ResponseMessage`
  - **400** - Trying to revoke own access
    - `ResponseMessage`
  - **403** - User is not the owner
    - `ResponseMessage`
  - **404** - Board, user, or user in board not found
    - `ResponseMessage`

---

## `/api/tasks`

Task route group. **ALL** routes require a valid `access_token` cookie.

### GET `/api/tasks/<int:id>`

- **response**
  - **200** - OK
    - `Task`

### PATCH `/api/tasks/<int:id>`

- **request**
  ```json
  {
    "title": "string",
    "status": "string",
    "content": "string",
    "importance": "string",
    "assigned_to": "integer"
  }
  ```
- **response**
  - **200** - Task updated successfully
    - `ResponseMessage`
  - **400** - User does not have access to the task
    - `ResponseMessage`

### DELETE `/api/tasks/<int:id>`

- **response**
  - **200** - Task deleted successfully
    - `ResponseMessage`
  - **400** - User does not have access to the task
    - `ResponseMessage`

---

# Frontend Specification

## Using API Routes That Require Authentication

Use `fetchWithAuth(url, options)` when doing so. Call it like `fetch()`.

**Usage:**

```javascript
const res = await fetchWithAuth(`/api/boards/${boardId}/tasks`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    title: title,
    status: updateStatus.board,
    content: desc,
    importance: 1,
  }),
});
```

## Displaying Notifications

Use `showNotification(message, isError)` when doing so.

**Usage:**

```javascript
showNotification("Board created successfully", false);
showNotification("Incorrect username or password", true);
```
