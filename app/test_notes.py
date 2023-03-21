from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

from app.db.Get_db_engine import engine
from app.db.Schemas import TaskStatus
from fastapi.testclient import TestClient
from app.main import app
from datetime import datetime

from app.db.Schemas import UserLoginSchema

from app.db.AuthJWT import path_to_token_endpoint
client = TestClient(app)


#settings
use_test_login = 'tester@x.com'
use_test_password = '123456'



url_map = {
    'users': {'root': '/api/v1/users',
              'endpoints': ['/list','/signup','/login','/token', f'/id/{1}']},
    'notes': {'root': '/api/v1/n',
             'endpoints': ['/create_note','/create_update/', f'/id/{1}', '/bank', '/inwork', '/done', '/quited']}
}
def urlchk(url_path, endpoint):
    assert url_path in url_map.keys()
    root = url_map[url_path]['root']
    assert root[0] == '/'
    assert root[-1] != '/'
    assert endpoint in url_map[url_path]['endpoints']
    assert endpoint[0] == '/'
    print("URL=", root+endpoint)
    return root + endpoint

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World!"}


def test_get_token_if_user_exist(url_path='users',
                                 endpoint='/login',
                                 test_login = use_test_login,
                                 test_password = use_test_password,
                                 ):
    print("Check if user exist")
    url = urlchk(url_path, endpoint)
    user_data = UserLoginSchema(**{"email": test_login, "password": test_password, "name": "Just tester"})
    json = {"email": test_login, "password": test_password, "name": "Just tester"}
    response = client.post(url, json=json)
    print("RESPONSE FROM test_get_token_if_user_exist: ", response)
    if response.status_code == 200:
        print('Test user exist')
        #assert response.text.startswith("Bearer")
        #assert len(response.text)>120
        #assert '\n' not in response.text
        print("OK Check if user exist OK")
        return response.text[1:-1]
    else:
        return None


def test_register(
    url_path='users',
    endpoint='/signup',
    test_login=use_test_login,
    test_password=use_test_password,
    ):
    print("Check "+endpoint)
    url=urlchk(url_path, endpoint)
    user_data =UserLoginSchema(**{"email": test_login, "password": test_password, "name":"Just tester"})
    response = client.post(url, json=user_data)
    assert response.status_code == 200
    assert response.text =='{"msg": "you have been registered! Welcome to login."}'

    url = urlchk(url_path, '/login')
    response = client.post(url, json=user_data)
    if response.status_code == 200:
        print('Test user exist')
    assert response.text.startswith("Bearer")
    assert len(response.text)>120
    assert '\n' not in response.text
    return response.text[1:-1]





def test_api_get_user_from_db(
        token,
        url_path='users',
        endpoint=f'/id/{1}',
):
    url = urlchk(url_path, endpoint)
    # no auth:
    response = client.get(url)
    print("THIIIIIS ISSSS RESSSPONSSSSE: ", response)
    assert response.status_code == 401
    data = response.json()
    data["title"] == True
    data["body"] == True

    #with auth:
    headers = {"authorization": token}
    response = client.get(url, headers=headers)
    assert response.status_code == 200
    data= response.json()
    data["title"] == True
    data["body"] == True


def test_api_get_by_status(
        token: str,
        url_path='notes',
):

    #no auth:
    for endpoint in ['/bank', '/inwork', '/done']: #, 'quited'
        url = urlchk(url_path, endpoint)
        response = client.get(url)
        assert response.status_code == 401
        data = response.json()
        assert data.get("detail") == "Not authenticated"

    print("NO-AUTH group endpoinds work fine")
    #with auth

    for endpoint in ['/bank', '/inwork', '/done']: #, 'quited'
        url = urlchk(url_path, endpoint)
        headers = {"authorization": token}
        response = client.get(url, headers=headers)
        print(response)
        print(response.text)
        assert response.status_code == 200
        data = response.json()
        assert type(data) == list
        assert type(data[0]) == dict
        data[0]["id"] == True
        data[0]['title'] == True
        data[0]['body'] == True

def test_api_create_task():
    data = {
        "title": f"testing_task_{datetime.now().strftime('%d.%m.%y %H:%M')}",
        "body": "testing_task_body"
    }


def test_api_create_update():
    pass

def test_get_test_user():
    token = test_get_token_if_user_exist()
    if not token:
        test_register()
        token = test_get_token_if_user_exist()
        if not token:
            assert 0==1==2
    return token


if __name__=="__main__":
    test_read_main()
    assert path_to_token_endpoint == url_map['users']['root']
    token = test_get_test_user()
    test_api_get_user_from_db(token)
    test_api_get_by_status(token)
    test_api_create_task()
    test_api_create_update()
