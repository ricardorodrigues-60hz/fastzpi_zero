from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from fastzpi_zero.schemas import Message, UserDB, UserPublic, UserSchema

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
    user_with_id = UserDB(  # **user.model_dump()
        username=user.username,
        email=user.email,
        password=user.password,
        id=len(database) + 1
    )

    database.append(user_with_id)

    return user_with_id
