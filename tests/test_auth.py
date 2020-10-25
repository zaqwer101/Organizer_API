from shared import *
import shared


@pytest.fixture(autouse=True)
def before():
    shared._before()

def test_auth_token_fail():
    content = request('GET', '/auth', 'token=123456789')
    assert content['error'] == 'invalid token'


def test_auth_token_success():
    token = register('test', 'testpassword')

    content = request('GET', '/auth', f'token={token}')
    assert 'user' in content
    assert content['user'] == 'test'


def test_auth_crypted_success():
    """ 
    с использованием поля password_encrypted 
    """
    register('test', 'testpassword')

    content = request('POST', '/auth', {"user": "test", "password_encrypted": "e16b2ab8d12314bf4efbd6203906ea6c"})
    assert 'token' in content

    token = content['token']
    auth = request('GET', '/auth', f'token={token}')
    assert 'user' in auth


def test_auth_password_success():
    """
    с использованием логина и пароля (поле password)
    """

    register('test', 'testpassword')

    content = request('POST', '/auth', {"user": "test", "password": "testpassword"})
    assert 'token' in content
