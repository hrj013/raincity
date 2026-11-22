import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Rain City",
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
<title>Rain City</title>
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
    <div class="title-logo">RAIN CITY</div>
    <div class="title-sub">기후 위기로 사막화된 땅에 다시 생명의 숨결을</div>
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
let previousCo2Emission = 420;

// 기후 위기로 사막화가 진행된 사막 도시의 환경 및 시뮬레이션 지표
let budget = 250;
let droughtLevel = 68; // 목표: 30% 미만
let totalRainDays = 0;
let acidRainDays = 0;

let weather = {
  type: 'CLEAR',
  cloudType: 'WARM', // 'WARM'(고온·대기 정체) or 'COLD'(저온·대기 확산)
  windDir: '북서풍',
  windSpeed: 3.2,
  humidity: 32,
  temp: 36,
  rainProb: 15,
  so2: 75,
  nox: 65,
  pm25: 80,
  ph: 4.6,
  ecoHealth: 45,
  co2: 420 // 사막 도시의 추정 온실가스 배출량 (tCO₂e/일)
};

// 실시간 현장 액션 상태 (환경영향평가원 업무)
let activeTasks = {
  seedingReady: true,      // 기후적응 사업 검토 가능 여부 (하루 1회)
  phAlert: false,          // 수질오염 저감대책 검토 필요 여부
  sensorDirty: false,      // 황사 등으로 대기질 센서 오염 여부
  phoneRinging: false,     // 주민 의견·관계기관 협의 요청 수신 여부
  currentAudit: null
};

// 정책 데이터 (선택 후 2일 뒤에 적용)
const POLICIES = [
  { id: 'fgd', name: '저탄소 에너지 전환 계획', cost: 45, desc: '화석연료 의존도를 낮추고 재생에너지와 고효율 에너지원을 도입하도록 권고해 온실가스와 대기오염 배출을 줄입니다.', status: 'READY', applyDay: null },
  { id: 'esp', name: '산업시설 에너지 효율 개선', cost: 40, desc: '노후 설비의 에너지 손실을 줄이고 고효율 장비로 교체하도록 제안해 미세먼지와 탄소배출량을 함께 낮춥니다.', status: 'READY', applyDay: null },
  { id: 'sensor', name: '온실가스·대기질 통합 측정망', cost: 25, desc: 'CO₂, SO₂, NOₓ, PM2.5 등을 지속적으로 측정해 배출 현황과 환경영향평가 예측의 정확도를 높입니다.', status: 'READY', applyDay: null },
  { id: 'raingarden', name: '사막 오아시스·토착식생 복원', cost: 30, desc: '오아시스 주변의 토착 식생과 생태 완충 구역을 복원해 토양 유실을 줄이고 사막 생태계의 회복력을 높입니다.', status: 'READY', applyDay: null },
  { id: 'permeable', name: '빗물 침투·토양 수분 보전 사업', cost: 35, desc: '빗물이 땅속으로 스며들 수 있도록 토양과 지표를 개선하고 증발 손실을 줄여 지하수 함양과 토양 수분 보전을 돕습니다.', status: 'READY', applyDay: null },
  { id: 'reservoir', name: '우수 저장·중수 재이용 시설', cost: 50, desc: '드물게 내리는 비와 생활하수를 안전하게 저장·처리해 농업과 생활용수로 재이용하고 물 부족에 대비합니다.', status: 'READY', applyDay: null },
  { id: 'seeding', name: '인공 강우 및 수자원 확보 타당성 조사', cost: 55, desc: '구름과 습도 등 기상 조건을 확인해 인공 강우의 가능성과 한계를 평가하고, 강수에 따른 수질·생태계 영향까지 검토합니다. 인공 강우는 온실가스 감축을 대신하지 않는 보조적 적응 수단입니다.', status: 'READY', applyDay: null }
];

// 창밖 3개 공장
const FACTORIES = [
  { id: 'factory1', name: '제1 화력·담수화 복합발전소', role: '사막 도시의 전력과 담수를 공급하는 시설입니다. 연료 사용량, 에너지 효율, 온배수와 염수 배출이 주변 사막 생태계와 해안 환경에 미치는 영향을 조사해야 합니다.', pollutants: '이산화탄소(CO₂), 아황산가스(SO₂), 질소산화물(NOₓ), 온배수', relX: 0.22, relY: 0.42, relW: 0.13, relH: 0.16 },
  { id: 'factory2', name: '제2 광물·자원 가공 플랜트', role: '사막 지역의 광물 자원을 가공하는 산업시설입니다. 에너지 사용량과 온실가스·분진 배출, 지하수 사용량, 주변 토양과 주거지역에 미치는 영향을 평가해야 합니다.', pollutants: '이산화탄소(CO₂), 휘발성유기화합물(VOCs), 아황산가스(SO₂), 초미세먼지(PM2.5)', relX: 0.44, relY: 0.43, relW: 0.14, relH: 0.15 },
  { id: 'factory3', name: '제3 시멘트·건설자재 공장', role: '사막 도시의 기반 시설을 건설하는 자재 생산 시설입니다. 공정 에너지 사용과 분진, 운송 과정의 온실가스 배출이 사막 토양과 주변 생태계에 미치는 영향을 검토해야 합니다.', pollutants: '이산화탄소(CO₂), 미세먼지(PM10/PM2.5), 질소산화물(NOₓ), 중금속 분진', relX: 0.68, relY: 0.41, relW: 0.13, relH: 0.17 }
];

// 책상 위 오브젝트 (환경영향평가 현장 조사·분석 장비)
const DESK_ITEMS = [
  { id: 'radio', name: '📻 현장 조사팀 무전기', relX: 0.04, relY: 0.65, relW: 0.07, relH: 0.13 },
  { id: 'newspaper', name: '📰 개발사업 환경영향평가 공고', relX: 0.13, relY: 0.74, relW: 0.14, relH: 0.12 },
  { id: 'documents', name: '📁 환경영향평가 보고서 및 조사 체크리스트', relX: 0.29, relY: 0.70, relW: 0.13, relH: 0.14 },
  { id: 'laptop', name: '💻 환경 데이터 분석 노트북', relX: 0.44, relY: 0.64, relW: 0.16, relH: 0.17 },
  { id: 'sensor_pad', name: '📡 수질·대기 측정장비 점검 단말기', relX: 0.62, relY: 0.67, relW: 0.08, relH: 0.12 },
  { id: 'beaker', name: '🧪 오아시스·지하수 수질 시료 분석 세트', relX: 0.72, relY: 0.66, relW: 0.07, relH: 0.14 },
  { id: 'photo', name: '🗺️ 개발사업 대상지 생태·토지이용 지도', relX: 0.80, relY: 0.73, relW: 0.06, relH: 0.10 },
  { id: 'penholder', name: '✏️ 현장 조사 기록용 필기구', relX: 0.87, relY: 0.72, relW: 0.04, relH: 0.10 },
  { id: 'phone', name: '☎️ 주민 의견·관계기관 협의 전화기', relX: 0.85, relY: 0.61, relW: 0.07, relH: 0.09 },
  { id: 'calendar', name: '📅 환경조사 및 평가 일정 캘린더', relX: 0.92, relY: 0.71, relW: 0.06, relH: 0.11 }
];

// 긴급 환경 감사/민원 시나리오 풀
const AUDIT_SCENARIOS = [
  {
    title: "신규 산업단지의 온실가스 배출량 검토 요청",
    desc: "산업단지 개발계획서가 접수되었습니다. 사업자는 고용 창출 효과를 강조하지만, 에너지 사용량과 온실가스 배출량 예측이 충분하지 않습니다. 환경평가원으로서 어떤 의견을 제시할까요?",
    choices: [
      { text: "배출량 산정 자료를 보완하도록 하고 저탄소 에너지 대안을 제시한다 (예산 -5억, CO₂ 감축 권고)", effect: () => { budget = Math.max(0, budget - 5); weather.co2 = Math.max(250, weather.co2 - 18); return "배출량 산정 근거와 저탄소 에너지 대안을 보완 의견으로 제출했습니다."; } },
      { text: "기존 자료만으로 평가를 마무리한다 (추가 조치 없음)", effect: () => { return "검토는 마무리했지만 배출량 예측의 불확실성이 남았습니다."; } }
    ]
  },
  {
    title: "도시개발 예정지의 습지 훼손 우려",
    desc: "신도시 도로가 철새와 양서류가 서식하는 습지를 통과할 예정입니다. 습지는 탄소를 저장하고 홍수를 완화하는 기능도 있습니다. 어떤 대안을 제시할까요?",
    choices: [
      { text: "도로 노선을 조정하고 핵심 습지와 생태 연결축을 보전한다 (예산 -8억, 생태 건강도 상승)", effect: () => { budget = Math.max(0, budget - 8); weather.ecoHealth = Math.min(100, weather.ecoHealth + 12); return "습지 핵심 구역을 보전하도록 노선 조정 의견을 제출했습니다. 생태계와 탄소흡수 기능을 지키는 데 도움이 될 거야."; } },
      { text: "훼손을 허용하고 공사 이후 대체 녹지만 조성하도록 권고한다 (생태 건강도 소폭 하락)", effect: () => { weather.ecoHealth = Math.max(10, weather.ecoHealth - 5); return "대체 녹지 조성을 권고했지만 기존 습지의 기능을 완전히 대신하기는 어려워."; } }
    ]
  },
  {
    title: "집중호우 때 침수 위험이 커진다는 주민 의견",
    desc: "주민들이 사막 도시의 포장 면적이 넓어지면 드문 강우 때 빗물이 땅속으로 스며들지 못하고 유실될 수 있다고 주민들이 의견을 보내왔습니다. 환경평가원으로서 어떤 대책을 검토할까요?",
    choices: [
      { text: "빗물저류시설과 투수성 포장, 자연 배수 공간을 계획에 반영하도록 한다 (예산 -7억, 가뭄·침수 대응 개선)", effect: () => { budget = Math.max(0, budget - 7); droughtLevel = Math.max(5, droughtLevel - 5); return "주민 의견을 반영해 물순환 개선 대책을 개발계획에 포함하도록 권고했습니다."; } },
      { text: "공사 이후 침수 민원이 발생하면 대책을 마련하도록 한다 (개선 효과 제한)", effect: () => { return "사후 대응만으로는 집중호우에 따른 피해를 충분히 예방하기 어려울 수 있어."; } }
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
    showDialogue('나', '기후 위기로 평균 기온이 오르고 폭염과 장기 가뭄이 반복되면서 이 지역의 초원이 빠르게 사라졌어. 토양은 메말라 모래바람이 잦아졌고, 오아시스와 지하수도 줄어들고 있지. 앞으로 15일 동안 환경평가원으로서 사막화의 원인과 개발사업의 영향을 조사하고, 온실가스 감축·토양과 생태계 복원·물 절약 대책을 평가해야 해. 인공 강우도 기상 조건과 환경 영향을 따져 신중하게 검토해야 해.');
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
    alerts.push(`<div class="alert-pill" onclick="handleObjectClick('beaker')">🧪 경고: 수질 시료 산성화 확인 필요! [수질 분석 세트] 클릭</div>`);
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

function getChecklistStatus() {
  const acidFreq = totalRainDays === 0 ? 12.0 : (acidRainDays / Math.max(1, day)) * 100;
  return {
    check1: weather.co2 < 350,
    check2: droughtLevel < 30,
    acidFreq: acidFreq.toFixed(1)
  };
}

// --- 오브젝트 클릭 핸들러 ---
function handleObjectClick(id) {
  if (id === 'newspaper') {
    recordDailyTask('사막 지역 개발사업 공고 확인', '기후 위기로 취약해진 사막 지역의 개발사업 환경영향평가 공고와 사업 개요를 확인했습니다.');
    openModal(`
      <div class="modal-header">
        <span class="modal-title">📰 개발사업 환경영향평가 공고</span>
        <button class="close-btn" onclick="closeModal()">닫기</button>
      </div>
      <div class="newspaper-sheet">
        <div class="news-head">
          <div style="font-size:0.85rem; letter-spacing:0.2em;">THE RAIN CITY CHRONICLE</div>
          <h2 style="font-size:1.55rem; margin-top:4px;">"사막이 된 땅에 다시 지속 가능한 미래를"</h2>
        </div>
        <p style="line-height:1.8; font-size:1.05rem;">
          기후 위기로 폭염과 가뭄이 심해지면서 한때 초원이던 지역은 사막으로 변해가고 있다. 줄어드는 지하수와 오아시스, 잦아진 모래폭풍으로 주민들의 삶과 생태계가 위협받는 가운데, 새로운 산업·관광 개발 계획까지 발표되었다. 환경영향평가팀은 기후 위기와 개발이 사막화에 미치는 영향을 조사하고 지속 가능한 대책을 마련하기로 했다.
        </p>
      </div>
    `);
    setTimeout(() => {
      document.getElementById('dialogue-speaker').innerText = '나';
      document.getElementById('dialogue-text').innerText = '기후 위기로 사막화가 진행된 원인을 살피고, 개발이 물과 토양, 생태계에 미칠 영향을 평가해야 해. 인공 강우만으로 문제를 해결할 수는 없어. 온실가스 감축과 물 관리, 토착 생태계 복원을 함께 검토하자.';
      document.getElementById('dialogue-box').style.display = 'block';
    }, 250);
  }
  else if (id === 'documents') {
    recordDailyTask('환경영향평가 보고서 검토', '조사 결과와 환경보전 목표 달성 현황을 확인했습니다.');
    const status = getChecklistStatus();
    openModal(`
      <div class="modal-header">
        <span class="modal-title">📁 환경영향평가 보고서 및 조사 체크리스트</span>
        <button class="close-btn" onclick="closeModal()">닫기</button>
      </div>
      <div class="dossier-box">
        <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:2px solid #8c7a5b; padding-bottom:12px; margin-bottom:16px;">
          <span style="font-size:1.15rem; font-weight:700;">💰 가용 사막 환경 복원 예산</span>
          <span style="font-size:1.5rem; font-weight:800; color:#1b4332;">${budget} 억 디르함</span>
        </div>
        <h3 style="margin-bottom:10px; color:#3d3122;">📋 사막 지역 환경관리 목표 (실시간 갱신)</h3>
        <div class="check-item">
          <span>1. 지역 온실가스 추정 배출량이 350tCO₂e/일 미만인가? (현재: ${weather.co2.toFixed(0)}tCO₂e/일)</span>
          <span style="font-size:1.25rem;">${status.check1 ? '✅ 달성' : '⬜ 미달성'}</span>
        </div>
        <div class="check-item">
          <span>2. 사막 지역의 사막 지역 물 부족 위험 지수가 30% 미만인가? (현재: ${droughtLevel.toFixed(1)}%)</span>
          <span style="font-size:1.25rem;">${status.check2 ? '✅ 달성' : '⬜ 미달성'}</span>
        </div>
      </div>
    `);
  }
  else if (id === 'laptop') {
    renderLaptopModal();
  }
  else if (id === 'radio') {
    openSeedingMinigame();
  }
  else if (id === 'beaker') {
    openPhNeutralizeMinigame();
  }
  else if (id === 'sensor_pad') {
    openSensorRepairMinigame();
  }
  else if (id === 'phone') {
    openAuditPhoneModal();
  }
  else if (id === 'photo') {
    recordDailyTask('개발 대상지 지도 검토', '토지이용 현황과 생태적으로 민감한 구역을 지도에서 확인했습니다.');
    showDialogue('나', '사막 지역 조사 지도야. 오아시스와 지하수 이용 지역, 토착 식생이 남아 있는 곳, 모래폭풍 취약 지역을 확인하고 개발 구역과 겹치는지 살펴봐야 해.');
  }
  else if (id === 'penholder') {
    showDialogue('나', '현장 조사 기록을 정리할 필기구들이야. 측정값뿐 아니라 조사 시간과 장소, 날씨 같은 조건도 정확하게 기록해야 해.');
  }
  else if (id === 'calendar') {
    showDialogue('나', `오늘은 전체 15일 중 ${day}일차야. 최종 환경평가 보고서 제출까지 ${TOTAL_GAME_DAYS - day}일 남았어.`);
  }
  else if (id.startsWith('factory')) {
    const f = FACTORIES.find(item => item.id === id);
    recordDailyTask('사업장 배출원 현장 조사', `${f.name}의 주요 배출원과 주변 환경 영향을 확인했습니다.`);
    openModal(`
      <div class="modal-header">
        <span class="modal-title">🏭 ${f.name}</span>
        <button class="close-btn" onclick="closeModal()">닫기</button>
      </div>
      <div style="line-height:1.8; font-size:1.05rem;">
        <p><strong style="color:#e3c891;">[시설 역할]</strong><br>${f.role}</p><br>
        <p><strong style="color:#ff8fa3;">[주요 배출 오염물질]</strong><br>${f.pollutants}</p>
      </div>
    `);
  }
}

// --- [미니게임 1] 기후적응 사업의 환경성·타당성 검토 ---
function openSeedingMinigame() {
  if (!activeTasks.seedingReady) {
    showDialogue('나', '오늘의 인공 강우·수자원 확보 타당성 검토는 이미 완료했어. 내일 새로운 구름·습도·수자원 자료를 확인하고 다시 검토하자.');
    return;
  }
  const cloudDesc = weather.cloudType === 'WARM'
    ? '고온·대기 정체 조건 → 배출원 주변의 대기질과 확산 영향 집중 검토'
    : '저온·대기 확산 조건 → 오염물질 이동 범위와 주변 영향 검토';

  openModal(`
    <div class="modal-header">
      <span class="modal-title">📻 인공 강우·기후 적응 사업 환경성 검토</span>
      <button class="close-btn" onclick="closeModal()">닫기</button>
    </div>
    <p style="font-size:0.95rem; color:#e3c891; margin-bottom:8px;">📡 현재 상공 기상 레이더 분석: <strong>${cloudDesc}</strong></p>
    <p style="font-size:0.88rem; color:#cfc9bc; margin-bottom:14px;">
      구름의 상태와 습도 등 기상 조건을 분석해 인공 강우 가능성을 평가하세요. 조건이 맞지 않으면 시행해도 효과를 기대하기 어렵습니다. 인공 강우는 가뭄 대응을 위한 보조 수단이며 온실가스 감축·사막화 방지 대책을 대신할 수 없습니다. 레이더 커서가 <strong>초록색 조사 적정 시점</strong>에 들어왔을 때 검토 결과를 제출하세요. (조사 비용: 10억)
    </p>
    <div style="margin-bottom:12px;">
      <label style="margin-right:16px; cursor:pointer;">
        <input type="radio" name="seedType" value="WARM" checked> 🌡️ 고온·대기 정체 조건 조사
      </label>
      <label style="cursor:pointer;">
        <input type="radio" name="seedType" value="COLD"> 🌬️ 저온·대기 확산 조건 조사
      </label>
    </div>
    <div class="radar-bar">
      <div class="radar-target" style="left: 38%; width: 24%;"></div>
      <div class="radar-cursor" id="radar-cursor" style="left: 0%;"></div>
    </div>
    <div style="text-align:center; margin-top:16px;">
      <button class="action-btn btn-yes" onclick="fireSeeding()">📋 환경성 검토 결과 제출 (10억)</button>
    </div>
  `);

  let pos = 0;
  let dir = 1;
  radarInterval = setInterval(() => {
    pos += dir * 2.8;
    if (pos >= 98) { pos = 98; dir = -1; }
    if (pos <= 0) { pos = 0; dir = 1; }
    const cursor = document.getElementById('radar-cursor');
    if (cursor) cursor.style.left = pos + '%';
  }, 30);
}

function fireSeeding() {
  if (budget < 10) {
    closeModal();
    showDialogue('나', '예산이 부족해서 현장 조사와 자료 분석 비용(10억)을 집행할 수 없어...');
    return;
  }
  const cursor = document.getElementById('radar-cursor');
  const pos = parseFloat(cursor.style.left);
  const selectedSeed = document.querySelector('input[name="seedType"]:checked').value;

  budget -= 10;
  activeTasks.seedingReady = false;
  closeModal();

  const isTimingGood = (pos >= 38 && pos <= 62);
  const isTypeCorrect = (selectedSeed === weather.cloudType);

  if (isTimingGood && isTypeCorrect) {
    // 조사 조건과 시점이 모두 적절하면 기후적응 사업의 시범 적용을 권고
    weather.type = 'RAIN';
    totalRainDays++;
    const acidLoad = (weather.so2 * 0.021) + (weather.nox * 0.015);
    weather.ph = +(Math.max(3.9, Math.min(6.8, 6.5 - acidLoad))).toFixed(2);
    droughtLevel = Math.max(5, droughtLevel - 11);
    weather.so2 *= 0.7;
    weather.pm25 *= 0.65;

    if (weather.ph < 5.6) {
      acidRainDays++;
      activeTasks.phAlert = true;
      showDialogue('나', `기후적응 사업 검토가 적절하게 마무리됐어. 다만 대기오염물질 때문에 강수 pH가 ${weather.ph}로 낮아졌어. 수질 시료를 분석하고 저감 대책을 검토해야 해.`);
    } else {
      showDialogue('나', `구름 상태와 조사 시점을 적절히 평가했어. 제한적인 강수 가능성을 고려한 수자원 확보 대책으로 물 부족 위험이 낮아졌어. 다만 장기적인 사막화 대응에는 온실가스 감축과 토양·생태계 복원도 필요해!`);
    }
  } else if (isTimingGood || isTypeCorrect) {
    droughtLevel = Math.max(5, droughtLevel - 4);
    showDialogue('나', '기상 조건과 조사 시점 중 하나가 맞지 않아 검토 결과의 신뢰도가 낮아졌어. 다음에는 관측 자료와 적정 조사 시점을 함께 확인하자.');
  } else {
    showDialogue('나', '기상 조건과 조사 시점을 모두 잘못 판단했어. 환경평가에서는 자료와 조건을 꼼꼼하게 확인해야 해.');
  }
  recordDailyTask('인공 강우·기후 적응 사업 환경성 검토', isTimingGood && isTypeCorrect ? '구름과 습도 등 기상 조건을 검토해 인공 강우 사업의 제한적 시범 적용 가능성을 평가했습니다.' : '기상 조건 또는 조사 시점이 맞지 않아 추가 자료 검토가 필요합니다.');
  updateWeatherHUD();
  updateAlertStrip();
}

// --- [미니게임 2] 수질 시료 분석 및 오염 저감대책 검토 ---
function openPhNeutralizeMinigame() {
  if (!activeTasks.phAlert && weather.ph >= 5.6) {
    showDialogue('나', `현재 수질 시료의 pH는 ${weather.ph}로 비교적 안정적이야. 오염이 확인되면 적정 처리량을 계산해 사업자에게 수질오염 저감대책을 권고해야 해.`);
    return;
  }

  const currentPh = weather.ph;
  openModal(`
    <div class="modal-header">
      <span class="modal-title">🧪 오아시스·지하수 수질 분석 및 저감대책 검토</span>
      <button class="close-btn" onclick="closeModal()">닫기</button>
    </div>
    <p style="font-size:0.95rem; color:#ffccd5; margin-bottom:10px;">
      ⚠️ 현재 측정된 수질 시료: <strong>pH ${currentPh}</strong> (산성화 여부 확인 필요)
    </p>
    <p style="font-size:0.9rem; color:#cfc9bc; margin-bottom:16px;">
      수질 개선 대책의 적정 처리량을 검토해 목표 관리 범위인 <strong>pH 6.2 ~ 6.8</strong>에 도달할 수 있도록 계산하세요.
      (게임 속 단순화된 모의 계산이며 실제 현장에서는 시료 특성과 법정 기준을 별도로 검토합니다.)
    </p>
    <div style="background:#1b1f2b; padding:16px; border-radius:10px; text-align:center;">
      <label style="font-size:1.05rem; font-weight:700; color:#f3d59b;">
        저감대책 적용량(모의값): <span id="alkali-val">150</span> kg
      </label><br><br>
      <input type="range" id="alkali-slider" min="20" max="300" value="150" style="width:85%;"
             oninput="document.getElementById('alkali-val').innerText = this.value">
    </div>
    <div style="text-align:center; margin-top:18px;">
      <button class="action-btn btn-yes" onclick="executePhNeutralize()">📊 분석 결과 및 저감대책 제출</button>
    </div>
  `);
}

function executePhNeutralize() {
  const dose = parseInt(document.getElementById('alkali-slider').value);
  const newPh = +(weather.ph + (dose * 0.01)).toFixed(2);
  recordDailyTask('수질 시료 분석 및 저감대책 검토', `시료 pH ${weather.ph}를 분석하고 처리량 ${dose}kg의 모의 결과를 검토했습니다.`);
  closeModal();

  if (newPh >= 6.2 && newPh <= 6.8) {
    weather.ph = newPh;
    activeTasks.phAlert = false;
    weather.ecoHealth = Math.min(100, weather.ecoHealth + 6);
    if (acidRainDays > 0) acidRainDays--;
    showDialogue('나', `분석 결과가 정확해! 수질 시료 pH ${newPh}를 기준 범위로 개선할 수 있는 적정 처리 대책을 제안했어.`);
  } else if (newPh < 6.2) {
    weather.ph = newPh;
    showDialogue('나', `검토한 처리량이 부족해 예상 pH가 ${newPh}에 머물렀어. 시료 특성과 처리 기준을 다시 확인하자.`);
  } else {
    weather.ph = 7.4;
    activeTasks.phAlert = false;
    showDialogue('나', `처리량을 지나치게 높게 산정해 예상 pH가 ${newPh}까지 올라갔어. 환경 대책은 과도한 처리로 2차 영향을 만들지 않도록 적정량을 검토해야 해.`);
  }
  updateWeatherHUD();
  updateAlertStrip();
}

// --- [미니게임 3] 대기질 센서 정비 단말기 ---
function openSensorRepairMinigame() {
  if (!activeTasks.sensorDirty) {
    showDialogue('나', '사막 지역의 4개 관측 지점에서 기온·습도·미세먼지·토양 수분 자료를 수집하고 있어. 측정값의 정확도를 주기적으로 점검해야 해.');
    return;
  }

  openModal(`
    <div class="modal-header">
      <span class="modal-title">📡 도심 대기질 센서망 원격 정비 단말기</span>
      <button class="close-btn" onclick="closeModal()">닫기</button>
    </div>
    <p style="font-size:0.92rem; color:#cfc9bc; margin-bottom:12px;">
      현장 먼지와 습기로 인해 환경 측정장비의 자료 품질에 문제가 생겼습니다. <strong>오류가 표시된 4개 측정 노드를 모두 클릭</strong>해 장비 상태를 점검하고 교정하세요!
    </p>
    <div class="sensor-grid">
      <div class="sensor-node dirty" id="node-1" onclick="cleanNode(1)">⚠️ 제1 발전소 구역 센서<br><small>[모래 먼지 막힘 - 클릭하여 세척]</small></div>
      <div class="sensor-node dirty" id="node-2" onclick="cleanNode(2)">⚠️ 제2 석유화학 구역 센서<br><small>[모래 먼지 막힘 - 클릭하여 세척]</small></div>
      <div class="sensor-node dirty" id="node-3" onclick="cleanNode(3)">⚠️ 제3 제련소 구역 센서<br><small>[모래 먼지 막힘 - 클릭하여 세척]</small></div>
      <div class="sensor-node dirty" id="node-4" onclick="cleanNode(4)">⚠️ 중앙 호수·주거지 센서<br><small>[모래 먼지 막힘 - 클릭하여 세척]</small></div>
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
      budget += 10;
      recordDailyTask('환경 측정장비 점검 및 자료 품질관리', '4개 구역 측정장비를 점검하고 데이터 신뢰도를 복구했습니다.');
      setTimeout(() => {
        closeModal();
        updateAlertStrip();
        showDialogue('나', '4개 구역의 환경 측정장비를 모두 점검했어! 이제 신뢰할 수 있는 측정 자료를 환경영향평가에 활용할 수 있어.');
      }, 350);
    }
  }
}

// --- [미니게임 4] 환경평가원 직통 전화기 (돌발 감사 & 민원) ---
function openAuditPhoneModal() {
  if (!activeTasks.phoneRinging || !activeTasks.currentAudit) {
    showDialogue('나', '현재 접수된 주민 의견이나 관계기관 협의 요청은 없어. 전화가 오면 개발사업의 환경영향과 대안을 검토하자.');
    return;
  }

  const audit = activeTasks.currentAudit;
  openModal(`
    <div class="modal-header">
      <span class="modal-title">☎️ [협의 요청] ${audit.title}</span>
      <button class="close-btn" onclick="closeModal()">닫기</button>
    </div>
    <p style="font-size:1.02rem; line-height:1.7; color:#f0ece1; margin-bottom:20px;">
      "${audit.desc}"
    </p>
    <button class="choice-btn" onclick="resolveAudit(0)">1. ${audit.choices[0].text}</button>
    <button class="choice-btn" onclick="resolveAudit(1)">2. ${audit.choices[1].text}</button>
  `);
}

function resolveAudit(choiceIdx) {
  const auditTitle = activeTasks.currentAudit.title;
  const resultMsg = activeTasks.currentAudit.choices[choiceIdx].effect();
  recordDailyTask(auditTitle, resultMsg);
  activeTasks.phoneRinging = false;
  activeTasks.currentAudit = null;
  closeModal();
  updateWeatherHUD();
  updateAlertStrip();
  showDialogue('나', resultMsg);
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
      <span class="modal-title">💻 환경보전 대책 검토 시스템 (잔여 예산: ${budget}억)</span>
      <button class="close-btn" onclick="closeModal()">닫기</button>
    </div>
    <p style="font-size:0.88rem; color:#c9b182; margin-bottom:12px;">
      ※ 선택한 환경보전 대책은 관계기관 협의와 사업 반영 절차를 거쳐 <strong>2일 후</strong>부터 적용됩니다.
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
    recordDailyTask('환경보전 대책 수립', `${p.name}을(를) 사업계획의 저감·적응 대책으로 제안했습니다.`);
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

  // 기후 위기로 사막화가 진행된 지역의 일일 환경 변화 (폭염·가뭄·모래폭풍·간헐적 폭우)
  const roll = Math.random() * 100;
  if (roll < 2) weather.type = 'HEAVY_RAIN';
  else if (roll < 17) weather.type = 'DROUGHT';
  else if (roll < 47) weather.type = 'DUST';
  else weather.type = 'CLEAR';

  weather.cloudType = Math.random() < 0.5 ? 'WARM' : 'COLD';

  if (weather.type === 'DUST') {
    activeTasks.sensorDirty = true;
    cleanedCount = 0;
  }

  // 매일 45% 확률로 주민 의견 또는 관계기관 협의 요청 수신
  if (!activeTasks.phoneRinging && Math.random() < 0.45) {
    activeTasks.phoneRinging = true;
    activeTasks.currentAudit = AUDIT_SCENARIOS[Math.floor(Math.random() * AUDIT_SCENARIOS.length)];
  }

  const dirs = ['북풍', '북서풍', '서풍', '남서풍', '남동풍', '동풍'];
  weather.windDir = dirs[Math.floor(Math.random() * dirs.length)];
  weather.windSpeed = +(1.2 + Math.random() * 6.5).toFixed(1);
  weather.temp = weather.type === 'DROUGHT' ? Math.floor(41 + Math.random() * 6) : Math.floor(29 + Math.random() * 9);
  weather.humidity = weather.type === 'HEAVY_RAIN' ? 88 : (weather.type === 'DROUGHT' ? 16 : Math.floor(25 + Math.random() * 35));
  if (activeIds.includes('seeding')) weather.humidity = Math.min(95, weather.humidity + 18);

  let so2Gen = activeIds.includes('fgd') ? 4 : 16;
  let noxGen = 13;
  let pmGen = activeIds.includes('esp') ? 4 : 15;
  if (weather.type === 'DUST') pmGen += 28;

  const dispersion = weather.windSpeed * 2.1;
  weather.so2 = Math.max(8, Math.min(150, weather.so2 + so2Gen - dispersion));
  weather.nox = Math.max(8, Math.min(140, weather.nox + noxGen - dispersion));
  weather.pm25 = Math.max(10, Math.min(200, weather.pm25 + pmGen - dispersion));

  // 산업시설의 에너지 전환·효율 개선 대책이 반영되면 추정 온실가스 배출량이 감소
  const co2Base = 420 + (weather.type === 'DROUGHT' ? 18 : 0) + (weather.type === 'DUST' ? 6 : 0);
  let co2Reduction = 0;
  if (activeIds.includes('fgd')) co2Reduction += 32;
  if (activeIds.includes('esp')) co2Reduction += 24;
  if (activeIds.includes('raingarden')) co2Reduction += 5;
  if (activeIds.includes('permeable')) co2Reduction += 7;
  weather.co2 = Math.max(250, Math.round(co2Base - co2Reduction));

  let rainProb = (weather.humidity * 0.55) - (weather.temp * 0.3);
  if (activeIds.includes('seeding')) rainProb += 28;
  if (weather.type === 'HEAVY_RAIN') rainProb = 95;
  if (weather.type === 'DROUGHT') rainProb = 3;
  weather.rainProb = Math.max(2, Math.min(95, Math.round(rainProb)));

  const didRain = (Math.random() * 100) < weather.rainProb;
  if (didRain) {
    if (weather.type !== 'HEAVY_RAIN') weather.type = 'RAIN';
    totalRainDays++;

    const acidLoad = (weather.so2 * 0.021) + (weather.nox * 0.015);
    weather.ph = +(Math.max(3.9, Math.min(6.8, 6.5 - acidLoad))).toFixed(2);

    weather.so2 *= 0.65;
    weather.nox *= 0.7;
    weather.pm25 *= 0.6;

    let droughtReduce = 7;
    if (activeIds.includes('raingarden')) droughtReduce += 4;
    if (activeIds.includes('permeable')) droughtReduce += 4;
    if (activeIds.includes('reservoir')) droughtReduce += 7;
    if (weather.type === 'HEAVY_RAIN') droughtReduce += 6;
    droughtLevel = Math.max(5, droughtLevel - droughtReduce);

    if (weather.ph < 5.6) {
      acidRainDays++;
      activeTasks.phAlert = true;
      weather.ecoHealth = Math.max(10, weather.ecoHealth - 6);
    } else {
      activeTasks.phAlert = false;
      weather.ecoHealth = Math.min(100, weather.ecoHealth + 5);
    }
  } else {
    let droughtInc = weather.type === 'DROUGHT' ? 5.5 : 2.2;
    if (activeIds.includes('reservoir')) droughtInc *= 0.65;
    droughtLevel = Math.min(100, droughtLevel + droughtInc);
  }

  updateWeatherHUD();
  updateAlertStrip();

  if (newlyApplied.length > 0) {
    pendingDayNotice = `오늘부터 [${newlyApplied.join(', ')}] 환경보전 대책이 적용되기 시작했습니다.`;
  }
}

function updateWeatherHUD() {
  const hud = document.getElementById('hud-weather');
  const weatherNames = {
    'CLEAR': '☀️ 맑음 (고온·건조한 사막 기후)',
    'DROUGHT': '🔥 기후 위기 영향: 극심한 폭염·장기 가뭄',
    'DUST': '🌪️ 기후 위기 영향: 강한 모래폭풍',
    'HEAVY_RAIN': '⛈️ 자연재해: 국지성 폭우',
    'RAIN': '🌧️ 비 내리는 중'
  };
  const hasSensor = POLICIES.find(p => p.id === 'sensor').status === 'ACTIVE';
  const sensorInfo = (hasSensor && !activeTasks.sensorDirty)
    ? `SO₂: ${weather.so2.toFixed(0)} | NOₓ: ${weather.nox.toFixed(0)} | PM2.5: ${weather.pm25.toFixed(0)} | 강수 pH: ${weather.ph}`
    : (activeTasks.sensorDirty ? `⚠️ 센서 오염됨 (정비 단말기 클릭 필요)` : `환경 측정 데이터: [측정망 미설치]`);

  hud.innerHTML = `
    <div style="font-weight:700; color:#f3d59b;">${weatherNames[weather.type]}</div>
    <div style="font-size:0.84rem; color:#ddd;">바람: ${weather.windDir} ${weather.windSpeed}m/s | 습도: ${weather.humidity}% | 강수확률: ${weather.rainProb}%</div>
    <div style="font-size:0.82rem; color:#a8dadc; margin-top:2px;">온실가스 추정 배출량: ${weather.co2.toFixed(0)}tCO₂e/일</div>
    <div style="font-size:0.82rem; color:#a8dadc; margin-top:2px;">${sensorInfo}</div>
  `;
}

// --- 하루 업무 결산 ---
function showDailySummary(completedDay, snapshot, isFinalDay) {
  pendingFinalDay = isFinalDay;
  const taskList = snapshot.tasks.length
    ? snapshot.tasks.map((task, index) => `
        <div class="check-item" style="display:block;">
          <div style="font-weight:700;">${index + 1}. ${task.title}</div>
          <div style="font-size:0.88rem; font-weight:400; margin-top:5px; line-height:1.5;">${task.detail}</div>
        </div>
      `).join('')
    : `<div class="check-item"><span>오늘 기록된 주요 업무가 없습니다. 내일은 사막화 현장 조사와 기후 자료 검토를 진행해 보세요.</span></div>`;

  const co2Change = snapshot.co2 - snapshot.previousCo2;
  const co2Text = co2Change < 0
    ? `전날보다 ${Math.abs(co2Change).toFixed(0)}tCO₂e/일 감소`
    : (co2Change > 0 ? `전날보다 ${co2Change.toFixed(0)}tCO₂e/일 증가` : '전날과 동일');

  openModal(`
    <div class="modal-header">
      <span class="modal-title">📋 ${completedDay}일차 오늘 한 일 결산</span>
      <button class="close-btn" onclick="closeDailySummary()">확인</button>
    </div>
    <div class="dossier-box">
      <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:2px solid #8c7a5b; padding-bottom:12px; margin-bottom:14px;">
        <span style="font-size:1.05rem; font-weight:700;">오늘의 환경평가 업무</span>
        <span style="font-size:1.25rem; font-weight:800; color:#1b4332;">${snapshot.tasks.length}건</span>
      </div>
      ${taskList}
      <div class="check-item">
        <span>지역 추정 온실가스 배출량</span>
        <strong>${snapshot.co2.toFixed(0)}tCO₂e/일</strong>
      </div>
      <div style="font-size:0.88rem; margin:4px 0 12px 4px; color:#4b453a;">${co2Text}</div>
      <div class="check-item">
        <span>사막 지역 물 부족 위험 지수</span>
        <strong>${snapshot.drought.toFixed(1)}%</strong>
      </div>
      <div class="check-item">
        <span>남은 사막 환경 복원 예산</span>
        <strong>${snapshot.budget.toFixed(0)}억 디르함</strong>
      </div>
      ${pendingDayNotice ? `<div style="margin-top:12px; padding:10px; background:#e6decb; line-height:1.6;">📌 ${pendingDayNotice}</div>` : ''}
    </div>
    <div style="text-align:center; margin-top:18px;">
      <button class="action-btn btn-yes" onclick="closeDailySummary()">${isFinalDay ? '최종 평가 결과 확인' : '다음 날 업무 시작'}</button>
    </div>
  `);
  pendingDayNotice = '';
}

function closeDailySummary() {
  closeModal();
  if (pendingFinalDay) {
    pendingFinalDay = false;
    checkCampaignEnd();
  }
}

function advanceGameDay() {
  const completedDay = day;
  const snapshot = {
    tasks: dailyWork.tasks.slice(),
    co2: weather.co2,
    previousCo2: previousCo2Emission,
    drought: droughtLevel,
    budget: budget
  };

  if (day >= TOTAL_GAME_DAYS) {
    showDailySummary(completedDay, snapshot, true);
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

// --- 15일차 최종 환경평가 결산 및 엔딩 ---
function checkCampaignEnd() {
  const status = getChecklistStatus();
  if (status.check1 && status.check2) {
    scene = 'ENDING';
    isPaused = true;
    document.getElementById('hud-clock').style.display = 'none';
    document.getElementById('hud-weather').style.display = 'none';
    document.getElementById('alert-strip').style.display = 'none';
    openModal(`
      <div style="text-align:center; padding:15px;">
        <h2 style="font-family:'Cinzel', serif; font-size:2rem; color:#f3d59b; margin-bottom:10px;">HAPPY ENDING : 사막에 되찾은 희망</h2>
        <p style="font-family:'Gowun Batang', serif; font-size:1.12rem; line-height:1.8; color:#f0ece1; margin-bottom:20px;">
          온실가스 배출량 <strong>${weather.co2.toFixed(0)}tCO₂e/일</strong>, 사막 지역 물 부족 위험 지수 <strong>${droughtLevel.toFixed(1)}%</strong>!<br>
          당신은 온실가스 감축과 물 관리, 토착 식생 복원 대책을 과학적으로 평가해 사막 지역의 환경 회복에 기여했습니다.<br>
          인공 강우는 적절한 기상 조건에서 제한적으로 검토했고, 근본적인 기후 위기 대응을 위해 온실가스 감축도 함께 추진했습니다.<br>
          사막에 다시 생명이 깃들 수 있다는 희망을 남기며 15일간의 환경평가 임무를 마쳤습니다.
        </p>
        <button class="start-btn" onclick="location.reload()">처음부터 다시하기</button>
      </div>
    `);
  } else if (status.check1 || status.check2) {
    scene = 'ENDING';
    isPaused = true;
    document.getElementById('hud-clock').style.display = 'none';
    document.getElementById('hud-weather').style.display = 'none';
    document.getElementById('alert-strip').style.display = 'none';
    openModal(`
      <div style="text-align:center; padding:15px;">
        <h2 style="font-family:'Cinzel', serif; font-size:1.9rem; color:#f3d59b; margin-bottom:10px;">PARTIAL ENDING : 아직 끝나지 않은 사막화 대응</h2>
        <p style="font-family:'Gowun Batang', serif; font-size:1.1rem; line-height:1.8; color:#f0ece1; margin-bottom:20px;">
          두 가지 핵심 목표 중 하나를 달성했지만, 사막 지역의 환경 위기를 해결하기에는 아직 부족합니다.<br>
          인공 강우와 같은 단기적인 수자원 대책뿐 아니라 온실가스 감축과 토양·생태계 복원을 꾸준히 이어가야 합니다.<br>
          최종 보고서를 보완해 다시 도전해 보세요.
        </p>
        <button class="start-btn" onclick="location.reload()">처음부터 다시하기</button>
      </div>
    `);
  } else {
    scene = 'ENDING';
    isPaused = true;
    openModal(`
      <div style="text-align:center; padding:15px;">
        <h2 style="font-family:'Cinzel', serif; font-size:1.9rem; color:#ff8fa3; margin-bottom:10px;">BAD ENDING : 사막화 대응 실패</h2>
        <p style="font-family:'Gowun Batang', serif; font-size:1.1rem; line-height:1.8; color:#f0ece1; margin-bottom:20px;">
          온실가스 배출량 <strong>${weather.co2.toFixed(0)}tCO₂e/일</strong>, 사막 지역 물 부족 위험 지수 <strong>${droughtLevel.toFixed(1)}%</strong>...<br>
          기후 위기로 심해진 사막화와 물 부족 문제에 대응하기 위한 대책이 충분히 마련되지 못했습니다.<br>
          인공 강우만으로는 사막화를 막을 수 없습니다. 온실가스 감축과 수자원 관리, 토양·생태계 복원 대책을 함께 검토해야 합니다.
        </p>
        <button class="start-btn" onclick="location.reload()">다시 도전하기</button>
      </div>
    `);
  }
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
  if (weather.type === 'DUST') return 'dust';
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

  // 모래언덕
  for (let xx = 0; xx < lw; xx++) {
    const dy = Math.round(groundY - 2 - 3 * Math.sin(xx * 0.045 + 1) - 2 * Math.sin(xx * 0.11));
    pr(xx, dy, 1, groundY - dy + 2, '#c9a56a');
    pr(xx, dy, 1, 1, '#ddbf88');
  }

  // 지면 (가뭄이 풀리면 초록으로)
  const base = green ? '#4a6b48' : '#b89468';
  const lite = green ? '#6f9a5a' : '#d3b27f';
  const dk = green ? '#365236' : '#94724b';
  pr(0, groundY, lw, groundH, base);
  pr(0, groundY, lw, 1, lite);
  for (let i = 0; i < 170; i++) {
    const sx = Math.floor(r() * lw);
    const sy = groundY + 2 + Math.floor(r() * Math.max(1, groundH - 2));
    pr(sx, sy, r() < 0.4 ? 2 : 1, 1, r() < 0.5 ? lite : dk);
  }
  if (green) {
    [0.05, 0.17, 0.39, 0.6, 0.86, 0.95].forEach((tx, idx) => {
      const px = Math.round(lw * tx);
      const py = groundY + 5 + (idx % 2) * 3;
      pr(px, py, 2, 4, '#5b3a22');
      pixDisc(px + 1, py - 1, 4, '#2f6b3a');
      pixDisc(px, py - 2, 2, '#4f9a52');
    });
  } else {
    [0.07, 0.52, 0.93].forEach((tx, idx) => {
      const px = Math.round(lw * tx);
      const py = groundY + 8 + idx * 2;
      pr(px, py - 6, 2, 7, '#3f6b3c');
      pr(px - 3, py - 4, 3, 1, '#3f6b3c');
      pr(px - 3, py - 6, 1, 3, '#3f6b3c');
      pr(px + 2, py - 5, 3, 1, '#3f6b3c');
      pr(px + 4, py - 7, 1, 3, '#3f6b3c');
    });
  }

  // 공장 건물
  FACTORIES.forEach(f => {
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
  FACTORIES.forEach(f => {
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
    const q = factoryGeom(f);
    const stacks = [[q.x + q.w * 0.27, q.y], [q.x + q.w * 0.72, q.y + q.h * 0.08]];
    stacks.forEach((s, si) => {
      for (let k = 0; k < 5; k++) {
        const prog = (T * 0.3 + k * 0.2 + fi * 0.13 + si * 0.31) % 1;
        const px = s[0] + Math.sin(T * 0.8 + k + fi) * 1.5 + prog * 7;
        const py = s[1] - 2 - prog * lh * 0.13;
        const size = 2 + prog * 6;
        g.globalAlpha = a * (1 - prog);
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

  // 5. 수질·대기 측정장비 점검 단말기
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

  // 6. 하천 수질 시료 분석 실험 세트 (비커)
  {
    const r = rr(DESK_ITEMS[5]);
    g.globalAlpha = 0.35; pr(r.x, r.y, r.w, r.h, '#c8e6ff'); g.globalAlpha = 1;
    const liqY = r.y + Math.round(r.h * 0.45);
    const liqH = Math.max(3, Math.round(r.h * 0.5));
    pr(r.x + 1, liqY, r.w - 2, liqH, (activeTasks.phAlert && blink) ? '#e63946' : '#4cc9f0');
    pr(r.x + 1, liqY, r.w - 2, 1, 'rgba(255,255,255,0.45)');
    pr(r.x, r.y, 1, r.h, INK);
    pr(r.x + r.w - 1, r.y, 1, r.h, INK);
    pr(r.x, r.y + r.h - 1, r.w, 1, INK);
    pr(r.x - 1, r.y, r.w + 2, 1, '#bfe0f0');
    for (let yy = r.y + 4; yy < r.y + r.h - 3; yy += 4) pr(r.x + r.w - 4, yy, 3, 1, 'rgba(22,17,31,0.55)');
    pr(r.x + 2, r.y + 2, 1, r.h - 5, 'rgba(255,255,255,0.5)');
    for (let k = 0; k < 2; k++) {
      const bp = Math.floor((T * 6 + k * 7) % liqH);
      pr(r.x + 4 + k * 4, liqY + liqH - 1 - bp, 1, 1, 'rgba(255,255,255,0.85)');
    }
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
  pixelBands(0, lh, [[0, '#0a0d2a'], [0.38, '#222a6b'], [0.62, '#7a4a7c'], [0.8, '#e08a6a'], [1, '#f5b878']], 3);
  drawMoon(Math.round(lw * 0.5), Math.round(lh * 0.36), Math.round(Math.min(lw, lh) * 0.15));
}

function titleDuneY(t) {
  return Math.round(lh * (0.78 + 0.035 * Math.sin(t * 5.2 + 0.6) + 0.015 * Math.sin(t * 11 + 1)));
}

function drawTitleCity() {
  const r = makeRng(23);
  const baseY = Math.round(lh * 0.78);
  const list = [
    { x: 0.15, w: 0.04, h: 0.22 }, { x: 0.21, w: 0.05, h: 0.32 }, { x: 0.28, w: 0.03, h: 0.19 },
    { x: 0.34, w: 0.06, h: 0.42 }, { x: 0.42, w: 0.04, h: 0.28 }, { x: 0.48, w: 0.05, h: 0.48 },
    { x: 0.55, w: 0.06, h: 0.36 }, { x: 0.63, w: 0.04, h: 0.25 }, { x: 0.69, w: 0.05, h: 0.39 },
    { x: 0.76, w: 0.04, h: 0.21 }
  ];
  list.forEach(b => {
    const bx = Math.round(lw * b.x);
    const bw = Math.max(6, Math.round(lw * b.w));
    const bh = Math.round(lh * b.h);
    const by = baseY - bh;
    pr(bx, by, bw, bh + 14, '#0e1230');
    pr(bx + bw - 1, by, 1, bh + 14, '#2a3170');
    pr(bx, by, bw, 1, '#2a3170');
    const sp = 8;
    for (let k = 0; k < sp; k++) {
      const w2 = Math.max(1, Math.round(bw * 0.3 * (1 - k / sp)));
      pr(bx + Math.round(bw / 2 - w2 / 2), by - 1 - k, w2, 1, '#0e1230');
    }
    for (let wy = by + 4; wy < baseY - 2; wy += 4) {
      for (let wx = bx + 2; wx < bx + bw - 2; wx += 3) {
        if (r() < 0.32) pr(wx, wy, 1, 2, r() < 0.8 ? '#f3c76a' : '#6ad0c8');
      }
    }
  });

  // 사막 언덕
  for (let x = 0; x < lw; x++) {
    const y = titleDuneY(x / lw);
    pr(x, y, 1, lh - y, '#170e1c');
    pr(x, y, 1, 1, '#6a3f58');
  }
  // 앞쪽 짙은 언덕
  for (let x = 0; x < lw; x++) {
    const y = Math.round(lh * (0.9 + 0.02 * Math.sin(x / lw * 7 + 2)));
    pr(x, y, 1, lh - y, '#0f0913');
    pr(x, y, 1, 1, '#3a2236');
  }
  // 선인장 실루엣
  [0.08, 0.9].forEach(tx => {
    const cx = Math.round(lw * tx);
    const cy = titleDuneY(tx) + 3;
    pr(cx, cy - 12, 2, 12, '#0d0814');
    pr(cx - 4, cy - 8, 4, 1, '#0d0814');
    pr(cx - 4, cy - 11, 1, 4, '#0d0814');
    pr(cx + 2, cy - 7, 4, 1, '#0d0814');
    pr(cx + 5, cy - 10, 1, 4, '#0d0814');
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
  const greenFlag = Math.max(0, (100 - droughtLevel) / 100) > 0.6;
  const size = lw + 'x' + lh;

  cachedLayer('sky', variant + '|' + size, () => pixelBands(0, Math.round(lh * 0.68), SKY_STOPS[variant], 3));
  drawCelestial(variant, dayProgress, T);
  cachedLayer('city', variant + '|' + greenFlag + '|' + size, () => drawCityLayer(variant, greenFlag));
  drawSmoke();

  if (weather.type === 'DUST') {
    drawParticles('rgba(218, 165, 95, 0.65)', 12);
  } else if (weather.type === 'RAIN' || weather.type === 'HEAVY_RAIN') {
    drawRain(weather.type === 'HEAVY_RAIN', weather.ph < 5.6);
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
