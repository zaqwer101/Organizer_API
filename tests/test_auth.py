import requests
import pytest
import paramiko
import time

URL = 'palearis.cloud'
SSHKEY = '/home/zaqwer/.ssh/id_rsa'


def request(method, endpoint, data):
    if method == 'POST':
        r = requests.post(url="https://" + URL + "/" + endpoint, json=data)
    elif method == 'GET':
        r = requests.get(url="https://" + URL + "/" + endpoint, params=data)

    return r.json()


@pytest.fixture(autouse=True)
def before():
    # очищаем БД от всех данных и перезапускаем database-контейнер
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(username='root', key_filename=SSHKEY, hostname=URL)
    stderr = ssh.exec_command(
        f"docker exec services_mongo_1 bash -c 'echo -e \"use organizer\\ndb.dropDatabase()\" | mongo -uroot -proot'")[2]
    # если есть ошибки, выводим их
    for line in stderr.read().splitlines():
        print(line)
    print("Done!")


def register(username, password):
    content = request('POST', '/register', {"user": username, "password": password})
    return content['token']


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
