import requests
import pytest
import paramiko
import os
import urllib3


HOST='localhost'
SSHKEY = '~/.ssh/id_rsa'


def _before():
    urllib3.disable_warnings()
    # очищаем БД от всех данных и перезапускаем database-контейнер
    if HOST != 'localhost' and HOST != '127.0.0.1':
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(username='root', key_filename=SSHKEY, hostname=HOST)
        stderr = ssh.exec_command(
            f"docker exec services_mongo_1 bash -c 'echo -e \"use organizer\\ndb.dropDatabase()\" | mongo -uroot -proot'")[2]
        # если есть ошибки, выводим их
        for line in stderr.read().splitlines():
            print(line)
    else:
        os.system("docker exec services_mongo_1 bash -c 'echo -e \"use organizer\\ndb.dropDatabase()\" | mongo -uroot -proot'")
    print("Done!")


def request(method, endpoint, data):
    if method == 'POST':
        r = requests.post(url="https://" + HOST + endpoint, json=data, verify=False)
    elif method == 'GET':
        r = requests.get(url="https://" + HOST + endpoint, params=data, verify=False)
    elif method == 'DELETE':
        r = requests.delete(url="https://" + HOST + endpoint, json=data, verify=False)
    return r.json()


def get_shoplist_items(token):
    data = request('GET', '/shoplist', f"token={token}")
    return data


def register(username, password):
    content = request('POST', '/register', {"user": username, "password": password})
    return content['token']