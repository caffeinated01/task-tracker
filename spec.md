# api routes

## `/api/auth`

authentication route group

### POST `/api/auth/signup`

- **request**
  - ```json
    {
        "username": string,
        "password": string
    }
    ```
- **response**
  - 201 - Signup successful

  ```json
  {
    "message": string
  }
  ```

  - 400 - Missing username or password

  ```json
  {
    "message": string
  }
  ```

  - 409 - Username already exists

  ```json
  {
    "message": string
  }
  ```

### POST `/api/auth/login`

- **request**
  - ```json
    {
        "username": string,
        "password": string
    }
    ```
- **response**
  - 200 - OK

    ```json
    {
        "message": string,
        "user": {
            "id": int,
            "username": string
        }
    }
    ```

    cookies
    - `access_token`
    - `refresh_token`

  - 400 - Missing username or password

  ```json
  {
    "message": string
  }
  ```

  - 401 - Incorrect username or password

  ```json
  {
    "message": string
  }
  ```

### POST `/api/refresh`

- **request**
  - cookies
    - `refresh_token`
- **response**
  - 200 - OK

    ```json
    {
        "access_token": string,
    }
    ```

    cookies
    - `access_token`
    - `refresh_token`

  - 401 - Invalid refresh token

    ```json
    {
        "message": string
    }
    ```

### GET `/api/logout`

- **request**
  - cookies
    - `refresh_token`

- **response**
  - 200 - OK
    ```json
    {
      "message": string,
    }
    ```
