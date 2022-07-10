from collections import OrderedDict

from app.get_weather_info import get_current, get_historical_hourly, get_forecast_hourly


class MessageGenerator:
    head_up_msg_dict = {}

    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon
        self.current_result = get_current(lat, lon)
        self.twenty_four_history_results = {i: get_historical_hourly(lat, lon, i)
                                            for i in range(-6, (-24 - 1), -6)}
        self.forty_eight_forecast_results = [get_forecast_hourly(lat, lon, i)
                                             for i in range(6, (48 + 1), 6)]

    def generate_greeting_msg(self):
        weather_code = self.current_result.get('code')
        rain_in_1h = self.current_result.get('rain1h')
        temp = self.current_result.get('temp')
        if weather_code == 3:
            if rain_in_1h >= 100:
                return '폭설이 내리고 있어요.'
            return '눈이 포슬포슬 내립니다.'
        if weather_code == 2:
            if rain_in_1h >= 100:
                return '폭우가 내리고 있어요.'
            return '비가 오고 있습니다.'
        if weather_code == 1:
            return '날씨가 약간은 칙칙해요.'
        if weather_code == 0:
            if temp >= 30:
                return '따사로운 햇살을 맞으세요.'
        if temp <= 0:
            return '날이 참 춥네요.'
        return '날이 참 춥네요.'

    def generate_temperature_msg(self):
        return f'{self._generate_temperature_diff_msg()} {self._generate_temperature_max_min_msg()}'

    def _generate_temperature_diff_msg(self):
        current_temp = self.current_result.get('temp')
        twenty_four_before_temp = self.twenty_four_history_results[-24].get('temp')
        temp_change = current_temp - twenty_four_before_temp
        abs_temp_change = abs(temp_change)
        if temp_change < 0:
            if current_temp >= 15:
                return f'어제보다 {abs_temp_change}도 덜 덥습니다.'
            return f'어제보다 {abs_temp_change}도 더 춥습니다.'
        if temp_change > 0:
            if current_temp >= 15:
                return f'어제보다 {abs_temp_change}도 더 덥습니다.'
            return f'어제보다 {abs_temp_change}도 덜 춥습니다.'
        if current_temp >= 15:
            return '어제와 비슷하게 덥습니다.'
        return '어제와 비슷하게 춥습니다.'

    def _generate_temperature_max_min_msg(self):
        current_result_temp = self.current_result.get('temp')
        historic_result_temps = [i.get('temp') for i in self.twenty_four_history_results.values()]
        total_results = [current_result_temp] + historic_result_temps
        max_temp = max(total_results)
        min_temp = min(total_results)
        return f'최고기온은 {max_temp}도, 최저기온은 {min_temp}도 입니다.'

    def generate_heads_up_msg(self):
        def check_consecutive_weather_code(code_list, checking_code):
            if code_list[i] == checking_code and code_list[i] == code_list[i + 1]:
                return True
            return False

        head_up_msg_dict = OrderedDict(
            {'내일 폭설이 내릴 수도 있으니 외출 시 주의하세요.': None,
             '눈이 내릴 예정이니 외출 시 주의하세요.': None,
             '폭우가 내릴 예정이에요. 우산을 미리 챙겨두세요.': None,
             '며칠동안 비 소식이 있어요.': None,
             '날씨는 대체로 평온할 예정이에요.': True
             }
        )

        forty_eight_h_result_codes = [i.get('code') for i in
                                      self.forty_eight_forecast_results]
        twenty_four_h_codes = forty_eight_h_result_codes[:3]

        for i in range(len(twenty_four_h_codes) - 1):
            if check_consecutive_weather_code(twenty_four_h_codes, 3):
                head_up_msg_dict['내일 폭설이 내릴 수도 있으니 외출 시 주의하세요.'] = True
            if check_consecutive_weather_code(twenty_four_h_codes, 2):
                head_up_msg_dict['폭우가 내릴 예정이에요. 우산을 미리 챙겨두세요.'] = True

        for i in range(len(forty_eight_h_result_codes) - 1):
            if check_consecutive_weather_code(forty_eight_h_result_codes, 3):
                head_up_msg_dict['눈이 내릴 예정이니 외출 시 주의하세요.'] = True
            if check_consecutive_weather_code(forty_eight_h_result_codes, 2):
                head_up_msg_dict['며칠동안 비 소식이 있어요.'] = True

        for k, v in head_up_msg_dict.items():
            if v:
                return k


def generate_summary(lat, lon):
    msg = MessageGenerator(lat, lon)
    return {
        "summary": {
            "greeting": msg.generate_greeting_msg(),
            "temperature": msg.generate_temperature_msg(),
            "heads-up": msg.generate_heads_up_msg()
        }
    }
