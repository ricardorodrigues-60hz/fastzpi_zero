from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from fastzpi_zero.schemas import Message

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
