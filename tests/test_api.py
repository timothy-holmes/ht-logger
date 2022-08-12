from tests.ex_data import consume_url

from sqlmodel import Session, select
from src.models import Temperature

def test_consume_endpoint(client, engine):
    with Session(engine) as session:
        db_entries_pre = len(session.exec(select(Temperature)).all())
        consume_response = client.get(consume_url)
        assert consume_response.status_code == 200
        assert consume_response.json()['message'] == 'Success'
        assert len(session.exec(select(Temperature)).all()) > db_entries_pre

# needs more intelligent/details test
def test_all_endpoints(client,f_app):
    for route in f_app.routes:
        path = route.path
        response = client.get(path)
        assert response.status_code == 200 or response.status_code == 422
