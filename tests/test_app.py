from http import HTTPStatus

from fastapi.testclient import TestClient

from fastzpi_zero.app import app


def test_root_deve_retornar_ola_mundo():
    """
    Esse teste tem 3 etapas (AAA)
    - A: Arrange - Arranjo
    - A: Act - Executa a coisa (o SUT)
    - A: Assert - Garanta que o A é A
    """

    # Arrange
    client = TestClient(app)
    # Act
    response = client.get('/')
    # Assert
    assert response.json() == {'message': 'Olá Mundo!'}
    assert response.status_code == HTTPStatus.OK


def test_read_html_deve_retornar_ola_mundo():

    client = TestClient(app)

    response = client.get('/htmlolamundo')

    assert response.status_code == HTTPStatus.OK

    assert 'text/html' in response.headers['content-type']

    assert '<html>' in response.text
    assert '</html>' in response.text
    assert '<h1> Olá Mundo </h1>' in response.text


def test_create_user():

    client = TestClient(app)

    response = client.post(
        '/users/',
        json={
            'username': 'alice',
            'email': 'alice@example',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'alice',
        'email': 'alice@examle',
        'id': 1,
    }
