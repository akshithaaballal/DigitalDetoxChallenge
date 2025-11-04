import pytest
from backend.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_index_routes_registered(client):
    # confirm the API endpoints we expect are present in the url map
    urls = [r.rule for r in client.application.url_map.iter_rules()]
    assert any('/api/groups' in u for u in urls)
    assert any('/api/check-group-completion' in u for u in urls)
    assert any('/api/notify-group' in u for u in urls)
