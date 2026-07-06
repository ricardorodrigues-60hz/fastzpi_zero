from http import HTTPStatus

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

from fastzpi_zero.schemas import (
    Message,
    UserDB,
    UserList,
    UserPublic,
    UserSchema,
)

app = FastAPI(title='Minha API BALA')

database = []


@app.get(
    '/', status_code=HTTPStatus.OK, response_model=Message
)  # Definindo um endpoint com o endereço `/` acessível pelo método HTTP `GET`
def read_root():
    return {'message': 'Olá Mundo!'}


@app.get(
    '/htmlolamundo', status_code=HTTPStatus.OK, response_class=HTMLResponse
)
def read_html():
    return """
    <html>
        <head>
            <title>Olá Mundo teste</title>
        </head>
        <body>
            <h1> Olá Mundo </h1>
        </body>
    </html> """


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):
    user_with_id = UserDB(
        **user.model_dump(),
        # username=user.username,
        # email=user.email,
        # password=user.password,
        id=len(database) + 1,
        # Aqui precisamos criar um novo modelo que represent o banco
        # Precisamos de um identificador para esse registro
    )

    database.append(user_with_id)

    return user_with_id


@app.get('/users/', status_code=HTTPStatus.OK, response_model=UserList)
def read_users():
    return {'users': database}


@app.put(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic
)
def update_user(user_id: int, user: UserSchema):

    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Deu Ruim" Não Achei...'
        )

    user_with_id = UserDB(**user.model_dump(), id=user_id)
    database[user_id - 1] = user_with_id

    return user_with_id


@app.delete(
    '/users/{user_id}',
    status_code=HTTPException.OK,
    response_model=UserPublic
)
def delete_user(user_id: int):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Deu Ruim" Não Achei...'
        )
    return database.pop[user_id - 1]