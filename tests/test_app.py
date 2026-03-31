from http import HTTPStatus

from fastapi.testclient import TestClient

from fastapi_zero.app import app


def test_root_deve_retornar_ola_mundo(client):
    """
    Esse teste tem 3 etapas (AAA):
    - Arrange - Arranjo
    - Act - Executa a coisa
    - Assert - Garante que X é X
    """
    # Arrange é criar o client, que nesse caso já se cria automaticamente

    # Act
    response = client.get('/')

    # Assert
    assert response.json() == {'message': 'Olá mundo!'}
    assert response.status_code == HTTPStatus.OK


def test_create_user(client):
    client = TestClient(app)

    response = client.post(
        '/users/',
        json={
            'username': 'alice',
            'password': 'secret',
            'email': 'alice@example.com',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'email': 'alice@example.com',
        'username': 'alice',
    }


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'id': 1,
                'email': 'alice@example.com',
                'username': 'alice',
            }
        ]
    }


def test_read_user(client):
    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'email': 'alice@example.com',
        'username': 'alice',
    }


def test_read_user_not_found(client):
    response = client.get('users/100')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'user_id não encontrado!'}


def test_update_user(client):
    response = client.put(
        '/users/1',
        json={
            'username': 'Bob',
            'email': 'bob@example.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'Bob',
        'email': 'bob@example.com',
    }


def test_update_user_not_found(client):
    response = client.put(
        '/users/100',
        json={
            'username': 'Not Found',
            'email': 'not_found@example.com',
            'password': '404',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'user_id não encontrado!'}


def test_delete_user(client):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'Bob',
        'email': 'bob@example.com',
    }


def test_delete_user_not_found(client):
    response = client.delete('/users/100')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'user_id não encontrado!'}
