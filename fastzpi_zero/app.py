from http import HTTPStatus

from fastapi import FastAPI

from fastzpi_zero.schemas import Message

app = FastAPI()


@app.get(
    '/', status_code=HTTPStatus.OK, response_model=Message
)  # Definindo um endpoint com o endereço `/` acessível pelo método HTTP `GET`
def read_root():
    return {'message': 'Olá Mundo!'}
