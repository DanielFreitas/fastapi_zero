from http import HTTPStatus


def test_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá Mundo!'}


def test_ola_deve_retornar_html_com_ola_mundo(client):
    response = client.get('/ola')

    assert response.status_code == HTTPStatus.OK
    assert 'olá mundo' in response.text


def test_creat_user(client):
    user_data = {'username': 'alice', 'email': 'alice@example.com', 'password': 'secret'}

    response = client.post('/users/', json=user_data)

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {'id': 1, 'username': 'alice', 'email': 'alice@example.com'}


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [{'id': 1, 'username': 'alice', 'email': 'alice@example.com'}]}


def test_update_user(client):
    response = client.put(
        '/users/1',
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'bob',
        'email': 'bob@example.com',
        'id': 1,
    }


def test_delete_user(client):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_update_user_not_found(client):
    response = client.put(
        '/users/999',
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_delete_user_not_found(client):
    response = client.delete('/users/999')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_read_user(client):
    # First create a user
    user_data = {'username': 'testuser', 'email': 'test@example.com', 'password': 'secret'}
    client.post('/users/', json=user_data)

    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'id': 1, 'username': 'testuser', 'email': 'test@example.com'}


def test_read_user_not_found(client):
    response = client.get('/users/999')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}
