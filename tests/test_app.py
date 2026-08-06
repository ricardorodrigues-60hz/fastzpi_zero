from http import HTTPStatus


def test_root_deve_retornar_ola_mundo(client):
    """
    Esse teste tem 3 etapas (AAA)
    - A: Arrange - Arranjo
    - A: Act - Executa a coisa (o SUT)
    - A: Assert - Garanta que o A é A
    """

    # Arrange
    # client = TestClient(app)
    # Act
    response = client.get('/')
    # Assert
    assert response.json() == {'message': 'Olá Mundo!'}
    assert response.status_code == HTTPStatus.OK


def test_read_html_deve_retornar_ola_mundo(client):

    response = client.get('/htmlolamundo')

    assert response.status_code == HTTPStatus.OK

    assert 'text/html' in response.headers['content-type']

    assert '<html>' in response.text
    assert '</html>' in response.text
    assert '<h1> Olá Mundo </h1>' in response.text
