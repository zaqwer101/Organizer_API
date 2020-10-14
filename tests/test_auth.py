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
    stderr = ssh.exec_command(f"docker exec services_mongo_1 bash -c 'echo -e \"use organizer\\ndb.dropDatabase()\" | mongo -uroot -proot'")[2]
    # если есть ошибки, выводим их
    for line in stderr.read().splitlines():
        print(line)
    time.sleep(2)

    print("Done!")

def test_auth_fail():
    content = request('GET', '/auth', 'token=123456789')
    assert content['error'] == 'invalid token'

def test_register_success():
    content = request('POST', '/register', { "user": "test", "password": "testpassword" })
    print(content)
    assert 'token' in content