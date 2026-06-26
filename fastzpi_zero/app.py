from fastapi import FastAPI

app = FastAPI()


@app.get(
    '/'
)  # Definindo um endpoint com o endereço `/` acessível pelo método HTTP `GET`
def read_root():
    return {'message': 'Olá Mundo!'}
