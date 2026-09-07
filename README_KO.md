# 🚀 Freqtrade 한국어 종합 가이드 & 고도화 패키지

본 저장소는 글로벌 암호화폐 자동매매 봇인 **Freqtrade (최신 2026.9+ 엔진)**를 기반으로, 한국어 사용자 및 실전 트레이더를 위한 **커스텀 전략, 원클릭 유틸리티 도구, 거래소별 설정 템플릿, 검증 테스트 스위트**를 완비한 고도화 저장소입니다.

---

## 🌟 주요 특징 및 추가 구성품

| 분류 | 파일 / 도구 | 설명 |
| :--- | :--- | :--- |
| **최신 엔진** | `Freqtrade 2026.9-dev` | 최신 Open Interest(미결제약정) 캔들 지원, 백테스트 펀딩비 최적화, 호가창 캐싱 반영 |
| **커스텀 전략** | [`KoreanStarterStrategy.py`](user_data/strategies/KoreanStarterStrategy.py) | 입문자 및 모의거래용 안전 추세추종 전략 (EMA200 + ADX20 + RSI) |
| | [`MultiTimeframeAtrStrategy.py`](user_data/strategies/MultiTimeframeAtrStrategy.py) | 1h 매크로 추세 + 5m 모멘텀 + 동적 트레일링 손절/본전 보존 전략 |
| | [`OpenInterestTrendStrategy.py`](user_data/strategies/OpenInterestTrendStrategy.py) | **선물 전용**: 기관 자금 유입(OI 급증) 및 펀딩비 편향 분석 롱/숏 전략 |
| | [`VibeRsiStrategy.py`](user_data/strategies/VibeRsiStrategy.py) | 5m RSI 과매도 반등 + EMA 정배열 단타 전략 |
| **설정 템플릿** | [`config.dryrun.example.json`](user_data/config.dryrun.example.json) | 안전한 가상 모의투자(Dry-run) 및 FreqUI 기본 활성화 템플릿 |
| | [`config.binance-futures.example.json`](user_data/config.binance-futures.example.json) | 바이낸스 USDT 선물(격리 마진, 펀딩비, 레버리지) 설정 |
| | [`config.upbit.example.json`](user_data/config.upbit.example.json) | 업비트 KRW 현물 마켓(수수료 0.05%, 원화 스테이크) 설정 |
| | [`.env.example`](.env.example) | API 키 및 텔레그램 토큰 안전 보관용 환경변수 템플릿 |
| **자동화 도구** | [`download_market_data.py`](scripts/download_market_data.py) | 페어, 기간, 타임프레임, 미결제약정(OI) 데이터 원클릭 다운로더 |
| | [`validate_strategy.py`](scripts/validate_strategy.py) | 전략 문법, 필수 메서드, 룩어헤드 편향(미래 참조) 자동 정적 검사기 |
| | [`report_backtest.py`](scripts/report_backtest.py) | 백테스트 JSON 결과를 Markdown 및 터미널 KPI 리포트로 변환 |
| **검증 테스트** | [`test_custom_user_strategies.py`](tests/strategy/test_custom_user_strategies.py) | 커스텀 전략 4종 자동 규격 검증 단위 테스트 스위트 |

---

## ⚡ 빠른 시작 (Quick Start)

### 1. 환경 설정 파일 준비
```bash
# 기본 설정 복사
cp user_data/config.dryrun.example.json user_data/config.json

# 환경변수 파일 복사 (필요 시 수정)
cp .env.example .env
```

### 2. Docker Compose로 실행 (가장 권장)
Docker가 설치되어 있다면 명령어 한 줄로 Freqtrade와 FreqUI 웹 대시보드가 즉시 구동됩니다:

```bash
# 봇 백그라운드 실행
docker compose up -d

# 웹 UI 접속: 브라우저에서 http://localhost:8080 열기
# 기본 계정: freqtrader / ChangeMeStrongPassword123 (config.json에서 변경 가능)
```

---

## 🛠️ 유틸리티 스크립트 활용법

### 1) 과거 마켓 데이터 다운로드 (`download_market_data.py`)
백테스팅에 필요한 과거 캔들 데이터를 간편하게 수집합니다:

```bash
# 바이낸스 현물 60일치 데이터 다운로드 (5m, 15m, 1h, 1d)
python scripts/download_market_data.py --days 60

# 선물 마켓 데이터 + 미결제약정(Open Interest) 캔들 함께 다운로드
python scripts/download_market_data.py --trading-mode futures --include-oi --days 30

# Docker 컨테이너 환경에서 다운로드 실행 시
python scripts/download_market_data.py --docker --days 60
```

### 2) 전략 사전 유효성 검사기 (`validate_strategy.py`)
전략 코딩 후 백테스트나 실매매에 돌입하기 전, 문법 오류나 미래 참조(Lookahead Bias)가 없는지 검사합니다:

```bash
python scripts/validate_strategy.py "user_data/strategies/*.py"
```

### 3) 백테스트 실행 및 성과 리포트 출력 (`report_backtest.py`)
백테스트를 실행하고 그 결과를 깔끔한 Markdown 표로 요약합니다:

```bash
# 백테스트 실행 (로컬 또는 도커)
freqtrade backtesting --config user_data/config.json --strategy KoreanStarterStrategy --timerange 20260101-

# 최신 백테스트 결과를 터미널 및 Markdown 리포트로 저장
python scripts/report_backtest.py -o backtest_summary.md
```

---

## 📈 수록 전략 상세 안내

### 1. KoreanStarterStrategy
* **타임프레임**: 15m
* **대상 시장**: 현물(Spot) 및 모의투자(Dry-run)
* **로직**: EMA 200 장기 상승 추세 위에서 EMA 20/50 정배열 + ADX > 20(추세 강도) + RSI 골든크로스 발생 시 진입.
* **리스크 관리**: 3단계 최소 ROI + 트레일링 스탑(이익 2.5% 도달 시 활성화) + 8% 하드 스탑로스.

### 2. MultiTimeframeAtrStrategy
* **타임프레임**: 1h(상위 추세) + 5m(진입 타이밍)
* **대상 시장**: 단기 스윙 및 데이트레이딩
* **로직**: 1h 봉의 EMA 50 > 200 골든크로스 상태를 확인하고, 5m 봉에서 풀백(Pullback) 반등 시 진입.
* **리스크 관리**: 수익률 1.5% 도달 시 즉시 수수료 버퍼(+0.3%)를 포함한 본전(Break-even) 스탑로스로 전환, 3% 도달 시 최소 1.5% 수익 확보.

### 3. OpenInterestTrendStrategy
* **타임프레임**: 1h
* **대상 시장**: 선물(Futures, Long/Short 양방향)
* **특징**: Freqtrade 2026.9+ 최신 엔진의 `open_interest` 캔들 활용. 단순 가격 지표뿐만 아니라 기관 및 대규모 포지션 유입(OI 급증)을 확인하여 롱/숏 포지션 진입. 보수적 2~3x 레버리지 제한 적용.

### 4. VibeRsiStrategy
* **타임프레임**: 5m
* **대상 시장**: 현물 스캘핑 / 단타
* **로직**: 단기 상승 추세(EMA20 > EMA50) 속에서 RSI가 30 미만으로 일시적 과매도 상태에 빠졌을 때 매수하여, RSI 70 과매수 도달 시 빠른 차익 실현.

---

## 🧪 단위 테스트 실행
저장소에 내장된 단위 테스트를 통해 전략 인터페이스 규격을 언제든 검증할 수 있습니다:

```bash
python -m unittest tests/strategy/test_custom_user_strategies.py
```

---

## ⚠️ 안전 트레이딩 수칙
1. **반드시 모의투자(Dry-run)를 거치세요**: 새 전략은 최소 1~2주간 Dry-run으로 시장 환경별 동작을 확인해야 합니다.
2. **API 권한 최소화**: 실전 매매 전환 시 거래소 API Key 설정에서 `출금(Withdrawal)` 권한은 **절대 비활성화**하고 `거래(Trading)` 권한만 부여하세요.
3. **비밀번호 변경**: `config.json`의 FreqUI 웹서버 비밀번호 및 JWT 시크릿 키는 반드시 본인만의 강력한 값으로 변경하세요.
