# FastAPI Users - Example
FastAPI 0Auth2 user access and security based implementation based on [FastAPI Users](https://fastapi-users.github.io/fastapi-users/10.2/)

## Dependencies
- fastapi
- fastapi-users[sqlalchemy]
- uvicorn[standard]
- aiosqlite

## Launch
```
pipenv run python main.py
```

## Swagger docs
Visit http://127.0.0.1:8000/docs

## Usage
Check [official docs](https://fastapi-users.github.io/fastapi-users/10.2/usage/flow/)

- Create User<br>
POST to http://127.0.0.1:8000/docs#/auth/register_register_auth_register_post<br>
Body:
```json
{
  "email": "user@email.com",
  "password": "user_password",
  "is_active": true,
  "is_superuser": false,
  "is_verified": false
}
```
- (Optional) Become superuser (First time)
```SQL
UPDATE <user_table> SET is_superuser = true WHERE email = <user_email>;
```
- Request Verify User<br>
POST to http://127.0.0.1:8000/auth/request-verify-token<br>
Body:
{
    "email": <user_email>
}

A temporary token will be logged on server, use this token in next step

- Verify user<br>
POST to http://127.0.0.1:8000/auth/verify<br>
Body:
```json
{
    "token": <token_from_previous_step>
}
```

- Login
POST to http://127.0.0.1:8000/auth/jwt/login<br>
Parameters:
  - username / username
  - password / password

Response:
```json
{
  "access_token": "<access_token>",
  "token_type": "bearer"
}
```

- (Optional) Login + Cookie for frontend request 
POST to http://localhost:8000/auth/cookie/login
Params:
- Body -> Form-data
  - username / username
  - password / password

Response is null, but JWT token is stored in 'fastapiuserauth' cookie on browser

- Request Backend
GET to http://127.0.0.1:8000/authenticated-route
Use Authentication -> Bearear and JWT token provided in http://127.0.0.1:8000/auth/jwt/login

- Request Frontend
GET to http://127.0.0.1:8000/authenticated-route
Use Authentication -> Bearear and JWT token provided in fastapiuserauth cookie
