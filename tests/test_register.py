from shared import *
import shared


@pytest.fixture(autouse=True)
def before():
    shared._before()


def test_register_success():
    content = request('POST', '/register', {"user": "test", "password": "testpassword"})
    print(content)
    assert 'token' in content


def test_register_fail():
    content = request('POST', '/register', {"user": "test", "password": "testpassword"})
    assert 'token' in content

    content = request('POST', '/register', {"user": "test", "password": "testpassword"})
    assert 'error' in content
