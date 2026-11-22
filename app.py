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
    width: min(820px, 92vw);
    max-height: 88vh;
    overflow-y: auto;
  }

  .modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 4px solid rgba(233, 239, 255, 0.25);
    padding-bottom: 12px;
    margin-bottom: 16px;
  }

  .modal-title {
    font-family: 'Noto Sans KR', sans-serif;
    font-size: 1.25rem;
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
    padding: 20px;
    border-radius: 0;
    font-family: 'Gowun Batang', serif;
    box-shadow: 0 0 0 3px var(--ink), 0 6px 0 3px var(--ink);
  }

  .check-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 12px;
    margin: 9px 0;
    background: #e6decb;
    border-left: 6px solid #7d6844;
    border-radius: 0;
    font-size: 1.02rem;
    font-weight: 700;
  }

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
    padding: 10px 22px;
    border-radius: 0;
    font-size: 0.98rem;
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
    padding: 13px 16px;
    border-radius: 0;
    margin-bottom: 12px;
    cursor: pointer;
    font-size: 0.96rem;
    box-shadow: 0 0 0 3px #4b63c9, 0 0 0 6px var(--ink);
  }

  .choice-btn:hover {
    background: #2a3a94;
    box-shadow: 0 0 0 3px var(--gold), 0 0 0 6px var(--ink);
  }

  .speaker-bubble-card {
    display: flex;
    align-items: center;
    gap: 14px;
    background: #f6efd8;
    color: #221d17;
    border: 3px solid #9b835d;
    border-radius: 14px;
    padding: 12px 16px;
    margin: 12px 0;
    cursor: pointer;
    box-shadow: 0 5px 0 var(--ink);
    transition: transform 0.08s steps(2), background 0.08s steps(2), border-color 0.08s steps(2);
    text-align: left;
    width: 100%;
  }

  .speaker-bubble-card:hover {
    background: #fff8e3;
    border-color: var(--gold);
    transform: translateY(-2px);
  }

  .pixel-person-box {
    width: 48px;
    height: 48px;
    flex: 0 0 48px;
    background: #1a2766;
    border: 3px solid var(--ink);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.65rem;
    box-shadow: inset 0 0 0 2px #4b63c9;
  }

  .speech-text-box {
    position: relative;
    flex: 1;
    font-family: 'Noto Sans KR', sans-serif;
    font-size: 0.98rem;
    font-weight: 600;
    line-height: 1.55;
  }

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

  <div id="title-overlay">
    <div class="title-logo">GREEN HORIZON</div>
    <div class="title-sub">기후 위기 속, 지속 가능한 대한민국의 미래를 평가하다</div>
    <button class="start-btn" onclick="startGame()">START</button>
  </div>

  <div id="hud-weather"></div>
  <div id="alert-strip"></div>

  <div id="hud-clock">
    <span class="clock-day" id="clock-day-text">1/15일차</span>
    <span class="clock-time" id="clock-time-text">07시 00분</span>
    <div>
      <button class="speed-btn active" id="spd-1" onclick="setSpeed(1)">1x</button>
      <button class="speed-btn" id="spd-5" onclick="setSpeed(5)">5x</button>
      <button class="speed-btn" id="spd-15" onclick="setSpeed(15)">15x</button>
    </div>
  </div>

  <div id="hover-tooltip"></div>

  <div id="dialogue-box" onclick="closeDialogue()">
    <div class="speaker-tag" id="dialogue-speaker">나</div>
    <div class="dialogue-text" id="dialogue-text"></div>
    <div class="dialogue-next">▼ 클릭하여 계속</div>
  </div>

  <div id="modal-backdrop">
    <div class="hollow-panel modal-card" id="modal-content"></div>
  </div>
</div>

<script>
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

let width, height;
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

let scene = 'TITLE';
let day = 1;
const TOTAL_GAME_DAYS = 15;
let gameMinutes = 7 * 60;
let timeMultiplier = 1;
let lastTimestamp = 0;
let isPaused = false;

let dailyWork = {
  tasks: [],
  budgetAtStart: 250
};
let pendingFinalDay = false;
let pendingDayNotice = '';
let previousCo2Emission = 280;

let budget = 250;
let pollutionRisk = 38;

let weather = {
  type: 'CLEAR',
  windDir: '서풍',
  windSpeed: 2.4,
  humidity: 55,
  temp: 19,
  so2: 18,
  nox: 24,
  pm25: 32,
  ecoHealth: 72,
  co2: 280
};

let activeTasks = {
  seedingReady: true,
  phAlert: false,
  sensorDirty: false,
  phoneRinging: false,
  currentAudit: null
};

const POLICIES = [
  { id: 'fgd', name: '저NOx 연소·배출가스 방지시설', cost: 45, desc: '연소 효율을 높이고 질소산화물·황산화물 저감시설을 설치하도록 사업계획에 반영합니다.', status: 'READY', applyDay: null },
  { id: 'esp', name: '고효율 설비 및 전력 사용 최적화', cost: 40, desc: '고효율 모터·전기화 설비와 에너지 관리 시스템을 적용해 온실가스와 대기오염 배출을 줄입니다.', status: 'READY', applyDay: null },
  { id: 'sensor', name: '대기질·소음 통합 측정망', cost: 25, desc: '사업지 경계와 주거지역에 측정망을 설치해 미세먼지와 소음 영향을 지속적으로 확인합니다.', status: 'READY', applyDay: null },
  { id: 'raingarden', name: '완충녹지 및 생태 연결축 확보', cost: 30, desc: '주거지와 사업시설 사이에 완충녹지를 두고 기존 녹지·하천 생태축을 연결하도록 권고합니다.', status: 'READY', applyDay: null },
  { id: 'permeable', name: '저영향개발(LID)·빗물관리', cost: 35, desc: '투수성 포장과 빗물정원, 저류시설을 반영해 불투수면 증가와 집중호우 때의 유출 영향을 줄입니다.', status: 'READY', applyDay: null },
  { id: 'reservoir', name: '폐수 재이용 및 비점오염 저감', cost: 50, desc: '폐수 재이용, 초기우수 처리, 유출수 관리계획을 마련해 하천과 토양에 미치는 영향을 줄입니다.', status: 'READY', applyDay: null },
  { id: 'seeding', name: '공사차량·비산먼지 관리계획', cost: 30, desc: '공사차량 동선과 운행시간을 조정하고 살수·세륜·덮개 등 비산먼지 저감대책을 마련합니다.', status: 'READY', applyDay: null }
];

const FACTORIES = [
  { id: 'factory1', name: '제1 에너지 공급시설 부지', facility: 'LNG 열병합발전소', benefit: '도시와 산업시설에 안정적인 전력과 열을 공급합니다.', role: '전력 공급은 필요하지만 연료 연소 과정에서 온실가스와 질소산화물 등이 발생할 수 있습니다. 주거지와의 이격거리, 배출구 높이, 저NOx 연소기술, 방지시설, 대체 에너지 입지를 비교해야 합니다.', pollutants: '온실가스(CO₂), 질소산화물(NOx), 황산화물(SOx), 소음 및 냉각수 영향', relX: 0.22, relY: 0.42, relW: 0.13, relH: 0.16 },
  { id: 'factory2', name: '제2 자원순환시설 부지', facility: '폐기물 소각·자원회수시설', benefit: '도시에서 발생하는 폐기물을 처리하고 열과 자원을 회수합니다.', role: '폐기물 처리시설은 도시 운영에 필요하지만 대기배출, 악취, 폐수, 폐기물 운반차량과 주민 수용성 문제가 발생할 수 있습니다. 재활용·감량 대안, 배출가스 처리, 밀폐형 반입시설, 교통 동선을 함께 비교해야 합니다.', pollutants: '질소산화물(NOx), 먼지, 악취, 폐수, 운반차량 배출가스 및 소음', relX: 0.44, relY: 0.43, relW: 0.14, relH: 0.15 },
  { id: 'factory3', name: '제3 물류지원시설 부지', facility: '대형 물류센터', benefit: '생활물자와 산업 원료를 공급하고 지역 일자리와 물류 기능을 지원합니다.', role: '물류시설은 지역경제와 생활에 필요하지만 대형 화물차 통행, 야간 소음, 대기오염, 넓은 불투수면과 녹지 훼손을 유발할 수 있습니다. 기존 도로 활용, 대중교통·친환경 차량, 완충녹지, 빗물관리 대안을 검토해야 합니다.', pollutants: '화물차 배출가스(PM2.5·NOx), 교통소음, 불투수면 증가, 녹지 훼손', relX: 0.68, relY: 0.41, relW: 0.13, relH: 0.17 }
];

let facilityDecisions = [null, null, null];
let ecologyGameCompleted = [false, false, false];
let noiseGameCompleted = [false, false, false];
let mitigationGameCompleted = [false, false, false];
let windGameCompleted = [false, false, false];
let dragClimbCompleted = [false, false, false];
let typingGameCompleted = [false, false, false];
let projectImpactScore = 0;
let assessmentQuality = 0;
let pendingMilestoneIndex = null;
let pendingFinalSettlement = false;
let endingType = null;

const DESK_ITEMS = [
  { id: 'radio', name: '🏭 배출기준 초과 사업장 현장 점검 무전기', relX: 0.04, relY: 0.65, relW: 0.07, relH: 0.13 },
  { id: 'newspaper', name: '📰 대한민국 개발사업 평가 공고', relX: 0.13, relY: 0.74, relW: 0.14, relH: 0.12 },
  { id: 'documents', name: '📁 환경영향평가서·조사 체크리스트', relX: 0.29, relY: 0.70, relW: 0.13, relH: 0.14 },
  { id: 'laptop', name: '💻 환경 데이터 분석 노트북', relX: 0.44, relY: 0.64, relW: 0.16, relH: 0.17 },
  { id: 'sensor_pad', name: '📡 대기질·소음 측정자료 점검 단말기', relX: 0.62, relY: 0.67, relW: 0.08, relH: 0.12 },
  { id: 'beaker', name: '📝 환경영향평가서 초안 작성 도면', relX: 0.72, relY: 0.66, relW: 0.07, relH: 0.14 },
  { id: 'photo', name: '⛰️ 현장 사면·완충대 드래그 조사 지도', relX: 0.80, relY: 0.73, relW: 0.06, relH: 0.10 },
  { id: 'penholder', name: '🏭 배출기준 초과 사업장 점검 수첩', relX: 0.87, relY: 0.72, relW: 0.04, relH: 0.10 },
  { id: 'phone', name: '☎️ 주민 의견 말풍선 접수 전화기', relX: 0.85, relY: 0.61, relW: 0.07, relH: 0.09 },
  { id: 'calendar', name: '📅 환경조사 및 평가 일정 캘린더', relX: 0.92, relY: 0.71, relW: 0.06, relH: 0.11 },
  { id: 'ecology_game', name: '🌿 서식지 교란 차단 현장 조사', relX: 0.04, relY: 0.85, relW: 0.10, relH: 0.09 },
  { id: 'noise_game', name: '🔊 소음 파형 피크 측정 점검', relX: 0.36, relY: 0.85, relW: 0.11, relH: 0.09 },
  { id: 'mitigation_game', name: '🧱 완충·저감시설 배치 시뮬레이터', relX: 0.68, relY: 0.85, relW: 0.11, relH: 0.09 },
  { id: 'wind_game', name: '💨 바람길·확산 경로 저감 대응', relX: 0.86, relY: 0.85, relW: 0.10, relH: 0.09 }
];

const AUDIT_SCENARIOS = [
  {
    title: "주민 의견 수렴 · 발전시설 대기확산 우려",
    situation: "주거지 방향 바람이 잦은 시기입니다. 각 주민의 말풍선을 직접 클릭해 환경영향평가에서 우선 검토할 핵심 근거 발언을 고르세요.",
    speakers: [
      {
        avatar: "🧑",
        name: "인근 주민 A",
        bubble: "계절별 풍향·풍속과 배출량으로 만든 대기확산 예측부터 먼저 확인해야 우리 동네 미세먼지 영향을 알 수 있어요!",
        correct: true,
        effect: () => {
          budget = Math.max(0, budget - 5);
          weather.co2 = Math.max(180, weather.co2 - 10);
          pollutionRisk = Math.max(5, pollutionRisk - 2);
          return "정확해! 풍향·풍속과 배출량 자료를 함께 봐야 오염물질 이동과 농도를 예측할 수 있어.";
        }
      },
      {
        avatar: "👩",
        name: "행인 B",
        bubble: "공장 울타리 페인트 색깔만 파란색으로 바꾸면 연기도 시원해 보이지 않을까요?",
        correct: false,
        effect: () => "외벽 색상은 대기오염 농도나 확산 경로를 줄이지 못해. 배출량과 기상 조건, 확산 예측이 필요해."
      },
      {
        avatar: "🧔",
        name: "주민 C",
        bubble: "근처 편의점 도시락 종류가 늘어나면 발전소 연기가 줄어들 것 같아요!",
        correct: false,
        effect: () => {
          pollutionRisk = Math.min(100, pollutionRisk + 1);
          return "편의점 상품과 대기오염 확산은 관련이 없어. 풍향·풍속과 배출량 자료를 봐야 해.";
        }
      }
    ]
  },
  {
    title: "주민 의견 수렴 · 물류차량 소음·통학로 안전",
    situation: "새벽 대형차 통행과 등굣길 안전에 관한 주민 의견입니다. 평가 근거가 담긴 말풍선을 직접 클릭하세요.",
    speakers: [
      {
        avatar: "👵",
        name: "할머니 주민",
        bubble: "시간대별 교통량과 통학로 위치, 소음 예측 자료를 봐야 새벽 트럭 동선과 방음 대책을 제대로 세울 수 있죠!",
        correct: true,
        effect: () => {
          budget = Math.max(0, budget - 6);
          pollutionRisk = Math.max(5, pollutionRisk - 2);
          return "맞아! 시간대별 교통량·통학로·소음 예측을 함께 봐야 안전과 소음을 동시에 검토할 수 있어.";
        }
      },
      {
        avatar: "👨",
        name: "지나가는 시민",
        bubble: "트럭 운전기사님들이 좋아하는 멜빵바지 스타일을 조사하면 소음이 줄어들 거예요!",
        correct: false,
        effect: () => "복장 취향은 교통량이나 소음 예측과 무관해. 통학로와 시간대별 교통·소음 자료가 핵심이야."
      },
      {
        avatar: "🧑",
        name: "주민 D",
        bubble: "물류센터 휴게실 의자 쿠션 두께를 재보면 도로 소음 문제가 해결될까요?",
        correct: false,
        effect: () => {
          pollutionRisk = Math.min(100, pollutionRisk + 1);
          return "실내 의자 쿠션은 외부 도로 소음이나 통학로 안전을 설명하지 못해.";
        }
      }
    ]
  },
  {
    title: "주민 의견 수렴 · 하천 녹지 훼손 및 우수 유출",
    situation: "집중호우 시 하천 인근 녹지 훼손과 초기우수 유입 우려가 제기되었습니다. 핵심 근거 말풍선을 직접 클릭하세요.",
    speakers: [
      {
        avatar: "👩‍🌾",
        name: "하천 인근 주민",
        bubble: "하천·녹지 현황도와 생태 조사, 불투수면·우수 유출 예측을 봐야 완충녹지와 저류시설을 제대로 배치할 수 있어요!",
        correct: true,
        effect: () => {
          budget = Math.max(0, budget - 7);
          weather.ecoHealth = Math.min(100, weather.ecoHealth + 7);
          pollutionRisk = Math.max(5, pollutionRisk - 2);
          return "정확해! 생태 현황도와 불투수면·우수 유출 예측을 함께 봐야 하천과 녹지를 지킬 수 있어.";
        }
      },
      {
        avatar: "🧔",
        name: "주민 E",
        bubble: "공사장 밥차 메뉴에 떡볶이가 나오면 빗물 유출량이 확 줄어들 걸요!",
        correct: false,
        effect: () => "식단 메뉴로는 빗물 유출이나 생태축 훼손을 막을 수 없어. 하천·녹지 현황과 유출 예측이 필요해."
      },
      {
        avatar: "👩",
        name: "주민 F",
        bubble: "사업부지 담벼락에 스티커를 많이 붙이면 하천 수질이 깨끗해질까요?",
        correct: false,
        effect: () => {
          pollutionRisk = Math.min(100, pollutionRisk + 1);
          return "담벼락 스티커는 수질이나 비점오염 저감과 관련이 적어.";
        }
      }
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

let activeMinigameCleanup = null;

function stopActiveMinigame() {
  if (typeof activeMinigameCleanup === 'function') {
    activeMinigameCleanup();
  }
  activeMinigameCleanup = null;
}

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
    showDialogue('나', '기후 위기로 폭염과 집중호우, 미세먼지 문제가 심해진 대한민국의 한 도시야. 환경평가원 실무로서 배출기준 초과 사업장 점검, 사면·완충대 드래그 조사, 주민 말풍선 근거 확인, 저감시설 배치 등을 진행해 보자!');
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
  stopActiveMinigame();
  isPaused = true;
  document.getElementById('modal-content').innerHTML = htmlContent;
  document.getElementById('modal-backdrop').style.display = 'flex';
}

function closeModal() {
  stopActiveMinigame();
  document.getElementById('modal-backdrop').style.display = 'none';
  if (document.getElementById('dialogue-box').style.display !== 'block') {
    isPaused = false;
  }
}

function updateAlertStrip() {
  const strip = document.getElementById('alert-strip');
  let alerts = [];
  if (activeTasks.phAlert) {
    alerts.push(`<div class="alert-pill" onclick="handleObjectClick('beaker')">📝 평가서 초안 작성 필요 [예측 도면] 클릭</div>`);
  }
  if (activeTasks.sensorDirty) {
    alerts.push(`<div class="alert-pill" onclick="handleObjectClick('sensor_pad')">📡 경고: 환경 측정장비 데이터 오류 발생! [점검 단말기] 클릭</div>`);
  }
  if (activeTasks.phoneRinging) {
    alerts.push(`<div class="alert-pill" onclick="handleObjectClick('phone')">☎️ 수신 중: 주민 말풍선 의견 도착! [전화기] 클릭</div>`);
  }
  strip.innerHTML = alerts.join('');
  strip.style.display = alerts.length > 0 ? 'flex' : 'none';
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

function handleObjectClick(id) {
  if (id === 'newspaper') {
    recordDailyTask('개발사업 평가 공고 및 사업계획 확인', '사업 목적, 규모, 입지, 공사·운영 계획과 환경영향평가 대상 항목을 확인했습니다.');
    openModal(`
      <div class="modal-header"><span class="modal-title">📰 대한민국 개발사업 환경영향평가 공고</span><button class="close-btn" onclick="closeModal()">닫기</button></div>
      <div class="newspaper-sheet"><div class="news-head"><div style="font-size:0.85rem; letter-spacing:0.2em;">대한민국 환경영향평가팀</div>
      <h2 style="font-size:1.45rem; margin-top:4px;">"필요한 개발과 환경 보전, 두 가지를 함께 검토합니다"</h2></div>
      <p style="line-height:1.8; font-size:1.02rem;">기후 위기로 폭염과 집중호우, 대기오염 위험이 커진 대한민국의 한 도시. 도시 외곽에 에너지 공급시설, 자원순환시설, 물류지원시설의 입지가 제안되었다. 세 시설은 도시 운영에 필요하지만 온실가스와 대기오염, 소음, 교통량 증가, 녹지 훼손 등의 영향을 일으킬 수 있다.</p></div>
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
      <div class="check-item"><span>승인 결정된 시설</span><strong>${built}/3곳</strong></div>
      <div class="check-item"><span>평가 예산 잔액</span><strong>${budget}억 원</strong></div></div>`);
  } else if (id === 'laptop') {
    renderLaptopModal();
  } else if (id === 'radio' || id === 'penholder') {
    openEmissionInspectionGame();
  } else if (id === 'beaker') {
    openTypingChallengeGame();
  } else if (id === 'sensor_pad') {
    openSensorRepairMinigame();
  } else if (id === 'phone') {
    openAuditPhoneModal();
  } else if (id === 'photo') {
    openDragClimbMinigame();
  } else if (id === 'ecology_game') {
    openHabitatShieldArcadeGame();
  } else if (id === 'noise_game') {
    openNoisePeakTimingGame();
  } else if (id === 'mitigation_game') {
    openMitigationPlacementGame();
  } else if (id === 'wind_game') {
    openWindPlumeDefenseGame();
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
    <div class="check-item"><span>현재 사업 결정</span><strong>${status}</strong></div></div>`);
}

// --- [업무 1] 배출허용기준 초과 사업장 현장 점검 ---
function openEmissionInspectionGame() {
  if (!activeTasks.seedingReady) {
    showDialogue('나', '오늘의 배출시설 현장 점검은 이미 마쳤어. 내일 다시 점검해 보자.');
    return;
  }

  let inspected = 0;
  let falseChecks = 0;
  let running = true;

  const sites = [
    { x: 110, y: 85, vx: 1.5, vy: 1.0, exceed: true, label: 'NOx 기준초과' },
    { x: 280, y: 155, vx: -1.8, vy: 1.2, exceed: true, label: 'PM2.5 기준초과' },
    { x: 450, y: 95, vx: 1.4, vy: -1.3, exceed: false, label: '기준적합 사업장' },
    { x: 560, y: 185, vx: -1.5, vy: -1.0, exceed: true, label: 'SOx 기준초과' }
  ];

  openModal(`
    <div class="modal-header"><span class="modal-title">🏭 배출허용기준 초과 사업장 점검 (${inspected}/3 조치)</span><button class="close-btn" onclick="closeModal()">닫기</button></div>
    <p style="line-height:1.65; color:#d9d1bd; margin-bottom:10px;">
      현장 모니터링에서 <strong>기준 초과(붉은 마커)</strong>로 잡힌 사업장을 클릭해 저감·개선 조치를 지시하세요! (기준적합 사업장은 불필요한 제재를 피하세요)
    </p>
    <canvas id="shooterCanvas" width="700" height="270" style="position:relative; width:100%; height:260px; border:3px solid #e9efff; background:#0d163b; cursor:pointer;"></canvas>
    <p id="shooter-status" style="min-height:24px; color:#ffd166; font-weight:700; margin-top:10px;">기준 초과 사업장을 클릭해 개선 조치를 내리세요!</p>
  `);

  const c = document.getElementById('shooterCanvas');
  const sctx = c.getContext('2d');

  c.onclick = (e) => {
    if (!running) return;
    const rect = c.getBoundingClientRect();
    const sx = ((e.clientX - rect.left) / rect.width) * c.width;
    const sy = ((e.clientY - rect.top) / rect.height) * c.height;
    const stEl = document.getElementById('shooter-status');

    for (let i = sites.length - 1; i >= 0; i--) {
      const t = sites[i];
      const dist = Math.hypot(sx - t.x, sy - t.y);
      if (dist <= 30) {
        if (t.exceed) {
          sites.splice(i, 1);
          inspected++;
          const titleEl = document.querySelector('.modal-title');
          if (titleEl) titleEl.innerText = `🏭 배출허용기준 초과 사업장 점검 (${inspected}/3 조치)`;
          if (stEl) stEl.innerText = `✅ ${t.label} 사업장 개선 조치 완료! (${inspected}/3)`;
          if (inspected >= 3) {
            running = false;
            clearInterval(iv);
            activeTasks.seedingReady = false;
            assessmentQuality += 1.5;
            pollutionRisk = Math.max(5, pollutionRisk - 2.5);
            recordDailyTask('배출허용기준 초과 사업장 점검 완료', '기준 초과 사업장 3곳을 확인하고 배출저감 개선 조치를 기록했습니다.');
            closeModal();
            updateWeatherHUD();
            showDialogue('나 · 현장 점검 완료', '기준 초과 사업장 3곳에 개선 조치를 지시했어! 대기오염 관리 실적이 올랐어.');
          }
        } else {
          falseChecks++;
          if (stEl) stEl.innerText = `⚠️ 해당 사업장은 배출기준 적합 상태입니다! (오점검 ${falseChecks}회)`;
        }
        break;
      }
    }
  };

  const iv = setInterval(() => {
    if (!running) return;
    sites.forEach(t => {
      t.x += t.vx;
      t.y += t.vy;
      if (t.x < 48 || t.x > c.width - 48) t.vx *= -1;
      if (t.y < 36 || t.y > c.height - 36) t.vy *= -1;
    });

    sctx.clearRect(0, 0, c.width, c.height);
    sctx.fillStyle = '#0d163b';
    sctx.fillRect(0, 0, c.width, c.height);

    sctx.fillStyle = '#18275c';
    for (let gx = 0; gx < c.width; gx += 35) sctx.fillRect(gx, 0, 1, c.height);
    for (let gy = 0; gy < c.height; gy += 35) sctx.fillRect(0, gy, c.width, 1);

    sites.forEach(t => {
      sctx.fillStyle = t.exceed ? '#e0505a' : '#52b788';
      sctx.beginPath();
      sctx.arc(t.x, t.y, 24, 0, Math.PI * 2);
      sctx.fill();
      sctx.lineWidth = 3;
      sctx.strokeStyle = '#16111f';
      sctx.stroke();

      sctx.fillStyle = '#ffffff';
      sctx.font = 'bold 11px "Noto Sans KR", sans-serif';
      sctx.textAlign = 'center';
      sctx.fillText(t.label, t.x, t.y + 4);
    });
  }, 16);

  activeMinigameCleanup = () => {
    running = false;
    clearInterval(iv);
  };
}

// --- [업무 2 · 드래그 조작 개선] 현장 사면·완충대 드래그 조사 ---
function openDragClimbMinigame() {
  const idx = Math.min(2, Math.floor((day - 1) / 5));
  const f = FACTORIES[idx];

  openModal(`
    <div class="modal-header">
      <span class="modal-title">⛰️ 현장 사면·완충대 드래그 조사 · ${f.facility}</span>
      <button class="close-btn" onclick="closeModal()">닫기</button>
    </div>
    <p style="line-height:1.65; color:#d9d1bd; margin-bottom:10px;">
      조사원 위에서 <strong>마우스를 원하는 방향과 길이만큼 뒤로 당긴 뒤 놓으세요</strong>! 당기는 길이와 각도에 따라 <strong>점프 높이와 방향</strong>이 달라지며, 노란 점선으로 궤적을 미리 볼 수 있습니다.
    </p>
    <div style="display:flex; justify-content:space-between; background:#0d1438; padding:8px 14px; border:2px solid #4b63c9; margin-bottom:10px; font-size:0.9rem;">
      <span>도달 고도: <strong id="drag-climb-pct" style="color:#ffd166;">0%</strong></span>
      <span>조작: <strong style="color:#6ad0c8;">드래그 길이 = 세기 · 드래그 반대 방향 = 각도</strong></span>
      <span>상태: <strong id="drag-climb-status" style="color:#a8e6cf;">현장 조사 중</strong></span>
    </div>
    <canvas id="dragClimbCanvas" width="700" height="360" style="position:relative; width:100%; height:340px; border:3px solid #e9efff; background:#101942; cursor:grab;"></canvas>
    <div style="text-align:right; margin-top:10px;">
      <button class="action-btn btn-no" id="drag-reset-btn">출발 지점 복귀</button>
    </div>
  `);

  const c = document.getElementById('dragClimbCanvas');
  const dctx = c.getContext('2d');
  const W = c.width;
  const H = c.height;

  const platforms = [
    { x: 0, y: H - 26, w: W, h: 26, type: 'ground' },
    { x: 85, y: H - 82, w: 150, h: 14, type: 'plat' },
    { x: 300, y: H - 134, w: 145, h: 14, type: 'plat' },
    { x: 495, y: H - 188, w: 145, h: 14, type: 'plat' },
    { x: 265, y: H - 242, w: 155, h: 14, type: 'plat' },
    { x: 75, y: H - 294, w: 140, h: 14, type: 'plat' },
    { x: 450, y: H - 332, w: 185, h: 16, type: 'goal' }
  ];

  const player = { x: 120, y: H - 52, w: 22, h: 26, vx: 0, vy: 0, grounded: true };
  let dragging = false;
  let dragStart = { x: 0, y: 0 };
  let dragCurr = { x: 0, y: 0 };
  let maxPct = 0;
  let cleared = false;
  let running = true;

  const GRAVITY = 1150;
  const MAX_DRAG = 160;

  function toCanvasCoords(evt) {
    const rect = c.getBoundingClientRect();
    return {
      x: ((evt.clientX - rect.left) / rect.width) * W,
      y: ((evt.clientY - rect.top) / rect.height) * H
    };
  }

  // 드래그 벡터를 실제 초기 속도 (vx, vy)로 변환
  function computeLaunchVelocity() {
    const pullX = dragStart.x - dragCurr.x;
    const pullY = dragStart.y - dragCurr.y;
    const rawDist = Math.hypot(pullX, pullY);
    if (rawDist < 8) return null;
    const clampedDist = Math.min(MAX_DRAG, rawDist);
    const ratio = clampedDist / MAX_DRAG;
    const nx = pullX / rawDist;
    const ny = pullY / rawDist;

    // 수평·수직 방향 모두 드래그 방향과 세기에 비례하게 반응
    const speed = 140 + ratio * 520;
    let vx = nx * speed;
    let vy = ny * speed;
    // 아래로 당겨 위로 쏘는 기본 감각을 유지하되, 드래그 각도에 따라 높이·방향이 확실히 변하도록 조정
    if (vy > -110 && ratio > 0.25) {
      vy = -110 - ratio * 260;
    }
    return { vx, vy, powerPct: Math.round(ratio * 100) };
  }

  c.onmousedown = (evt) => {
    if (!running || !player.grounded) return;
    const pt = toCanvasCoords(evt);
    dragging = true;
    dragStart = { x: player.x + player.w / 2, y: player.y + player.h / 2 };
    dragCurr = pt;
    c.style.cursor = 'grabbing';
  };

  window.addEventListener('mousemove', onDragMove);
  function onDragMove(evt) {
    if (!dragging) return;
    dragCurr = toCanvasCoords(evt);
  }

  window.addEventListener('mouseup', onDragRelease);
  function onDragRelease() {
    if (!dragging) return;
    dragging = false;
    c.style.cursor = 'grab';
    if (!player.grounded) return;

    const vel = computeLaunchVelocity();
    if (!vel) return;
    player.vx = vel.vx;
    player.vy = vel.vy;
    player.grounded = false;
  }

  document.getElementById('drag-reset-btn').onclick = () => {
    player.x = 120;
    player.y = H - 52;
    player.vx = 0;
    player.vy = 0;
    player.grounded = true;
    dragging = false;
  };

  let prevT = performance.now();
  function loop(now) {
    if (!running) return;
    const dt = Math.min(0.033, (now - prevT) / 1000);
    prevT = now;

    if (!player.grounded) {
      player.vy += GRAVITY * dt;
    }
    const prevBottom = player.y + player.h;
    player.x += player.vx * dt;
    player.y += player.vy * dt;

    if (player.x < 0) { player.x = 0; player.vx = Math.abs(player.vx) * 0.5; }
    if (player.x + player.w > W) { player.x = W - player.w; player.vx = -Math.abs(player.vx) * 0.5; }
    if (player.y < 0) { player.y = 0; player.vy = 0; }

    let landed = false;
    if (player.vy >= 0) {
      for (const p of platforms) {
        const overlapX = (player.x + player.w - 2) > p.x && (player.x + 2) < (p.x + p.w);
        if (overlapX && prevBottom <= p.y + 12 && (player.y + player.h) >= p.y) {
          player.y = p.y - player.h;
          player.vy = 0;
          player.vx = 0;
          player.grounded = true;
          landed = true;
          if (p.type === 'goal' && !cleared) {
            cleared = true;
            dragClimbCompleted[idx] = true;
            assessmentQuality += 2;
            pollutionRisk = Math.max(5, pollutionRisk - 3);
            weather.ecoHealth = Math.min(100, weather.ecoHealth + 5);
            recordDailyTask('현장 사면·완충대 조사 완료', `${f.facility} 주변 상부 완충녹지 관측 지점에 도달했습니다.`);
            updateWeatherHUD();
            const stEl = document.getElementById('drag-climb-status');
            if (stEl) stEl.innerText = '상부 관측 지점 도달! (+2 평가품질)';
          }
          break;
        }
      }
    }
    if (!landed) player.grounded = false;

    const pct = Math.max(0, Math.min(100, Math.round(((H - 26 - (player.y + player.h)) / (H - 358)) * 100)));
    if (pct > maxPct) maxPct = pct;
    const pctEl = document.getElementById('drag-climb-pct');
    if (pctEl) pctEl.innerText = `${pct}% (최고 ${maxPct}%)`;

    dctx.clearRect(0, 0, W, H);
    dctx.fillStyle = '#101942';
    dctx.fillRect(0, 0, W, H);

    // 상부 관측 지점 표식
    const goal = platforms[platforms.length - 1];
    dctx.fillStyle = '#95d5b2';
    dctx.fillRect(goal.x + goal.w - 32, goal.y - 22, 5, 22);
    dctx.fillStyle = '#ffd166';
    dctx.fillRect(goal.x + goal.w - 27, goal.y - 22, 18, 10);

    platforms.forEach(p => {
      dctx.fillStyle = p.type === 'goal' ? '#2d6a4f' : (p.type === 'ground' ? '#4f3a28' : '#5e74a6');
      dctx.fillRect(p.x, p.y, p.w, p.h);
      dctx.fillStyle = p.type === 'goal' ? '#95d5b2' : '#9bb3e6';
      dctx.fillRect(p.x, p.y, p.w, 3);
    });

    // 드래그 조준선 및 포물선 미리보기
    if (dragging && player.grounded) {
      const cx = player.x + player.w / 2;
      const cy = player.y + player.h / 2;
      const vel = computeLaunchVelocity();
      if (vel) {
        dctx.strokeStyle = '#ffd166';
        dctx.lineWidth = 3;
        dctx.beginPath();
        dctx.moveTo(cx, cy);
        dctx.lineTo(dragCurr.x, dragCurr.y);
        dctx.stroke();

        // 예상 궤적 점선
        dctx.fillStyle = '#6ad0c8';
        for (let step = 1; step <= 10; step++) {
          const tSim = step * 0.065;
          const pxSim = cx + vel.vx * tSim;
          const pySim = cy + vel.vy * tSim + 0.5 * GRAVITY * tSim * tSim;
          dctx.fillRect(pxSim - 2, pySim - 2, 4, 4);
        }

        dctx.fillStyle = '#ffe9a8';
        dctx.font = 'bold 12px "Noto Sans KR", sans-serif';
        dctx.fillText(`출력 ${vel.powerPct}%`, cx + 10, cy - 12);
      }
    }

    // 조사원 캐릭터
    dctx.fillStyle = '#f2c14e';
    dctx.fillRect(player.x, player.y, player.w, player.h);
    dctx.fillStyle = '#16111f';
    dctx.fillRect(player.x + 5, player.y + 6, 4, 4);
    dctx.fillRect(player.x + 13, player.y + 6, 4, 4);

    requestAnimationFrame(loop);
  }
  requestAnimationFrame(loop);

  activeMinigameCleanup = () => {
    running = false;
    window.removeEventListener('mousemove', onDragMove);
    window.removeEventListener('mouseup', onDragRelease);
  };
}

// --- [업무 3] 환경영향평가서 초안 작성 타자 ---
const TYPING_PROMPTS = [
  "배출가스 저감시설과 완충녹지를 확보해 환경영향을 줄입니다",
  "주민 의견과 계절별 풍향 자료를 반영해 입지 대안을 비교합니다",
  "저영향개발과 빗물관리로 집중호우 유출과 녹지 훼손을 막습니다"
];

function openTypingChallengeGame() {
  const idx = Math.min(2, Math.floor((day - 1) / 5));
  const targetText = TYPING_PROMPTS[idx % TYPING_PROMPTS.length];
  let submitted = false;
  let startedAt = performance.now();
  let timeLeft = 30.0;

  openModal(`
    <div class="modal-header">
      <span class="modal-title">📝 환경영향평가서 초안 작성 · ${FACTORIES[idx].facility}</span>
      <button class="close-btn" onclick="closeModal()">닫기</button>
    </div>
    <p style="line-height:1.65; color:#d9d1bd; margin-bottom:12px;">
      제한 시간 <strong>30초</strong> 안에 평가서 검토 문장을 입력하세요!
    </p>
    <div class="dossier-box">
      <div style="display:flex; justify-content:space-between; margin-bottom:10px; font-weight:700;">
        <span>남은 시간: <strong id="typing-time-left" style="color:#b3262e;">30.0초</strong></span>
        <span>정확도: <strong id="typing-acc-label" style="color:#1b4332;">0%</strong></span>
      </div>
      <div style="background:#e6decb; padding:14px; border-left:6px solid #1b2766; font-size:1.05rem; font-weight:700; line-height:1.6; margin-bottom:14px;">${targetText}</div>
      <input id="typing-input-box" type="text" placeholder="여기에 평가서 문장을 입력하세요..."
        style="width:100%; padding:12px 14px; font-size:1rem; background:#fffdf7; color:#181512; border:3px solid #16111f; outline:none;" />
    </div>
    <div style="text-align:center; margin-top:16px; display:flex; justify-content:center; gap:12px;">
      <button class="action-btn btn-yes" id="typing-submit-btn">초안 반영</button>
      <button class="action-btn btn-no" onclick="openTypingChallengeGame()">다시 작성</button>
    </div>
  `);

  function calcAcc(typed) {
    if (!targetText.length) return 0;
    let matches = 0;
    const len = Math.max(typed.length, targetText.length);
    for (let i = 0; i < typed.length; i++) {
      if (i < targetText.length && typed[i] === targetText[i]) matches++;
    }
    return Math.max(0, Math.min(100, Math.round((matches / len) * 100)));
  }

  function finish() {
    if (submitted) return;
    submitted = true;
    clearInterval(iv);
    const inp = document.getElementById('typing-input-box');
    const typed = inp ? inp.value.trim() : '';
    const acc = calcAcc(typed);
    const elapsedSec = Math.max(1, (performance.now() - startedAt) / 1000);
    const cpm = Math.round((typed.length / elapsedSec) * 60);
    activeTasks.phAlert = false;
    typingGameCompleted[idx] = true;
    if (acc >= 70) {
      assessmentQuality += 1.5;
      pollutionRisk = Math.max(5, pollutionRisk - 2.5);
      recordDailyTask('환경영향평가서 초안 작성 완료', `정확도 ${acc}%, 타수 ${cpm}타/분으로 검토 문장을 반영했습니다.`);
      closeModal();
      updateWeatherHUD();
      updateAlertStrip();
      showDialogue('나 · 초안 반영 완료', `정확도 ${acc}% (${cpm}타/분)로 평가서 초안을 정리했어.`);
    } else {
      recordDailyTask('환경영향평가서 초안 입력', `정확도 ${acc}%로 초안을 입력했습니다.`);
      closeModal();
      updateWeatherHUD();
      updateAlertStrip();
      showDialogue('나 · 초안 입력 완료', `정확도 ${acc}%였어. 정확도를 더 높이면 검토 완성도가 올라가.`);
    }
  }

  const inp = document.getElementById('typing-input-box');
  if (inp) {
    inp.focus();
    inp.addEventListener('input', () => {
      const accEl = document.getElementById('typing-acc-label');
      if (accEl) accEl.innerText = `${calcAcc(inp.value)}%`;
    });
  }
  const subBtn = document.getElementById('typing-submit-btn');
  if (subBtn) subBtn.addEventListener('click', finish);

  const iv = setInterval(() => {
    if (submitted) return;
    timeLeft = Math.max(0, +(timeLeft - 0.1).toFixed(1));
    const tEl = document.getElementById('typing-time-left');
    if (tEl) tEl.innerText = `${timeLeft.toFixed(1)}초`;
    if (timeLeft <= 0) finish();
  }, 100);

  activeMinigameCleanup = () => {
    submitted = true;
    clearInterval(iv);
  };
}

// --- [업무 4] 서식지 교란 차단 현장 조사 ---
function openHabitatShieldArcadeGame() {
  const idx = Math.min(2, Math.floor((day - 1) / 5));
  if (ecologyGameCompleted[idx]) {
    showDialogue('나', '이 부지의 생태 서식지 교란 점검은 이미 마쳤어.');
    return;
  }

  let saved = 0;
  let running = true;
  const threats = [
    { x: 130, y: 30, vx: 0.7, vy: 1.5, tag: '토사유출' },
    { x: 350, y: 20, vx: -0.9, vy: 1.7, tag: '식생훼손' },
    { x: 540, y: 40, vx: 0.8, vy: 1.4, tag: '동선침범' }
  ];

  openModal(`
    <div class="modal-header"><span class="modal-title">🌿 서식지 교란 차단 조사 (${saved}/4 조치)</span><button class="close-btn" onclick="closeModal()">닫기</button></div>
    <p style="line-height:1.65; color:#d9d1bd; margin-bottom:10px;">
      하단 <strong>생태 보전 구역</strong>으로 접근하는 교란 요인(토사유출·식생훼손·동선침범)을 클릭해 4번 저지하세요!
    </p>
    <canvas id="ecoArcadeCanvas" width="700" height="250" style="position:relative; width:100%; height:240px; border:3px solid #e9efff; background:#0d1838; cursor:pointer;"></canvas>
    <p id="eco-arcade-status" style="min-height:24px; color:#ffd166; font-weight:700; margin-top:10px;">교란 요인을 클릭해 보전 대책을 적용하세요!</p>
  `);

  const c = document.getElementById('ecoArcadeCanvas');
  const ectx = c.getContext('2d');

  c.onclick = (e) => {
    if (!running) return;
    const rect = c.getBoundingClientRect();
    const mx = ((e.clientX - rect.left) / rect.width) * c.width;
    const my = ((e.clientY - rect.top) / rect.height) * c.height;
    const stEl = document.getElementById('eco-arcade-status');

    for (let i = threats.length - 1; i >= 0; i--) {
      const t = threats[i];
      if (Math.hypot(mx - t.x, my - t.y) <= 30) {
        saved++;
        t.y = 15;
        t.x = 80 + Math.random() * (c.width - 160);
        const titleEl = document.querySelector('.modal-title');
        if (titleEl) titleEl.innerText = `🌿 서식지 교란 차단 조사 (${saved}/4 조치)`;
        if (stEl) stEl.innerText = `✅ ${t.tag} 차단 대책 반영! (${saved}/4)`;
        if (saved >= 4) {
          running = false;
          clearInterval(iv);
          ecologyGameCompleted[idx] = true;
          assessmentQuality += 1;
          pollutionRisk = Math.max(5, pollutionRisk - 2);
          weather.ecoHealth = Math.min(100, weather.ecoHealth + 5);
          recordDailyTask('생태 서식지 교란 차단 조사 완료', '서식지 보전 구역으로 향하던 교란 요인 4건을 저지했습니다.');
          closeModal();
          updateWeatherHUD();
          showDialogue('나 · 서식지 보전 완료', '서식지 교란 요인 4건을 모두 막아냈어! 생태 연결축 보전 점수가 올랐어.');
        }
        break;
      }
    }
  };

  const iv = setInterval(() => {
    if (!running) return;
    threats.forEach(t => {
      t.x += t.vx;
      t.y += t.vy;
      if (t.x < 45 || t.x > c.width - 45) t.vx *= -1;
      if (t.y > c.height - 46) {
        t.y = 18;
        t.x = 70 + Math.random() * (c.width - 140);
      }
    });

    ectx.clearRect(0, 0, c.width, c.height);
    ectx.fillStyle = '#0d1838';
    ectx.fillRect(0, 0, c.width, c.height);

    ectx.fillStyle = '#2d6a4f';
    ectx.fillRect(0, c.height - 28, c.width, 28);
    ectx.fillStyle = '#95d5b2';
    ectx.fillRect(0, c.height - 28, c.width, 3);

    threats.forEach(t => {
      ectx.fillStyle = '#e0505a';
      ectx.beginPath();
      ectx.arc(t.x, t.y, 22, 0, Math.PI * 2);
      ectx.fill();
      ectx.lineWidth = 2;
      ectx.strokeStyle = '#16111f';
      ectx.stroke();
      ectx.fillStyle = '#fff';
      ectx.font = 'bold 10px "Noto Sans KR", sans-serif';
      ectx.textAlign = 'center';
      ectx.fillText(t.tag, t.x, t.y + 4);
    });
  }, 16);

  activeMinigameCleanup = () => {
    running = false;
    clearInterval(iv);
  };
}

// --- [업무 5] 소음 파형 피크 측정 점검 ---
function openNoisePeakTimingGame() {
  const idx = Math.min(2, Math.floor((day - 1) / 5));
  if (noiseGameCompleted[idx]) {
    showDialogue('나', '이 부지의 소음 피크 측정은 이미 완료했어.');
    return;
  }

  let cursorX = 12;
  let dir = 1;
  let captures = 0;
  let running = true;

  openModal(`
    <div class="modal-header"><span class="modal-title">🔊 소음 파형 피크 측정 (${captures}/3 포착)</span><button class="close-btn" onclick="closeModal()">닫기</button></div>
    <p style="line-height:1.65; color:#d9d1bd; margin-bottom:10px;">움직이는 <strong>노란 커서</strong>가 <strong>초록 고소음 피크 구간</strong>에 들어왔을 때 <strong>[피크 포착!]</strong>을 눌러 3번 측정하세요.</p>
    <div style="position:relative; width:100%; height:56px; background:#0b1236; border:3px solid #e9efff; margin:16px 0; overflow:hidden;">
      <div style="position:absolute; left:22%; width:18%; top:0; bottom:0; background:rgba(82,183,136,0.45); border-left:2px solid #95d5b2; border-right:2px solid #95d5b2;"></div>
      <div style="position:absolute; left:58%; width:20%; top:0; bottom:0; background:rgba(82,183,136,0.45); border-left:2px solid #95d5b2; border-right:2px solid #95d5b2;"></div>
      <div id="peak-cursor" style="position:absolute; left:12px; top:0; width:10px; height:100%; background:#ffd166; box-shadow:0 0 0 2px #0a0d24;"></div>
    </div>
    <p id="peak-status" style="min-height:24px; color:#ffd166; font-weight:700; margin-bottom:12px;">커서를 초록 구간에 맞춰 포착하세요!</p>
    <div style="text-align:center;">
      <button class="action-btn btn-yes" id="peak-capture-btn">🎯 피크 포착!</button>
    </div>
  `);

  const iv = setInterval(() => {
    if (!running) return;
    cursorX += dir * 2.1;
    if (cursorX >= 96) { cursorX = 96; dir = -1; }
    if (cursorX <= 2) { cursorX = 2; dir = 1; }
    const cur = document.getElementById('peak-cursor');
    if (cur) cur.style.left = `${cursorX}%`;
  }, 16);

  document.getElementById('peak-capture-btn').onclick = () => {
    if (!running) return;
    const inZone1 = cursorX >= 22 && cursorX <= 40;
    const inZone2 = cursorX >= 58 && cursorX <= 78;
    const stEl = document.getElementById('peak-status');
    if (inZone1 || inZone2) {
      captures++;
      const tEl = document.querySelector('.modal-title');
      if (tEl) tEl.innerText = `🔊 소음 파형 피크 측정 (${captures}/3 포착)`;
      if (stEl) stEl.innerText = `✅ 고소음 피크 포착 성공! (${captures}/3)`;
      if (captures >= 3) {
        running = false;
        clearInterval(iv);
        noiseGameCompleted[idx] = true;
        assessmentQuality += 1;
        pollutionRisk = Math.max(5, pollutionRisk - 2);
        recordDailyTask('소음 파형 피크 측정 완료', '고소음 발생 구간의 최대 소음 피크를 3회 포착해 방음 대책 근거를 확보했습니다.');
        closeModal();
        updateWeatherHUD();
        showDialogue('나 · 소음 피크 측정 완료', '고소음 피크를 3번 정확히 포착했어!');
      }
    } else if (stEl) {
      stEl.innerText = '❌ 초록 구간 밖에서 눌렀어요! 초록 구역에 들어올 때 다시 시도하세요.';
    }
  };

  activeMinigameCleanup = () => {
    running = false;
    clearInterval(iv);
  };
}

// --- [업무 6] 완충·저감시설 배치 시뮬레이터 ---
function openMitigationPlacementGame() {
  const idx = Math.min(2, Math.floor((day - 1) / 5));
  if (mitigationGameCompleted[idx]) {
    showDialogue('나', '이 부지의 완충·저감시설 배치는 이미 마쳤어.');
    return;
  }
  const tools = [
    { id: 'buffer', label: '🌳 완충녹지', effect: '주변 완충·생태 보호' },
    { id: 'rain', label: '💧 투수·저류시설', effect: '빗물 유출 저감' },
    { id: 'wall', label: '🧱 방음벽', effect: '소음 차단' }
  ];
  let selectedTool = 'buffer';
  const slots = [
    { name: '주거지 경계', placed: null },
    { name: '하천 수변부', placed: null },
    { name: '학교 통학로 옆', placed: null },
    { name: '도로변 완충대', placed: null }
  ];

  function renderPlacement() {
    const placedCount = slots.filter(s => s.placed).length;
    openModal(`
      <div class="modal-header"><span class="modal-title">🧱 완충·저감시설 배치 시뮬레이터 (${placedCount}/3 설치)</span><button class="close-btn" onclick="closeModal()">닫기</button></div>
      <p style="line-height:1.65; color:#d9d1bd; margin-bottom:12px;">아래에서 <strong>저감 도구</strong>를 고른 뒤, 보호가 필요한 구역 <strong>3곳</strong>에 차례로 설치하세요.</p>
      <div class="dossier-box">
        <div style="display:flex; gap:8px; margin-bottom:14px; flex-wrap:wrap;">
          ${tools.map(t => `<button class="action-btn ${selectedTool === t.id ? 'btn-yes' : 'btn-no'}" onclick="pickPlaceTool('${t.id}')">${t.label}</button>`).join('')}
        </div>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px;">
          ${slots.map((s, i) => `
            <button class="choice-btn" style="margin:0; background:${s.placed ? '#286b4c' : '#1d2a70'};" onclick="placeOnSlot(${i})">
              <strong>${s.name}</strong><br><small>${s.placed ? '설치됨: ' + s.placed.label : '클릭하여 설치'}</small>
            </button>
          `).join('')}
        </div>
        <p id="place-fb" style="color:#b3262e; min-height:22px; margin-top:10px; font-weight:700;"></p>
      </div>
      <div style="text-align:center; margin-top:14px;">
        <button class="action-btn btn-yes" id="place-confirm-btn">배치안 적용</button>
      </div>
    `);

    window.pickPlaceTool = (tid) => { selectedTool = tid; renderPlacement(); };
    window.placeOnSlot = (si) => {
      const currentPlacedCount = slots.filter(x => x.placed).length;
      if (slots[si].placed) {
        slots[si].placed = null;
      } else if (currentPlacedCount < 3) {
        slots[si].placed = tools.find(t => t.id === selectedTool);
      }
      renderPlacement();
    };
    document.getElementById('place-confirm-btn').onclick = () => {
      const fb = document.getElementById('place-fb');
      const done = slots.filter(s => s.placed);
      if (done.length < 3) {
        if (fb) fb.innerText = '저감시설 3곳을 모두 배치해야 합니다.';
        return;
      }
      mitigationGameCompleted[idx] = true;
      assessmentQuality += 1;
      pollutionRisk = Math.max(5, pollutionRisk - 3);
      weather.ecoHealth = Math.min(100, weather.ecoHealth + 4);
      recordDailyTask('완충·저감시설 공간 배치 완료', `3개 구역(${done.map(d => d.placed.label).join(', ')})에 저감시설을 배치했습니다.`);
      closeModal();
      updateWeatherHUD();
      showDialogue('나 · 시설 배치 완료', '주변 민감 구역에 저감시설을 배치했어!');
    };
  }

  renderPlacement();
}

// --- [업무 7] 바람길·확산 경로 저감 대응 ---
function openWindPlumeDefenseGame() {
  const idx = Math.min(2, Math.floor((day - 1) / 5));
  if (windGameCompleted[idx]) {
    showDialogue('나', '이 부지의 대기확산 저감 점검은 이미 마쳤어.');
    return;
  }

  let plumeX = 12;
  let blockedCount = 0;
  let running = true;

  openModal(`
    <div class="modal-header"><span class="modal-title">💨 바람길·확산 경로 저감 대응 (${blockedCount}/2 제어)</span><button class="close-btn" onclick="closeModal()">닫기</button></div>
    <p style="line-height:1.65; color:#d9d1bd; margin-bottom:10px;">바람을 타고 오른쪽 <strong>주거·녹지 구역</strong>으로 이동하는 <strong>오염 확산 기둥</strong>이 <strong>중간 저감 구역(45%~68%)</strong>에 있을 때 <strong>[차단막 전개!]</strong>를 눌러 2번 제어하세요.</p>
    <div style="position:relative; width:100%; height:64px; background:#0d163b; border:3px solid #e9efff; margin:16px 0; overflow:hidden;">
      <div style="position:absolute; left:0; top:0; bottom:0; width:14%; background:#4a3f55; display:flex; align-items:center; justify-content:center; font-size:0.75rem;">배출원</div>
      <div style="position:absolute; left:45%; top:0; bottom:0; width:23%; background:rgba(106,208,200,0.35); border-left:2px dashed #6ad0c8; border-right:2px dashed #6ad0c8;"></div>
      <div style="position:absolute; right:0; top:0; bottom:0; width:16%; background:#2d6a4f; display:flex; align-items:center; justify-content:center; font-size:0.75rem;">주거·녹지</div>
      <div id="plume-token" style="position:absolute; left:12%; top:14px; width:34px; height:34px; background:#b5a692; border:2px solid #16111f; display:flex; align-items:center; justify-content:center; font-size:1.1rem;">☁️</div>
    </div>
    <p id="plume-status" style="min-height:24px; color:#ffd166; font-weight:700; margin-bottom:12px;">확산 기둥이 점선 저감 구역에 오면 전개하세요!</p>
    <div style="text-align:center;">
      <button class="action-btn btn-yes" id="plume-block-btn">🛡️ 차단막 전개!</button>
    </div>
  `);

  const iv = setInterval(() => {
    if (!running) return;
    plumeX += 0.95;
    if (plumeX > 84) plumeX = 12;
    const tok = document.getElementById('plume-token');
    if (tok) tok.style.left = `${plumeX}%`;
  }, 20);

  document.getElementById('plume-block-btn').onclick = () => {
    if (!running) return;
    const stEl = document.getElementById('plume-status');
    if (plumeX >= 42 && plumeX <= 70) {
      blockedCount++;
      plumeX = 12;
      const tEl = document.querySelector('.modal-title');
      if (tEl) tEl.innerText = `💨 바람길·확산 경로 저감 대응 (${blockedCount}/2 제어)`;
      if (stEl) stEl.innerText = `✅ 확산 경로 제어 성공! (${blockedCount}/2)`;
      if (blockedCount >= 2) {
        running = false;
        clearInterval(iv);
        windGameCompleted[idx] = true;
        assessmentQuality += 1;
        pollutionRisk = Math.max(5, pollutionRisk - 2);
        recordDailyTask('바람길·확산 경로 저감 대응 완료', '확산 경로상에서 오염 기둥을 2회 제어해 대기오염 대응 방안을 검증했습니다.');
        closeModal();
        updateWeatherHUD();
        showDialogue('나 · 확산 제어 완료', '오염 확산 기둥을 2번 제어했어!');
      }
    } else if (stEl) {
      stEl.innerText = '❌ 아직 점선 저감 구역(45%~68%)에 들어오지 않았어요!';
    }
  };

  activeMinigameCleanup = () => {
    running = false;
    clearInterval(iv);
  };
}

// --- 주민 의견 말풍선 직접 선택 ---
function openAuditPhoneModal() {
  const audit = (activeTasks.phoneRinging && activeTasks.currentAudit)
    ? activeTasks.currentAudit
    : AUDIT_SCENARIOS[(day + Math.floor(gameMinutes / 60)) % AUDIT_SCENARIOS.length];

  openModal(`
    <div class="modal-header">
      <span class="modal-title">☎️ ${audit.title}</span>
      <button class="close-btn" onclick="closeModal()">닫기</button>
    </div>
    <p style="line-height:1.65; color:#d9d1bd; margin-bottom:10px;">${audit.situation}</p>
    ${audit.speakers.map((sp, i) => `
      <button class="speaker-bubble-card" onclick="pickSpeakerBubble(${i}, '${encodeURIComponent(audit.title)}')">
        <div class="pixel-person-box">${sp.avatar}</div>
        <div class="speech-text-box">
          <div style="font-size:0.82rem; color:#72512c; font-weight:700; margin-bottom:3px;">${sp.name}의 말풍선 (클릭하여 선택)</div>
          “${sp.bubble}”
        </div>
      </button>
    `).join('')}
  `);
}

function pickSpeakerBubble(idx, encodedTitle) {
  const title = decodeURIComponent(encodedTitle);
  const audit = (activeTasks.currentAudit && activeTasks.currentAudit.title === title)
    ? activeTasks.currentAudit
    : (AUDIT_SCENARIOS.find(s => s.title === title) || AUDIT_SCENARIOS[0]);
  const sp = audit.speakers[idx];
  if (!sp) return;
  const msg = sp.effect();
  if (sp.correct) {
    assessmentQuality += 1;
    recordDailyTask('주민 말풍선 근거 선택 성공', `${audit.title} — ${sp.name}: ${sp.bubble}`);
  } else {
    recordDailyTask('주민 말풍선 검토 및 재확인', `${audit.title} — ${sp.name}의 발언을 검토했습니다.`);
  }
  activeTasks.phoneRinging = false;
  activeTasks.currentAudit = null;
  closeModal();
  updateWeatherHUD();
  updateAlertStrip();
  showDialogue(sp.correct ? `나 · ${sp.name} 근거 채택` : `나 · ${sp.name} 발언 검토`, msg);
}

// --- 센서 점검 ---
let cleanedCount = 0;
function openSensorRepairMinigame() {
  if (!activeTasks.sensorDirty) {
    showDialogue('나', '사업지 경계와 인근 주거지역의 대기질·소음 자료를 수집하고 있어.');
    return;
  }
  cleanedCount = 0;
  openModal(`
    <div class="modal-header"><span class="modal-title">📡 도심 대기질 센서망 원격 정비 단말기</span><button class="close-btn" onclick="closeModal()">닫기</button></div>
    <p style="font-size:0.92rem; color:#cfc9bc; margin-bottom:12px;">오류가 표시된 <strong>4개 측정 노드</strong>를 모두 클릭해 교정하세요!</p>
    <div class="sensor-grid">
      <div class="sensor-node dirty" id="node-1" onclick="cleanNode(1)">⚠️ 제1 부지 경계 센서<br><small>[미세먼지 막힘 - 클릭하여 세척]</small></div>
      <div class="sensor-node dirty" id="node-2" onclick="cleanNode(2)">⚠️ 주거지역 대기질 센서<br><small>[미세먼지 막힘 - 클릭하여 세척]</small></div>
      <div class="sensor-node dirty" id="node-3" onclick="cleanNode(3)">⚠️ 도로변 소음 센서<br><small>[미세먼지 막힘 - 클릭하여 세척]</small></div>
      <div class="sensor-node dirty" id="node-4" onclick="cleanNode(4)">⚠️ 하천변 환경 센서<br><small>[미세먼지 막힘 - 클릭하여 세척]</small></div>
    </div>
  `);
}

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
        showDialogue('나', '4개 지점의 환경 측정장비를 모두 점검했어!');
      }, 350);
    }
  }
}

// --- 노트북 정책 ---
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
    <div class="modal-header"><span class="modal-title">💻 환경영향 저감방안 검토 시스템 (잔여 예산: ${budget}억)</span><button class="close-btn" onclick="closeModal()">닫기</button></div>
    <p style="font-size:0.88rem; color:#c9b182; margin-bottom:12px;">※ 선택한 저감방안은 사업계획 반영과 협의 절차를 거쳐 <strong>2일 후</strong>부터 적용됩니다.</p>
    <div class="policy-grid">${cardsHtml}</div>
  `);
}

function confirmPolicy(policyId) {
  const p = POLICIES.find(item => item.id === policyId);
  openModal(`
    <div style="text-align:center; padding:20px 10px;">
      <h3 style="font-family:'Gowun Batang', serif; font-size:1.45rem; color:#f5e6c8; margin-bottom:12px;">"${p.name}"을(를) 선택하시겠습니까?</h3>
      <p style="color:#cfc9bc; font-size:0.98rem;">소요 예산: <strong>${p.cost}억</strong> | 적용 시점: <strong>${day + 2}일차 아침</strong></p>
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
  if (weather.type === 'HEAVY_RAIN') { activeTasks.phAlert = true; }

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
  openModal(`<div class="modal-header"><span class="modal-title">⚖️ ${index + 1}번 부지 환경영향평가 협의 의견</span><span style="font-size:0.8rem; color:#c9b182;">결정 필요</span></div>
    <div class="dossier-box"><div style="font-weight:700; margin-bottom:8px;">${dayRange} 평가 대상: ${f.name}</div>
    <h3>${f.facility}</h3><p style="line-height:1.7; margin:10px 0;">${f.benefit}</p>
    <p style="line-height:1.7; margin:10px 0;"><strong>주요 예상 환경영향</strong><br>${f.pollutants}</p>
    <p style="line-height:1.7; margin:10px 0;">${f.role}</p></div>
    <div style="display:grid; gap:10px; margin-top:14px;">
      <button class="choice-btn" onclick="decideFacility(${index}, 'standard')">① 협의 동의 · 기본 계획으로 사업 추진 (환경 부담 큼)</button>
      <button class="choice-btn" onclick="decideFacility(${index}, 'conditional')">② 조건부 동의 · 저감대책 이행을 전제로 사업 추진 (예산 18억)</button>
      <button class="choice-btn" onclick="decideFacility(${index}, 'reject')">③ 부동의 의견 · 입지/규모 대안 재검토 (사업 보류)</button>
    </div>`);
}

function decideFacility(index, decision) {
  if (facilityDecisions[index]) return;
  if (decision === 'conditional' && budget < 18) {
    showDialogue('나', '조건부 동의에 필요한 환경저감 예산이 부족해.');
    return;
  }
  const f = FACTORIES[index];
  facilityDecisions[index] = decision;
  if (decision === 'standard') {
    projectImpactScore += 2.1;
    recordDailyTask(`${f.facility} 기본 계획 협의 동의`, '기본 계획으로 사업이 추진됩니다.');
    pendingDayNotice = `${f.facility} 기본 계획 협의 동의.`;
  } else if (decision === 'conditional') {
    budget -= 18;
    projectImpactScore += 0.65;
    recordDailyTask(`${f.facility} 조건부 동의`, '환경관리 조건을 붙여 사업을 추진합니다.');
    pendingDayNotice = `${f.facility} 조건부 동의.`;
  } else {
    recordDailyTask(`${f.facility} 부동의 및 대안 재검토`, '사업이 보류되었습니다.');
    pendingDayNotice = `${f.facility} 사업은 부동의되었습니다.`;
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
  const rows = [
    { label: '도시에 꼭 필요한 시설이 모두 들어왔는가?', score: scores.utilityScore, detail: `${scores.builtCount}/3개 시설 건설` },
    { label: '도시의 환경오염 정도가 악화되지 않고 환경을 보존하였는가?', score: scores.environmentScore, detail: `누적 환경오염 위험도 ${scores.risk}% · 잔여 영향 지수 ${scores.netImpact}` }
  ];
  openModal(`<div class="modal-header"><span class="modal-title">📋 15일 최종 환경영향평가 결산</span></div>
    <div class="dossier-box"><h3>최종 협의 의견</h3>
      ${FACTORIES.map((f,i)=>`<div class="check-item"><span>${i+1}. ${f.facility}</span><strong>${facilityDecisions[i] === 'standard' ? '협의 동의' : facilityDecisions[i] === 'conditional' ? '조건부 동의' : '부동의'}</strong></div>`).join('')}
      <h3 style="margin-top:18px;">도시의 최종 평가 체크리스트</h3>
      ${rows.map(r=>`<div class="check-item" style="align-items:flex-start;"><span style="max-width:76%; line-height:1.6;">${r.label}<br><small>${r.detail}</small></span><strong style="font-size:1.45rem; min-width:34px; text-align:center;">${scoreMark(r.score)}</strong></div>`).join('')}
    </div><div style="text-align:center; margin-top:18px;"><button class="start-btn" onclick="checkCampaignEnd()">엔딩 보기</button></div>`);
}

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
    message = `15일 동안의 평가가 끝났어. 평가 결과에서 우수한 성과를 얻은 덕분에 도시는 환경을 보전할 기회를 지켜냈어.`;
  } else if (hasTriangle) {
    title = 'PARTIAL ENDING : 버텨내는 도시';
    message = `도시는 유지되고 있지만, 일부 개발사업의 환경 부담이 남아 있어.`;
  } else {
    title = 'BAD ENDING : 사막이 된 도시';
    message = `필요한 시설과 환경 보전, 두 가지 모두 놓치고 말았어.`;
  }
  openModal(`<div style="text-align:center; padding:15px;"><h2 style="font-family:'Cinzel', serif; font-size:1.8rem; color:#f3d59b; margin-bottom:14px;">${title}</h2>
    <div style="font-size:1.1rem; line-height:1.9; color:#f0ece1; margin-bottom:22px;">${message}</div>
    <button class="start-btn" onclick="location.reload()">처음부터 다시하기</button></div>`);
}

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

function pr(x, y, w, h, c) {
  g.fillStyle = c;
  g.fillRect(Math.round(x), Math.round(y), Math.max(1, Math.round(w)), Math.max(1, Math.round(h)));
}

function box(x, y, w, h, fill, line) {
  pr(x, y, w, h, line || INK);
  if (w > 2 && h > 2) pr(x + 1, y + 1, w - 2, h - 2, fill);
}

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

function rr(o) {
  return {
    x: Math.round(lw * o.relX),
    y: Math.round(lh * o.relY),
    w: Math.max(4, Math.round(lw * o.relW)),
    h: Math.max(4, Math.round(lh * o.relH))
  };
}

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

  for (let xx = 0; xx < lw; xx++) {
    const dy = Math.round(groundY - 2 - 3 * Math.sin(xx * 0.035 + 1) - 2 * Math.sin(xx * 0.09));
    pr(xx, dy, 1, groundY - dy + 2, endingType === 'desert' ? '#9b805e' : '#526b62');
    pr(xx, dy, 1, 1, '#82958a');
  }

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

  const tone = CITY_TONE[variant];
  if (tone) {
    g.globalCompositeOperation = 'source-atop';
    g.fillStyle = tone;
    g.fillRect(0, 0, lw, lh);
    g.globalCompositeOperation = 'source-over';
  }

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

function drawFrameAndDesk() {
  const fh = Math.round(lh * 0.65);
  const frame = '#2a2340';
  const frameHi = '#4a4066';
  const ink = '#100c18';

  g.globalAlpha = 0.07;
  for (let i = 0; i < 4; i++) {
    const px = Math.round(lw / 4 * i) + 10;
    for (let yy = 4; yy < fh - 6; yy++) pr(px + Math.round(yy * 0.35), yy, 3, 1, '#ffffff');
  }
  g.globalAlpha = 1;

  pr(0, 0, lw, 4, ink); pr(0, 1, lw, 2, frame); pr(0, 1, lw, 1, frameHi);
  pr(0, 0, 4, fh, ink); pr(1, 0, 2, fh, frame);
  pr(lw - 4, 0, 4, fh, ink); pr(lw - 3, 0, 2, fh, frame);
  pr(0, fh - 3, lw, 3, ink);
  for (let i = 1; i <= 3; i++) {
    const mx = Math.round(lw / 4 * i) - 2;
    pr(mx, 0, 4, fh, ink); pr(mx + 1, 0, 2, fh, frame); pr(mx + 1, 0, 1, fh, frameHi);
  }

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

function drawDeskObjects() {
  const T = Date.now() / 1000;
  const blink = Math.floor(Date.now() / 400) % 2 === 0;

  DESK_ITEMS.forEach(o => {
    const s = rr(o);
    pr(s.x + 1, s.y + s.h, s.w, 2, 'rgba(0,0,0,0.32)');
  });

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

  {
    const r = rr(DESK_ITEMS[2]);
    for (let i = 2; i >= 0; i--) box(r.x + i, r.y - i, r.w, r.h, i === 0 ? '#f7f3e8' : '#dcd3be');
    for (let yy = r.y + 4; yy < r.y + r.h - 8; yy += 3) pr(r.x + 3, yy, r.w - 8, 1, '#9a907a');
    pr(r.x + r.w - 9, r.y + r.h - 9, 6, 6, '#b3262e');
    pr(r.x + r.w - 8, r.y + r.h - 8, 4, 4, '#f7f3e8');
    pr(r.x + r.w - 7, r.y + r.h - 7, 2, 2, '#b3262e');
  }

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

  {
    const r = rr(DESK_ITEMS[5]);
    box(r.x, r.y, r.w, r.h, '#e9e2c9');
    pr(r.x + 2, r.y + 2, r.w - 4, r.h - 4, '#f6efd8');
    const ix = r.x + 3, iy = r.y + 3, iw = r.w - 6, ih = r.h - 6;
    pline(ix, iy + Math.round(ih * 0.72), ix + Math.round(iw * 0.35), iy + Math.round(ih * 0.48), '#4b9bc4');
    pline(ix + Math.round(iw * 0.35), iy + Math.round(ih * 0.48), ix + Math.round(iw * 0.78), iy + Math.round(ih * 0.62), '#4b9bc4');
    pline(ix + 1, iy + Math.round(ih * 0.22), ix + iw - 1, iy + Math.round(ih * 0.22), '#626b78');
    pr(ix + Math.round(iw * 0.08), iy + Math.round(ih * 0.08), Math.max(2, Math.round(iw * 0.22)), Math.max(2, Math.round(ih * 0.22)), '#8cad75');
    pr(ix + Math.round(iw * 0.62), iy + Math.round(ih * 0.08), Math.max(2, Math.round(iw * 0.28)), Math.max(2, Math.round(ih * 0.28)), '#b7a58b');
    pr(ix + Math.round(iw * 0.42), iy + Math.round(ih * 0.42), Math.max(3, Math.round(iw * 0.24)), Math.max(3, Math.round(ih * 0.3)), '#c85a52');
    pline(ix + Math.round(iw * 0.42), iy + 1, ix + Math.round(iw * 0.42), iy + ih - 1, '#b94b4b');
  }

  {
    const r = rr(DESK_ITEMS[6]);
    box(r.x, r.y, r.w, r.h, '#d8d0a8');
    pr(r.x + 2, r.y + 2, r.w - 4, r.h - 4, '#e6dfbf');
    const ix = r.x + 3, iy = r.y + 3, iw = r.w - 6, ih = r.h - 6;
    pline(ix, iy + Math.round(ih * 0.7), ix + Math.round(iw * 0.35), iy + Math.round(ih * 0.48), '#4b9bc4');
    pline(ix + Math.round(iw * 0.35), iy + Math.round(ih * 0.48), ix + Math.round(iw * 0.7), iy + Math.round(ih * 0.62), '#4b9bc4');
    pr(ix + 1, iy + 1, Math.max(2, Math.round(iw * 0.28)), Math.max(2, Math.round(ih * 0.3)), '#8cad75');
    pr(ix + Math.round(iw * 0.58), iy + 1, Math.max(2, Math.round(iw * 0.32)), Math.max(2, Math.round(ih * 0.36)), '#9ab77b');
    pline(ix + Math.round(iw * 0.45), iy + 1, ix + Math.round(iw * 0.45), iy + ih - 1, '#b94b4b');
    pline(ix + Math.round(iw * 0.45), iy + Math.round(ih * 0.5), ix + iw - 1, iy + Math.round(ih * 0.5), '#b94b4b');
    pr(ix + Math.round(iw * 0.42), iy + Math.round(ih * 0.42), 3, 3, '#b3262e');
  }

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

  {
    const r = rr(DESK_ITEMS[9]);
    box(r.x, r.y, r.w, r.h, '#f5efe2');
    pr(r.x + 1, r.y + 1, r.w - 2, Math.round(r.h * 0.28), '#b3262e');
    pr(r.x + 3, r.y - 1, 2, 3, '#2a2430');
    pr(r.x + r.w - 5, r.y - 1, 2, 3, '#2a2430');
    pr(r.x + 3, r.y + r.h - 4, r.w - 6, 1, '#cfc7b4');
  }

  {
    const r = rr(DESK_ITEMS[10]); box(r.x, r.y, r.w, r.h, '#315d43'); shade(r.x, r.y, r.w, r.h, '#6c9a65', '#203b31');
    pr(r.x+3,r.y+3,r.w-6,2,'#c4d7a1'); pr(r.x+Math.floor(r.w*.25),r.y+Math.floor(r.h*.35),3,4,'#7ecb75');
    pr(r.x+Math.floor(r.w*.55),r.y+Math.floor(r.h*.3),3,5,'#a9d18e'); pr(r.x+Math.floor(r.w*.72),r.y+Math.floor(r.h*.55),3,3,'#f0d77a');
  }
  {
    const r = rr(DESK_ITEMS[11]); box(r.x, r.y, r.w, r.h, '#343d4d'); shade(r.x, r.y, r.w, r.h, '#687c91', '#202735');
    pr(r.x+3,r.y+3,r.w-6,r.h-6,'#172b3c');
    for(let k=0;k<5;k++) pline(r.x+4,r.y+Math.floor(r.h*(.25+k*.12)),r.x+r.w-4,r.y+Math.floor(r.h*(.25+k*.12)),k===2?'#e5a14a':'#587a91');
    pr(r.x+Math.floor(r.w*.48),r.y+Math.floor(r.h*.25),3,3,'#f3c969');
  }
  {
    const r = rr(DESK_ITEMS[12]); box(r.x, r.y, r.w, r.h, '#6d5940'); shade(r.x, r.y, r.w, r.h, '#a58b62','#3b3028');
    pr(r.x+3,r.y+3,r.w-6,r.h-6,'#d7c9a5');
    pr(r.x+Math.floor(r.w*.2),r.y+Math.floor(r.h*.25),Math.max(3,Math.floor(r.w*.22)),Math.max(3,Math.floor(r.h*.25)),'#579b69');
    pr(r.x+Math.floor(r.w*.58),r.y+Math.floor(r.h*.48),Math.max(3,Math.floor(r.w*.22)),Math.max(3,Math.floor(r.h*.25)),'#579b69');
  }
  {
    const r = rr(DESK_ITEMS[13]); box(r.x, r.y, r.w, r.h, '#344d63'); shade(r.x, r.y, r.w, r.h, '#7895a7','#1e2b3c');
    pr(r.x+3,r.y+3,r.w-6,r.h-6,'#dce6df');
    pline(r.x+Math.floor(r.w*.25),r.y+Math.floor(r.h*.5),r.x+Math.floor(r.w*.75),r.y+Math.floor(r.h*.5),'#4b9bc4');
    pr(r.x+Math.floor(r.w*.48),r.y+Math.floor(r.h*.3),3,3,'#d96b55');
  }
}

function presentBuffer(withText) {
  ctx.imageSmoothingEnabled = false;
  ctx.drawImage(pcan, 0, 0, lw, lh, 0, 0, width, height);

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

function drawTitleSky() {
  pixelBands(0, lh, [[0, '#0a0d2a'], [0.38, '#222a6b'], [0.62, '#526b86'], [0.8, '#b7a18a'], [1, '#e5c9a6']], 3);
  drawMoon(Math.round(lw * 0.5), Math.round(lh * 0.36), Math.round(Math.min(lw, lh) * 0.15));
}

function drawTitleCity() {
  const r = makeRng(23);
  const baseY = Math.round(lh * 0.79);
  const list = [
    { x: 0.12, w: 0.045, h: 0.24 }, { x: 0.19, w: 0.055, h: 0.34 }, { x: 0.27, w: 0.04, h: 0.2 },
    { x: 0.34, w: 0.06, h: 0.42 }, { x: 0.43, w: 0.045, h: 0.28 }, { x: 0.5, w: 0.06, h: 0.46 },
    { x: 0.59, w: 0.055, h: 0.32 }, { x: 0.67, w: 0.045, h: 0.25 }, { x: 0.75, w: 0.055, h: 0.38 },
    { x: 0.84, w: 0.04, h: 0.22 }
  ];
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
    if (b.h > 0.3) { pr(bx + 2, by - 2, bw - 4, 2, '#0e1230'); pr(bx + Math.floor(bw / 2), by - 5, 1, 3, '#0e1230'); }
  });
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
      gameMinutes += deltaSec * 12 * timeMultiplier;

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
