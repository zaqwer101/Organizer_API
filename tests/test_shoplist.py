from shared import *
import shared


@pytest.fixture(autouse=True)
def before():
    shared._before()


def test_add_success():
    """ добавление элемента в список. Успешные сценарии """
    token = register('test', 'testpassword')
    request('POST', '/shoplist', {"name": "item1", "token": token})
    data = request('GET', '/shoplist', f"token={token}")
    print(data)
    assert len(data) == 1
    assert data[0]['name'] == 'item1'
    assert data[0]['user'] == 'test'
    assert data[0]['bought'] == 'false'
    assert data[0]['amount'] == 1