import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="GREEN HORIZON",
    page_icon="🌧️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .block-container {
            padding: 0rem !important;
            max-width: 100% !important;
        }
        iframe {
            border: none;
            display: block;
        }
    </style>
""", unsafe_allow_html=True)

game_html = """
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>GREEN HORIZON</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Cinzel:wght@600;800&family=Gowun+Batang:wght@400;700&family=Noto+Sans+KR:wght@300;400;600;700&display=swap');

  :root {
    --ink: #0a0d24;
    --navy: #111a44;
    --navy-2: #1c2866;
    --edge: #e9efff;
    --gold: #f2c14e;
    --gold-dk: #a45f1c;
    --cream: #f6efd8;
    --teal: #6ad0c8;
    --rose: #e0505a;
  }

  * {
    box-sizing: border-box;
    user-select: none;
    margin: 0;
    padding: 0;
  }

  body, html {
    width: 100%;
    height: 100%;
    overflow: hidden;
    background-color: #070a1c;
    font-family: 'Noto Sans KR', sans-serif;
    color: #f0ece1;
  }

  #game-container {
    position: relative;
    width: 100vw;
    height: 100vh;
    overflow: hidden;
    background: #0b0f2a;
  }

  canvas {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: block;
    image-rendering: pixelated;
    image-rendering: crisp-edges;
  }

  /* 픽셀 테두리 (투더문 대화창 느낌의 각진 이중 테두리) */
  .hollow-panel,
  #dialogue-box,
  #hud-clock,
  #hud-weather {
    border: none;
    border-radius: 0;
    box-shadow:
      -4px 0 0 0 var(--edge), 4px 0 0 0 var(--edge), 0 -4px 0 0 var(--edge), 0 4px 0 0 var(--edge),
      -8px 0 0 0 var(--ink), 8px 0 0 0 var(--ink), 0 -8px 0 0 var(--ink), 0 8px 0 0 var(--ink),
      0 14px 0 0 rgba(0, 0, 0, 0.35);
  }

  .hollow-panel {
    background: linear-gradient(180deg, #16215a 0%, #0f1744 100%);
    padding: 24px;
    position: relative;
  }

  .hollow-panel::before {
    content: "★";
    position: absolute;
    top: -14px;
    left: 50%;
    transform: translateX(-50%);
    background: #14205a;
    padding: 0 10px;
    color: var(--gold);
    font-size: 14px;
  }

  /* 타이틀 화면 */
  #title-overlay {
    position: absolute;
    inset: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    z-index: 20;
    transition: opacity 1.2s ease, transform 2.2s cubic-bezier(0.25, 0.8, 0.25, 1);
  }

  /* 타이틀 글자 뒤를 살짝 어둡게 해서 건물 창문과 겹쳐도 읽히도록 */
  #title-overlay::before {
    content: '';
    position: absolute;
    inset: 0;
    z-index: -1;
    background: radial-gradient(ellipse 42% 30% at 50% 50%, rgba(6, 8, 28, 0.78) 0%, rgba(6, 8, 28, 0.45) 55%, rgba(6, 8, 28, 0) 100%);
    pointer-events: none;
  }

  #title-overlay.zooming {
    transform: scale(4.5) translate(5%, -5%);
    opacity: 0;
    pointer-events: none;
  }

  .title-logo {
    font-family: 'Press Start 2P', 'Cinzel', monospace;
    font-size: clamp(1.7rem, 5.2vw, 3.6rem);
    font-weight: 400;
    letter-spacing: 0.06em;
    color: #ffe9a8;
    text-shadow: 4px 4px 0 #b4533a, 8px 8px 0 #0a0d24;
    margin-bottom: 26px;
  }

  .title-sub {
    font-family: 'Noto Sans KR', sans-serif;
    font-weight: 600;
    font-size: 1.1rem;
    letter-spacing: 0.22em;
    color: #d6e4ff;
    margin-bottom: 45px;
    text-shadow: 2px 2px 0 #0a0d24;
  }

  .start-btn {
    font-family: 'Press Start 2P', 'Cinzel', monospace;
    font-size: 1.05rem;
    letter-spacing: 0.15em;
    padding: 16px 44px;
    background: var(--gold);
    color: #1a1030;
    border: none;
    border-radius: 0;
    cursor: pointer;
    transition: transform 0.08s steps(2), box-shadow 0.08s steps(2);
    box-shadow:
      -4px 0 0 0 var(--ink), 4px 0 0 0 var(--ink), 0 -4px 0 0 var(--ink), 0 4px 0 0 var(--ink),
      0 10px 0 0 var(--gold-dk), 0 10px 0 4px var(--ink);
  }

  .start-btn:hover {
    background: #ffd978;
    transform: translateY(-2px);
  }

  .start-btn:active {
    transform: translateY(6px);
    box-shadow:
      -4px 0 0 0 var(--ink), 4px 0 0 0 var(--ink), 0 -4px 0 0 var(--ink), 0 4px 0 0 var(--ink),
      0 4px 0 0 var(--gold-dk), 0 4px 0 4px var(--ink);
  }

  /* 우측 상단 시계 HUD */
  #hud-clock {
    position: absolute;
    top: 24px;
    right: 28px;
    z-index: 15;
    background: linear-gradient(180deg, #1a2766 0%, #101847 100%);
    padding: 10px 18px;
    display: none;
    align-items: center;
    gap: 12px;
  }

  .clock-day {
    font-family: 'Noto Sans KR', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: #ffe08a;
  }

  .clock-time {
    font-family: 'Noto Sans KR', sans-serif;
    font-size: 1.05rem;
    font-weight: 700;
    color: #ffffff;
    background: rgba(0, 0, 0, 0.35);
    padding: 4px 10px;
    border-radius: 0;
    letter-spacing: 0.04em;
  }

  .speed-btn {
    background: #26357f;
    border: none;
    color: #cfdcff;
    font-size: 0.78rem;
    padding: 5px 9px;
    border-radius: 0;
    cursor: pointer;
    box-shadow: 0 0 0 2px var(--ink), 0 4px 0 2px var(--ink);
    margin-right: 3px;
  }

  .speed-btn.active {
    background: var(--gold);
    color: #1a1030;
    font-weight: 700;
  }

  /* 좌측 상단 기상 및 실시간 알림 배지 */
  #hud-weather {
    position: absolute;
    top: 24px;
    left: 28px;
    z-index: 15;
    background: linear-gradient(180deg, #16215a 0%, #0f1744 100%);
    padding: 10px 18px;
    display: none;
    font-size: 0.9rem;
    line-height: 1.55;
  }

  /* 긴급 현장 작업 알림 배너 */
  #alert-strip {
    position: absolute;
    top: 120px;
    left: 28px;
    z-index: 15;
    display: none;
    flex-direction: column;
    gap: 12px;
  }

  .alert-pill {
    background: #b3262e;
    border: none;
    border-radius: 0;
    color: #fff;
    padding: 7px 14px;
    font-size: 0.85rem;
    font-weight: 700;
    cursor: pointer;
    animation: pulse 1.3s steps(2) infinite;
    box-shadow:
      -3px 0 0 0 #ffccd5, 3px 0 0 0 #ffccd5, 0 -3px 0 0 #ffccd5, 0 3px 0 0 #ffccd5,
      -6px 0 0 0 var(--ink), 6px 0 0 0 var(--ink), 0 -6px 0 0 var(--ink), 0 6px 0 0 var(--ink);
  }

  @keyframes pulse {
    0%, 100% { transform: translateY(0); filter: brightness(0.92); }
    50% { transform: translateY(-2px); filter: brightness(1.15); }
  }

  /* 하단 대화창 (투더문 스타일) */
  #dialogue-box {
    position: absolute;
    bottom: 30px;
    left: 50%;
    transform: translateX(-50%);
    width: min(820px, 88vw);
    z-index: 25;
    background: linear-gradient(180deg, #17235f 0%, #0d1540 100%);
    padding: 18px 26px;
    display: none;
    cursor: pointer;
  }

  .speaker-tag {
    display: inline-block;
    background: var(--gold);
    color: #1a1030;
    font-weight: 700;
    font-size: 0.88rem;
    padding: 3px 14px;
    border-radius: 0;
    margin-bottom: 10px;
    box-shadow: 0 0 0 2px var(--ink), 0 4px 0 2px var(--ink);
  }

  .dialogue-text {
    font-family: 'Noto Sans KR', sans-serif;
    font-size: 1.05rem;
    font-weight: 400;
    line-height: 1.7;
    letter-spacing: 0.01em;
    color: #f4f1e6;
  }

  .dialogue-next {
    text-align: right;
    font-size: 0.8rem;
    color: var(--gold);
    margin-top: 6px;
    animation: blink 1s steps(2) infinite;
  }

  @keyframes blink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.25; }
  }

  /* 모달 오버레이 */
  #modal-backdrop {
    position: absolute;
    inset: 0;
    background: rgba(4, 6, 20, 0.78);
    z-index: 30;
    display: none;
    align-items: center;
    justify-content: center;
  }

  .modal-card {
    width: min(780px, 90vw);
    max-height: 84vh;
    overflow-y: auto;
  }

  .modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 4px solid rgba(233, 239, 255, 0.25);
    padding-bottom: 12px;
    margin-bottom: 18px;
  }

  .modal-title {
    font-family: 'Noto Sans KR', sans-serif;
    font-size: 1.3rem;
    font-weight: 700;
    color: #ffe08a;
    text-shadow: 2px 2px 0 var(--ink);
  }

  .close-btn {
    background: #26357f;
    border: none;
    color: #dbe6ff;
    font-size: 0.95rem;
    padding: 5px 14px;
    border-radius: 0;
    cursor: pointer;
    box-shadow: 0 0 0 3px var(--ink), 0 5px 0 3px var(--ink);
  }

  .close-btn:hover {
    background: var(--gold);
    color: #1a1030;
  }

  /* 신문 & 서류 더미 */
  .newspaper-sheet {
    background: #e8dec8;
    color: #241f18;
    padding: 26px;
    border-radius: 0;
    font-family: 'Gowun Batang', serif;
    box-shadow: 0 0 0 3px var(--ink), 0 6px 0 3px var(--ink);
  }

  .news-head {
    text-align: center;
    border-top: 3px double #241f18;
    border-bottom: 3px double #241f18;
    padding: 10px 0;
    margin-bottom: 16px;
  }

  .dossier-box {
    background: #f4efe4;
    color: #222;
    padding: 22px;
    border-radius: 0;
    font-family: 'Gowun Batang', serif;
    box-shadow: 0 0 0 3px var(--ink), 0 6px 0 3px var(--ink);
  }

  .check-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 13px;
    margin: 10px 0;
    background: #e6decb;
    border-left: 6px solid #7d6844;
    border-radius: 0;
    font-size: 1.05rem;
    font-weight: 700;
  }

  /* 노트북 정책 카드 */
  .policy-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(290px, 1fr));
    gap: 16px;
  }

  .policy-card {
    background: #1b2766;
    border: none;
    border-radius: 0;
    padding: 14px;
    cursor: pointer;
    transition: transform 0.08s steps(2);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    box-shadow: 0 0 0 3px #4b63c9, 0 0 0 6px var(--ink), 0 9px 0 6px var(--ink);
  }

  .policy-card:hover:not(.disabled) {
    box-shadow: 0 0 0 3px var(--gold), 0 0 0 6px var(--ink), 0 9px 0 6px var(--ink);
    transform: translateY(-3px);
    background: #25348a;
  }

  .policy-card.disabled {
    opacity: 0.52;
    cursor: not-allowed;
  }

  .badge-status {
    display: inline-block;
    font-size: 0.78rem;
    padding: 2px 8px;
    border-radius: 0;
    margin-top: 8px;
  }

  .badge-active { background: #2d6a4f; color: #d8f3dc; }
  .badge-pending { background: #b58328; color: #fff3b0; }
  .badge-ready { background: #3d405b; color: #e0e1dd; }

  /* 미니게임 UI 컴포넌트 */
  .radar-bar {
    position: relative;
    width: 100%;
    height: 36px;
    background: #0a0f2e;
    border: none;
    border-radius: 0;
    overflow: hidden;
    margin: 18px 0;
    box-shadow: 0 0 0 3px var(--edge), 0 0 0 6px var(--ink);
  }

  .radar-target {
    position: absolute;
    top: 0;
    height: 100%;
    background: rgba(64, 200, 130, 0.6);
    border-left: 3px solid #95d5b2;
    border-right: 3px solid #95d5b2;
  }

  .radar-cursor {
    position: absolute;
    top: 0;
    width: 8px;
    height: 100%;
    background: #ffd166;
    box-shadow: 0 0 0 2px var(--ink);
  }

  .sensor-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 18px;
    margin: 16px 0;
  }

  .sensor-node {
    background: #1b2250;
    border: none;
    border-radius: 0;
    padding: 16px;
    text-align: center;
    cursor: pointer;
    transition: transform 0.08s steps(2);
    box-shadow: 0 0 0 3px #6c757d, 0 0 0 6px var(--ink);
  }

  .sensor-node.dirty {
    background: #4a3420;
    box-shadow: 0 0 0 3px #e09f3e, 0 0 0 6px var(--ink);
  }

  .sensor-node.clean {
    background: #17402f;
    box-shadow: 0 0 0 3px #52b788, 0 0 0 6px var(--ink);
  }

  .action-btn {
    padding: 10px 24px;
    border-radius: 0;
    font-size: 1rem;
    font-weight: 700;
    cursor: pointer;
    border: none;
    transition: transform 0.08s steps(2);
    box-shadow: 0 0 0 3px var(--ink), 0 7px 0 3px var(--ink);
  }

  .action-btn:active { transform: translateY(4px); }

  .btn-yes { background: var(--gold); color: #1a1030; }
  .btn-yes:hover { background: #ffd978; }
  .btn-no { background: #3b4a9a; color: #e6e9f8; }
  .btn-no:hover { background: #4d5fbd; }

  .choice-btn {
    display: block;
    width: 100%;
    text-align: left;
    background: #1d2a70;
    border: none;
    color: #f0ece1;
    padding: 14px 18px;
    border-radius: 0;
    margin-bottom: 16px;
    cursor: pointer;
    font-size: 0.98rem;
    box-shadow: 0 0 0 3px #4b63c9, 0 0 0 6px var(--ink);
  }

  .choice-btn:hover {
    background: #2a3a94;
    box-shadow: 0 0 0 3px var(--gold), 0 0 0 6px var(--ink);
  }

  /* 툴팁 */
  #hover-tooltip {
    position: absolute;
    pointer-events: none;
    background: #101846;
    border: none;
    color: #fff4d2;
    padding: 5px 12px;
    border-radius: 0;
    font-size: 0.86rem;
    font-weight: 600;
    z-index: 18;
    display: none;
    transform: translate(-50%, -140%);
    white-space: nowrap;
    box-shadow: 0 0 0 3px var(--edge), 0 0 0 6px var(--ink);
  }
</style>
</head>
<body>

<div id="game-container">
  <canvas id="gameCanvas"></canvas>

  <!-- 타이틀 화면 -->
  <div id="title-overlay">
    <div class="title-logo">GREEN HORIZON</div>
    <div class="title-sub">기후 위기 속, 지속 가능한 대한민국의 미래를 평가하다</div>
    <button class="start-btn" onclick="startGame()">START</button>
  </div>

  <!-- 좌측 상단 기상 및 대기질 현황 -->
  <div id="hud-weather"></div>

  <!-- 긴급 현장 작업 알림 배너 -->
  <div id="alert-strip"></div>

  <!-- 우측 상단 시간 HUD -->
  <div id="hud-clock">
    <span class="clock-day" id="clock-day-text">1/15일차</span>
    <span class="clock-time" id="clock-time-text">07시 00분</span>
    <div>
      <button class="speed-btn active" id="spd-1" onclick="setSpeed(1)">1x</button>
      <button class="speed-btn" id="spd-5" onclick="setSpeed(5)">5x</button>
      <button class="speed-btn" id="spd-15" onclick="setSpeed(15)">15x</button>
    </div>
  </div>

  <!-- 호버 툴팁 -->
  <div id="hover-tooltip"></div>

  <!-- 하단 대화창 -->
  <div id="dialogue-box" onclick="closeDialogue()">
    <div class="speaker-tag" id="dialogue-speaker">나</div>
    <div class="dialogue-text" id="dialogue-text"></div>
    <div class="dialogue-next">▼ 클릭하여 계속</div>
  </div>

  <!-- 모달 창 -->
  <div id="modal-backdrop">
    <div class="hollow-panel modal-card" id="modal-content"></div>
  </div>
</div>

<script>
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

let width, height;
// 픽셀 아트용 저해상도 버퍼 (화면보다 작게 그린 뒤 확대)
let PS = 4, lw = 300, lh = 225;
const pcan = document.createElement('canvas');
let g = pcan.getContext('2d');
function resize() {
  width = canvas.width = window.innerWidth;
  height = canvas.height = window.innerHeight;
  PS = Math.max(3, Math.min(6, Math.round(height / 220)));
  lw = Math.max(80, Math.round(width / PS));
  lh = Math.max(60, Math.round(height / PS));
  pcan.width = lw;
  pcan.height = lh;
  g = pcan.getContext('2d');
}
window.addEventListener('resize', resize);
resize();

// --- 게임 상태 변수 ---
let scene = 'TITLE';
let day = 1;
const TOTAL_GAME_DAYS = 15;
let gameMinutes = 7 * 60; // 07:00 시작
let timeMultiplier = 1;   // 1배속 기준 게임 1시간 = 현실 5초
let lastTimestamp = 0;
let isPaused = false;

// 하루 동안 수행한 환경평가 업무 기록
let dailyWork = {
  tasks: [],
  budgetAtStart: 250
};
let pendingFinalDay = false;
let pendingDayNotice = '';
let previousCo2Emission = 280;

// 기후 위기 영향이 커진 대한민국 도시의 환경 및 시뮬레이션 지표
let budget = 250;
let pollutionRisk = 38; // 개발사업 누적 환경오염 위험도 (낮을수록 좋음)
let totalRainDays = 0;
let acidRainDays = 0;

let weather = {
  type: 'CLEAR',
  cloudType: 'WARM',
  windDir: '서풍',
  windSpeed: 2.4,
  humidity: 55,
  temp: 19,
  rainProb: 20,
  so2: 18,
  nox: 24,
  pm25: 32,
  ph: 6.5,
  ecoHealth: 72,
  co2: 280 // 도시 개발사업의 모의 온실가스 배출량 (tCO₂e/일)
};

// 실시간 현장 액션 상태 (환경영향평가원 업무)
let activeTasks = {
  seedingReady: true,      // 환경영향 예측 검토 가능 여부 (하루 1회)
  phAlert: false,          // 집중호우 시 비점오염 검토 필요 여부
  sensorDirty: false,      // 미세먼지 등으로 측정자료 품질 점검 필요 여부
  phoneRinging: false,     // 주민 의견·관계기관 협의 요청 수신 여부
  currentAudit: null
};

// 정책 데이터 (선택 후 2일 뒤에 적용)
const POLICIES = [
  { id: 'fgd', name: '저NOx 연소·배출가스 방지시설', cost: 45, desc: '연소 효율을 높이고 질소산화물·황산화물 저감시설을 설치하도록 사업계획에 반영합니다.', status: 'READY', applyDay: null },
  { id: 'esp', name: '고효율 설비 및 전력 사용 최적화', cost: 40, desc: '고효율 모터·전기화 설비와 에너지 관리 시스템을 적용해 온실가스와 대기오염 배출을 줄입니다.', status: 'READY', applyDay: null },
  { id: 'sensor', name: '대기질·소음 통합 측정망', cost: 25, desc: '사업지 경계와 주거지역에 측정망을 설치해 미세먼지와 소음 영향을 지속적으로 확인합니다.', status: 'READY', applyDay: null },
  { id: 'raingarden', name: '완충녹지 및 생태 연결축 확보', cost: 30, desc: '주거지와 사업시설 사이에 완충녹지를 두고 기존 녹지·하천 생태축을 연결하도록 권고합니다.', status: 'READY', applyDay: null },
  { id: 'permeable', name: '저영향개발(LID)·빗물관리', cost: 35, desc: '투수성 포장과 빗물정원, 저류시설을 반영해 불투수면 증가와 집중호우 때의 유출 영향을 줄입니다.', status: 'READY', applyDay: null },
  { id: 'reservoir', name: '폐수 재이용 및 비점오염 저감', cost: 50, desc: '폐수 재이용, 초기우수 처리, 유출수 관리계획을 마련해 하천과 토양에 미치는 영향을 줄입니다.', status: 'READY', applyDay: null },
  { id: 'seeding', name: '공사차량·비산먼지 관리계획', cost: 30, desc: '공사차량 동선과 운행시간을 조정하고 살수·세륜·덮개 등 비산먼지 저감대책을 마련합니다.', status: 'READY', applyDay: null }
];

// 창밖에 보이는 세 곳의 개발사업 예정 부지. 승인 전에는 빈 부지로만 보입니다.
const FACTORIES = [
  { id: 'factory1', name: '제1 에너지 공급시설 부지', facility: 'LNG 열병합발전소', benefit: '도시와 산업시설에 안정적인 전력과 열을 공급합니다.', role: '전력 공급은 필요하지만 연료 연소 과정에서 온실가스와 질소산화물 등이 발생할 수 있습니다. 주거지와의 이격거리, 배출구 높이, 저NOx 연소기술, 방지시설, 대체 에너지 입지를 비교해야 합니다.', pollutants: '온실가스(CO₂), 질소산화물(NOx), 황산화물(SOx), 소음 및 냉각수 영향', relX: 0.22, relY: 0.42, relW: 0.13, relH: 0.16 },
  { id: 'factory2', name: '제2 자원순환시설 부지', facility: '폐기물 소각·자원회수시설', benefit: '도시에서 발생하는 폐기물을 처리하고 열과 자원을 회수합니다.', role: '폐기물 처리시설은 도시 운영에 필요하지만 대기배출, 악취, 폐수, 폐기물 운반차량과 주민 수용성 문제가 발생할 수 있습니다. 재활용·감량 대안, 배출가스 처리, 밀폐형 반입시설, 교통 동선을 함께 비교해야 합니다.', pollutants: '질소산화물(NOx), 먼지, 악취, 폐수, 운반차량 배출가스 및 소음', relX: 0.44, relY: 0.43, relW: 0.14, relH: 0.15 },
  { id: 'factory3', name: '제3 물류지원시설 부지', facility: '대형 물류센터', benefit: '생활물자와 산업 원료를 공급하고 지역 일자리와 물류 기능을 지원합니다.', role: '물류시설은 지역경제와 생활에 필요하지만 대형 화물차 통행, 야간 소음, 대기오염, 넓은 불투수면과 녹지 훼손을 유발할 수 있습니다. 기존 도로 활용, 대중교통·친환경 차량, 완충녹지, 빗물관리 대안을 검토해야 합니다.', pollutants: '화물차 배출가스(PM2.5·NOx), 교통소음, 불투수면 증가, 녹지 훼손', relX: 0.68, relY: 0.41, relW: 0.13, relH: 0.17 }
];

// 세 부지의 최종 결정: standard(협의 동의), conditional(조건부 동의), reject(부동의/대안 재검토)
let facilityDecisions = [null, null, null];
let surveyPlanCompleted = [false, false, false];
let ecologyGameCompleted = [false, false, false];
let noiseGameCompleted = [false, false, false];
let mitigationGameCompleted = [false, false, false];
let windGameCompleted = [false, false, false];
let windChoice = null;
let windTarget = null;
let ecologySelections = [];
let noiseSelections = [];
let mitigationSelections = [];
let projectImpactScore = 0;
let assessmentQuality = 0;
let pendingMilestoneIndex = null;
let pendingFinalSettlement = false;
let endingType = null;

// 책상 위 오브젝트 (환경영향평가 현장 조사·분석 장비)
const DESK_ITEMS = [
  { id: 'radio', name: '📻 현장 조사팀 무전기', relX: 0.04, relY: 0.65, relW: 0.07, relH: 0.13 },
  { id: 'newspaper', name: '📰 대한민국 개발사업 평가 공고', relX: 0.13, relY: 0.74, relW: 0.14, relH: 0.12 },
  { id: 'documents', name: '📁 환경영향평가서·조사 체크리스트', relX: 0.29, relY: 0.70, relW: 0.13, relH: 0.14 },
  { id: 'laptop', name: '💻 환경 데이터 분석 노트북', relX: 0.44, relY: 0.64, relW: 0.16, relH: 0.17 },
  { id: 'sensor_pad', name: '📡 대기질·소음 측정자료 점검 단말기', relX: 0.62, relY: 0.67, relW: 0.08, relH: 0.12 },
  { id: 'beaker', name: '📐 개발사업 환경영향 예측 도면', relX: 0.72, relY: 0.66, relW: 0.07, relH: 0.14 },
  { id: 'photo', name: '🗺️ 대한민국 사업지 입지·토지이용 지도', relX: 0.80, relY: 0.73, relW: 0.06, relH: 0.10 },
  { id: 'penholder', name: '📝 조사 계획 수첩·근거 카드', relX: 0.87, relY: 0.72, relW: 0.04, relH: 0.10 },
  { id: 'phone', name: '☎️ 주민 의견·관계기관 협의 전화기', relX: 0.85, relY: 0.61, relW: 0.07, relH: 0.09 },
  { id: 'calendar', name: '📅 환경조사 및 평가 일정 캘린더', relX: 0.92, relY: 0.71, relW: 0.06, relH: 0.11 },
  { id: 'ecology_game', name: '🌿 생태 조사 표본 상자 미니게임', relX: 0.04, relY: 0.85, relW: 0.10, relH: 0.09 },
  { id: 'noise_game', name: '🔊 소음 측정 지도 미니게임', relX: 0.36, relY: 0.85, relW: 0.11, relH: 0.09 },
  { id: 'mitigation_game', name: '🧱 환경 저감시설 배치판 미니게임', relX: 0.68, relY: 0.85, relW: 0.11, relH: 0.09 },
  { id: 'wind_game', name: '💨 대기오염 확산 예측 미니게임', relX: 0.86, relY: 0.85, relW: 0.10, relH: 0.09 }
];

// 긴급 환경 감사/민원 시나리오 풀
const AUDIT_SCENARIOS = [
  {
    title: "주민 민원 · 발전시설의 대기오염 우려",
    speaker: "인근 아파트 주민",
    quote: "요즘 바람이 우리 동네 쪽으로 불 때가 많아요. 발전소가 들어오면 미세먼지나 냄새가 더 심해지는 건 아닌가요?",
    prompt: "주민의 우려를 확인하기 위해 가장 먼저 확보해야 할 근거는 무엇일까요?",
    evidence: [
      { text: "계절별 풍향·풍속 자료와 배출량을 이용한 대기확산 예측 결과", correct: true,
        effect: () => { budget = Math.max(0, budget - 5); weather.co2 = Math.max(180, weather.co2 - 10); pollutionRisk = Math.max(5, pollutionRisk - 2); return "정확해! 바람 방향과 배출량을 함께 봐야 오염물질이 어느 지역에 영향을 줄지 예측할 수 있어. 사업자에게 계절별 대기확산 예측과 배출량 산정 근거를 보완하도록 요청했어."; } },
      { text: "사업장 주변의 조경수 종류와 화단 면적", correct: false,
        effect: () => { return "조경도 중요하지만 주민이 걱정하는 대기오염의 이동과 농도를 판단하기에는 근거가 부족해. 풍향·풍속과 배출량, 대기확산 예측 자료가 더 직접적인 근거야."; } },
      { text: "공장 건물 외벽의 색상과 지붕 높이", correct: false,
        effect: () => { pollutionRisk = Math.min(100, pollutionRisk + 1); return "건물 외관은 대기오염 확산을 판단하는 핵심 자료가 아니야. 배출량과 기상 조건을 함께 살펴봐야 해."; } }
    ]
  },
  {
    title: "주민 민원 · 물류센터 차량 소음",
    speaker: "인근 초등학교 학부모",
    quote: "물류센터가 생기면 큰 트럭이 새벽에도 다닐 것 같아요. 아이들이 등교할 때 위험하고 소음도 걱정됩니다.",
    prompt: "교통과 생활환경 영향을 확인할 가장 적절한 근거는 무엇일까요?",
    evidence: [
      { text: "시간대별 교통량·차종 자료, 통학로 위치, 소음 예측 결과", correct: true,
        effect: () => { budget = Math.max(0, budget - 6); pollutionRisk = Math.max(5, pollutionRisk - 2); return "좋은 판단이야! 차량 통행량과 시간대, 통학로, 소음 예측을 함께 봐야 안전한 진출입 동선과 운행시간을 제안할 수 있어."; } },
      { text: "물류센터 내부 사무실의 책상 배치도", correct: false,
        effect: () => { return "내부 사무실 배치는 주변 도로의 교통량이나 통학로 안전, 외부 소음을 설명하지 못해. 시간대별 차량 자료와 소음 예측이 필요해."; } },
      { text: "사업장 직원들의 선호하는 출퇴근 복장", correct: false,
        effect: () => { pollutionRisk = Math.min(100, pollutionRisk + 1); return "주변 주민에게 미치는 교통·소음 영향과 관련이 적은 자료야. 차량 통행량과 통학로, 소음 예측 자료를 확인해야 해."; } }
    ]
  },
  {
    title: "주민 민원 · 하천 주변 녹지 훼손 우려",
    speaker: "하천 인근 주민",
    quote: "센터 진입도로가 하천 옆 나무가 많은 곳을 지나간다고 들었어요. 비가 많이 오면 흙탕물이 하천으로 들어갈까 걱정돼요.",
    prompt: "생태와 빗물 유출 영향을 확인할 가장 직접적인 근거는 무엇일까요?",
    evidence: [
      { text: "하천·녹지 현황도, 생태 조사 결과, 불투수면과 우수 유출 예측", correct: true,
        effect: () => { budget = Math.max(0, budget - 7); weather.ecoHealth = Math.min(100, weather.ecoHealth + 7); pollutionRisk = Math.max(5, pollutionRisk - 2); return "정확해! 녹지와 생태축의 위치, 불투수면 증가, 빗물 유출을 함께 봐야 해. 대체 노선과 완충녹지, 빗물 저류시설을 비교하도록 요청했어."; } },
      { text: "사업지 주변 상가의 간판 디자인 조사", correct: false,
        effect: () => { return "상권 경관 자료만으로는 하천 생태와 빗물 유출 영향을 알기 어려워. 생태 현황도와 불투수면, 우수 유출 예측이 필요해."; } },
      { text: "건설 현장 근로자의 식사 시간표", correct: false,
        effect: () => { pollutionRisk = Math.min(100, pollutionRisk + 1); return "주민이 우려한 하천 오염과 녹지 훼손을 판단할 근거가 아니야. 생태 조사와 빗물 유출 자료를 살펴봐야 해."; } }
    ]
  }
];

let particles = [];
for (let i = 0; i < 120; i++) {
  particles.push({
    x: Math.random() * 2000,
    y: Math.random() * 1200,
    speedX: 2 + Math.random() * 5,
    speedY: -0.5 + Math.random() * 1.5,
    size: 1 + Math.random() * 2.5,
    alpha: 0.2 + Math.random() * 0.5
  });
}

let radarInterval = null;

function setSpeed(spd) {
  timeMultiplier = spd;
  document.querySelectorAll('.speed-btn').forEach(b => b.classList.remove('active'));
  document.getElementById(`spd-${spd}`).classList.add('active');
}

function startGame() {
  const overlay = document.getElementById('title-overlay');
  overlay.classList.add('zooming');
  scene = 'ZOOMING';

  setTimeout(() => {
    overlay.style.display = 'none';
    scene = 'OFFICE';
    document.getElementById('hud-clock').style.display = 'flex';
    document.getElementById('hud-weather').style.display = 'block';
    updateWeatherHUD();
    updateAlertStrip();
    showDialogue('나', '기후 위기로 폭염과 집중호우, 미세먼지 문제가 심해진 대한민국의 한 도시야. 도시 외곽에는 에너지 공급시설, 자원순환시설, 물류지원시설을 새로 만들자는 계획이 나왔어. 세 시설은 시민 생활에 꼭 필요하지만 온실가스와 대기오염, 소음, 교통량 증가, 녹지 훼손을 일으킬 수 있지. 앞으로 15일 동안 환경평가원으로서 세 부지의 환경현황을 조사하고, 사업 시행 전·후의 영향을 예측한 뒤 대안과 저감방안을 비교해 협의 의견을 마련해야 해. 실제 사업 허가는 승인기관이 결정하지만, 우리의 평가 의견이 중요한 근거가 될 거야.');
  }, 1800);
}

function showDialogue(speaker, text) {
  isPaused = true;
  document.getElementById('dialogue-speaker').innerText = speaker;
  document.getElementById('dialogue-text').innerText = text;
  document.getElementById('dialogue-box').style.display = 'block';
}

function closeDialogue() {
  document.getElementById('dialogue-box').style.display = 'none';
  if (document.getElementById('modal-backdrop').style.display !== 'flex') {
    isPaused = false;
  }
}

function openModal(htmlContent) {
  isPaused = true;
  document.getElementById('modal-content').innerHTML = htmlContent;
  document.getElementById('modal-backdrop').style.display = 'flex';
}

function closeModal() {
  if (radarInterval) {
    clearInterval(radarInterval);
    radarInterval = null;
  }
  document.getElementById('modal-backdrop').style.display = 'none';
  if (document.getElementById('dialogue-box').style.display !== 'block') {
    isPaused = false;
  }
}

function updateAlertStrip() {
  const strip = document.getElementById('alert-strip');
  let alerts = [];
  if (activeTasks.phAlert) {
    alerts.push(`<div class="alert-pill" onclick="handleObjectClick('beaker')">📐 집중호우 영향 검토 필요 [환경영향 예측 도면] 클릭</div>`);
  }
  if (activeTasks.sensorDirty) {
    alerts.push(`<div class="alert-pill" onclick="handleObjectClick('sensor_pad')">📡 경고: 환경 측정장비 데이터 오류 발생! [점검 단말기] 클릭</div>`);
  }
  if (activeTasks.phoneRinging) {
    alerts.push(`<div class="alert-pill" onclick="handleObjectClick('phone')">☎️ 수신 중: 주민 의견·관계기관 협의 요청 도착! [전화기] 클릭</div>`);
  }
  if (alerts.length > 0) {
    strip.innerHTML = alerts.join('');
    strip.style.display = 'flex';
  } else {
    strip.style.display = 'none';
  }
}

function recordDailyTask(title, detail) {
  dailyWork.tasks.push({ title, detail });
}

function calculateFinalScores() {
  const builtCount = facilityDecisions.filter(d => d && d !== 'reject').length;
  const utilityScore = builtCount === 3 ? 3 : (builtCount >= 2 ? 2 : 1);
  const activePolicyCount = POLICIES.filter(p => p.status === 'ACTIVE' && p.id !== 'sensor').length;
  const netImpact = Math.max(0, projectImpactScore - activePolicyCount * 0.65 - assessmentQuality * 0.25);
  const risk = pollutionRisk;
  const environmentScore = (netImpact <= 1.5 && risk <= 48) ? 3 : ((netImpact <= 5 && risk <= 72) ? 2 : 1);
  return {
    utilityScore,
    environmentScore,
    builtCount,
    netImpact: +netImpact.toFixed(1),
    risk: +risk.toFixed(1)
  };
}

function scoreMark(score) {
  return score === 3 ? 'O' : (score === 2 ? '△' : 'x');
}

// --- 오브젝트 클릭 핸들러 ---
// --- 오브젝트 클릭 핸들러 ---
function handleObjectClick(id) {
  if (id === 'newspaper') {
    recordDailyTask('개발사업 평가 공고 및 사업계획 확인', '사업 목적, 규모, 입지, 공사·운영 계획과 환경영향평가 대상 항목을 확인했습니다.');
    openModal(`
      <div class="modal-header"><span class="modal-title">📰 대한민국 개발사업 환경영향평가 공고</span><button class="close-btn" onclick="closeModal()">닫기</button></div>
      <div class="newspaper-sheet"><div class="news-head"><div style="font-size:0.85rem; letter-spacing:0.2em;">대한민국 환경영향평가팀</div>
      <h2 style="font-size:1.45rem; margin-top:4px;">"필요한 개발과 환경 보전, 두 가지를 함께 검토합니다"</h2></div>
      <p style="line-height:1.8; font-size:1.02rem;">기후 위기로 폭염과 집중호우, 대기오염 위험이 커진 대한민국의 한 도시. 도시 외곽에 에너지 공급시설, 자원순환시설, 물류지원시설의 입지가 제안되었다. 세 시설은 도시 운영에 필요하지만 온실가스와 대기오염, 소음, 교통량 증가, 녹지 훼손 등의 영향을 일으킬 수 있다. 평가팀은 각 사업의 환경현황을 조사하고 사업 시행 전·후의 영향을 예측한 뒤, 입지 대안과 저감방안을 비교해 승인 의견을 마련해야 한다.</p></div>
    `);
  } else if (id === 'documents') {
    recordDailyTask('환경영향평가서 및 조사 체크리스트 검토', '환경현황, 영향예측, 대안 비교, 저감방안, 주민 의견 반영 여부를 점검했습니다.');
    const built = facilityDecisions.filter(d => d && d !== 'reject').length;
    openModal(`<div class="modal-header"><span class="modal-title">📁 환경영향평가서 검토 현황</span><button class="close-btn" onclick="closeModal()">닫기</button></div>
      <div class="dossier-box"><h3>평가서 핵심 검토 항목</h3>
      <div class="check-item"><span>① 사업 목적·규모·입지와 주변 토지이용</span><strong>검토</strong></div>
      <div class="check-item"><span>② 대기질·소음·물환경·생태·교통 현황</span><strong>조사 중</strong></div>
      <div class="check-item"><span>③ 사업 시행 전·후 환경영향 예측</span><strong>분석 중</strong></div>
      <div class="check-item"><span>④ 입지·규모·공법 대안 및 저감방안</span><strong>비교 중</strong></div>
      <div class="check-item"><span>⑤ 주민 의견 및 협의 조건 반영</span><strong>확인 중</strong></div>
      <div class="check-item"><span>승인 결정된 시설</span><strong>${built}/3곳</strong></div>
      <div class="check-item"><span>평가 예산 잔액</span><strong>${budget}억 원</strong></div></div>`);
  } else if (id === 'laptop') {
    renderLaptopModal();
  } else if (id === 'radio') {
    openImpactReviewMinigame();
  } else if (id === 'beaker') {
    openSiteImpactOverview();
  } else if (id === 'sensor_pad') {
    openSensorRepairMinigame();
  } else if (id === 'phone') {
    openAuditPhoneModal();
  } else if (id === 'photo') {
    recordDailyTask('사업지 입지 및 주변 환경 지도 검토', '주거지, 학교, 하천, 녹지, 기존 도로와 개발 예정 부지의 공간적 관계를 확인했습니다.');
    showDialogue('나', '지도에서 사업지와 주변 주거지, 학교, 하천, 녹지, 기존 도로가 얼마나 가까운지 확인해야 해. 입지를 조금만 조정해도 환경영향을 크게 줄일 수 있는지 비교해 보자.');
  } else if (id === 'penholder') {
    openSurveyPlanMinigame();
  } else if (id === 'ecology_game') {
    openEcologyFieldGame();
  } else if (id === 'noise_game') {
    openNoiseMappingGame();
  } else if (id === 'mitigation_game') {
    openMitigationPlacementGame();
  } else if (id === 'wind_game') {
    openWindDispersionGame();
  } else if (id === 'calendar') {
    const siteIndex = Math.min(2, Math.floor((day - 1) / 5));
    showDialogue('나', `오늘은 전체 15일 중 ${day}일차야. 현재는 ${siteIndex + 1}번 부지 평가 기간이고, ${Math.min(5, (siteIndex + 1) * 5 - day + 1)}일 안에 이 사업의 환경영향 검토를 마쳐야 해.`);
  } else if (id.startsWith('factory')) {
    openSiteInfoModal(id);
  }
}

function openSiteInfoModal(id) {
  const idx = FACTORIES.findIndex(f => f.id === id);
  const f = FACTORIES[idx];
  const decision = facilityDecisions[idx];
  const status = decision === 'standard' ? '협의 동의' : decision === 'conditional' ? '조건부 동의' : decision === 'reject' ? '부동의·대안 재검토' : '평가 중 · 미결정';
  recordDailyTask(`${f.name} 현장 입지 검토`, `${f.facility}의 필요성과 예상 환경영향, 주변 주거지·생태·교통 여건을 확인했습니다.`);
  openModal(`<div class="modal-header"><span class="modal-title">🏗️ ${f.name}</span><button class="close-btn" onclick="closeModal()">닫기</button></div>
    <div class="dossier-box"><div class="check-item"><span>제안 시설</span><strong>${f.facility}</strong></div>
    <p style="line-height:1.7; margin:12px 0;"><strong>도시에 필요한 이유</strong><br>${f.benefit}</p>
    <p style="line-height:1.7; margin:12px 0;"><strong>예상 환경영향</strong><br>${f.role}</p>
    <div class="check-item"><span>주요 검토 항목</span><strong>${f.pollutants}</strong></div>
    <div class="check-item"><span>현재 사업 결정</span><strong>${status}</strong></div>
    <p style="margin-top:12px; color:#e3c891; line-height:1.6;">부지의 클릭은 현장 정보를 확인하는 기능이야. 최종 승인 여부는 각 5일차 평가 결산 뒤에 결정해.</p></div>`);
}

function openSiteImpactOverview() {
  const idx = Math.min(2, Math.floor((day - 1) / 5));
  const f = FACTORIES[idx];
  recordDailyTask('사업 시행 전·후 환경영향 예측 검토', `${f.facility}의 예상 배출·소음·교통·토지이용 변화를 검토하고 저감방안 전후를 비교했습니다.`);
  openModal(`<div class="modal-header"><span class="modal-title">📐 환경영향 예측·대안 비교 도면</span><button class="close-btn" onclick="closeModal()">닫기</button></div>
    <div class="dossier-box"><h3>${f.facility} · ${idx + 1}번 부지</h3>
    <p style="line-height:1.7; margin:10px 0;">환경평가에서는 사업이 없을 때의 환경 상태와 사업 시행 시 예상되는 변화를 비교하고, 저감방안을 적용한 뒤 남는 영향을 다시 예측해.</p>
    <div class="check-item"><span>대기환경</span><strong>배출량·확산 범위</strong></div>
    <div class="check-item"><span>생활환경</span><strong>소음·진동·교통량</strong></div>
    <div class="check-item"><span>자연환경</span><strong>녹지·하천·생태축</strong></div>
    <div class="check-item"><span>물환경·토지</span><strong>불투수면·우수 유출</strong></div>
    <p style="margin-top:12px; color:#e3c891; line-height:1.6;">현재 검토 중인 사업: ${f.name}. 사업을 하지 않는 대안, 입지 조정, 규모 축소, 저감시설 설치를 함께 비교해 보자.</p></div>`);
}

// --- [미니게임 1] 개발사업 환경영향 예측 및 저감방안 선택 ---
function openImpactReviewMinigame() {
  if (!activeTasks.seedingReady) {
    showDialogue('나', '오늘의 환경영향 예측 검토는 완료했어. 다른 조사 자료를 확인하고 내일 새 자료가 들어오면 다시 비교하자.');
    return;
  }
  const idx = Math.min(2, Math.floor((day - 1) / 5));
  const f = FACTORIES[idx];
  openModal(`
    <div class="modal-header"><span class="modal-title">📻 ${f.facility} 환경영향 예측 검토</span><button class="close-btn" onclick="closeModal()">닫기</button></div>
    <p style="line-height:1.7; color:#cfc9bc; margin-bottom:12px;">사업계획의 영향을 예측하고 적절한 저감방안을 선택하세요. 평가 항목과 대책이 잘 맞을수록 검토의 질이 높아집니다.</p>
    <div class="dossier-box">
      <p><strong>예상 주요 영향</strong><br>${f.pollutants}</p>
      <label style="display:block; margin:14px 0 6px;">① 가장 우선해 검토할 영향 항목</label>
      <select id="impact-category" style="width:100%; padding:10px; background:#f6efd8; color:#1b1b1b;">
        <option value="air">대기질·온실가스</option><option value="noise">소음·교통</option><option value="water">물순환·수질</option><option value="eco">생태·토지이용</option>
      </select>
      <label style="display:block; margin:14px 0 6px;">② 가장 적절한 저감방안</label>
      <select id="impact-mitigation" style="width:100%; padding:10px; background:#f6efd8; color:#1b1b1b;">
        <option value="emission">배출가스 방지시설·고효율 설비</option><option value="buffer">입지 조정·완충녹지</option><option value="traffic">공사·운영 차량 동선 및 시간 관리</option><option value="water">빗물·폐수 관리와 투수성 포장</option>
      </select>
      <p style="font-size:0.82rem; color:#cfc9bc; margin-top:10px;">힌트: 시설의 종류와 주변 환경을 함께 고려하고, 영향이 큰 항목부터 우선 관리하세요.</p>
    </div>
    <div style="text-align:center; margin-top:16px;"><button class="action-btn btn-yes" onclick="submitImpactReview()">📊 예측·저감 검토 결과 제출</button></div>
  `);
}

function submitImpactReview() {
  const idx = Math.min(2, Math.floor((day - 1) / 5));
  const category = document.getElementById('impact-category').value;
  const mitigation = document.getElementById('impact-mitigation').value;
  const f = FACTORIES[idx];
  const expected = idx === 0 ? 'air' : (idx === 1 ? 'air' : 'traffic');
  const matched = category === expected || (idx === 1 && category === 'water') || (idx === 2 && category === 'noise');
  const mitigationGood = (category === 'air' && mitigation === 'emission') || (category === 'eco' && mitigation === 'buffer') || (category === 'noise' && mitigation === 'traffic') || (category === 'water' && mitigation === 'water');
  activeTasks.seedingReady = false;
  if (matched && mitigationGood) {
    assessmentQuality += 1;
    weather.ecoHealth = Math.min(100, weather.ecoHealth + 3);
    recordDailyTask('환경영향 예측 및 저감방안 비교', `${f.facility}의 주요 영향 항목과 저감방안을 연계해 검토하고 예측 결과를 보완했습니다.`);
    closeModal();
    showDialogue('나', '좋아! 주요 영향 항목과 저감방안이 잘 연결됐어. 평가서에는 저감방안 적용 전·후의 예측 결과와 선택한 대안의 이유를 구체적으로 남기자.');
  } else {
    recordDailyTask('환경영향 예측 검토', `${f.facility}의 영향 항목과 저감방안을 검토했으나 일부 연결이 적절하지 않아 추가 보완이 필요합니다.`);
    closeModal();
    showDialogue('나', '검토 방향을 조금 더 다듬어야겠어. 사업의 주요 배출·소음·교통·생태 영향을 먼저 파악하고, 그 영향에 직접 대응하는 저감방안을 연결해 보자.');
  }
  updateWeatherHUD();
}

// --- [미니게임 2] 환경 측정자료 품질관리 및 현장 점검 ---
function openPhNeutralizeMinigame() {
  openSiteImpactOverview();
}

// --- [미니게임 3] 대기질 센서 정비 단말기 ---
function openSensorRepairMinigame() {
  if (!activeTasks.sensorDirty) {
    showDialogue('나', '사업지 경계와 인근 주거지역의 대기질·소음 자료를 수집하고 있어. 측정 위치와 장비 교정 상태를 주기적으로 점검해야 해.');
    return;
  }

  openModal(`
    <div class="modal-header">
      <span class="modal-title">📡 도심 대기질 센서망 원격 정비 단말기</span>
      <button class="close-btn" onclick="closeModal()">닫기</button>
    </div>
    <p style="font-size:0.92rem; color:#cfc9bc; margin-bottom:12px;">
      장비 교정값이 기준에서 벗어나 측정자료의 품질에 문제가 생겼습니다. <strong>오류가 표시된 4개 측정 노드를 모두 클릭</strong>해 장비 상태를 점검하고 교정하세요!
    </p>
    <div class="sensor-grid">
      <div class="sensor-node dirty" id="node-1" onclick="cleanNode(1)">⚠️ 제1 부지 경계 센서<br><small>[미세먼지 막힘 - 클릭하여 세척]</small></div>
      <div class="sensor-node dirty" id="node-2" onclick="cleanNode(2)">⚠️ 주거지역 대기질 센서<br><small>[미세먼지 막힘 - 클릭하여 세척]</small></div>
      <div class="sensor-node dirty" id="node-3" onclick="cleanNode(3)">⚠️ 도로변 소음 센서<br><small>[미세먼지 막힘 - 클릭하여 세척]</small></div>
      <div class="sensor-node dirty" id="node-4" onclick="cleanNode(4)">⚠️ 하천변 환경 센서<br><small>[미세먼지 막힘 - 클릭하여 세척]</small></div>
    </div>
  `);
}

let cleanedCount = 0;
function cleanNode(idx) {
  const el = document.getElementById(`node-${idx}`);
  if (el && el.classList.contains('dirty')) {
    el.classList.remove('dirty');
    el.classList.add('clean');
    el.innerHTML = `✅ 구역 센서 정상 가동<br><small>[교정 완료]</small>`;
    cleanedCount++;
    if (cleanedCount >= 4) {
      cleanedCount = 0;
      activeTasks.sensorDirty = false;
      recordDailyTask('환경 측정장비 교정 및 자료 품질관리', '사업지 주변 4개 지점의 측정장비를 교정하고 자료 신뢰도를 복구했습니다.');
      setTimeout(() => {
        closeModal();
        updateAlertStrip();
        showDialogue('나', '4개 지점의 환경 측정장비를 모두 점검했어! 이제 신뢰할 수 있는 측정 자료를 환경영향평가에 활용할 수 있어.');
      }, 350);
    }
  }
}

// --- [추가 미니게임 A] 생태 현장 조사: 서식지 흔적 찾기 ---
function openEcologyFieldGame() {
  const idx = Math.min(2, Math.floor((day - 1) / 5));
  if (ecologyGameCompleted[idx]) {
    showDialogue('나', '이 부지의 생태 현장 조사는 완료했어. 조사 기록을 바탕으로 서식지 보전과 대체 공간을 검토하자.');
    return;
  }
  ecologySelections = [];
  const tiles = [
    ['🏙️','주차장'],['🌳','큰 나무'],['🪨','나지'],
    ['🐦','새 둥지'],['🏢','건물'],['🌾','풀밭'],
    ['🐸','물가 흔적'],['🚧','공사장'],['🦋','꽃 주변']
  ];
  openModal(`<div class="modal-header"><span class="modal-title">🌿 생태 현장 조사 · 서식 흔적 찾기</span><button class="close-btn" onclick="closeModal()">닫기</button></div>
    <p style="line-height:1.7;color:#d9d1bd;">사업지 주변을 살펴보고 생물 서식 가능성이 높은 지점 3곳을 직접 선택해 봐. 선택한 지점은 조사 기록에 표시돼.</p>
    <div class="dossier-box"><strong>조사 대상: ${FACTORIES[idx].facility}</strong><p style="margin:7px 0 12px;">서식 흔적이 있는 지점 3곳을 골라줘. 선택: <b id="eco-count">0/3</b></p><p id="eco-feedback" style="color:#ffd166;min-height:22px;"></p>
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:9px;">${tiles.map((t,i)=>`<button id="eco-tile-${i}" class="choice-btn" style="margin:0;text-align:center;min-height:78px;padding:9px;" onclick="toggleEcoTile(${i})"><span style="font-size:1.5rem;display:block;">${t[0]}</span><small>${t[1]}</small></button>`).join('')}</div></div>
    <div style="text-align:center;margin-top:16px;"><button class="action-btn btn-yes" onclick="submitEcologyGame()">조사 기록 제출</button></div>`);
}
function toggleEcoTile(i) {
  const pos = ecologySelections.indexOf(i);
  if (pos >= 0) ecologySelections.splice(pos,1);
  else if (ecologySelections.length < 3) ecologySelections.push(i);
  const el = document.getElementById(`eco-tile-${i}`);
  if (el) el.style.background = ecologySelections.includes(i) ? '#286b4c' : '#1d2a70';
  const count = document.getElementById('eco-count'); if (count) count.innerText = `${ecologySelections.length}/3`;
}
function submitEcologyGame() {
  if (ecologySelections.length !== 3) { const fb=document.getElementById('eco-feedback'); if(fb)fb.innerText='서식 가능성이 있는 지점을 정확히 세 곳 선택해 줘.'; return; }
  const idx = Math.min(2, Math.floor((day - 1) / 5));
  const targets = [[1,3,8],[1,5,6],[3,5,8]][idx];
  const good = targets.every(v => ecologySelections.includes(v)) && ecologySelections.every(v => targets.includes(v));
  if (!good) { const fb=document.getElementById('eco-feedback'); if(fb)fb.innerText='일부 선택 지점의 서식 근거가 부족해. 나무·물가·꽃 주변을 다시 살펴보자.'; return; }
  ecologyGameCompleted[idx] = true; assessmentQuality += 1; pollutionRisk = Math.max(5,pollutionRisk-2); weather.ecoHealth = Math.min(100,weather.ecoHealth+5);
  recordDailyTask('생태 현장 조사 및 서식 흔적 기록', `${FACTORIES[idx].facility} 주변의 서식 가능 지점을 확인하고 생태 보전 검토 자료를 확보했습니다.`);
  closeModal(); updateWeatherHUD(); showDialogue('나 · 생태 조사 완료','좋아! 서식 가능 지점을 기록했어. 이제 공사 구역 조정과 생태 연결축 확보 등 회피·저감 대안을 검토할 수 있어.');
}

// --- [추가 미니게임 B] 소음 측정: 측정값이 높은 구역 찾기 ---
function openNoiseMappingGame() {
  const idx = Math.min(2, Math.floor((day - 1) / 5));
  if (noiseGameCompleted[idx]) { showDialogue('나','이 부지의 소음 분포 측정은 완료했어. 측정 결과를 바탕으로 주거지와 학교 주변의 영향을 검토하자.'); return; }
  noiseSelections = [];
  const values = [42,48,51,39,55,78,73,44,40,69,82,50,35,47,58,41];
  openModal(`<div class="modal-header"><span class="modal-title">🔊 소음 측정 · 고소음 지점 추적</span><button class="close-btn" onclick="closeModal()">닫기</button></div>
    <p style="line-height:1.7;color:#d9d1bd;">측정 지도를 보고 소음이 큰 지점 3곳을 선택해. 숫자는 모의 측정값(dB)이야. 높은 값이 표시된 구역을 찾아보자.</p>
    <div class="dossier-box"><strong>사업지 주변 소음 측정 지도</strong><p style="margin:7px 0 12px;">고소음 지점 선택: <b id="noise-count">0/3</b></p><p id="noise-feedback" style="color:#ffd166;min-height:22px;"></p>
    <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px;">${values.map((v,i)=>`<button id="noise-tile-${i}" class="choice-btn" style="margin:0;text-align:center;padding:14px 4px;background:${v>=69?'#75402d':'#263b62'};" onclick="toggleNoiseTile(${i})"><b>${v}</b><small style="display:block;">dB · 구역 ${i+1}</small></button>`).join('')}</div>
    <p style="font-size:.82rem;margin-top:10px;color:#d9d1bd;">참고: 실제 소음 평가는 시간대·측정 위치·측정 조건을 함께 고려해야 해.</p></div>
    <div style="text-align:center;margin-top:16px;"><button class="action-btn btn-yes" onclick="submitNoiseGame()">소음 지도 완성</button></div>`);
}
function toggleNoiseTile(i) {
  const pos=noiseSelections.indexOf(i); if(pos>=0) noiseSelections.splice(pos,1); else if(noiseSelections.length<3) noiseSelections.push(i);
  const el=document.getElementById(`noise-tile-${i}`); if(el) el.style.outline=noiseSelections.includes(i)?'4px solid #ffd166':'none';
  const count=document.getElementById('noise-count'); if(count) count.innerText=`${noiseSelections.length}/3`;
}
function submitNoiseGame() {
  if(noiseSelections.length!==3){const fb=document.getElementById('noise-feedback');if(fb)fb.innerText='측정값이 높은 지점을 세 곳 선택해 줘.';return;}
  const idx=Math.min(2,Math.floor((day-1)/5));
  const targets=[5,6,10];
  const good=targets.every(v=>noiseSelections.includes(v))&&noiseSelections.every(v=>targets.includes(v));
  if(!good){const fb=document.getElementById('noise-feedback');if(fb)fb.innerText='선택한 지점에 고소음 구역이 아닌 곳이 포함됐어. 측정값을 다시 비교해 보자.';return;}
  noiseGameCompleted[idx]=true; assessmentQuality+=1; pollutionRisk=Math.max(5,pollutionRisk-1.5);
  recordDailyTask('주변 소음 측정 및 고소음 구역 지도화',`${FACTORIES[idx].facility} 주변의 소음 측정값을 비교해 우선 관리 구역을 표시했습니다.`);
  closeModal(); updateWeatherHUD(); showDialogue('나 · 소음 조사 완료','고소음 구역을 찾아냈어! 이 결과를 활용해 방음벽 위치, 운행 시간 조정, 주거지와의 완충거리 등을 검토하자.');
}

// --- [추가 미니게임 C] 저감시설 배치: 환경 민감 구역 보호하기 ---
function openMitigationPlacementGame() {
  const idx=Math.min(2,Math.floor((day-1)/5));
  if(mitigationGameCompleted[idx]){showDialogue('나','이 부지의 저감시설 배치안은 이미 검토했어. 다음은 실제 이행 여부를 확인하는 일이야.');return;}
  mitigationSelections=[];
  const cells=[['주거지','🏠'],['도로','🚚'],['녹지','🌳'],['하천','🌊'],['사업지','🏭'],['학교','🏫'],['공원','🌲'],['주차장','🅿️'],['마을','🏘️']];
  openModal(`<div class="modal-header"><span class="modal-title">🧱 환경 저감시설 배치 시뮬레이터</span><button class="close-btn" onclick="closeModal()">닫기</button></div>
    <p style="line-height:1.7;color:#d9d1bd;">사업지 주변의 민감한 공간을 보호하도록 완충시설을 둘 두 곳에 배치해 봐. 타일을 누르면 녹지 완충시설을 설치하거나 해제할 수 있어.</p>
    <div class="dossier-box"><strong>${FACTORIES[idx].facility} · 배치 도면</strong><p style="margin:7px 0 12px;">완충시설 설치 지점: <b id="mitigation-count">0/2</b></p><p id="mitigation-feedback" style="color:#ffd166;min-height:22px;"></p>
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:8px;">${cells.map((c,i)=>`<button id="mit-tile-${i}" class="choice-btn" style="margin:0;text-align:center;padding:12px 4px;" onclick="toggleMitigationTile(${i})"><span style="font-size:1.4rem;display:block;">${c[1]}</span><small>${c[0]}</small></button>`).join('')}</div>
    <p style="font-size:.82rem;margin-top:10px;color:#d9d1bd;">목표는 사업지 자체가 아니라 주변의 민감한 공간과 오염 이동 경로를 보호하는 거야.</p></div>
    <div style="text-align:center;margin-top:16px;"><button class="action-btn btn-yes" onclick="submitMitigationGame()">배치안 검토</button></div>`);
}
function toggleMitigationTile(i){const pos=mitigationSelections.indexOf(i);if(pos>=0)mitigationSelections.splice(pos,1);else if(mitigationSelections.length<2)mitigationSelections.push(i);const el=document.getElementById(`mit-tile-${i}`);if(el)el.style.background=mitigationSelections.includes(i)?'#286b4c':'#1d2a70';const count=document.getElementById('mitigation-count');if(count)count.innerText=`${mitigationSelections.length}/2`;}
function submitMitigationGame(){
  if(mitigationSelections.length!==2){const fb=document.getElementById('mitigation-feedback');if(fb)fb.innerText='완충시설을 둘 지점 두 곳을 선택해 줘.';return;}
  const idx=Math.min(2,Math.floor((day-1)/5));
  const targets=[[0,3],[1,5],[0,5]][idx];
  const good=targets.every(v=>mitigationSelections.includes(v))&&mitigationSelections.every(v=>targets.includes(v));
  if(!good){const fb=document.getElementById('mitigation-feedback');if(fb)fb.innerText='환경 민감 구역을 충분히 보호하지 못해. 주거지·학교·하천과 사업지의 관계를 다시 살펴보자.';return;}
  mitigationGameCompleted[idx]=true; assessmentQuality+=1; pollutionRisk=Math.max(5,pollutionRisk-3); weather.ecoHealth=Math.min(100,weather.ecoHealth+3);
  recordDailyTask('환경 저감시설 공간 배치 및 대안 비교',`${FACTORIES[idx].facility} 주변의 민감 공간을 고려해 완충시설 배치 대안을 검토했습니다.`);
  closeModal(); updateWeatherHUD(); showDialogue('나 · 저감대책 배치 완료','좋아! 환경 민감 구역을 고려한 배치안을 만들었어. 실제 평가에서는 이 배치의 효과와 유지관리 가능성도 확인해야 해.');
}

// --- [추가 미니게임 D] 대기오염 확산 예측: 풍향과 영향권 맞추기 ---
function openWindDispersionGame(){
  const idx=Math.min(2,Math.floor((day-1)/5));
  if(windGameCompleted[idx]){showDialogue('나','이 부지의 대기확산 방향 검토는 완료했어. 실제 평가서에는 계절별 풍향·풍속과 배출량을 함께 검토해야 해.');return;}
  windChoice=null; windTarget=null;
  openModal(`<div class="modal-header"><span class="modal-title">💨 대기오염 확산 예측 시뮬레이터</span><button class="close-btn" onclick="closeModal()">닫기</button></div>
    <p style="line-height:1.7;color:#d9d1bd;">바람은 오염물질이 이동하는 방향에 영향을 줘. 먼저 바람이 불어오는 방향을 선택하고, 그 바람이 불어가는 쪽의 영향권을 골라 봐.</p>
    <div class="dossier-box"><strong>${FACTORIES[idx].facility} · 모의 풍향 조작</strong>
      <p style="margin:8px 0;">① 바람이 불어오는 방향을 선택해.</p>
      <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:7px;">${[['west','서풍'],['east','동풍'],['south','남풍'],['north','북풍']].map(v=>`<button id="wind-${v[0]}" class="choice-btn" style="margin:0;text-align:center;padding:10px 3px;" onclick="chooseWind('${v[0]}')">${v[1]}</button>`).join('')}</div>
      <p id="wind-arrow" style="text-align:center;font-size:1.15rem;margin:12px 0;color:#ffd166;min-height:28px;">풍향을 선택하면 이동 방향이 표시돼.</p>
      <p style="margin:8px 0;">② 오염물질이 이동할 가능성이 높은 영향권을 선택해.</p>
      <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:7px;">${[['north','북쪽'],['east','동쪽'],['south','남쪽'],['west','서쪽']].map(v=>`<button id="zone-${v[0]}" class="choice-btn" style="margin:0;text-align:center;padding:12px 3px;" onclick="chooseWindZone('${v[0]}')">${v[1]} 영향권</button>`).join('')}</div>
      <p id="wind-feedback" style="color:#ffd166;min-height:22px;margin-top:10px;"></p>
    </div><div style="text-align:center;margin-top:16px;"><button class="action-btn btn-yes" onclick="submitWindGame()">확산 예측 제출</button></div>`);
}
function chooseWind(dir){
  windChoice=dir; const map={west:['east','서풍 → 동쪽'],east:['west','동풍 → 서쪽'],south:['north','남풍 → 북쪽'],north:['south','북풍 → 남쪽']};
  ['west','east','south','north'].forEach(d=>{const el=document.getElementById(`wind-${d}`);if(el)el.style.background=d===dir?'#286b4c':'#1d2a70';});
  const label=document.getElementById('wind-arrow');if(label)label.innerText=`바람 이동 방향: ${map[dir][1]} →`;
}
function chooseWindZone(zone){windTarget=zone;['north','east','south','west'].forEach(d=>{const el=document.getElementById(`zone-${d}`);if(el)el.style.background=d===zone?'#286b4c':'#1d2a70';});}
function submitWindGame(){
  if(!windChoice||!windTarget){const fb=document.getElementById('wind-feedback');if(fb)fb.innerText='풍향과 영향권을 모두 선택해 줘.';return;}
  const expected={west:'east',east:'west',south:'north',north:'south'}[windChoice];
  if(windTarget!==expected){const fb=document.getElementById('wind-feedback');if(fb)fb.innerText='바람이 불어가는 방향과 영향권이 일치하지 않아. 화살표를 다시 확인해 봐.';return;}
  const idx=Math.min(2,Math.floor((day-1)/5));windGameCompleted[idx]=true;assessmentQuality+=1;pollutionRisk=Math.max(5,pollutionRisk-2);
  recordDailyTask('풍향에 따른 대기오염 확산 영향권 예측',`${FACTORIES[idx].facility}의 모의 풍향과 오염물질 이동 방향을 연결해 영향권을 검토했습니다.`);
  closeModal();updateWeatherHUD();showDialogue('나 · 대기확산 검토 완료','정확해! 바람이 불어가는 쪽을 영향권으로 표시했어. 실제 평가는 계절별 풍향·풍속, 배출량, 굴뚝 조건과 지형을 반영한 확산 모델로 더 정밀하게 예측해야 해.');
}

// --- [미니게임] 조사 계획 수립: 사업별 핵심 영향과 조사 근거 연결 ---
function openSurveyPlanMinigame() {
  const idx = Math.min(2, Math.floor((day - 1) / 5));
  const f = FACTORIES[idx];
  if (surveyPlanCompleted[idx]) {
    showDialogue('나', `${idx + 1}번 부지의 조사 계획은 이미 검토했어. 이제 다른 자료를 확인하거나 남은 업무를 진행하자.`);
    return;
  }

  const planGuides = [
    {
      impact: 'air',
      evidence: 'wind',
      method: 'dispersion',
      impactLabel: '대기질·온실가스',
      evidenceLabel: '계절별 풍향·풍속 및 기존 대기질 자료',
      methodLabel: '배출량 산정과 계절별 대기확산 예측 비교',
      hint: '연료를 태우는 시설은 무엇이 배출되는지, 바람을 타고 어디로 이동하는지 확인해야 해.'
    },
    {
      impact: 'airwater',
      evidence: 'stack',
      method: 'waste',
      impactLabel: '대기오염·악취·폐수',
      evidenceLabel: '주변 대기질, 악취 민감시설, 하천·배수로 현황',
      methodLabel: '배출가스 처리와 폐수·악취 관리대책 비교',
      hint: '폐기물 처리시설은 굴뚝 배출뿐 아니라 악취, 폐수, 반입 차량도 함께 살펴봐야 해.'
    },
    {
      impact: 'traffic',
      evidence: 'traffic',
      method: 'route',
      impactLabel: '교통·소음·생태·토지이용',
      evidenceLabel: '시간대별 교통량, 통학로, 녹지·생태축 지도',
      methodLabel: '진입도로 대안, 운행시간 조정, 완충녹지 비교',
      hint: '물류시설은 차량이 언제 어디로 다니는지, 도로가 주거지와 녹지를 어떻게 통과하는지가 중요해.'
    }
  ];
  const guide = planGuides[idx];
  const options = {
    impact: [
      ['air', '대기질·온실가스'], ['airwater', '대기오염·악취·폐수'], ['traffic', '교통·소음·생태·토지이용'], ['visual', '건물 외관·조경 디자인']
    ],
    evidence: [
      ['wind', '계절별 풍향·풍속 및 기존 대기질 자료'],
      ['stack', '주변 대기질·악취 민감시설·하천 및 배수로 현황'],
      ['traffic', '시간대별 교통량·통학로·녹지와 생태축 지도'],
      ['irrelevant', '건물 외벽 색상과 사무실 배치도']
    ],
    method: [
      ['dispersion', '배출량 산정과 계절별 대기확산 예측 비교'],
      ['waste', '배출가스 처리와 폐수·악취 관리대책 비교'],
      ['route', '진입도로 대안·운행시간·완충녹지 비교'],
      ['beauty', '건물 외관과 조경 디자인만 비교']
    ]
  };
  const makeOptions = (key) => `<option value="" selected>선택하세요</option>` + options[key].map(([value, label]) => `<option value="${value}">${label}</option>`).join('');
  openModal(`
    <div class="modal-header"><span class="modal-title">📝 ${idx + 1}번 부지 조사 계획 수립</span><button class="close-btn" onclick="closeModal()">닫기</button></div>
    <div class="dossier-box">
      <div style="font-size:0.82rem; color:#765d3d; margin-bottom:6px;">${day}일차 · ${f.facility}</div>
      <h3>무엇을, 어떤 자료로, 어떻게 조사할까?</h3>
      <p style="line-height:1.65; margin:9px 0;">${f.benefit}</p>
      <div style="background:#e8dfc9; padding:11px; line-height:1.65; margin:10px 0;">
        <strong>💡 조사 계획을 세우는 순서</strong><br>
        ① 시설 특성상 가장 큰 환경영향을 고른다.<br>
        ② 그 영향을 확인할 수 있는 현황 자료를 고른다.<br>
        ③ 영향 예측과 대안 비교 방법을 정한다.
      </div>
      <p style="font-size:0.9rem; line-height:1.6; color:#5e503d;">힌트: ${guide.hint}</p>
      <label style="display:block; margin:14px 0 6px; font-weight:700;">1. 우선 조사할 환경영향</label>
      <select id="plan-impact" style="width:100%; padding:11px; background:#f6efd8; color:#211d18;">${makeOptions('impact')}</select>
      <label style="display:block; margin:14px 0 6px; font-weight:700;">2. 확보해야 할 현황 자료</label>
      <select id="plan-evidence" style="width:100%; padding:11px; background:#f6efd8; color:#211d18;">${makeOptions('evidence')}</select>
      <label style="display:block; margin:14px 0 6px; font-weight:700;">3. 적절한 예측·대안 검토 방법</label>
      <select id="plan-method" style="width:100%; padding:11px; background:#f6efd8; color:#211d18;">${makeOptions('method')}</select>
      <div style="font-size:0.82rem; line-height:1.6; margin-top:12px; color:#69583f;">정답을 맞히면 조사 계획이 평가서에 반영되고 평가 품질이 올라가. 틀려도 설명을 확인한 뒤 다시 도전할 수 있어.</div>
    </div>
    <div style="text-align:center; margin-top:16px;"><button class="action-btn btn-yes" onclick="submitSurveyPlan(${idx})">조사 계획 제출</button></div>
  `);
}

function submitSurveyPlan(idx) {
  const guide = [
    { impact: 'air', evidence: 'wind', method: 'dispersion' },
    { impact: 'airwater', evidence: 'stack', method: 'waste' },
    { impact: 'traffic', evidence: 'traffic', method: 'route' }
  ][idx];
  const impact = document.getElementById('plan-impact')?.value;
  const evidence = document.getElementById('plan-evidence')?.value;
  const method = document.getElementById('plan-method')?.value;
  const correctCount = Number(impact === guide.impact) + Number(evidence === guide.evidence) + Number(method === guide.method);
  if (correctCount === 3) {
    surveyPlanCompleted[idx] = true;
    assessmentQuality += 1.5;
    pollutionRisk = Math.max(5, pollutionRisk - 2);
    recordDailyTask('사업 특성에 맞는 환경현황 조사 계획 수립', `${FACTORIES[idx].facility}: 핵심 영향, 현황 자료, 예측·대안 검토 방법을 올바르게 연결했습니다.`);
    closeModal();
    showDialogue('나 · 조사 계획 승인', '완벽해! 무엇을 조사할지, 어떤 자료가 필요한지, 어떻게 영향을 예측할지 논리적으로 연결했어. 이 계획을 바탕으로 평가서의 신뢰도를 높일 수 있겠어.');
  } else {
    const hints = [
      impact !== guide.impact ? '① 시설에서 가장 크게 발생할 수 있는 환경영향부터 생각해 봐.' : '',
      evidence !== guide.evidence ? '② 주민·자연환경에 미치는 영향을 실제로 확인할 수 있는 현황 자료를 골라야 해.' : '',
      method !== guide.method ? '③ 조사한 자료를 이용해 사업 전후의 변화와 대안을 비교할 수 있는 방법을 골라야 해.' : ''
    ].filter(Boolean).join('<br>');
    openModal(`
      <div class="modal-header"><span class="modal-title">🔎 조사 계획을 조금 더 다듬어 보자</span><button class="close-btn" onclick="closeModal()">닫기</button></div>
      <div class="dossier-box">
        <h3>${correctCount}/3개 항목이 적절해</h3>
        <p style="line-height:1.8; margin-top:10px;">${hints}</p>
        <p style="line-height:1.7; margin-top:12px; color:#6b5638;">조사 계획은 시설의 특성 → 예상 영향 → 필요한 현황 자료 → 예측 방법 순서로 생각하면 쉬워.</p>
      </div>
      <div style="text-align:center; margin-top:16px;"><button class="action-btn btn-yes" onclick="openSurveyPlanMinigame()">다시 계획하기</button></div>
    `);
  }
}

// --- [미니게임 4] 환경평가원 직통 전화기 (돌발 감사 & 민원) ---
function openAuditPhoneModal() {
  if (!activeTasks.phoneRinging || !activeTasks.currentAudit) {
    showDialogue('나', '아직 접수된 주민 의견이 없어. 전화가 오면 주민의 말을 듣고, 가장 관련 깊은 자료를 골라 근거를 찾아보자.');
    return;
  }

  const audit = activeTasks.currentAudit;
  openModal(`
    <div class="modal-header">
      <span class="modal-title">☎️ 주민 의견 접수 · ${audit.title}</span>
      <button class="close-btn" onclick="closeModal()">닫기</button>
    </div>
    <div style="display:flex; gap:12px; align-items:flex-start; margin:8px 0 16px;">
      <div style="font-size:2.2rem; flex:0 0 auto;">🧑</div>
      <div style="position:relative; background:#f6efd8; color:#29251f; border:3px solid #9b835d; padding:14px 16px; line-height:1.8; border-radius:12px; flex:1;">
        <strong style="display:block; color:#72512c; margin-bottom:5px;">${audit.speaker}</strong>
        “${audit.quote}”
      </div>
    </div>
    <div class="dossier-box">
      <h3>🔎 어떤 자료를 확인해야 할까?</h3>
      <p style="line-height:1.65; margin:8px 0 12px;">${audit.prompt}</p>
      <p style="font-size:0.85rem; color:#66563f; margin-bottom:10px;">가장 직접적인 근거가 되는 카드를 하나 선택해 봐.</p>
      ${audit.evidence.map((item, i) => `
        <button class="choice-btn" style="text-align:left; margin:7px 0; line-height:1.55;" onclick="resolveAudit(${i})">
          <strong>${String.fromCharCode(65 + i)}.</strong> ${item.text}
        </button>
      `).join('')}
    </div>
  `);
}

function resolveAudit(choiceIdx) {
  const audit = activeTasks.currentAudit;
  if (!audit || !audit.evidence || !audit.evidence[choiceIdx]) return;
  const selected = audit.evidence[choiceIdx];
  const wasCorrect = selected.correct;
  const resultMsg = selected.effect();
  if (wasCorrect) {
    assessmentQuality += 1;
    recordDailyTask('주민 의견에서 환경영향 근거 찾기 성공', `${audit.title}: ${selected.text}`);
  } else {
    recordDailyTask('주민 의견 검토 및 근거 자료 재확인', `${audit.title}: 선택한 자료가 핵심 우려와 직접 연결되지 않아 추가 확인이 필요합니다.`);
  }
  activeTasks.phoneRinging = false;
  activeTasks.currentAudit = null;
  closeModal();
  updateWeatherHUD();
  updateAlertStrip();
  showDialogue(wasCorrect ? '나 · 근거 확인 성공' : '나 · 자료를 다시 살펴보자', resultMsg);
}

// --- 노트북 정책 화면 ---
function renderLaptopModal() {
  let cardsHtml = POLICIES.map(p => {
    let badge = '';
    let disabledClass = '';
    let onClickAttr = `onclick="confirmPolicy('${p.id}')"`;

    if (p.status === 'ACTIVE') {
      badge = `<span class="badge-status badge-active">✔ 가동 중</span>`;
      disabledClass = 'disabled';
      onClickAttr = '';
    } else if (p.status === 'PENDING') {
      badge = `<span class="badge-status badge-pending">⏳ 설치 중 (${p.applyDay}일차 적용 예정)</span>`;
      disabledClass = 'disabled';
      onClickAttr = '';
    } else if (budget < p.cost) {
      badge = `<span class="badge-status badge-ready">예산 부족 (${p.cost}억 필요)</span>`;
      disabledClass = 'disabled';
      onClickAttr = '';
    } else {
      badge = `<span class="badge-status badge-ready">시행 가능 (비용: ${p.cost}억)</span>`;
    }

    return `
      <div class="policy-card ${disabledClass}" ${onClickAttr}>
        <div>
          <div style="font-weight:700; font-size:1.05rem; color:#f5e6c8; margin-bottom:5px;">${p.name}</div>
          <div style="font-size:0.86rem; color:#cfc9bc; line-height:1.45;">${p.desc}</div>
        </div>
        <div>${badge}</div>
      </div>
    `;
  }).join('');

  openModal(`
    <div class="modal-header">
      <span class="modal-title">💻 환경영향 저감방안 검토 시스템 (잔여 예산: ${budget}억)</span>
      <button class="close-btn" onclick="closeModal()">닫기</button>
    </div>
    <p style="font-size:0.88rem; color:#c9b182; margin-bottom:12px;">
      ※ 선택한 저감방안은 사업계획 반영과 협의 절차를 거쳐 <strong>2일 후</strong>부터 적용됩니다.
    </p>
    <div class="policy-grid">${cardsHtml}</div>
  `);
}

function confirmPolicy(policyId) {
  const p = POLICIES.find(item => item.id === policyId);
  openModal(`
    <div style="text-align:center; padding:20px 10px;">
      <h3 style="font-family:'Gowun Batang', serif; font-size:1.45rem; color:#f5e6c8; margin-bottom:12px;">
        "${p.name}"을(를) 선택하시겠습니까?
      </h3>
      <p style="color:#cfc9bc; font-size:0.98rem;">
        소요 예산: <strong>${p.cost}억</strong> | 적용 시점: <strong>${day + 2}일차 아침</strong>
      </p>
      <div style="display:flex; justify-content:center; gap:16px; margin-top:24px;">
        <button class="action-btn btn-yes" onclick="executePolicy('${p.id}')">확인</button>
        <button class="action-btn btn-no" onclick="renderLaptopModal()">아니오</button>
      </div>
    </div>
  `);
}

function executePolicy(policyId) {
  const p = POLICIES.find(item => item.id === policyId);
  if (budget >= p.cost && p.status === 'READY') {
    budget -= p.cost;
    recordDailyTask('환경영향 저감방안 제안', `${p.name}을(를) 사업계획의 저감·적응 대책으로 제안했습니다.`);
    p.status = 'PENDING';
    p.applyDay = day + 2;
    renderLaptopModal();
  }
}

// --- 일일 환경 & 대기화학 시뮬레이션 ---
function simulateNewDay() {
  activeTasks.seedingReady = true;
  let newlyApplied = [];
  POLICIES.forEach(p => {
    if (p.status === 'PENDING' && day >= p.applyDay) {
      p.status = 'ACTIVE';
      newlyApplied.push(p.name);
    }
  });
  const activeIds = POLICIES.filter(p => p.status === 'ACTIVE').map(p => p.id);
  const standardCount = facilityDecisions.filter(d => d === 'standard').length;
  const conditionalCount = facilityDecisions.filter(d => d === 'conditional').length;

  const roll = Math.random() * 100;
  if (roll < 12) weather.type = 'HEAVY_RAIN';
  else if (roll < 34) weather.type = 'FINE_DUST';
  else if (roll < 48) weather.type = 'HEATWAVE';
  else weather.type = 'CLEAR';
  if (weather.type === 'FINE_DUST') { activeTasks.sensorDirty = true; cleanedCount = 0; }

  if (!activeTasks.phoneRinging && Math.random() < 0.48) {
    activeTasks.phoneRinging = true;
    activeTasks.currentAudit = AUDIT_SCENARIOS[Math.floor(Math.random() * AUDIT_SCENARIOS.length)];
  }

  const dirs = ['북풍', '북서풍', '서풍', '남서풍', '남동풍', '동풍'];
  weather.windDir = dirs[Math.floor(Math.random() * dirs.length)];
  weather.windSpeed = +(0.8 + Math.random() * 5.5).toFixed(1);
  weather.temp = weather.type === 'HEATWAVE' ? Math.floor(33 + Math.random() * 5) : Math.floor(12 + Math.random() * 16);
  weather.humidity = weather.type === 'HEAVY_RAIN' ? 88 : Math.floor(35 + Math.random() * 45);

  const dispersion = weather.windSpeed * 1.8;
  const facilityLoad = standardCount * 9 + conditionalCount * 4;
  weather.so2 = Math.max(5, Math.min(150, 18 + facilityLoad * 0.3 - (activeIds.includes('fgd') ? 12 : 0) - dispersion));
  weather.nox = Math.max(7, Math.min(140, 24 + facilityLoad * 0.7 - (activeIds.includes('fgd') ? 14 : 0) - dispersion));
  weather.pm25 = Math.max(8, Math.min(200, 30 + (weather.type === 'FINE_DUST' ? 28 : 0) + facilityLoad * 0.5 - (activeIds.includes('sensor') ? 4 : 0) - dispersion));
  weather.co2 = Math.max(170, Math.round(280 + standardCount * 55 + conditionalCount * 22 - (activeIds.includes('fgd') ? 22 : 0) - (activeIds.includes('esp') ? 30 : 0)));

  let dailyRiskChange = 0.65 + standardCount * 0.85 + conditionalCount * 0.28;
  if (weather.type === 'FINE_DUST') dailyRiskChange += 2.2;
  if (weather.type === 'HEATWAVE') dailyRiskChange += 1.2;
  if (weather.type === 'HEAVY_RAIN') dailyRiskChange += 0.8;
  if (activeIds.includes('fgd')) dailyRiskChange -= 0.55;
  if (activeIds.includes('esp')) dailyRiskChange -= 0.55;
  if (activeIds.includes('raingarden')) dailyRiskChange -= 0.45;
  if (activeIds.includes('permeable')) dailyRiskChange -= 0.35;
  if (activeIds.includes('reservoir')) dailyRiskChange -= 0.3;
  if (activeIds.includes('seeding')) dailyRiskChange -= 0.25;
  pollutionRisk = Math.max(5, Math.min(100, pollutionRisk + dailyRiskChange));
  if (activeIds.includes('raingarden')) weather.ecoHealth = Math.min(100, weather.ecoHealth + 1.5);
  if (weather.type === 'FINE_DUST') weather.ecoHealth = Math.max(10, weather.ecoHealth - 1);

  updateWeatherHUD();
  updateAlertStrip();
  if (newlyApplied.length > 0) pendingDayNotice = `오늘부터 [${newlyApplied.join(', ')}] 저감방안이 적용되기 시작했습니다.`;
}

function updateWeatherHUD() {
  const hud = document.getElementById('hud-weather');
  const weatherNames = {
    'CLEAR': '🌤️ 보통 기상 · 환경 조사 가능',
    'HEATWAVE': '🌡️ 기후 위기 영향: 폭염·오존 주의',
    'FINE_DUST': '🌫️ 미세먼지 농도 상승 · 측정자료 확인',
    'HEAVY_RAIN': '🌧️ 집중호우 · 비점오염·침수 영향 검토',
    'RAIN': '🌦️ 강수 중 · 유출수 관리 확인'
  };
  const hasSensor = POLICIES.find(p => p.id === 'sensor').status === 'ACTIVE';
  const sensorInfo = (hasSensor && !activeTasks.sensorDirty)
    ? `SO₂: ${weather.so2.toFixed(0)} | NOₓ: ${weather.nox.toFixed(0)} | PM2.5: ${weather.pm25.toFixed(0)}`
    : (activeTasks.sensorDirty ? `⚠️ 측정자료 품질 점검 필요 (단말기 클릭)` : `환경 측정 데이터: [통합 측정망 미설치]`);
  hud.innerHTML = `
    <div style="font-weight:700; color:#f3d59b;">${weatherNames[weather.type]}</div>
    <div style="font-size:0.84rem; color:#ddd;">바람: ${weather.windDir} ${weather.windSpeed}m/s | 습도: ${weather.humidity}% | 기온: ${weather.temp}℃</div>
    <div style="font-size:0.82rem; color:#a8dadc; margin-top:2px;">온실가스 추정 배출량: ${weather.co2.toFixed(0)}tCO₂e/일</div>
    <div style="font-size:0.82rem; color:#a8dadc; margin-top:2px;">${sensorInfo} | 누적 환경오염 위험도: ${pollutionRisk.toFixed(1)}%</div>
  `;
}

// --- 하루 업무 결산 및 5일 단위 사업 추진 심의 ---
function showDailySummary(completedDay, snapshot, isFinalDay) {
  pendingFinalDay = isFinalDay;
  const taskList = snapshot.tasks.length
    ? snapshot.tasks.map((task, index) => `<div class="check-item" style="display:block;"><div style="font-weight:700;">${index + 1}. ${task.title}</div><div style="font-size:0.88rem; font-weight:400; margin-top:5px; line-height:1.5;">${task.detail}</div></div>`).join('')
    : `<div class="check-item"><span>오늘 기록된 업무가 없습니다. 사업계획서와 입지 자료를 확인해 보세요.</span></div>`;
  const co2Change = snapshot.co2 - snapshot.previousCo2;
  const co2Text = co2Change < 0 ? `전날보다 ${Math.abs(co2Change).toFixed(0)}tCO₂e/일 감소` : (co2Change > 0 ? `전날보다 ${co2Change.toFixed(0)}tCO₂e/일 증가` : '전날과 동일');
  const milestone = completedDay % 5 === 0;
  const siteNo = Math.ceil(completedDay / 5);
  openModal(`
    <div class="modal-header"><span class="modal-title">📋 ${completedDay}일차 환경평가 업무 결산</span><button class="close-btn" onclick="closeDailySummary()">확인</button></div>
    <div class="dossier-box">
      <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:2px solid #8c7a5b; padding-bottom:12px; margin-bottom:14px;"><span style="font-size:1.05rem; font-weight:700;">오늘의 환경평가 업무</span><span style="font-size:1.25rem; font-weight:800; color:#1b4332;">${snapshot.tasks.length}건</span></div>
      ${taskList}
      <div class="check-item"><span>온실가스 추정 배출량</span><strong>${snapshot.co2.toFixed(0)}tCO₂e/일</strong></div>
      <div style="font-size:0.88rem; margin:4px 0 12px 4px; color:#4b453a;">${co2Text}</div>
      <div class="check-item"><span>누적 환경오염 위험도 (모의 지표)</span><strong>${snapshot.risk.toFixed(1)}%</strong></div>
      <div class="check-item"><span>평가 예산 잔액</span><strong>${snapshot.budget.toFixed(0)}억 원</strong></div>
      ${pendingDayNotice ? `<div style="margin-top:12px; padding:10px; background:#e6decb; line-height:1.6;">📌 ${pendingDayNotice}</div>` : ''}
      ${milestone ? `<div style="margin-top:14px; padding:12px; background:#e6decb; color:#30291f; line-height:1.6;"><strong>⚖️ ${siteNo}번 부지 평가 완료</strong><br>5일간의 환경현황 조사, 영향 예측, 대안 및 저감방안 검토를 마쳤습니다. 결산을 닫으면 해당 부지의 환경영향평가 협의 의견을 결정합니다.</div>` : ''}
    </div>
    <div style="text-align:center; margin-top:18px;"><button class="action-btn btn-yes" onclick="closeDailySummary()">${milestone ? `${siteNo}번 부지 승인 심의하기` : (isFinalDay ? '최종 심의로 이동' : '다음 날 업무 시작')}</button></div>
  `);
  pendingDayNotice = '';
}

function closeDailySummary() {
  closeModal();
  if (pendingMilestoneIndex !== null) {
    showSiteDecisionModal(pendingMilestoneIndex);
  } else if (pendingFinalDay) {
    pendingFinalDay = false;
    showFinalAssessmentSummary();
  }
}

function advanceGameDay() {
  const completedDay = day;
  const snapshot = { tasks: dailyWork.tasks.slice(), co2: weather.co2, previousCo2: previousCo2Emission, risk: pollutionRisk, budget: budget };
  if (completedDay % 5 === 0) {
    pendingMilestoneIndex = Math.floor(completedDay / 5) - 1;
    pendingFinalSettlement = completedDay === TOTAL_GAME_DAYS;
    showDailySummary(completedDay, snapshot, pendingFinalSettlement);
    return;
  }
  previousCo2Emission = weather.co2;
  day++;
  gameMinutes = 7 * 60;
  dailyWork = { tasks: [], budgetAtStart: budget };
  pendingDayNotice = '';
  simulateNewDay();
  showDailySummary(completedDay, snapshot, false);
}

function showSiteDecisionModal(index) {
  const f = FACTORIES[index];
  const dayRange = index === 0 ? '1~5일차' : (index === 1 ? '6~10일차' : '11~15일차');
  const already = facilityDecisions[index];
  const decisionText = already ? '이미 결정된 부지입니다.' : '평가 결과를 바탕으로 사업 추진 여부를 결정하세요.';
  openModal(`<div class="modal-header"><span class="modal-title">⚖️ ${index + 1}번 부지 환경영향평가 협의 의견</span><span style="font-size:0.8rem; color:#c9b182;">결정 필요</span></div>
    <div class="dossier-box"><div style="font-weight:700; margin-bottom:8px;">${dayRange} 평가 대상: ${f.name}</div>
    <h3>${f.facility}</h3><p style="line-height:1.7; margin:10px 0;">${f.benefit}</p>
    <p style="line-height:1.7; margin:10px 0;"><strong>주요 예상 환경영향</strong><br>${f.pollutants}</p>
    <p style="line-height:1.7; margin:10px 0;">${f.role}</p>
    <p style="color:#e3c891; line-height:1.6;">실제 환경영향평가 담당자는 사업 허가를 직접 내리기보다 환경영향을 검토해 협의 의견과 저감 조건을 제시합니다. 이 게임에서는 그 의견을 바탕으로 사업이 추진되는 상황을 단순화했습니다. 기본 동의는 환경 부담이 크고, 조건부 동의는 저감시설·운영조건을 의무화하며, 부동의는 입지·규모 대안을 다시 검토하게 합니다.</p></div>
    <div style="display:grid; gap:10px; margin-top:14px;">
      <button class="choice-btn" onclick="decideFacility(${index}, 'standard')">① 협의 동의 · 기본 계획으로 사업 추진 (환경 부담 큼)</button>
      <button class="choice-btn" onclick="decideFacility(${index}, 'conditional')">② 조건부 동의 · 저감대책 이행을 전제로 사업 추진 (예산 18억)</button>
      <button class="choice-btn" onclick="decideFacility(${index}, 'reject')">③ 부동의 의견 · 입지/규모 대안 재검토 (사업 보류)</button>
    </div>`);
}

function decideFacility(index, decision) {
  if (facilityDecisions[index]) return;
  if (decision === 'conditional' && budget < 18) {
    showDialogue('나', '조건부 동의에 필요한 환경저감 예산이 부족해. 예산을 확인한 뒤 다른 결정을 선택해야 해.');
    return;
  }
  const f = FACTORIES[index];
  facilityDecisions[index] = decision;
  if (decision === 'standard') {
    projectImpactScore += 2.1;
    recordDailyTask(`${f.facility} 기본 계획 협의 동의`, '시설의 필요성을 인정해 협의 동의 의견을 냈지만, 제시된 환경관리 조건은 기본 수준으로 남았습니다.');
    pendingDayNotice = `${f.facility} 기본 계획 협의 동의. 시설이 부지에 건설되며 환경 부담이 반영됩니다.`;
  } else if (decision === 'conditional') {
    budget -= 18;
    projectImpactScore += 0.65;
    recordDailyTask(`${f.facility} 조건부 동의`, '배출 저감시설, 운영관리, 주변 환경 모니터링 등 구체적인 이행조건을 붙여 조건부 동의 의견을 제시했습니다.');
    pendingDayNotice = `${f.facility} 조건부 동의. 환경관리 조건을 붙여 시설을 건설합니다.`;
  } else {
    recordDailyTask(`${f.facility} 부동의 및 대안 재검토`, '현 입지의 환경영향을 피하기 위해 부동의 의견을 제시하고 대체 입지·규모·수요관리 대안을 다시 검토하도록 했습니다.');
    pendingDayNotice = `${f.facility} 사업은 부동의되었습니다. 해당 부지는 빈 상태로 유지됩니다.`;
  }
  closeModal();
  pendingMilestoneIndex = null;
  if (pendingFinalSettlement) {
    pendingFinalSettlement = false;
    pendingFinalDay = false;
    showFinalAssessmentSummary();
    return;
  }
  previousCo2Emission = weather.co2;
  day = (index + 1) * 5 + 1;
  gameMinutes = 7 * 60;
  dailyWork = { tasks: [], budgetAtStart: budget };
  simulateNewDay();
  updateWeatherHUD();
  isPaused = false;
}

function showFinalAssessmentSummary() {
  const scores = calculateFinalScores();
  const builtNames = FACTORIES.filter((f, i) => facilityDecisions[i] && facilityDecisions[i] !== 'reject').map(f => f.facility);
  const rows = [
    { label: '도시에 꼭 필요한 시설이 모두 들어왔는가?', score: scores.utilityScore, detail: `${scores.builtCount}/3개 시설 건설` },
    { label: '도시의 환경오염 정도가 악화되지 않고 환경을 보존하였는가?', score: scores.environmentScore, detail: `누적 환경오염 위험도 ${scores.risk}% · 잔여 영향 지수 ${scores.netImpact}` }
  ];
  openModal(`<div class="modal-header"><span class="modal-title">📋 15일 최종 환경영향평가 결산</span></div>
    <div class="dossier-box"><h3>최종 협의 의견</h3>
      ${FACTORIES.map((f,i)=>`<div class="check-item"><span>${i+1}. ${f.facility}</span><strong>${facilityDecisions[i] === 'standard' ? '협의 동의' : facilityDecisions[i] === 'conditional' ? '조건부 동의' : '부동의'}</strong></div>`).join('')}
      <h3 style="margin-top:18px;">도시의 최종 평가 체크리스트</h3>
      ${rows.map(r=>`<div class="check-item" style="align-items:flex-start;"><span style="max-width:76%; line-height:1.6;">${r.label}<br><small>${r.detail}</small></span><strong style="font-size:1.45rem; min-width:34px; text-align:center;">${scoreMark(r.score)}</strong></div>`).join('')}
      <p style="font-size:0.82rem; margin-top:12px; color:#6b5b46;">평가 표기: x = 1점(기준 미달) · △ = 2점(보통) · O = 3점(우수)</p>
    </div><div style="text-align:center; margin-top:18px;"><button class="start-btn" onclick="checkCampaignEnd()">엔딩 보기</button></div>`);
}

// --- 최종 체크리스트 점수에 따른 엔딩 ---
function checkCampaignEnd() {
  const status = calculateFinalScores();
  const hasO = status.utilityScore === 3 || status.environmentScore === 3;
  const hasTriangle = status.utilityScore === 2 || status.environmentScore === 2;
  endingType = hasO ? 'green' : (hasTriangle ? 'partial' : 'desert');
  scene = 'ENDING';
  isPaused = true;
  document.getElementById('hud-clock').style.display = 'none';
  document.getElementById('hud-weather').style.display = 'none';
  document.getElementById('alert-strip').style.display = 'none';

  let title = '';
  let message = '';
  if (hasO) {
    title = 'GOOD ENDING : 지속 가능한 대한민국';
    message = `15일 동안의 평가가 끝났어. 평가 결과에서 우수한 성과를 얻은 덕분에 도시는 환경을 보전할 기회를 지켜냈어.<br><br>창밖의 대한민국 도시는 녹지와 깨끗한 공기를 되찾아 가고 있어. 아직 보완할 점은 남아 있지만, 환경을 고려한 선택이 미래를 바꿀 수 있다는 걸 보여줬어.<br><br><em>주인공: "우리의 평가가 도시를 지키는 데 도움이 됐어. 정말 뿌듯하다."</em>`;
  } else if (hasTriangle) {
    title = 'PARTIAL ENDING : 버텨내는 도시';
    message = `도시는 유지되고 있지만, 일부 개발사업의 환경 부담이 남아 미세먼지와 생활환경 문제가 이전보다 심해졌어.<br><br>그래도 도시가 무너지지는 않았어. 앞으로 저감시설을 보완하고 사후환경영향조사를 꾸준히 해야 해.`;
  } else {
    title = 'BAD ENDING : 사막이 된 도시';
    message = `필요한 시설과 환경 보전, 두 가지 모두 놓치고 말았어. 기후 위기와 무분별한 개발이 겹치면서 도시의 녹지는 사라지고 땅은 메말라 사막처럼 변했어.<br><br><em>주인공: "너무 우리의 이득만 생각했나 봐..."</em>`;
  }
  openModal(`<div style="text-align:center; padding:15px;"><h2 style="font-family:'Cinzel', serif; font-size:1.8rem; color:#f3d59b; margin-bottom:14px;">${title}</h2>
    <div style="font-size:1.1rem; line-height:1.9; color:#f0ece1; margin-bottom:22px;">${message}</div>
    <div class="dossier-box" style="text-align:left;"><div class="check-item"><span>도시에 필요한 시설</span><strong>${scoreMark(status.utilityScore)} (${status.utilityScore}점)</strong></div><div class="check-item"><span>환경 보전</span><strong>${scoreMark(status.environmentScore)} (${status.environmentScore}점)</strong></div></div>
    <button class="start-btn" onclick="location.reload()">처음부터 다시하기</button></div>`);
}

// --- 그래픽 렌더링 (픽셀 아트 · 점프킹 + 투더문 감성) ---
// 모든 장면은 저해상도 버퍼(pcan)에 그린 뒤 확대해서 보여줍니다.
// 게임 로직과 클릭/호버 영역(relX, relY ...)은 그대로이고, 그리는 방식만 바뀌었습니다.
const INK = '#16111f';
let lastFrameT = 0;
let frameDt = 0.016;
const layerCache = {};

function beginFrame() {
  const now = performance.now();
  frameDt = lastFrameT ? Math.min(0.05, (now - lastFrameT) / 1000) : 0.016;
  lastFrameT = now;
  g.clearRect(0, 0, lw, lh);
}

function makeRng(seed) {
  let s = seed >>> 0;
  return function () {
    s = (s * 1664525 + 1013904223) >>> 0;
    return s / 4294967296;
  };
}

function hexToRgb(h) {
  const n = parseInt(h.slice(1), 16);
  return [(n >> 16) & 255, (n >> 8) & 255, n & 255];
}

function mixHex(a, b, t) {
  const A = hexToRgb(a);
  const B = hexToRgb(b);
  return 'rgb(' + Math.round(A[0] + (B[0] - A[0]) * t) + ',' + Math.round(A[1] + (B[1] - A[1]) * t) + ',' + Math.round(A[2] + (B[2] - A[2]) * t) + ')';
}

function colorAt(stops, t) {
  if (t <= stops[0][0]) return stops[0][1];
  for (let i = 1; i < stops.length; i++) {
    if (t <= stops[i][0]) {
      const a = stops[i - 1];
      const b = stops[i];
      return mixHex(a[1], b[1], (t - a[0]) / (b[0] - a[0]));
    }
  }
  return stops[stops.length - 1][1];
}

// 픽셀 사각형
function pr(x, y, w, h, c) {
  g.fillStyle = c;
  g.fillRect(Math.round(x), Math.round(y), Math.max(1, Math.round(w)), Math.max(1, Math.round(h)));
}

// 외곽선이 있는 상자
function box(x, y, w, h, fill, line) {
  pr(x, y, w, h, line || INK);
  if (w > 2 && h > 2) pr(x + 1, y + 1, w - 2, h - 2, fill);
}

// 안쪽 하이라이트 / 그림자
function shade(x, y, w, h, light, dark) {
  if (w < 4 || h < 4) return;
  pr(x + 1, y + 1, w - 2, 1, light);
  pr(x + 1, y + 1, 1, h - 2, light);
  pr(x + 1, y + h - 2, w - 2, 1, dark);
  pr(x + w - 2, y + 1, 1, h - 2, dark);
}

function pline(x0, y0, x1, y1, c) {
  x0 = Math.round(x0); y0 = Math.round(y0); x1 = Math.round(x1); y1 = Math.round(y1);
  const dx = Math.abs(x1 - x0);
  const dy = Math.abs(y1 - y0);
  const sx = x0 < x1 ? 1 : -1;
  const sy = y0 < y1 ? 1 : -1;
  let err = dx - dy;
  g.fillStyle = c;
  for (let guard = 0; guard < 300; guard++) {
    g.fillRect(x0, y0, 1, 1);
    if (x0 === x1 && y0 === y1) break;
    const e2 = 2 * err;
    if (e2 > -dy) { err -= dy; x0 += sx; }
    if (e2 < dx) { err += dx; y0 += sy; }
  }
}

function pixDisc(cx, cy, r, c) {
  g.fillStyle = c;
  for (let dy = -r; dy <= r; dy++) {
    const half = Math.round(Math.sqrt(r * r - dy * dy));
    g.fillRect(Math.round(cx - half), Math.round(cy + dy), half * 2 + 1, 1);
  }
}

// 상대 좌표(relX...) -> 버퍼 좌표
function rr(o) {
  return {
    x: Math.round(lw * o.relX),
    y: Math.round(lh * o.relY),
    w: Math.max(4, Math.round(lw * o.relW)),
    h: Math.max(4, Math.round(lh * o.relH))
  };
}

// 자주 안 바뀌는 배경은 한 번만 그려서 재사용 (성능)
function cachedLayer(name, key, fn) {
  let L = layerCache[name];
  if (!L) {
    L = layerCache[name] = { cv: document.createElement('canvas'), key: '' };
  }
  if (L.key !== key) {
    L.cv.width = lw;
    L.cv.height = lh;
    const prev = g;
    g = L.cv.getContext('2d');
    fn();
    g = prev;
    L.key = key;
  }
  g.drawImage(L.cv, 0, 0);
}

// 계단식 그라데이션 (16비트 느낌 + 경계 디더링)
function pixelBands(y0, y1, stops, step) {
  const n = Math.max(1, Math.ceil((y1 - y0) / step));
  for (let i = 0; i < n; i++) {
    const t = n === 1 ? 0 : i / (n - 1);
    const c = colorAt(stops, t);
    pr(0, y0 + i * step, lw, step, c);
    if (i > 0) {
      g.fillStyle = c;
      for (let x = i % 2; x < lw; x += 2) g.fillRect(x, y0 + i * step - 1, 1, 1);
    }
  }
}

// ---------- 하늘 / 천체 ----------
const SKY_STOPS = {
  dust:    [[0, '#7a4f2c'], [0.5, '#b8803f'], [1, '#d9a566']],
  rain:    [[0, '#1c2433'], [0.5, '#33425a'], [1, '#4a5a6e']],
  morning: [[0, '#2f3f78'], [0.5, '#9a7b9a'], [1, '#f0b088']],
  day:     [[0, '#2b6cb0'], [0.5, '#6fa8d8'], [1, '#ebd5b3']],
  dusk:    [[0, '#2d1e3e'], [0.6, '#b85d43'], [1, '#f2b872']],
  night:   [[0, '#080b24'], [0.55, '#16225a'], [1, '#2a3d78']]
};

const CITY_TONE = {
  dust: 'rgba(170,105,40,0.38)',
  rain: 'rgba(28,38,60,0.45)',
  morning: 'rgba(150,90,110,0.18)',
  day: null,
  dusk: 'rgba(120,45,40,0.28)',
  night: 'rgba(6,10,40,0.62)'
};

function skyVariant() {
  const clockMinutes = gameMinutes % (24 * 60);
  const hour = Math.floor(clockMinutes / 60);
  if (weather.type === 'FINE_DUST' || endingType === 'desert') return 'dust';
  if (weather.type === 'RAIN' || weather.type === 'HEAVY_RAIN') return 'rain';
  if (hour >= 5 && hour < 8) return 'morning';
  if (hour >= 8 && hour < 17) return 'day';
  if (hour >= 17 && hour < 19) return 'dusk';
  return 'night';
}

const STARS = (function () {
  const r = makeRng(7);
  const a = [];
  for (let i = 0; i < 80; i++) a.push({ x: r(), y: r(), ph: r() * 6.28, big: r() < 0.2 });
  return a;
})();

function drawStars(yMax, alphaMul, excl) {
  const T = Date.now() / 1000;
  STARS.forEach(s => {
    const x = Math.round(s.x * lw);
    const y = Math.round(s.y * yMax);
    if (excl && Math.abs(x - excl.x) < excl.r && Math.abs(y - excl.y) < excl.r) return;
    g.globalAlpha = (0.55 + 0.45 * Math.sin(T * 1.6 + s.ph)) * alphaMul;
    pr(x, y, 1, 1, '#f4f1d8');
    if (s.big) {
      pr(x - 1, y, 3, 1, '#f4f1d8');
      pr(x, y - 1, 1, 3, '#f4f1d8');
    }
  });
  g.globalAlpha = 1;
}

function drawMoon(cx, cy, r) {
  g.globalAlpha = 0.10; pixDisc(cx, cy, r + 8, '#cfe0ff');
  g.globalAlpha = 0.16; pixDisc(cx, cy, r + 4, '#cfe0ff');
  g.globalAlpha = 1;
  pixDisc(cx, cy, r, '#f6f0cf');
  pixDisc(cx - Math.round(r * 0.35), cy - Math.round(r * 0.25), Math.max(1, Math.round(r * 0.22)), '#dcd5ab');
  pixDisc(cx + Math.round(r * 0.3), cy + Math.round(r * 0.3), Math.max(1, Math.round(r * 0.28)), '#e3dcb4');
  pixDisc(cx + Math.round(r * 0.1), cy - Math.round(r * 0.5), Math.max(1, Math.round(r * 0.12)), '#d4cda3');
}

function drawSun(cx, cy, r, core, glow) {
  g.globalAlpha = 0.18; pixDisc(cx, cy, r + 7, glow);
  g.globalAlpha = 0.28; pixDisc(cx, cy, r + 3, glow);
  g.globalAlpha = 1;
  pixDisc(cx, cy, r, core);
}

const CLOUDS = [
  { x: 0.10, y: 0.10, s: 2, v: 2.0 }, { x: 0.45, y: 0.18, s: 3, v: 1.2 },
  { x: 0.75, y: 0.08, s: 2, v: 1.6 }, { x: 0.30, y: 0.30, s: 2, v: 0.8 },
  { x: 0.90, y: 0.26, s: 3, v: 1.0 }, { x: 0.60, y: 0.34, s: 2, v: 1.4 }
];

function pixCloud(x, y, s, light, shade2) {
  pr(x + 2 * s, y, 6 * s, 2 * s, light);
  pr(x, y + 2 * s, 12 * s, 2 * s, light);
  pr(x + s, y + 4 * s, 10 * s, s, shade2);
}

function drawClouds(light, shade2, count, T) {
  for (let i = 0; i < count; i++) {
    const c = CLOUDS[i];
    const x = ((c.x * lw + T * c.v * 3) % (lw + 50)) - 34;
    pixCloud(Math.round(x), Math.round(c.y * lh), c.s, light, shade2);
  }
}

function drawCelestial(variant, dp, T) {
  const sunR = Math.max(4, Math.round(lh * 0.055));
  const u = Math.max(0, Math.min(1, dp / 0.88));
  const sx = Math.round(lw * (0.08 + 0.84 * u));
  const sy = Math.round(lh * (0.43 - 0.29 * Math.sin(Math.PI * u)));
  if (variant === 'night') {
    drawStars(lh * 0.5, 1, null);
    drawMoon(Math.round(lw * 0.78), Math.round(lh * 0.2), Math.max(5, Math.round(lh * 0.07)));
    drawClouds('#26356e', '#1b2756', 2, T);
  } else if (variant === 'dusk') {
    drawStars(lh * 0.35, 0.4, null);
    drawSun(sx, sy, sunR, '#ffcf7a', '#ff9a5a');
    drawClouds('#e89a78', '#b8604f', 3, T);
  } else if (variant === 'morning') {
    drawSun(sx, sy, sunR, '#ffe0a0', '#ffb878');
    drawClouds('#f6d2c0', '#c49aa8', 3, T);
  } else if (variant === 'day') {
    drawSun(sx, sy, sunR, '#fff4c0', '#ffe28a');
    drawClouds('#ffffff', '#c9d9ea', 4, T);
  } else if (variant === 'dust') {
    drawSun(Math.round(lw * 0.7), Math.round(lh * 0.25), sunR, '#f3dca4', '#d8a860');
  } else if (variant === 'rain') {
    drawClouds('#59667c', '#434f66', 6, T);
  }
}

// ---------- 도시 레이어 (원경 + 지면 + 공장) ----------
function factoryGeom(f) {
  const x = Math.round(lw * f.relX);
  const y = Math.round(lh * f.relY);
  const w = Math.max(10, Math.round(lw * f.relW));
  const h = Math.max(10, Math.round(lh * f.relH));
  const bodyOff = Math.round(h * 0.35);
  return { x: x, y: y, w: w, h: h, bodyY: y + bodyOff, bodyH: h - bodyOff };
}

function chimney(cx, cy, cw, ch) {
  box(cx, cy, cw, ch, '#4a4f6a');
  pr(cx + 1, cy + 1, 1, ch - 2, '#6a708c');
  pr(cx, cy, cw, 2, INK);
  pr(cx + 1, cy + 1, cw - 2, 2, '#c0392b');
  pr(cx + 1, cy + 4, cw - 2, 2, '#e8e2d0');
  pr(cx + 1, cy + 7, cw - 2, 2, '#c0392b');
}

function drawCityLayer(variant, green) {
  const r = makeRng(11);
  const groundY = Math.round(lh * 0.54);
  const groundH = Math.round(lh * 0.14);
  const towerLights = [];

  // 원경 마천루
  let x = 0;
  while (x < lw) {
    const bw = 5 + Math.floor(r() * 8);
    const bh = Math.round(lh * (0.07 + r() * 0.15));
    const by = groundY + 2 - bh;
    pr(x, by, bw, bh + 4, '#8d9ab4');
    pr(x + bw - 2, by, 2, bh + 4, '#7684a2');
    if (r() < 0.35) pr(x + Math.floor(bw / 2), by - 4, 1, 4, '#8d9ab4');
    if (r() < 0.25) pr(x + 1, by - 2, bw - 2, 2, '#8d9ab4');
    for (let wy = by + 3; wy < groundY - 1; wy += 3) {
      for (let wx = x + 1; wx < x + bw - 2; wx += 2) {
        if (r() < 0.4) towerLights.push([wx, wy]);
      }
    }
    x += bw + (r() < 0.3 ? 1 + Math.floor(r() * 3) : 0);
  }

  // 대한민국 도시 외곽의 낮은 산 능선과 도로·녹지
  for (let xx = 0; xx < lw; xx++) {
    const dy = Math.round(groundY - 2 - 3 * Math.sin(xx * 0.035 + 1) - 2 * Math.sin(xx * 0.09));
    pr(xx, dy, 1, groundY - dy + 2, endingType === 'desert' ? '#9b805e' : '#526b62');
    pr(xx, dy, 1, 1, '#82958a');
  }

  // 지면은 한국의 도시 외곽 산업·물류 부지와 녹지로 표현
  const base = endingType === 'desert' ? '#a88b62' : (green ? '#4a6b48' : '#59615f');
  const lite = endingType === 'desert' ? '#c4a174' : (green ? '#6f9a5a' : '#78817c');
  const dk = endingType === 'desert' ? '#806746' : (green ? '#365236' : '#414947');
  pr(0, groundY, lw, groundH, base);
  pr(0, groundY, lw, 1, lite);
  for (let i = 0; i < 170; i++) {
    const sx = Math.floor(r() * lw);
    const sy = groundY + 2 + Math.floor(r() * Math.max(1, groundH - 2));
    pr(sx, sy, r() < 0.4 ? 2 : 1, 1, r() < 0.5 ? lite : dk);
  }
  // 도로와 가로수: 나쁜 엔딩에서는 녹지가 마르고, 좋은 엔딩에서는 녹지가 회복
  const roadY = groundY + Math.round(groundH * 0.62);
  pr(0, roadY, lw, Math.max(3, Math.round(groundH * 0.22)), endingType === 'desert' ? '#78664e' : '#343b42');
  pr(0, roadY, lw, 1, '#9a9b91');
  for (let rx = 5; rx < lw; rx += 18) pr(rx, roadY + 2, 5, 1, '#d9cda4');
  const treeColor = endingType === 'desert' ? '#74654b' : (green ? '#2f6b3a' : '#596f56');
  [0.05, 0.17, 0.39, 0.6, 0.86, 0.95].forEach((tx, idx) => {
    const px = Math.round(lw * tx);
    const py = groundY + 5 + (idx % 2) * 3;
    pr(px, py, 2, 4, '#5b3a22');
    pixDisc(px + 1, py - 1, 4, treeColor);
    pixDisc(px, py - 2, 2, endingType === 'desert' ? '#8b7856' : '#4f9a52');
  });

  // 아직 승인되지 않은 세 사업지는 펜스가 둘러진 빈 부지로 표시
  FACTORIES.forEach((f, idx) => {
    const q = factoryGeom(f);
    const decision = facilityDecisions[idx];
    if (!decision || decision === 'reject') {
      const py = q.bodyY + q.bodyH - 2;
      pr(q.x - 2, py, q.w + 4, 2, '#d4b86d');
      pr(q.x - 2, q.y + 2, 2, py - q.y, '#b9a16a');
      pr(q.x + q.w, q.y + 2, 2, py - q.y, '#b9a16a');
      for (let fx = q.x - 2; fx < q.x + q.w + 2; fx += 5) pr(fx, q.y + 2, 2, 2, '#d4b86d');
    }
  });

  // 승인된 시설만 공장 형태로 건설
  FACTORIES.forEach((f, idx) => {
    const decision = facilityDecisions[idx];
    if (!decision || decision === 'reject') return;
    const q = factoryGeom(f);
    box(q.x, q.bodyY, q.w, q.bodyH, '#3a3f58');
    for (let row = 0, yy = q.bodyY + 1; yy + 3 < q.bodyY + q.bodyH - 1; yy += 4, row++) {
      pr(q.x + 1, yy + 3, q.w - 2, 1, '#2f3347');
      for (let xx = q.x + 1 + (row % 2) * 3; xx < q.x + q.w - 1; xx += 6) pr(xx, yy, 1, 3, '#2f3347');
    }
    pr(q.x + 1, q.bodyY + 1, q.w - 2, 1, '#5a6080');
    pr(q.x + q.w - 2, q.bodyY + 1, 1, q.bodyH - 2, '#2a2e44');
    pr(q.x + Math.round(q.w * 0.45), q.bodyY + q.bodyH - 6, 4, 5, '#1a1c28');
    const cw = Math.max(4, Math.round(q.w * 0.14));
    chimney(q.x + Math.round(q.w * 0.2), q.y, cw, Math.round(q.h * 0.35) + 2);
    chimney(q.x + Math.round(q.w * 0.65), q.y + Math.round(q.h * 0.08), cw, Math.round(q.h * 0.27) + 2);
  });

  // 시간대/날씨 색조
  const tone = CITY_TONE[variant];
  if (tone) {
    g.globalCompositeOperation = 'source-atop';
    g.fillStyle = tone;
    g.fillRect(0, 0, lw, lh);
    g.globalCompositeOperation = 'source-over';
  }

  // 불 켜진 창문 (색조 위에 그려서 밤에 빛나게)
  const dim = (variant === 'night' || variant === 'dusk' || variant === 'rain' || variant === 'dust');
  if (dim) {
    g.globalAlpha = variant === 'night' ? 0.95 : 0.6;
    towerLights.forEach(p => pr(p[0], p[1], 1, 1, '#ffd36b'));
    g.globalAlpha = 1;
  }
  const rf = makeRng(31);
  FACTORIES.forEach((f, idx) => {
    if (!facilityDecisions[idx] || facilityDecisions[idx] === 'reject') return;
    const q = factoryGeom(f);
    for (let wy = q.bodyY + 4; wy < q.bodyY + q.bodyH - 8; wy += 5) {
      for (let wx = q.x + 3; wx < q.x + q.w - 5; wx += 5) {
        const on = rf() < 0.7;
        if (dim && on) {
          g.globalAlpha = 0.3; pr(wx - 1, wy - 1, 5, 4, '#ffb347');
          g.globalAlpha = 1;
          pr(wx, wy, 3, 2, '#ffd36b');
        } else {
          pr(wx, wy, 3, 2, dim ? '#232842' : '#6f80a6');
        }
      }
    }
  });
}

function drawSmoke() {
  const a = Math.min(0.75, weather.so2 / 140);
  const T = Date.now() / 1000;
  FACTORIES.forEach((f, fi) => {
    const decision = facilityDecisions[fi];
    if (!decision || decision === 'reject') return;
    const q = factoryGeom(f);
    const stacks = [[q.x + q.w * 0.27, q.y], [q.x + q.w * 0.72, q.y + q.h * 0.08]];
    stacks.forEach((s, si) => {
      for (let k = 0; k < 5; k++) {
        const prog = (T * 0.3 + k * 0.2 + fi * 0.13 + si * 0.31) % 1;
        const px = s[0] + Math.sin(T * 0.8 + k + fi) * 1.5 + prog * 7;
        const py = s[1] - 2 - prog * lh * 0.13;
        const size = 2 + prog * 6;
        g.globalAlpha = a * (decision === 'conditional' ? 0.28 : 0.75) * (1 - prog);
        pr(px - size / 2, py - size / 2, size, size, '#6a625c');
      }
    });
  });
  g.globalAlpha = 1;
}

// ---------- 날씨 파티클 ----------
const RAIN_DROPS = [];
for (let i = 0; i < 180; i++) RAIN_DROPS.push({ x: Math.random(), y: Math.random(), v: 0.85 + Math.random() * 0.7 });

function drawRain(heavy, acidic) {
  const count = heavy ? 140 : 65;
  const fh = lh * 0.65;
  g.fillStyle = acidic ? 'rgb(180,220,160)' : 'rgb(175,215,255)';
  g.globalAlpha = heavy ? 0.8 : 0.6;
  for (let i = 0; i < count; i++) {
    const d = RAIN_DROPS[i];
    d.y += d.v * (heavy ? 1.7 : 1.1) * frameDt;
    if (d.y > 1) { d.y -= 1; d.x = Math.random(); }
    const x = Math.round(d.x * lw);
    const y = Math.round(d.y * fh);
    g.fillRect(x, y, 1, 2);
    g.fillRect(x - 1, y + 2, 1, 2);
    if (heavy) g.fillRect(x - 2, y + 4, 1, 2);
  }
  g.globalAlpha = 1;
}

function drawParticles(color, speedMult) {
  const sx = lw / width;
  const sy = lh / height;
  g.fillStyle = color;
  particles.forEach(p => {
    p.x += p.speedX * speedMult * 0.3;
    p.y += p.speedY;
    if (p.x > width) p.x = 0;
    if (p.y > height) p.y = 0;
    if (p.y < 0) p.y = height;
    g.globalAlpha = p.alpha;
    const s = p.size > 2.9 ? 2 : 1;
    g.fillRect(Math.floor(p.x * sx), Math.floor(p.y * sy), s, s);
  });
  g.globalAlpha = 1;
}

// ---------- 창틀 + 책상 레이어 ----------
function drawFrameAndDesk() {
  const fh = Math.round(lh * 0.65);
  const frame = '#2a2340';
  const frameHi = '#4a4066';
  const ink = '#100c18';

  // 유리 반사광
  g.globalAlpha = 0.07;
  for (let i = 0; i < 4; i++) {
    const px = Math.round(lw / 4 * i) + 10;
    for (let yy = 4; yy < fh - 6; yy++) pr(px + Math.round(yy * 0.35), yy, 3, 1, '#ffffff');
  }
  g.globalAlpha = 1;

  // 창틀
  pr(0, 0, lw, 4, ink); pr(0, 1, lw, 2, frame); pr(0, 1, lw, 1, frameHi);
  pr(0, 0, 4, fh, ink); pr(1, 0, 2, fh, frame);
  pr(lw - 4, 0, 4, fh, ink); pr(lw - 3, 0, 2, fh, frame);
  pr(0, fh - 3, lw, 3, ink);
  for (let i = 1; i <= 3; i++) {
    const mx = Math.round(lw / 4 * i) - 2;
    pr(mx, 0, 4, fh, ink); pr(mx + 1, 0, 2, fh, frame); pr(mx + 1, 0, 1, fh, frameHi);
  }

  // 원목 책상
  const y0 = Math.round(lh * 0.63);
  const stops = [[0, '#6a4c34'], [0.18, '#4f3827'], [1, '#241911']];
  for (let y = y0; y < lh; y += 3) pr(0, y, lw, 3, colorAt(stops, (y - y0) / Math.max(1, lh - y0)));
  const rd = makeRng(5);
  for (let y = y0 + 9; y < lh; y += 10) {
    pr(0, y, lw, 1, 'rgba(18,10,5,0.5)');
    for (let x = Math.floor(rd() * 40); x < lw; x += 30 + Math.floor(rd() * 40)) pr(x, y - 9, 1, 9, 'rgba(18,10,5,0.38)');
  }
  for (let i = 0; i < 110; i++) {
    const gx = Math.floor(rd() * lw);
    const gy = y0 + 4 + Math.floor(rd() * (lh - y0 - 4));
    pr(gx, gy, 2 + Math.floor(rd() * 6), 1, rd() < 0.5 ? 'rgba(255,230,190,0.08)' : 'rgba(0,0,0,0.14)');
  }
  pr(0, y0, lw, 2, '#1a110b');
  pr(0, y0 + 2, lw, 1, '#8a6a48');
}

// ---------- 책상 위 오브젝트 ----------
function drawDeskObjects() {
  const T = Date.now() / 1000;
  const blink = Math.floor(Date.now() / 400) % 2 === 0;

  DESK_ITEMS.forEach(o => {
    const s = rr(o);
    pr(s.x + 1, s.y + s.h, s.w, 2, 'rgba(0,0,0,0.32)');
  });

  // 1. 현장 조사팀 무전기
  {
    const r = rr(DESK_ITEMS[0]);
    const ax = r.x + Math.round(r.w * 0.21);
    const ah = Math.round(lh * 0.06);
    pr(ax, r.y - ah, 1, ah, '#aab3c5');
    pr(ax - 1, r.y - ah - 1, 3, 2, '#e0505a');
    box(r.x, r.y, r.w, r.h, '#3e4658');
    shade(r.x, r.y, r.w, r.h, '#5f6b88', '#272c3a');
    for (let yy = r.y + Math.round(r.h * 0.42); yy < r.y + r.h - 3; yy += 2) pr(r.x + 3, yy, Math.round(r.w * 0.5), 1, '#171b26');
    const dx = r.x + Math.round(r.w * 0.68);
    const dy = r.y + Math.round(r.h * 0.55);
    pr(dx, dy, 4, 4, '#d4bc8b');
    pr(dx + 1, dy + 1, 2, 2, '#8f7449');
    const lx = r.x + Math.round(r.w * 0.5) - 1;
    const ly = r.y + Math.round(r.h * 0.2);
    if (activeTasks.seedingReady) {
      g.globalAlpha = 0.35; pr(lx - 1, ly - 1, 5, 5, '#52b788'); g.globalAlpha = 1;
    }
    pr(lx, ly, 3, 3, activeTasks.seedingReady ? '#7bf0b0' : '#6c757d');
  }

  // 2. 신문
  {
    const r = rr(DESK_ITEMS[1]);
    box(r.x, r.y, r.w, r.h, '#e6dcc5');
    pr(r.x + 2, r.y + 2, r.w - 4, 2, '#3b332b');
    const colW = Math.floor((r.w - 6) / 2);
    for (let yy = r.y + 6; yy < r.y + r.h - 2; yy += 2) {
      pr(r.x + 2, yy, colW, 1, '#8a806c');
      if (yy > r.y + 11) pr(r.x + 4 + colW, yy, colW, 1, '#8a806c');
    }
    pr(r.x + 4 + colW, r.y + 6, colW, 4, '#a79f8a');
  }

  // 3. 서류 더미
  {
    const r = rr(DESK_ITEMS[2]);
    for (let i = 2; i >= 0; i--) box(r.x + i, r.y - i, r.w, r.h, i === 0 ? '#f7f3e8' : '#dcd3be');
    for (let yy = r.y + 4; yy < r.y + r.h - 8; yy += 3) pr(r.x + 3, yy, r.w - 8, 1, '#9a907a');
    pr(r.x + r.w - 9, r.y + r.h - 9, 6, 6, '#b3262e');
    pr(r.x + r.w - 8, r.y + r.h - 8, 4, 4, '#f7f3e8');
    pr(r.x + r.w - 7, r.y + r.h - 7, 2, 2, '#b3262e');
  }

  // 4. 노트북
  {
    const r = rr(DESK_ITEMS[3]);
    const sh = Math.round(r.h * 0.68);
    const ins = Math.max(1, Math.round(lw * 0.01));
    box(r.x, r.y, r.w, sh, '#252934');
    const scH = Math.max(4, Math.round(r.h * 0.52));
    const sx = r.x + ins;
    const sy = r.y + 2;
    const sw = r.w - 2 * ins;
    pr(sx, sy, sw, scH, '#3b5266');
    pr(sx, sy, sw, 2, '#4f7a9c');
    pr(sx + 2, sy + 4, Math.round(sw * 0.4), 1, '#a8dadc');
    pr(sx + 2, sy + 7, Math.round(sw * 0.3), 1, '#7fb3c9');
    for (let k = 0; k < 4; k++) {
      const bh = 3 + ((k * 5 + 2) % 7);
      pr(sx + sw - 4 - k * 4, sy + scH - 2 - bh, 3, bh, k % 2 ? '#52b788' : '#e3c891');
    }
    if (blink) pr(sx + 2, sy + 10, 2, 1, '#ffffff');
    const by = r.y + sh;
    const bh2 = r.h - sh;
    box(r.x - ins, by, r.w + 2 * ins, bh2, '#3a3f4d');
    for (let yy = by + 2; yy < by + bh2 - 2; yy += 2) {
      for (let xx = r.x + 2; xx < r.x + r.w - 2; xx += 3) pr(xx, yy, 2, 1, '#5a6075');
    }
  }

  // 5. 대기질·소음 측정장비 점검 단말기
  {
    const r = rr(DESK_ITEMS[4]);
    box(r.x, r.y, r.w, r.h, '#1e222b');
    const scH = Math.max(3, Math.round(r.h * 0.55));
    const dirtyBlink = activeTasks.sensorDirty && blink;
    pr(r.x + 2, r.y + 2, r.w - 4, scH, dirtyBlink ? '#e09f3e' : '#2b9348');
    const wc = dirtyBlink ? '#7a4a10' : '#9ff0b4';
    for (let k = 0; k < r.w - 6; k++) {
      pr(r.x + 3 + k, r.y + 2 + Math.round(scH / 2 + Math.sin(k * 0.9 + T * 3) * (scH * 0.25)), 1, 1, wc);
    }
    if (activeTasks.sensorDirty) {
      for (let k = 0; k < 7; k++) pr(r.x + 3 + ((k * 5) % Math.max(1, r.w - 6)), r.y + 3 + ((k * 3) % scH), 1, 1, '#d8b982');
    }
    const by = r.y + r.h - 5;
    pr(r.x + 3, by, 3, 2, '#c0392b');
    pr(r.x + Math.min(8, r.w - 5), by, 3, 2, '#e0b13e');
    pr(r.x + Math.min(13, r.w - 4), by, 2, 2, '#4a90d9');
  }

  // 6. 환경영향 예측 도면 (접힌 설계·입지 검토도)
  {
    const r = rr(DESK_ITEMS[5]);
    box(r.x, r.y, r.w, r.h, '#e9e2c9');
    pr(r.x + 2, r.y + 2, r.w - 4, r.h - 4, '#f6efd8');
    const ix = r.x + 3, iy = r.y + 3, iw = r.w - 6, ih = r.h - 6;
    // 도로, 하천, 주거지, 개발 예정지를 나타내는 도면 기호
    pline(ix, iy + Math.round(ih * 0.72), ix + Math.round(iw * 0.35), iy + Math.round(ih * 0.48), '#4b9bc4');
    pline(ix + Math.round(iw * 0.35), iy + Math.round(ih * 0.48), ix + Math.round(iw * 0.78), iy + Math.round(ih * 0.62), '#4b9bc4');
    pline(ix + 1, iy + Math.round(ih * 0.22), ix + iw - 1, iy + Math.round(ih * 0.22), '#626b78');
    pr(ix + Math.round(iw * 0.08), iy + Math.round(ih * 0.08), Math.max(2, Math.round(iw * 0.22)), Math.max(2, Math.round(ih * 0.22)), '#8cad75');
    pr(ix + Math.round(iw * 0.62), iy + Math.round(ih * 0.08), Math.max(2, Math.round(iw * 0.28)), Math.max(2, Math.round(ih * 0.28)), '#b7a58b');
    pr(ix + Math.round(iw * 0.42), iy + Math.round(ih * 0.42), Math.max(3, Math.round(iw * 0.24)), Math.max(3, Math.round(ih * 0.3)), '#c85a52');
    pline(ix + Math.round(iw * 0.42), iy + 1, ix + Math.round(iw * 0.42), iy + ih - 1, '#b94b4b');
  }

  // 7. 개발사업 대상지 생태·토지이용 지도
  {
    const r = rr(DESK_ITEMS[6]);
    box(r.x, r.y, r.w, r.h, '#d8d0a8');
    pr(r.x + 2, r.y + 2, r.w - 4, r.h - 4, '#e6dfbf');
    const ix = r.x + 3;
    const iy = r.y + 3;
    const iw = r.w - 6;
    const ih = r.h - 6;
    // 하천과 녹지, 개발 예정 구역을 나타내는 간단한 지도
    pline(ix, iy + Math.round(ih * 0.7), ix + Math.round(iw * 0.35), iy + Math.round(ih * 0.48), '#4b9bc4');
    pline(ix + Math.round(iw * 0.35), iy + Math.round(ih * 0.48), ix + Math.round(iw * 0.7), iy + Math.round(ih * 0.62), '#4b9bc4');
    pr(ix + 1, iy + 1, Math.max(2, Math.round(iw * 0.28)), Math.max(2, Math.round(ih * 0.3)), '#8cad75');
    pr(ix + Math.round(iw * 0.58), iy + 1, Math.max(2, Math.round(iw * 0.32)), Math.max(2, Math.round(ih * 0.36)), '#9ab77b');
    pline(ix + Math.round(iw * 0.45), iy + 1, ix + Math.round(iw * 0.45), iy + ih - 1, '#b94b4b');
    pline(ix + Math.round(iw * 0.45), iy + Math.round(ih * 0.5), ix + iw - 1, iy + Math.round(ih * 0.5), '#b94b4b');
    pr(ix + Math.round(iw * 0.42), iy + Math.round(ih * 0.42), 3, 3, '#b3262e');
  }

  // 8. 펜꽂이
  {
    const r = rr(DESK_ITEMS[7]);
    ['#c94a4a', '#3b6ea5', '#e3b23c'].forEach((col, idx) => {
      const x0 = r.x + r.w * (0.25 + idx * 0.25);
      const y0 = r.y + r.h * 0.4;
      const x1 = r.x + r.w * (0.15 + idx * 0.3);
      const y1 = r.y - 4;
      pline(x0, y0, x1, y1, col);
      pline(x0 + 1, y0, x1 + 1, y1, col);
      pr(x1, y1 - 1, 2, 1, '#f5efe2');
    });
    const cy = r.y + Math.round(r.h * 0.35);
    box(r.x, cy, r.w, r.h - Math.round(r.h * 0.35), '#4a4e59');
    shade(r.x, cy, r.w, r.h - Math.round(r.h * 0.35), '#6a6f7d', '#33363f');
    pr(r.x + 2, cy + 3, r.w - 4, 1, '#2f323b');
  }

  // 9. 환경평가원 직통 전화기
  {
    const r = rr(DESK_ITEMS[8]);
    const ringing = activeTasks.phoneRinging;
    const sx = (ringing && blink) ? 1 : 0;
    box(r.x + sx, r.y, r.w, r.h, ringing ? '#b3262e' : '#2b2d42');
    shade(r.x + sx, r.y, r.w, r.h, ringing ? '#e0605e' : '#4a4d6e', ringing ? '#7a1a20' : '#1b1c2e');
    pr(r.x + sx + 1, r.y + 1, r.w - 2, 3, '#14131f');
    pr(r.x + sx, r.y + 1, 2, 4, '#14131f');
    pr(r.x + sx + r.w - 2, r.y + 1, 2, 4, '#14131f');
    for (let j = 0; j < 3; j++) {
      for (let i = 0; i < 3; i++) pr(r.x + sx + 3 + i * 3, r.y + 6 + j * 3, 2, 2, '#c9c2b0');
    }
    if (ringing) {
      g.globalAlpha = blink ? 0.95 : 0.5;
      pr(r.x + sx - 3, r.y - 2, 2, 1, '#ffd166');
      pr(r.x + sx - 5, r.y - 4, 2, 1, '#ffd166');
      pr(r.x + r.w + sx + 1, r.y - 2, 2, 1, '#ffd166');
      pr(r.x + r.w + sx + 3, r.y - 4, 2, 1, '#ffd166');
      g.globalAlpha = 1;
    }
  }

  // 10. 환경조사 일정 캘린더 (날짜 글자는 present 단계에서 선명하게 덧그림)
  {
    const r = rr(DESK_ITEMS[9]);
    box(r.x, r.y, r.w, r.h, '#f5efe2');
    pr(r.x + 1, r.y + 1, r.w - 2, Math.round(r.h * 0.28), '#b3262e');
    pr(r.x + 3, r.y - 1, 2, 3, '#2a2430');
    pr(r.x + r.w - 5, r.y - 1, 2, 3, '#2a2430');
    pr(r.x + 3, r.y + r.h - 4, r.w - 6, 1, '#cfc7b4');
  }

  // 11~13. 새 조작형 미니게임 오브젝트
  {
    const r=rr(DESK_ITEMS[10]); box(r.x,r.y,r.w,r.h,'#315d43'); shade(r.x,r.y,r.w,r.h,'#6c9a65','#203b31');
    pr(r.x+3,r.y+3,r.w-6,2,'#c4d7a1'); pr(r.x+Math.floor(r.w*.25),r.y+Math.floor(r.h*.35),3,4,'#7ecb75');
    pr(r.x+Math.floor(r.w*.55),r.y+Math.floor(r.h*.3),3,5,'#a9d18e'); pr(r.x+Math.floor(r.w*.72),r.y+Math.floor(r.h*.55),3,3,'#f0d77a');
  }
  {
    const r=rr(DESK_ITEMS[11]); box(r.x,r.y,r.w,r.h,'#343d4d'); shade(r.x,r.y,r.w,r.h,'#687c91','#202735');
    pr(r.x+3,r.y+3,r.w-6,r.h-6,'#172b3c');
    for(let k=0;k<5;k++) pline(r.x+4,r.y+Math.floor(r.h*(.25+k*.12)),r.x+r.w-4,r.y+Math.floor(r.h*(.25+k*.12)),k===2?'#e5a14a':'#587a91');
    pr(r.x+Math.floor(r.w*.48),r.y+Math.floor(r.h*.25),3,3,'#f3c969');
  }
  {
    const r=rr(DESK_ITEMS[12]); box(r.x,r.y,r.w,r.h,'#6d5940'); shade(r.x,r.y,r.w,r.h,'#a58b62','#3b3028');
    pr(r.x+3,r.y+3,r.w-6,r.h-6,'#d7c9a5');
    pr(r.x+Math.floor(r.w*.2),r.y+Math.floor(r.h*.25),Math.max(3,Math.floor(r.w*.22)),Math.max(3,Math.floor(r.h*.25)),'#579b69');
    pr(r.x+Math.floor(r.w*.58),r.y+Math.floor(r.h*.48),Math.max(3,Math.floor(r.w*.22)),Math.max(3,Math.floor(r.h*.25)),'#579b69');
  }
  {
    const r=rr(DESK_ITEMS[13]); box(r.x,r.y,r.w,r.h,'#344d63'); shade(r.x,r.y,r.w,r.h,'#7895a7','#1e2b3c');
    pr(r.x+3,r.y+3,r.w-6,r.h-6,'#dce6df');
    pline(r.x+Math.floor(r.w*.25),r.y+Math.floor(r.h*.5),r.x+Math.floor(r.w*.75),r.y+Math.floor(r.h*.5),'#4b9bc4');
    pr(r.x+Math.floor(r.w*.48),r.y+Math.floor(r.h*.3),3,3,'#d96b55');
  }
}

// ---------- 화면 출력 ----------
function presentBuffer(withText) {
  ctx.imageSmoothingEnabled = false;
  ctx.drawImage(pcan, 0, 0, lw, lh, 0, 0, width, height);

  // 달빛 같은 은은한 비네팅
  const vg = ctx.createRadialGradient(width / 2, height * 0.5, Math.min(width, height) * 0.35, width / 2, height * 0.5, Math.max(width, height) * 0.75);
  vg.addColorStop(0, 'rgba(5,8,28,0)');
  vg.addColorStop(1, 'rgba(5,8,28,0.38)');
  ctx.fillStyle = vg;
  ctx.fillRect(0, 0, width, height);

  if (withText) {
    const cal = DESK_ITEMS[9];
    ctx.fillStyle = '#1c1815';
    ctx.font = 'bold 14px Gowun Batang';
    ctx.fillText(`${day}일`, width * (cal.relX + 0.015), height * (cal.relY + 0.075));
  }
}

// ---------- 장면 ----------
function drawTitleSky() {
  pixelBands(0, lh, [[0, '#0a0d2a'], [0.38, '#222a6b'], [0.62, '#526b86'], [0.8, '#b7a18a'], [1, '#e5c9a6']], 3);
  drawMoon(Math.round(lw * 0.5), Math.round(lh * 0.36), Math.round(Math.min(lw, lh) * 0.15));
}

function titleDuneY(t) {
  return Math.round(lh * (0.79 + 0.025 * Math.sin(t * 5.2 + 0.6) + 0.012 * Math.sin(t * 11 + 1)));
}

function drawTitleCity() {
  const r = makeRng(23);
  const baseY = Math.round(lh * 0.79);
  // 한국의 도심 외곽을 떠올리게 하는 아파트·업무시설 실루엣
  const list = [
    { x: 0.12, w: 0.045, h: 0.24 }, { x: 0.19, w: 0.055, h: 0.34 }, { x: 0.27, w: 0.04, h: 0.2 },
    { x: 0.34, w: 0.06, h: 0.42 }, { x: 0.43, w: 0.045, h: 0.28 }, { x: 0.5, w: 0.06, h: 0.46 },
    { x: 0.59, w: 0.055, h: 0.32 }, { x: 0.67, w: 0.045, h: 0.25 }, { x: 0.75, w: 0.055, h: 0.38 },
    { x: 0.84, w: 0.04, h: 0.22 }
  ];
  // 뒤쪽 산 능선
  for (let x = 0; x < lw; x++) {
    const y = Math.round(lh * (0.69 + 0.035 * Math.sin(x / lw * 8 + 0.4) + 0.025 * Math.sin(x / lw * 17)));
    pr(x, y, 1, lh - y, '#171c3c');
    pr(x, y, 1, 1, '#3a456e');
  }
  list.forEach(b => {
    const bx = Math.round(lw * b.x), bw = Math.max(6, Math.round(lw * b.w));
    const bh = Math.round(lh * b.h), by = baseY - bh;
    pr(bx, by, bw, bh + 14, '#0e1230'); pr(bx + bw - 1, by, 1, bh + 14, '#2a3170');
    pr(bx, by, bw, 1, '#2a3170');
    for (let wy = by + 4; wy < baseY - 2; wy += 4) for (let wx = bx + 2; wx < bx + bw - 2; wx += 3) if (r() < 0.32) pr(wx, wy, 1, 2, r() < 0.8 ? '#f3c76a' : '#6ad0c8');
    // 아파트 옥상 구조물
    if (b.h > 0.3) { pr(bx + 2, by - 2, bw - 4, 2, '#0e1230'); pr(bx + Math.floor(bw / 2), by - 5, 1, 3, '#0e1230'); }
  });
  // 도심 앞쪽 가로수
  [0.07, 0.91].forEach(tx => {
    const cx = Math.round(lw * tx), cy = baseY - 2;
    pr(cx, cy - 10, 2, 10, '#0d0814');
    pixDisc(cx, cy - 12, 5, '#183b35');
    pixDisc(cx - 2, cy - 10, 3, '#245346');
  });
}

function drawTitleBackground() {
  beginFrame();
  const k = lw + 'x' + lh;
  cachedLayer('titleSky', k, drawTitleSky);
  const mr = Math.round(Math.min(lw, lh) * 0.15);
  drawStars(lh * 0.62, 1, { x: Math.round(lw * 0.5), y: Math.round(lh * 0.36), r: mr + 9 });
  cachedLayer('titleCity', k, drawTitleCity);
  drawParticles('#e6c288', 6);
  presentBuffer(false);
}

function drawOfficeScene() {
  beginFrame();
  const T = Date.now() / 1000;
  const variant = skyVariant();
  const clockMinutes = gameMinutes % (24 * 60);
  const dayProgress = Math.max(0, Math.min(1, (clockMinutes - 7 * 60) / (12 * 60)));
  const greenFlag = endingType === 'green' || (endingType === null && pollutionRisk < 45);
  const size = lw + 'x' + lh;

  cachedLayer('sky', variant + '|' + size, () => pixelBands(0, Math.round(lh * 0.68), SKY_STOPS[variant], 3));
  drawCelestial(variant, dayProgress, T);
  const facilityKey = facilityDecisions.map(v => v || '-').join('|');
  cachedLayer('city', variant + '|' + greenFlag + '|' + endingType + '|' + facilityKey + '|' + size, () => drawCityLayer(variant, greenFlag));
  drawSmoke();

  if (weather.type === 'FINE_DUST' || endingType === 'desert') {
    drawParticles(endingType === 'desert' ? 'rgba(174, 139, 91, 0.55)' : 'rgba(165, 170, 174, 0.55)', 8);
  } else if (endingType === 'partial') {
    drawParticles('rgba(145, 150, 155, 0.24)', 4);
  } else if (weather.type === 'RAIN' || weather.type === 'HEAVY_RAIN') {
    drawRain(weather.type === 'HEAVY_RAIN', false);
  }

  cachedLayer('frame', size, drawFrameAndDesk);
  drawDeskObjects();
  presentBuffer(true);
}

// --- 마우스 호버 & 클릭 ---
canvas.addEventListener('mousemove', (e) => {
  if (scene !== 'OFFICE' || isPaused) {
    document.getElementById('hover-tooltip').style.display = 'none';
    canvas.style.cursor = 'default';
    return;
  }
  const mx = e.clientX;
  const my = e.clientY;
  let hovered = null;

  [...DESK_ITEMS, ...FACTORIES].forEach(obj => {
    const ox = width * obj.relX;
    const oy = height * obj.relY;
    const ow = width * obj.relW;
    const oh = height * obj.relH;
    if (mx >= ox && mx <= ox + ow && my >= oy && my <= oy + oh) hovered = obj;
  });

  const tooltip = document.getElementById('hover-tooltip');
  if (hovered) {
    canvas.style.cursor = 'pointer';
    tooltip.style.display = 'block';
    tooltip.style.left = `${mx}px`;
    tooltip.style.top = `${my}px`;
    tooltip.innerText = hovered.name;
  } else {
    canvas.style.cursor = 'default';
    tooltip.style.display = 'none';
  }
});

canvas.addEventListener('click', (e) => {
  if (scene !== 'OFFICE' || isPaused) return;
  const mx = e.clientX;
  const my = e.clientY;

  for (const obj of [...DESK_ITEMS, ...FACTORIES]) {
    const ox = width * obj.relX;
    const oy = height * obj.relY;
    const ow = width * obj.relW;
    const oh = height * obj.relH;
    if (mx >= ox && mx <= ox + ow && my >= oy && my <= oy + oh) {
      handleObjectClick(obj.id);
      break;
    }
  }
});

// --- 메인 게임 루프 ---
function gameLoop(timestamp) {
  if (!lastTimestamp) lastTimestamp = timestamp;
  const deltaSec = (timestamp - lastTimestamp) / 1000;
  lastTimestamp = timestamp;

  ctx.clearRect(0, 0, width, height);

  if (scene === 'TITLE' || scene === 'ZOOMING') {
    drawTitleBackground();
  } else if (scene === 'OFFICE' || scene === 'ENDING') {
    drawOfficeScene();

    if (scene === 'OFFICE' && !isPaused) {
      // 1배속에서 게임 속 60분이 현실 시간 5초가 되도록 분당 12게임분 진행
      gameMinutes += deltaSec * 12 * timeMultiplier;

      // 07:00부터 24시간이 지나 다음 날 07:00이 되면 하루 결산
      if (gameMinutes >= (7 * 60) + (24 * 60)) {
        advanceGameDay();
      }

      const clockMinutes = gameMinutes % (24 * 60);
      const hrs = Math.floor(clockMinutes / 60);
      const mins = Math.floor(clockMinutes % 60);
      document.getElementById('clock-day-text').innerText = `${day}/${TOTAL_GAME_DAYS}일차`;
      document.getElementById('clock-time-text').innerText = `${String(hrs).padStart(2, '0')}시 ${String(mins).padStart(2, '0')}분`;
    }
  }

  requestAnimationFrame(gameLoop);
}

requestAnimationFrame(gameLoop);
</script>
</body>
</html>
"""

components.html(game_html, height=900, scrolling=False)
