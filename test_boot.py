from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

response = client.get("/api/limits")
if response.status_code == 200:
    print("SUCCESS: /api/limits returned", response.json())
else:
    print("FAILED! Status code:", response.status_code)
