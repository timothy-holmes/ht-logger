from tests.ex_data import consume_url

def test_status_endpoint(client):
    status_response = client.get('/status/1')
    assert status_response.status_code == 200
    assert status_response.text == '{\n    "message": "This message is evidence the app is running!",\n    "datetime": true\n}'

def test_consume_endpoint(client):
    consume_response = client.get(consume_url)
    assert consume_response.status_code == 200
    assert consume_response.json()['message'] == 'Success'
