from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from fastzpi_zero.database import get_session
from fastzpi_zero.models import User
from fastzpi_zero.schemas import (
    Message,
    UserList,
    UserPublic,
    UserSchema,
)

app = FastAPI(title='Minha API BALA')


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


# @app.post(
#   '/users/',
#    status_code=HTTPStatus.CREATED,
#    response_model=UserPublic
# )
# def create_user(user: UserSchema):
#     user_with_id = UserDB(
#         **user.model_dump(),
#         # username=user.username,
#         # email=user.email,
#         # password=user.password,
#         id=len(database) + 1,
#         # Aqui precisamos criar um novo modelo que represent o banco
#         # Precisamos de um identificador para esse registro
#     )

#     database.append(user_with_id)

#     return user_with_id


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(
    user: UserSchema,
    session=Depends(get_session),
):

    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Username already exists',
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Email already exists',
            )

    db_user = User(
        username=user.username,
        email=user.email,
        password=user.password,
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get('/users/', status_code=HTTPStatus.OK, response_model=UserList)
def read_users(
    limit: int = 100, offset: int = 0, session: Session = Depends(get_session)
):
    users = session.scalars(select(User).offset(offset).limit(limit)).all()
    return {'users': users}


# @app.put(
#     '/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic
# )
# def update_user(user_id: int, user: UserSchema):

#     if user_id < 1 or user_id > len(database):
#         raise HTTPException(
#             status_code=HTTPStatus.NOT_FOUND, detail='Deu Ruim! Não Achei...'
#         )

#     user_with_id = UserDB(**user.model_dump(), id=user_id)
#     database[user_id - 1] = user_with_id

#     return user_with_id


# @app.delete(
#     '/users/{user_id}',
#     status_code=HTTPStatus.OK,  # , response_model=Message
# )
# def delete_user(user_id: int):
#     if user_id < 1 or user_id > len(database):
#         raise HTTPException(
#             status_code=HTTPStatus.NOT_FOUND, detail='Deu Ruim! Não Achei...'
#         )

#     del database[user_id - 1]
#     return {'message': 'User deleted'}


@app.put(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic
)
def update_user(
    user_id: int, user: UserSchema, session: Session = Depends(get_session)
):

    user_db = session.scalar(select(User).where(User.id == user_id))

    if not user_db:
        raise HTTPException(
            detail='User not found', status_code=HTTPStatus.NOT_FOUND
        )
    try:
        user_db.username = user.username
        user_db.email = user.email
        user_db.password = user.password
        session.commit()
        session.refresh(user_db)

        return user_db
    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Username or Email already exists',
        )


@app.delete(
    '/users/{user_id}',
    status_code=HTTPStatus.OK,  # , response_model=Message
)
def delete_user(user_id: int, session: Session = Depends(get_session)):

    user_db = session.scalar(select(User).where(User.id == user_id))

    if not user_db:
        raise HTTPException(
            detail='User not found',
            status_code=HTTPStatus.NOT_FOUND,
        )

    session.delete(user_db)
    session.commit()

    return {'message': 'User deleted'}


@app.get(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic
)
def read_user(user_id: int, session: Session = Depends(get_session)):

    user_db = session.scalar(select(User).where(User.id == user_id))

    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    return user_db
