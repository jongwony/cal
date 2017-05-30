# console-calendar
Console Calendar by using Google API

## Install
```
virtualenv --python=python3 _ccal
pip install -U google-api-python-client
```

## Google OAuth
[Google API 사용자 인증 정보](https://console.developers.google.com/)에서 `client_secret_<client_ID>.json`을 다운로드 합니다.

```
mv $Downloads/client_secret_<client_ID>.json client_secret.json
```

## Run
```
python console_api
```