/**
 * FreqUI 한국어 현지화 엔진 (Korean Localization Engine)
 * 한국 금융/암호화폐 시장 표준 경제 용어 및 환경 설정 전면 한글화
 */

(function () {
  const KOREAN_DICT = {
    // 네비게이션 & 주요 메뉴
    "Dashboard": "대시보드",
    "Trade": "실시간 매매",
    "Trades": "체결 내역",
    "Chart": "차트 분석",
    "Charts": "차트 분석",
    "Backtesting": "전략 백테스팅",
    "Backtest": "백테스트",
    "Hyperopt": "하이퍼옵트 (파라미터 최적화)",
    "Pairlist": "감시 종목 (페어 목록)",
    "Pairlists": "종목 필터",
    "Logs": "실시간 로그",
    "Log": "로그",
    "Settings": "환경 설정",
    "FreqUI Settings": "FreqUI 환경 설정",
    "Documentation": "공식 문서",

    // 봇 상태 및 제어
    "Dry-run": "가상 모의투자 (Dry-Run)",
    "Dry-Run": "가상 모의투자 (Dry-Run)",
    "dry_run": "가상 모의투자",
    "Live": "실전 매매",
    "live": "실전 매매",
    "Running": "실행 중",
    "RUNNING": "실행 중",
    "running": "실행 중",
    "Stopped": "일시 정지됨",
    "STOPPED": "일시 정지됨",
    "stopped": "일시 정지됨",
    "Reloading": "설정 새로고침 중",
    "Start": "봇 시작",
    "Stop": "봇 정지",
    "Pause": "일시 중지",
    "Resume": "재개",
    "Stop Buy": "신규 매수 중단",
    "Stop entry": "신규 진입 중단",
    "Stop Entry": "신규 진입 중단",
    "Force exit": "즉시 시장가 청산",
    "Force Exit": "즉시 시장가 청산",
    "Force exit all": "전체 포지션 비상 청산",
    "Force Exit All": "전체 포지션 비상 청산",
    "Force Sell": "즉시 시장가 매도",
    "Reload Config": "설정 다시 읽기",

    // 환경 설정 (Settings) 전면 한글화
    "UI settings": "사용자 인터페이스 (UI) 설정",
    "UI Version:": "UI 버전:",
    "Lock dynamic layouts": "동적 화면 레이아웃 잠금",
    "Lock dynamic layouts, so they cannot move anymore. Can also be set from the navbar at the top.": "대시보드 위젯이 움직이지 않도록 화면 배치를 고정합니다. (상단 네비게이션 바에서도 설정 가능)",
    "Reset layout": "화면 레이아웃 초기화",
    "Reset dynamic layouts to how they were.": "화면 배치를 기본 초기 상태로 되돌립니다.",
    "Show open trades in header": "상단 헤더에 보유 포지션 표시",
    "Decide if open trades should be visualized": "헤더 영역에 현재 진행 중인 거래를 시각화할 방식을 선택합니다.",
    "Show pill in icon": "아이콘에 뱃지로 표시",
    "Show in title": "제목 표시줄 텍스트로 표시",
    "Don't show open trades in header": "상단 헤더에 표시하지 않음",
    "UTC Timezone": "표시 시간대 (Timezone) 설정",
    "Select timezone (UTC is recommended as exchanges usually work in UTC)": "표시할 시간대를 선택하세요. (거래소 서버 기준인 UTC 권장, 또는 한국 표준시 KST)",
    "Background sync": "백그라운드 실시간 동기화",
    "Keep background sync running while other bots are selected.": "다른 봇이나 탭을 보고 있을 때도 백그라운드 데이터 동기화를 유지합니다.",
    "Show Confirm Dialog for Trade Exits": "포지션 청산 시 확인 팝업창 띄우기",
    "Use confirmation dialogs when force-exiting a trade.": "즉시 시장가 청산(Force Exit) 실행 시 실수 방지를 위해 확인창을 띄웁니다.",
    "This will also show": "이 옵션을 켜면 제목 표시줄에 ",
    "in the title bar.": " 아이콘이 표시됩니다.",
    "Show Text on Multi Pane Buttons": "분할 창 버튼에 글자 라벨 표시",
    "Show text on multi pane buttons. If disabled, only shows images.": "다중 분할 창 제어 버튼에 글자를 표시합니다. 끄면 아이콘만 표시됩니다.",

    // 차트 설정 (Chart Settings)
    "Chart settings": "차트 디스플레이 설정",
    "Chart scale Side": "차트 가격 눈금(Scale) 위치",
    "Should the scale be displayed on the right or left?": "가격 축 눈금을 차트의 오른쪽 또는 왼쪽에 표시할지 선택합니다.",
    "Left": "왼쪽 (Left)",
    "Right": "오른쪽 (Right, 기본)",
    "Use Heikin Ashi candles": "하이켄아시(Heikin Ashi) 캔들 사용",
    "Use Heikin Ashi candles in your charts": "차트에 일반 캔들 대신 추세 왜곡을 줄여주는 하이켄아시 캔들을 표시합니다.",
    "Only request necessary columns": "필요한 캔들 컬럼만 요청 (데이터 절약)",
    "Can reduce the transfer size for large dataframes. May require additional calls if the plot config changes.": "네트워크 데이터 전송량을 줄입니다. 차트 지표 변경 시 추가 조회가 발생할 수 있습니다.",
    "Default number of candles to display (defaults to 250)": "기본 캔들 표시 개수 (기본값: 250개)",
    "Candle Color Preference": "캔들 색상 테마 (양봉/음봉 기준)",
    "Green Up/Red Down": "초록 상승 (양봉) / 빨강 하락 (음봉) [글로벌 표준]",
    "Red Up/Green Down": "빨강 상승 (양봉) / 파랑 하락 (음봉) [한국 주식·코인 표준]",

    // 알림 설정 (Notification Settings)
    "Notification Settings": "거래 이벤트 알림 설정",
    "Entry notifications": "포지션 진입 (매수) 알림",
    "Exit notifications": "포지션 청산 (매도) 알림",
    "Entry Cancel notifications": "진입 주문 취소 알림",
    "Exit Cancel notifications": "청산 주문 취소 알림",

    // 백테스팅 설정 (Backtesting Settings)
    "Backtesting settings": "백테스팅 분석 환경 설정",
    "Backtesting metrics": "백테스트 성과 지표 선택",
    "Select which metrics should be shown on a per pair / tag basis.": "종목별 및 태그별 결과 테이블에 표시할 성과 지표(승률, 수익률, MDD 등)를 선택합니다.",

    // 거래 테이블 & 포지션
    "Open Trades": "보유 포지션 (미청산)",
    "Open trades": "보유 포지션 (미청산)",
    "Trade History": "거래 내역 (청산 완료)",
    "Trade history": "거래 내역 (청산 완료)",
    "Closed Trades": "청산 완료 내역",
    "Closed trades": "청산 완료 내역",
    "No open trades": "현재 보유 중인 포지션이 없습니다.",
    "No trades to show": "표시할 거래 내역이 없습니다.",
    "Pair": "종목 (페어)",
    "Pairs": "종목 목록",
    "Side": "포지션 방향",
    "side": "포지션 방향",
    "Long": "롱 (매수)",
    "long": "롱 (매수)",
    "Short": "숏 (공매도)",
    "short": "숏 (공매도)",
    "Open Date": "진입 일시",
    "Close Date": "청산 일시",
    "Open Rate": "진입가",
    "Entry Price": "진입가",
    "Current Rate": "현재가",
    "Close Rate": "청산가",
    "Exit Price": "청산가",
    "Amount": "보유 수량",
    "Stake Amount": "투자 금액 (매수액)",
    "Current Profit": "현재 수익률",
    "Current profit": "현재 수익률",
    "Close Profit": "실현 손익",
    "Profit": "수익(손익)",
    "profit": "수익(손익)",
    "Profit / Loss": "수익 / 손실",
    "Profit/Loss": "평가 손익",
    "Total Profit": "총 실현 손익",
    "Total profit": "총 실현 손익",
    "Unrealized Profit": "미실현 손익 (평가 손익)",
    "Realized Profit": "실현 손익",
    "Duration": "보유 시간",
    "Avg Duration": "평균 보유 시간",
    "Exit Reason": "청산 사유",
    "exit reason": "청산 사유",

    // 리스크 관리 & 주문
    "Stoploss": "손절매 (스탑로스)",
    "Stop loss": "손절매 (스탑로스)",
    "stoploss": "손절매",
    "Trailing Stop": "트레일링 스탑 (이익 보존 손절)",
    "Trailing stop": "트레일링 스탑 (이익 보존 손절)",
    "Take Profit": "목표 수익률 (익절)",
    "ROI": "최소 목표 수익률 (ROI)",
    "minimal_roi": "최소 목표 수익률",
    "Leverage": "레버리지 (배율)",
    "leverage": "레버리지",
    "Limit": "지정가",
    "Market": "시장가",
    "Order Type": "주문 유형",
    "Order type": "주문 유형",

    // 자산 & 통계 지표
    "Balance": "총 보유 자산",
    "balance": "보유 자산",
    "Total Balance": "총 자산",
    "Available Balance": "주문 가능 잔고",
    "Free": "주문 가능",
    "Used": "사용 중 (포지션)",
    "Total": "합계",
    "Starting Capital": "초기 투자 자본",
    "Win Rate": "승률",
    "Win rate": "승률",
    "Win / Loss": "승 / 패",
    "Wins": "승리",
    "Losses": "패배",
    "Draws": "무승부",
    "Profit Factor": "손익비 (Profit Factor)",
    "Max Drawdown": "최대 낙폭 (MDD)",
    "Max drawdown": "최대 낙폭 (MDD)",
    "Drawdown": "낙폭 (MDD)",
    "Sharpe Ratio": "샤프 지수 (위험 대비 수익비)",
    "Sortino Ratio": "소르티노 지수",
    "Calmar Ratio": "칼마 지수",
    "Daily Profit": "일간 손익",
    "Weekly Profit": "주간 손익",
    "Monthly Profit": "월간 손익",
    "Total Trades": "총 거래 횟수",
    "Total trades": "총 거래 횟수",

    // 전략 & 백테스트
    "Strategy": "매매 전략",
    "strategy": "매매 전략",
    "Timeframe": "봉 주기 (타임프레임)",
    "timeframe": "봉 주기",
    "Timerange": "분석 기간",
    "timerange": "분석 기간",
    "Download Data": "과거 시세 다운로드",
    "Download data": "과거 시세 다운로드",
    "Lookahead Analysis": "미래참조 (과적합) 분석",
    "Recursive Analysis": "재귀 수식 검증",
    "Run Backtest": "백테스트 실행",
    "Backtest Results": "백테스트 분석 결과",

    // 로그인 & 계정 & 모달
    "Login": "로그인",
    "Logout": "로그아웃",
    "Login to Bot": "트레이딩 봇 로그인",
    "Username": "사용자 아이디",
    "Password": "비밀번호",
    "API Server": "API 서버",
    "Bot Name": "봇 이름",
    "Version": "버전",
    "Connected": "정상 연결됨",
    "Disconnected": "연결 끊김",
    "Dark": "다크 모드",
    "Light": "라이트 모드",
    "System": "시스템 테마",
    "Save": "저장",
    "Cancel": "취소",
    "Confirm": "확인",
    "Close": "닫기",
    "Search": "검색…",
    "Search…": "검색…",
    "Whitelisted pairs": "감시 대상 종목 목록",
    "Blacklisted pairs": "제외 대상 종목 목록",
    "Exchange": "거래소"
  };

  // 문장 단위 부분 치환 규칙
  const SUBSTRING_RULES = [
    [/UI Version:\s*/g, "UI 버전: "],
    [/Strategy:\s*/g, "매매 전략: "],
    [/Exchange:\s*/g, "거래소: "],
    [/Timeframe:\s*/g, "봉 주기: "],
    [/Stake:\s*/g, "투자 통화: "],
    [/Trades:\s*/g, "거래 수: "],
    [/Profit:\s*/g, "실현 손익: "]
  ];

  // 폰트 및 한국어 가독성 CSS 주입
  const style = document.createElement("style");
  style.textContent = `
    body, html, input, button, select, textarea, div, span, p, a, table, th, td, h1, h2, h3, h4, h5, h6, label {
      font-family: 'Pretendard Variable', Pretendard, -apple-system, BlinkMacSystemFont, system-ui, Roboto, 'Helvetica Neue', 'Segoe UI', 'Apple SD Gothic Neo', 'Noto Sans KR', 'Malgun Gothic', sans-serif !important;
      word-break: keep-all;
    }
  `;
  document.head.appendChild(style);

  // 번역 함수
  function translateText(text) {
    if (!text || typeof text !== "string") return text;
    let res = text;
    const trimmed = text.trim();

    // 1. 사전 완전 일치 매칭
    if (KOREAN_DICT[trimmed]) {
      return text.replace(trimmed, KOREAN_DICT[trimmed]);
    }

    // 2. 문장 규칙 매칭
    for (const [pattern, replacement] of SUBSTRING_RULES) {
      if (pattern.test(res)) {
        res = res.replace(pattern, replacement);
      }
    }

    return res;
  }

  function walkAndTranslate(node) {
    if (!node) return;

    if (node.nodeType === Node.TEXT_NODE) {
      const val = node.nodeValue;
      if (val && val.trim().length > 0) {
        const translated = translateText(val);
        if (translated !== val) {
          node.nodeValue = translated;
        }
      }
    } else if (node.nodeType === Node.ELEMENT_NODE) {
      if (["SCRIPT", "STYLE", "NOSCRIPT"].includes(node.tagName)) {
        return;
      }

      if (node.placeholder) {
        node.placeholder = translateText(node.placeholder);
      }
      if (node.title) {
        node.title = translateText(node.title);
      }
      if (node.getAttribute("aria-label")) {
        node.setAttribute("aria-label", translateText(node.getAttribute("aria-label")));
      }

      for (let child = node.firstChild; child; child = child.nextSibling) {
        walkAndTranslate(child);
      }
    }
  }

  let timeoutId = null;
  const observer = new MutationObserver(() => {
    if (timeoutId) return;
    timeoutId = setTimeout(() => {
      walkAndTranslate(document.body);
      timeoutId = null;
    }, 30);
  });

  document.addEventListener("DOMContentLoaded", () => {
    walkAndTranslate(document.body);
    observer.observe(document.body, {
      childList: true,
      subtree: true,
      characterData: true,
    });
    console.log("🇰🇷 FreqUI 한국어 환경설정 및 경제/트레이딩 표준 용어팩 활성화 완료");
  });
})();
