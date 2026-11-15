from fastapi.testclient import TestClient
from main import app          # change to your app's module

client = TestClient(app)

def test_app_starts():
    # any cheap route; replace with a real one, e.g. /getStaticData
    response = client.get("/docs")
    assert response.status_code == 200