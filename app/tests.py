from unittest import TestCase, mock

from fastapi.testclient import TestClient

from app.main import app


class WeatherBotTest(TestCase):
    def setUp(self):
        self.client = TestClient(app)

    @mock.patch('app.get_weather_info.get_current')
    @mock.patch('app.get_weather_info.get_forecast_hourly')
    @mock.patch('app.get_weather_info.get_historical_hourly')
    def test_summary(self, mock_historical, mock_forecast, mock_current):
        mock_current.return_value = {'timestamp': 1657464371, 'code': 1, 'temp': 34, 'rain1h': 0}
        mock_forecast.side_effect = [{'timestamp': 1657485974, 'code': 3, 'min_temp': -9, 'max_temp': 13, 'rain': 93},
                                     {'timestamp': 1657507575, 'code': 0, 'min_temp': 17, 'max_temp': 29, 'rain': 0}]
        mock_historical.side_effect = [{'timestamp': 1657442772, 'code': 1, 'temp': 16, 'rain1h': 0},
                                       {'timestamp': 1657421173, 'code': 2, 'temp': 21, 'rain1h': 33}]
        response = self.client.get("/summary/", params={"lat": 14.3, "lon": -175})
        result = response.json()
        summary = result.get('summary')
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(summary)
        self.assertIsNotNone(summary.get('greeting'))
        self.assertIsNotNone(summary.get('temperature'))
        self.assertIsNotNone(summary.get('heads-up'))
