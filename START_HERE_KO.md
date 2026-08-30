# Freqtrade 안전 시작 가이드

현재 구성은 Binance 현물, USDT, 15분봉, 모의투자(`dry_run`) 전용이다.
수익성을 보장하는 전략이 아니며 실거래 전에 백테스트와 장기간 모의투자가 필요하다.

## 1. 준비

Docker Desktop을 설치한 다음 이 폴더에서 실행한다.

```powershell
Copy-Item user_data/config.example.json user_data/config.json
docker compose pull
docker compose run --rm freqtrade list-pairs --config user_data/config.json
```

이 저장소에는 비밀값 없는 `config.example.json`만 커밋된다. 실제로 사용하는
`config.json`은 Git에서 제외된다.

거래소 또는 거래 페어가 맞지 않으면 먼저 `user_data/config.json`을 수정한다.

## 2. 데이터와 백테스트

```powershell
docker compose run --rm freqtrade download-data `
  --config user_data/config.json `
  --timeframes 15m `
  --days 180

docker compose run --rm freqtrade backtesting `
  --config user_data/config.json `
  --strategy KoreanStarterStrategy `
  --timerange 20260301-
```

백테스트에서는 총수익만 보지 말고 최대 낙폭, 거래 횟수, 손익비, 시장 구간별 결과를 확인한다.

## 3. 모의투자

```powershell
docker compose up -d
docker compose logs -f
```

거래 로그는 `user_data/logs/freqtrade.log`, 모의거래 DB는
`user_data/tradesv3.dryrun.sqlite`에 저장된다.

## 4. API 키 사용

API 키가 필요한 단계가 되면 `.env.example`을 `.env`로 복사해 값을 채운다.
API 키에는 조회와 현물거래 권한만 주고 출금 권한은 주지 않는다.

Compose에도 `FREQTRADE__DRY_RUN=true` 안전장치가 있으므로 `config.json`만
`false`로 바꿔서는 실거래가 켜지지 않는다. 실거래 전환은 다음을 모두 확인한
후 `.env`와 `config.json`의 두 값을 의도적으로 변경해 별도로 진행한다.

- 충분한 기간의 백테스트와 모의투자 완료
- 거래소 페어와 최소 주문금액 확인
- 최대 낙폭과 주문당 손실 한도 확인
- API IP 제한 및 출금 권한 비활성화
- `dry_run: false` 변경 전 설정 백업
