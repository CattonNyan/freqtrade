# ![freqtrade](https://raw.githubusercontent.com/freqtrade/freqtrade/develop/docs/assets/freqtrade_poweredby.svg)

[![Freqtrade CI](https://github.com/freqtrade/freqtrade/actions/workflows/ci.yml/badge.svg?branch=develop)](https://github.com/freqtrade/freqtrade/actions/workflows/ci.yml)
[![DOI](https://joss.theoj.org/papers/10.21105/joss.04864/status.svg)](https://doi.org/10.21105/joss.04864)
[![codecov](https://codecov.io/gh/freqtrade/freqtrade/branch/develop/graph/badge.svg?token=AD5BG3ATKI)](https://codecov.io/gh/freqtrade/freqtrade)
[![Documentation](https://readthedocs.org/projects/freqtrade/badge/)](https://www.freqtrade.io)
[![Discord Server](https://img.shields.io/badge/Freqtrade_Discord-4E4E4E?logo=discord)](https://discord.gg/p7nuUNVfP7)

**Freqtrade**는 파이썬(Python)으로 개발된 무료 오픈소스 암호화폐 자동매매 봇입니다. 주요 글로벌 및 국내 거래소를 폭넓게 지원하며, 텔레그램(Telegram) 또는 웹 UI(FreqUI)를 통해 원격으로 손쉽게 제어할 수 있습니다. 백테스팅, 데이터 시각화, 자금 관리 기능뿐만 아니라 머신러닝(FreqAI)을 활용한 전략 최적화 도구를 기본 탑재하고 있습니다.

![freqtrade](https://raw.githubusercontent.com/freqtrade/freqtrade/develop/docs/assets/freqtrade-screenshot.png)

---

## ⚠️ 면책 조항 (Disclaimer)

* 본 소프트웨어는 **교육 및 연구 목적**으로만 제공됩니다.
* 손실을 감당할 수 없는 자금으로 투자하지 마십시오.
* **소프트웨어의 사용에 따른 모든 책임은 사용자 본인에게 있습니다.** 개발자 및 기여자는 거래 결과에 대해 어떠한 법적/재정적 책임도 지지 않습니다.
* 실제 자금을 투입하기 전에 **반드시 가상 매매(Dry-run) 모드로 충분히 테스트**하고, 봇의 동작 메커니즘과 위험성을 완벽히 이해한 후 운용하시기 바랍니다.
* 파이썬 및 프로그래밍 기초 지식을 갖추는 것을 강력히 권장하며, 소스 코드와 공식 문서를 꼼꼼히 읽어보시기 바랍니다.

---

## 🌟 주요 기능 (Features)

* [x] **Python 3.11+ 기반**: Windows, macOS, Linux 등 모든 주요 OS에서 원활하게 구동.
* [x] **데이터 영속성**: SQLite 데이터베이스를 통해 거래 내역과 주문 상태를 안정적으로 기록.
* [x] **가상 모의투자(Dry-run)**: 실제 자금 입금 없이 실시간 시장 데이터로 안전하게 전략 시뮬레이션.
* [x] **강력한 백테스팅(Backtesting)**: 과거 캔들 데이터 기반의 정밀한 전략 수익률 및 MDD 분석.
* [x] **머신러닝 기반 전략 최적화**: 하이퍼옵트(Hyperopt)를 통한 파라미터 튜닝 및 FreqAI 적응형 예측 모델 지원.
* [x] **Open Interest(미결제약정) 캔들 지원**: Freqtrade 2026.9+ 최신 엔진의 파생상품 자금 유입 데이터 분석 지원.
* [x] **화이트리스트 & 블랙리스트 필터**: 거래할 코인 페어를 정적/동적으로 유연하게 필터링.
* [x] **내장 웹 대시보드 (FreqUI)**: 브라우저에서 실시간 차트, 포지션 현황, 수익률을 한눈에 모니터링.
* [x] **텔레그램(Telegram) 원격 제어**: 스마트폰으로 즉시 진입/청산 알림 수신 및 명령 실행.
* [x] **원화(KRW) 및 법정화폐 손익 표기**: USD뿐만 아니라 KRW 등 원하는 통화로 손익 자동 환산 표시.

---

## 🏛️ 지원 거래소

각 거래소별 상세 설정과 주의사항은 [거래소별 공식 안내 문서](https://www.freqtrade.io/en/stable/exchanges/)를 참조하십시오.

### 현물 (Spot) 거래소
* [X] [바이낸스 (Binance)](https://www.binance.com/)
* [X] [업비트 (Upbit)](https://upbit.com/) - *템플릿 제공: `config.upbit.example.json`*
* [X] [바이비트 (Bybit)](https://bybit.com/)
* [X] [비트겟 (Bitget)](https://www.bitget.com/)
* [X] [OKX](https://okx.com/)
* [X] [크라켄 (Kraken)](https://kraken.com/)
* [X] [하이퍼리퀴드 (Hyperliquid DEX)](https://hyperliquid.xyz/)
* [X] [Gate.io](https://www.gate.com/)
* [ ] [CCXT 지원 거래소 다수](https://github.com/ccxt/ccxt/)

### 선물 (Futures) 거래소
* [X] [바이낸스 선물 (Binance Futures)](https://www.binance.com/) - *템플릿 제공: `config.binance-futures.example.json`*
* [X] [바이비트 선물 (Bybit Futures)](https://bybit.com/)
* [X] [비트겟 선물 (Bitget Futures)](https://www.bitget.com/)
* [X] [하이퍼리퀴드 (Hyperliquid DEX)](https://hyperliquid.xyz/)
* [X] [OKX 선물](https://okx.com/)

---

## ⚡ 빠른 시작 (Quick Start)

### 1. 환경 설정 파일 준비
```bash
# 기본 모의투자 설정 파일 복사
cp user_data/config.dryrun.example.json user_data/config.json

# 환경변수 파일 복사 (필요 시 API 키 입력)
cp .env.example .env
```

### 2. Docker Compose로 1분 만에 실행 (가장 권장)
```bash
# 컨테이너 및 FreqUI 웹서버 백그라운드 구동
docker compose up -d

# 웹 브라우저에서 FreqUI 대시보드 접속:
# 주소: http://localhost:8080
# 기본 계정: freqtrader / ChangeMeStrongPassword123 (config.json에서 변경 가능)
```

---

## 📦 본 저장소 특화 추가 구성품

본 저장소는 실전 및 백테스팅 편의를 높이기 위해 아래의 전략과 유틸리티 도구를 기본 탑재하고 있습니다:

### 1. 내장 커스텀 전략 4종 (`user_data/strategies/`)
* **[`KoreanStarterStrategy.py`](user_data/strategies/KoreanStarterStrategy.py)**: 입문자 및 모의거래용 안전 추세추종 전략 (15m, EMA200 + ADX20 + RSI).
* **[`MultiTimeframeAtrStrategy.py`](user_data/strategies/MultiTimeframeAtrStrategy.py)**: 1h 매크로 추세(EMA 50/200) + 5m 진입 타이밍 + 동적 본전/트레일링 익절 전략.
* **[`OpenInterestTrendStrategy.py`](user_data/strategies/OpenInterestTrendStrategy.py)**: **선물 전용** 롱/숏 전략 (Freqtrade 최신 `open_interest` 미결제약정 급증 및 펀딩비 편향 분석).
* **[`VibeRsiStrategy.py`](user_data/strategies/VibeRsiStrategy.py)**: 5m RSI 과매도 반등 + EMA 정배열 단타 전략.

### 2. 유틸리티 스크립트 (`scripts/`)
* **[`download_market_data.py`](scripts/download_market_data.py)**: 현물/선물 캔들 데이터 및 미결제약정(OI) 데이터를 원클릭으로 일괄 다운로드.
  ```bash
  # 60일치 데이터 일괄 다운로드
  python scripts/download_market_data.py --days 60
  # 선물 데이터 + 미결제약정(OI) 캔들 다운로드
  python scripts/download_market_data.py --trading-mode futures --include-oi --days 30
  ```
* **[`validate_strategy.py`](scripts/validate_strategy.py)**: 전략 코드의 문법 오류, 필수 메서드 누락, 룩어헤드 편향(미래 데이터 참조)을 정적 분석.
  ```bash
  python scripts/validate_strategy.py "user_data/strategies/*.py"
  ```
* **[`report_backtest.py`](scripts/report_backtest.py)**: 백테스트 JSON 결과 파일을 터미널 요약표 및 GitHub Markdown 보고서로 자동 변환.
  ```bash
  python scripts/report_backtest.py -o backtest_summary.md
  ```

### 3. 검증 단위 테스트 스위트
* 전략 규격과 안전성을 자동 검증하는 단위 테스트:
  ```bash
  python -m unittest tests/strategy/test_custom_user_strategies.py
  ```

---

## 💻 기본 명령어 안내

### 주요 CLI 명령어

```bash
# 봇 실시간 거래 (Dry-run 또는 Live)
freqtrade trade --config user_data/config.json --strategy KoreanStarterStrategy

# 과거 데이터 백테스팅
freqtrade backtesting --config user_data/config.json --strategy MultiTimeframeAtrStrategy --timerange 20260101-

# 하이퍼옵트(파라미터 최적화)
freqtrade hyperopt --config user_data/config.json --strategy KoreanStarterStrategy --hyperopt-loss SharpeHyperOptLoss --epochs 100

# 룩어헤드 편향(과적합) 분석
freqtrade lookahead-analysis --config user_data/config.json --strategy KoreanStarterStrategy
```

### 텔레그램(Telegram) 원격 명령어
* `/start`: 자동매매 시작
* `/stop`: 자동매매 일시정지
* `/stopentry`: 신규 진입 중단 (기존 포지션 청산만 유지)
* `/status`: 현재 오픈된 포지션 상태 조회
* `/profit`: 최근 N일간 누적 손익 리포트 조회
* `/balance`: 계좌 잔고 및 코인별 보유 현황 조회
* `/forceexit <trade_id>|all`: 지정 또는 전체 포지션 즉시 시장가 청산

---

## ⚙️ 시스템 요구 사양

### 하드웨어 권장 사양
* **최소 사양**: 2vCPU, RAM 2GB, 디스크 여유 공간 1GB 이상
* 클라우드 VPS(AWS, GCP, Oracle Cloud, Vultr 등) 환경 구동을 권장합니다.

### 소프트웨어 요구 사항
* [Python >= 3.11](http://docs.python-guide.org/en/latest/starting/installation/)
* [Docker](https://www.docker.com/products/docker) (가장 권장)
* [TA-Lib](https://ta-lib.github.io/ta-lib-python/)
* 정확한 시스템 시간 (거래소 API 통신 오류를 방지하기 위해 NTP 서버 동기화 필수)

---

## 🤝 기여 및 커뮤니티

* 공식 영문 문서: [https://www.freqtrade.io](https://www.freqtrade.io)
* 공식 디스코드: [Freqtrade Discord](https://discord.gg/p7nuUNVfP7)
* 버그 제보 및 기능 제안: [GitHub Issues](https://github.com/freqtrade/freqtrade/issues)
