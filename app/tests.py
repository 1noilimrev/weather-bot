from fastapi.testclient import TestClient
from unittest import TestCase

from app.main import app


class WeatherBotTest(TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_summary(self):
        response = self.client.get("/summary/", params={"lat": 14.3, "lon": -175})
        self.assertEqual(response.status_code, 200)