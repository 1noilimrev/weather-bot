# WeatherBot API

## 현재 날씨와 예보 정보를 종합하여, 날씨 요약 문구를 생성해주는 HTTP API 입니다.

## 실행 방법

### direnv를 사용하여 환경변수 설정
```
maybe use export?
```

### Docker를 사용하여 실행하기
```
docker build -t weather-bot .
docker run -p 80:80 weather-bot
```
위의 명령어에서는 80번 port를 사용합니다.

### Local에서 개발서버 실행하기
Python 3.10 이상의 버젼이 필요합니다.
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
 위의 명령어에서는 8000번 port를 사용합니다.

### WeatherBot API Documentation
아래 주소를 접속하시면 Swagger로 작성된 API 문서를 볼 수 있습니다.
`http://localhost:<PORT>/docs/`

### Assignment 문서
https://droomws.notion.site/Backend-Take-Home-Assignment-43246478612b4489a76258cff986ba7a
