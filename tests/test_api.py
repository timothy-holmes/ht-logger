from tests.ex_data import consume_url

def test_status_endpoint(client):
    status_response = client.get('/status/')
    assert status_response.status_code == 200
    assert status_response.json()['status'] == 'OK'

def test_consume_endpoint(client):
    consume_response = client.get(consume_url)
    assert consume_response.status_code == 200
    assert consume_response.json()['message'] == 'Success'
