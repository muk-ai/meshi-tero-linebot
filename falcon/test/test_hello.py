import json
import requests


def test_hello():
    url = 'http://localhost:3031/hello'
    print(url)
    response = requests.get(url)
    print(response.text)
    response_json = json.loads(response.text)
    assert response.status_code == 200
    assert response_json['messages'] == 'hello, world'
