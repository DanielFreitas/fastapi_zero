from http import HTTPStatus

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

from fast_zero.schemas import MessageSchema, UserDB, UserListSchema, UserPublicSchema, UserSchema

app = FastAPI()
database = []


@app.get('/', status_code=HTTPStatus.OK, response_model=MessageSchema)
def read_root():
    return {'message': 'Olá Mundo!'}


@app.get('/ola', status_code=HTTPStatus.OK, response_class=HTMLResponse)
def ola_html():
    html_content = """
    <!doctype html>
    <html>
        <head>
            <meta charset="utf-8">
            <title>Olá</title>
        </head>
        <body>
            <h1>olá mundo</h1>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublicSchema)
def create_user(user: UserSchema):
    user_with_id = UserDB(id=len(database) + 1, **user.model_dump())
    database.append(user_with_id)
    return user_with_id


@app.get('/users/', status_code=HTTPStatus.OK, response_model=UserListSchema)
def read_users():
    return {'users': database}


@app.get('/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublicSchema)
def read_user(user_id: int):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found')

    return database[user_id - 1]


@app.put('/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublicSchema)
def update_user(user_id: int, user: UserSchema):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found')

    user_with_id = UserDB(id=user_id, **user.model_dump())
    database[user_id - 1] = user_with_id
    return user_with_id


@app.delete('/users/{user_id}', response_model=MessageSchema)
def delete_user(user_id: int):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found')

    del database[user_id - 1]

    return {'message': 'User deleted'}
