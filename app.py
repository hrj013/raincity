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
<title>Rain City - Art Style</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=DungGeunMo&display=swap');

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
    background-color: #121018;
    font-family: 'DungGeunMo', monospace;
    color: #f0ece1;
  }

  #game-container {
    position: relative;
    width: 100vw;
    height: 100vh;
    overflow: hidden;
    background: #121018;
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

  /* 레트로 윈도우 UI 패널 */
  .retro-window {
    background: #191424;
    border: 3px solid #ff758f;
    box-shadow: 4px 4px 0px #ff2a5f, 8px 8px 0px #0b0a10;
    border-radius: 2px;
    padding: 20px;
    position: relative;
  }

  .window-titlebar {
    background: linear-gradient(90deg, #ff758f, #7928ca);
    color: #fff;
    padding: 4px 10px;
    font-size: 0.9rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: -20px -20px 16px -20px;
    border-bottom: 2px solid #ff2a5f;
  }

  .window-controls span {
    display: inline-block;
    width: 12px;
    height: 12px;
    background: #ff2a5f;
    border: 1px solid #fff;
    margin-left: 4px;
    text-align: center;
    font-size: 8px;
    line-height: 10px;
    cursor: pointer;
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
    background: #121018;
    transition: opacity 1.2s ease;
  }

  .title-logo {
    font-size: clamp(3.5rem, 7vw, 6rem);
    color: #ff758f;
    text-shadow: 4px 4px 0px #7928ca, 8px 8px 0px #0b0a10;
    margin-bottom: 10px;
    letter-spacing: 3px;
  }

  .title-sub {
    font-size: 1.1rem;
    color: #b19cd9;
    margin-bottom: 40px;
    letter-spacing: 1px;
  }

  .start-btn {
    font-family: 'DungGeunMo', monospace;
    font-size: 1.4rem;
    padding: 14px 45px;
    background: #7928ca;
    color: #fff;
    border: 3px solid #ff758f;
    box-shadow: 5px 5px 0px #ff2a5f;
    cursor: pointer;
    transition: 0.1s;
  }

  .start-btn:hover {
    background: #9d4edd;
    transform: translate(-2px, -2px);
    box-shadow: 7px 7px 0px #ff2a5f;
  }

  /* 우측 상단 시계 HUD */
  #hud-clock {
    position: absolute;
    top: 16px;
    right: 20px;
    z-index: 15;
    background: #191424;
    border: 3px solid #00f5d4;
    box-shadow: 3px 3px 0px #0b0a10;
    padding: 10px 16px;
    display: none;
    align-items: center;
    gap: 12px;
  }

  .clock-day {
    font-size: 1.1rem;
    color: #00f5d4;
  }

  .clock-time {
    font-size: 1rem;
    color: #ff758f;
    background: #0b0a10;
    padding: 3px 8px;
    border: 2px solid #7928ca;
  }

  .speed-btn {
    font-family: 'DungGeunMo', monospace;
    background: #241e38;
    border: 2px solid #00f5d4;
    color: #e2dfd2;
    font-size: 0.8rem;
    padding: 3px 6px;
    cursor: pointer;
  }

  .speed-btn.active {
    background: #00f5d4;
    color: #0b0a10;
    border-color: #fff;
  }

  /* 좌측 상단 기상 HUD */
  #hud-weather {
    position: absolute;
    top: 16px;
    left: 20px;
    z-index: 15;
    background: #191424;
    border: 3px solid #ff758f;
    box-shadow: 3px 3px 0px #0b0a10;
    padding: 10px 16px;
    display: none;
    font-size: 0.9rem;
    line-height: 1.5;
  }

  /* 긴급 알림 배지 */
  #alert-strip {
    position: absolute;
    top: 105px;
    left: 20px;
    z-index: 15;
    display: none;
    flex-direction: column;
    gap: 8px;
  }

  .alert-pill {
    background: #ff2a5f;
    border: 2px solid #fff;
    color: #fff;
    padding: 6px 12px;
    font-size: 0.85rem;
    cursor: pointer;
    box-shadow: 3px 3px 0px #0b0a10;
  }

  /* 하단 대화창 */
  #dialogue-box {
    position: absolute;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    width: min(820px, 92vw);
    z-index: 25;
    background: #191424;
    border: 4px solid #b19cd9;
    box-shadow: 6px 6px 0px #0b0a10;
    padding: 16px 22px;
    display: none;
    cursor: pointer;
  }

  .speaker-tag {
    display: inline-block;
    background: #ff758f;
    color: #0b0a10;
    font-size: 0.9rem;
    font-weight: bold;
    padding: 3px 10px;
    border: 2px solid #fff;
    margin-bottom: 8px;
  }

  .dialogue-text {
    font-size: 1.05rem;
    line-height: 1.6;
    color: #f0ece1;
  }

  .dialogue-next {
    text-align: right;
    font-size: 0.78rem;
    color: #00f5d4;
    margin-top: 6px;
  }

  /* 모달 오버레이 */
  #modal-backdrop {
    position: absolute;
    inset: 0;
    background: rgba(11, 10, 16, 0.85);
    z-index: 30;
    display: none;
    align-items: center;
    justify-content: center;
  }

  .modal-card {
    width: min(740px, 92vw);
    max-height: 86vh;
    overflow-y: auto;
  }

  .close-btn {
    font-family: 'DungGeunMo', monospace;
    background: #ff2a5f;
    border: 2px solid #fff;
    color: #fff;
    font-size: 0.9rem;
    padding: 2px 8px;
    cursor: pointer;
  }

  .newspaper-sheet {
    background: #e2d7be;
    color: #211c16;
    padding: 24px;
    border: 3px solid #7928ca;
  }

  .news-head {
    text-align: center;
    border-bottom: 3px double #211c16;
    padding-bottom: 8px;
    margin-bottom: 14px;
  }

  .dossier-box {
    background: #191424;
    color: #f0ece1;
    padding: 20px;
    border: 3px solid #7928ca;
  }

  .check-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 12px;
    margin: 8px 0;
    background: #241e38;
    border: 2px solid #b19cd9;
    font-size: 1rem;
  }

  .policy-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 12px;
  }

  .policy-card {
    background: #121018;
    border: 2px solid #7928ca;
    padding: 14px;
    cursor: pointer;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }

  .policy-card:hover:not(.disabled) {
    border-color: #00f5d4;
    background: #1f1a2d;
  }

  .policy-card.disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .badge-status {
    display: inline-block;
    font-size: 0.75rem;
    padding: 2px 6px;
    margin-top: 8px;
    border: 1px solid #7928ca;
  }

  .badge-active { background: #00f5d4; color: #121018; }
  .badge-pending { background: #ffb703; color: #121018; }
  .badge-ready { background: #7928ca; color: #fff; }

  .mixer-box {
    background: #121018;
    border: 3px solid #00f5d4;
    padding: 20px;
    text-align: center;
    margin-top: 10px;
  }

  .action-btn {
    font-family: 'DungGeunMo', monospace;
    padding: 10px 22px;
    background: #7928ca;
    color: #fff;
    border: 2px solid #ff758f;
    box-shadow: 3px 3px 0px #ff2a5f;
    cursor: pointer;
    font-size: 1rem;
  }

  .choice-btn {
    font-family: 'DungGeunMo', monospace;
    display: block;
    width: 100%;
    text-align: left;
    background: #1f1a2d;
    border: 2px solid #7928ca;
    color: #f0ece1;
    padding: 12px 16px;
    margin-bottom: 10px;
    cursor: pointer;
    font-size: 0.95rem;
  }

  .choice-btn:hover {
    border-color: #00f5d4;
  }

  #hover-tooltip {
    position: absolute;
    pointer-events: none;
    background: #191424;
    border: 2px solid #ff758f;
    color: #00f5d4;
    padding: 4px 10px;
    font-size: 0.8rem;
    z-index: 18;
    display: none;
    transform: translate(-50%, -140%);
    white-space: nowrap;
    box-shadow: 3px 3px 0px #ff2a5f;
  }
</style>
</head>
<body>

<div id="game-container">
  <canvas id="gameCanvas"></canvas>

  <!-- 타이틀 화면 -->
  <div id="title-overlay">
    <div class="title-logo">RAIN CITY</div>
    <div class="title-sub">디스토피아 사막 도시, 감성 레트로 환경경영 시뮬레이션</div>
    <button class="start-btn" onclick="startZoomInSequence()">도시로 출근하기 ▶</button>
  </div>

  <!-- 좌측 상단 기상 HUD -->
  <div id="hud-weather"></div>

  <!-- 긴급 알림 배지 -->
  <div id="alert-strip"></div>

  <!-- 우측 상단 시계 HUD -->
  <div id="hud-clock">
    <span class="clock-day" id="clock-day-text">1일차</span>
    <span class="clock-time" id="clock-time-text">07:00</span>
    <div>
      <button class="speed-btn active" id="spd-1" onclick="setSpeed(1)">1x</button>
      <button class="speed-btn" id="spd-3" onclick="setSpeed(3)">3x</button>
      <button class="speed-btn" id="spd-10" onclick="setSpeed(10)">10x</button>
    </div>
  </div>

  <!-- 툴팁 -->
  <div id="hover-tooltip"></div>

  <!-- 하단 대화창 -->
  <div id="dialogue-box" onclick="closeDialogue()">
    <div class="speaker-tag" id="dialogue-speaker">나</div>
    <div class="dialogue-text" id="dialogue-text"></div>
    <div class="dialogue-next">▼ 클릭해서 계속</div>
  </div>

  <!-- 모달 창 -->
  <div id="modal-backdrop">
    <div class="retro-window modal-card" id="modal-content"></div>
  </div>
</div>

<script>
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

let width, height;
function resize() {
  width = canvas.width = window.innerWidth;
  height = canvas.height = window.innerHeight;
}
window.addEventListener('resize', resize);
resize();

let scene = 'TITLE'; // 'TITLE' -> 'ZOOM_IN' -> 'OFFICE' -> 'ENDING'
let day = 1;
let month = 1;
let gameMinutes = 7 * 60; 
let timeMultiplier = 1;   
let lastTimestamp = 0;
let isPaused = false;

let budget = 250;
let droughtLevel = 68; 
let totalRainDays = 0;
let acidRainDays = 0;

let zoomProgress = 0; // 0.0 ~ 1.0

let weather = {
  type: 'CLEAR',       // CLEAR, DROUGHT, DUST, HEAVY_RAIN, RAIN
  cloudType: 'WARM',
  windDir: '북서풍',
  windSpeed: 3.2,
  humidity: 32,
  temp: 36,
  rainProb: 15,
  so2: 75,
  nox: 65,
  pm25: 80,
  ph: 4.6,
  ecoHealth: 45
};

let activeTasks = {
  phPrepared: false,       
  sensorDirty: false,      
  phoneRinging: false,     
  currentAudit: null
};

const POLICIES = [
  { id: 'fgd', name: '배연탈황설비 (FGD)', cost: 45, desc: '공장 SO₂를 줄여 산성비 위험을 낮춰줍니다.', status: 'READY', applyDay: null },
  { id: 'esp', name: '전기집진기 (ESP)', cost: 40, desc: '초미세먼지(PM2.5)를 잡아서 공기를 맑게 해줘요.', status: 'READY', applyDay: null },
  { id: 'sensor', name: '정밀 대기질 센서망', cost: 25, desc: '도시 대기 상태와 강수 pH를 실시간으로 보여줍니다.', status: 'READY', applyDay: null },
  { id: 'raingarden', name: '빗물정원 조성', cost: 30, desc: '빗물이 땅에 스며들게 해 홍수와 오염물 유출을 막아요.', status: 'READY', applyDay: null },
  { id: 'permeable', name: '투수성 포장 도로', cost: 35, desc: '아스팔트를 빗물이 통하는 재질로 바꿔줍니다.', status: 'READY', applyDay: null },
  { id: 'reservoir', name: '지하 빗물저류조', cost: 50, desc: '빗물을 모아두었다가 가뭄 때 꺼내 쓸 수 있어요.', status: 'READY', applyDay: null },
  { id: 'seeding', name: '인공강우 시딩 장비', cost: 55, desc: '구름에 촉매를 뿌려 강수 확률을 확 높여줍니다.', status: 'READY', applyDay: null }
];

// 1번째 이미지 감성을 담은 만화풍 도시 구조물 정의
const CITY_BUILDINGS = [
  { x: 0.15, y: 0.35, w: 0.18, h: 0.22, type: 'factory_major', color: '#8b4532' },
  { x: 0.65, y: 0.32, w: 0.16, h: 0.25, type: 'factory_castle', color: '#3d6b5c' },
  { x: 0.42, y: 0.48, w: 0.14, h: 0.18, type: 'factory_center', color: '#c49a45' },
  { x: 0.05, y: 0.52, w: 0.12, h: 0.16, type: 'houses', color: '#a0523d' },
  { x: 0.32, y: 0.55, w: 0.12, h: 0.15, type: 'houses', color: '#b26b48' },
  { x: 0.82, y: 0.50, w: 0.13, h: 0.17, type: 'houses', color: '#9e5a47' }
];

// 2번째 이미지 감성: 책상을 화면 정중앙에 배치
const DESK_ITEMS = [
  { id: 'beaker', name: '🧪 pH 배합기 (산성비 중화 준비)', relX: 0.22, relY: 0.65, relW: 0.07, relH: 0.16 },
  { id: 'radio', name: '🛩️ 인공강우 무전기 (비 내리기)', relX: 0.31, relY: 0.65, relW: 0.07, relH: 0.15 },
  { id: 'newspaper', name: '📰 조간신문', relX: 0.24, relY: 0.77, relW: 0.11, relH: 0.11 },
  { id: 'documents', name: '📁 서류 더미 (목표 체크리스트)', relX: 0.39, relY: 0.71, relW: 0.11, relH: 0.14 },
  { id: 'laptop', name: '💻 업무용 노트북 (정책 구매)', relX: 0.52, relY: 0.63, relW: 0.14, relH: 0.18 },
  { id: 'sensor_pad', name: '📡 대기질 센서 정비기', relX: 0.68, relY: 0.67, relW: 0.07, relH: 0.13 },
  { id: 'photo', name: '🖼️ 가족사진', relX: 0.77, relY: 0.73, relW: 0.05, relH: 0.10 },
  { id: 'phone', name: '☎️ 민원 전화기', relX: 0.83, relY: 0.62, relW: 0.07, relH: 0.10 }
];

const AUDIT_SCENARIOS = [
  {
    title: "제2 플랜트 야간 무단 배출 제보",
    desc: "야밤에 몰래 필터를 끄고 황가스를 뿜어냈다는 제보가 들어왔어! 어떻게 할까?",
    choices: [
      { text: "당장 들이닥쳐서 과태료 25억 뜯어내고 연기 줄이기!", effect: () => { budget += 25; weather.so2 = Math.max(10, weather.so2 - 15); return "흐흐, 꼬리를 잡았지! 25억 벌고 공장 콧대를 납작하게 눌러줬어."; } },
      { text: "경고장만 툭 던져주고 조용히 넘어가기", effect: () => { weather.so2 = Math.max(10, weather.so2 - 5); return "경고장 먹더니 당분간은 눈치 보며 살겠지 뭐."; } }
    ]
  },
  {
    title: "왕실 건설청의 예산 압박",
    desc: "신도시 공업용수 모자라다고 인공강우 예산 좀 떼달라는데 이거 원...",
    choices: [
      { text: "내 완벽한 수자원 보고서로 콧대를 꺾고 15억 더 받아내기!", effect: () => { budget += 15; return "데이터로 팩폭을 날려줬더니 오히려 15억을 더 쥐여주네? 땡큐지!"; } },
      { text: "예산 조금 양보하고 살수차 지원받기", effect: () => { droughtLevel = Math.max(5, droughtLevel - 3); return "아쉽지만 살수차로 도로 먼지라도 좀 씻어내야지."; } }
    ]
  }
];

let dustParticles = [];
for (let i = 0; i < 100; i++) {
  dustParticles.push({
    x: Math.random() * 3000,
    y: Math.random() * 2000,
    speedX: 1.5 + Math.random() * 4,
    speedY: -0.3 + Math.random() * 1,
    size: 1.5 + Math.random() * 3,
    alpha: 0.3 + Math.random() * 0.4
  });
}

// 빗소리/비 내리기 입자
let raindrops = [];
for (let i = 0; i < 150; i++) {
  raindrops.push({
    x: Math.random() * window.innerWidth,
    y: Math.random() * window.innerHeight,
    speed: 12 + Math.random() * 8,
    len: 15 + Math.random() * 15
  });
}

function setSpeed(spd) {
  timeMultiplier = spd;
  document.querySelectorAll('.speed-btn').forEach(b => b.classList.remove('active'));
  document.getElementById(`spd-${spd}`).classList.add('active');
}

function startZoomInSequence() {
  const overlay = document.getElementById('title-overlay');
  overlay.style.opacity = '0';
  setTimeout(() => {
    overlay.style.display = 'none';
    scene = 'ZOOM_IN';
    zoomProgress = 0;
  }, 1000);
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
  document.getElementById('modal-content').innerHTML = `
    <div class="window-titlebar">
      <span>SYSTEM WINDOW</span>
      <div class="window-controls"><span onclick="closeModal()">×</span></div>
    </div>
    ${htmlContent}
  `;
  document.getElementById('modal-backdrop').style.display = 'flex';
}

function closeModal() {
  document.getElementById('modal-backdrop').style.display = 'none';
  if (document.getElementById('dialogue-box').style.display !== 'block') {
    isPaused = false;
  }
}

function updateAlertStrip() {
  const strip = document.getElementById('alert-strip');
  let alerts = [];
  if (!activeTasks.phPrepared) {
    alerts.push(`<div class="alert-pill" onclick="handleObjectClick('beaker')">🧪 [pH 배합기]로 먼저 중화 준비를 해주세요!</div>`);
  }
  if (activeTasks.sensorDirty) {
    alerts.push(`<div class="alert-pill" onclick="handleObjectClick('sensor_pad')">📡 [센서 정비기] 모래바람으로 오류 발생!</div>`);
  }
  if (activeTasks.phoneRinging) {
    alerts.push(`<div class="alert-pill" onclick="handleObjectClick('phone')">☎️ [민원 전화기]가 울리고 있어요!</div>`);
  }
  if (alerts.length > 0) {
    strip.innerHTML = alerts.join('');
    strip.style.display = 'flex';
  } else {
    strip.style.display = 'none';
  }
}

function getChecklistStatus() {
  const acidFreq = totalRainDays === 0 ? 12.0 : (acidRainDays / Math.max(1, day)) * 100;
  return {
    check1: droughtLevel < 30,
    check2: acidFreq < 10,
    acidFreq: acidFreq.toFixed(1)
  };
}

function handleObjectClick(id) {
  if (id === 'newspaper') {
    openModal(`
      <div style="margin-bottom:10px; font-size:1.1rem; color:#ff758f;">📰 레인 시티 조간신문</div>
      <div class="newspaper-sheet">
        <div class="news-head">
          <h2 style="font-size:1.3rem;">"비가 오지 않는 사막 도시의 눈물"</h2>
        </div>
        <p style="line-height:1.6; font-size:0.95rem;">
          모래바람과 매연으로 뒤덮인 이 도시에 구원투수로 환경공학자가 부임했다.
          과연 30일 안에 이 지독한 가뭄을 끝내고 푸른 하늘을 되찾아줄 수 있을 것인가?
        </p>
      </div>
    `);
  }
  else if (id === 'documents') {
    const status = getChecklistStatus();
    openModal(`
      <div style="margin-bottom:10px; font-size:1.1rem; color:#00f5d4;">📁 예산 및 목표 체크리스트</div>
      <div class="dossier-box">
        <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:2px solid #7928ca; padding-bottom:8px; margin-bottom:12px;">
          <span>💰 남은 예산</span>
          <span style="font-size:1.3rem; color:#00f5d4; font-weight:bold;">${budget} 억</span>
        </div>
        <h3 style="margin-bottom:8px; color:#ff758f;">📋 30일차 최종 평가 목표</h3>
        <div class="check-item">
          <span>1. 가뭄 진행도 30% 미만 (현재: ${droughtLevel.toFixed(1)}%)</span>
          <span>${status.check1 ? '✅ 달성' : '⬜ 진행중'}</span>
        </div>
        <div class="check-item">
          <span>2. 산성비 빈도 10% 미만 (현재: ${status.acidFreq}%)</span>
          <span>${status.check2 ? '✅ 달성' : '⬜ 진행중'}</span>
        </div>
      </div>
    `);
  }
  else if (id === 'laptop') { renderLaptopModal(); }
  else if (id === 'beaker') { openPhMixerMinigame(); }
  else if (id === 'radio') { openSeedingMinigame(); }
  else if (id === 'sensor_pad') { openSensorRepairMinigame(); }
  else if (id === 'phone') { openAuditPhoneModal(); }
  else if (id === 'photo') { showDialogue('나', '지갑 속 가족사진... 힘들 때마다 이거 보면서 버티는 거지 뭐.'); }
}

function openPhMixerMinigame() {
  if (activeTasks.phPrepared) {
    showDialogue('나', '이미 알칼리 중화제 배합을 깔끔하게 끝내놨지!');
    return;
  }
  openModal(`
    <div style="margin-bottom:10px; font-size:1.1rem; color:#00f5d4;">🧪 pH 배합기 (산성비 사전 중화)</div>
    <p style="font-size:0.9rem; color:#ff758f; margin-bottom:12px;">슬라이더를 움직여 알칼리 중화제를 딱 맞는 양으로 배합해봐.</p>
    <div class="mixer-box">
      <p style="font-size:1.1rem; margin-bottom:10px;">소석회 투입량: <span id="mix-val" style="color:#00f5d4; font-size:1.3rem;">150</span> kg</p>
      <input type="range" id="mix-slider" min="50" max="250" value="150" style="width:85%; cursor:pointer;"
             oninput="document.getElementById('mix-val').innerText = this.value">
      <p style="font-size:0.8rem; color:#b19cd9; margin-top:10px;">(목표 중성 구간: 120 ~ 180kg)</p>
    </div>
    <div style="text-align:center; margin-top:18px;">
      <button class="action-btn" onclick="executeMixer()">✨ 배합 완료 및 저장고 세팅하기</button>
    </div>
  `);
}

function executeMixer() {
  const val = parseInt(document.getElementById('mix-slider').value);
  closeModal();
  activeTasks.phPrepared = true;
  showDialogue('나', `완벽한 황금 비율(${val}kg)로 중화 세팅을 완료했어! 비가 와도 안전하다구.`);
  updateAlertStrip();
}

function openSeedingMinigame() {
  if (!activeTasks.phPrepared) {
    showDialogue('나', '먼저 [pH 배합기]로 중화 세팅을 끝내야 산성비 피해를 막을 수 있어!');
    return;
  }
  openModal(`
    <div style="margin-bottom:10px; font-size:1.1rem; color:#00f5d4;">🛩️ 인공강우 작전 무전기</div>
    <div style="margin-bottom:12px; background:#121018; padding:12px; border:2px solid #7928ca;">
      <label style="margin-right:15px; cursor:pointer;"><input type="radio" name="seedChoice" value="WARM" checked> 🧂 흡습성 입자</label>
      <label style="cursor:pointer;"><input type="radio" name="seedChoice" value="COLD"> ❄️ 빙정핵 입자</label>
    </div>
    <div style="text-align:center;">
      <button class="action-btn" onclick="fireSeeding()">🚀 인공강우 작전 개시! (10억)</button>
    </div>
  `);
}

function fireSeeding() {
  if (budget < 10) {
    closeModal();
    showDialogue('나', '출격 비용 10억이 모자라네...');
    return;
  }
  budget -= 10;
  activeTasks.phPrepared = false;
  closeModal();

  weather.type = 'RAIN'; // 인공강우 성공 -> 비 내림 이벤트 즉시 발생
  totalRainDays++;
  droughtLevel = Math.max(5, droughtLevel - 15);
  showDialogue('나', '인공강우 작전 대성공! 통유리창 밖에 시원한 비가 내리기 시작한다!');
  updateWeatherHUD();
  updateAlertStrip();
}

function openSensorRepairMinigame() {
  if (!activeTasks.sensorDirty) {
    showDialogue('나', '센서 모두 아주 정상적으로 작동 중이야.');
    return;
  }
  openModal(`
    <div style="margin-bottom:10px; font-size:1.1rem; color:#ff758f;">📡 대기질 센서 정비기</div>
    <p style="font-size:0.9rem; color:#f0ece1; margin-bottom:12px;">모래바람으로 먹통이 된 센서 4개를 클릭해서 정비해줘!</p>
    <div style="display:grid; grid-template-columns:repeat(2, 1fr); gap:10px;">
      <div id="sn-1" class="choice-btn" onclick="cleanSensor(1)">⚠️ 1번 발전소 센서</div>
      <div id="sn-2" class="choice-btn" onclick="cleanSensor(2)">⚠️ 2번 석유화학 센서</div>
      <div id="sn-3" class="choice-btn" onclick="cleanSensor(3)">⚠️ 3번 제련소 센서</div>
      <div id="sn-4" class="choice-btn" onclick="cleanSensor(4)">⚠️ 4번 주거구역 센서</div>
    </div>
  `);
}

let cleanedSensors = 0;
function cleanSensor(idx) {
  const el = document.getElementById(`sn-${idx}`);
  if (el && !el.dataset.cleaned) {
    el.dataset.cleaned = "true";
    el.style.background = "#00f5d4";
    el.style.color = "#121018";
    el.innerHTML = "✅ 정상 작동 중";
    cleanedSensors++;
    if (cleanedSensors >= 4) {
      cleanedSensors = 0;
      activeTasks.sensorDirty = false;
      budget += 10;
      setTimeout(() => {
        closeModal();
        updateAlertStrip();
        showDialogue('나', '모든 센서 청소 완료! 연구 수당 10억 획득!');
      }, 300);
    }
  }
}

function openAuditPhoneModal() {
  if (!activeTasks.phoneRinging || !activeTasks.currentAudit) {
    showDialogue('나', '걸려온 전화가 없어.');
    return;
  }
  const audit = activeTasks.currentAudit;
  openModal(`
    <div style="margin-bottom:10px; font-size:1.1rem; color:#ff758f;">☎️ [긴급 전화] ${audit.title}</div>
    <p style="font-size:0.95rem; line-height:1.6; color:#f0ece1; margin-bottom:16px;">"${audit.desc}"</p>
    <button class="choice-btn" onclick="resolveAudit(0)">1. ${audit.choices[0].text}</button>
    <button class="choice-btn" onclick="resolveAudit(1)">2. ${audit.choices[1].text}</button>
  `);
}

function resolveAudit(idx) {
  const msg = activeTasks.currentAudit.choices[idx].effect();
  activeTasks.phoneRinging = false;
  activeTasks.currentAudit = null;
  closeModal();
  updateWeatherHUD();
  updateAlertStrip();
  showDialogue('나', msg);
}

function renderLaptopModal() {
  let cardsHtml = POLICIES.map(p => {
    let badge = '';
    let disabled = '';
    let clickAttr = `onclick="confirmPolicy('${p.id}')"`;

    if (p.status === 'ACTIVE') {
      badge = `<span class="badge-status badge-active">✔ 설치 완료</span>`;
      disabled = 'disabled';
      clickAttr = '';
    } else if (p.status === 'PENDING') {
      badge = `<span class="badge-status badge-pending">⏳ 시공 중 (${p.applyDay}일차)</span>`;
      disabled = 'disabled';
      clickAttr = '';
    } else if (budget < p.cost) {
      badge = `<span class="badge-status badge-ready">예산 부족 (${p.cost}억)</span>`;
      disabled = 'disabled';
      clickAttr = '';
    } else {
      badge = `<span class="badge-status badge-ready">설치 가능 (${p.cost}억)</span>`;
    }

    return `
      <div class="policy-card ${disabled}" ${clickAttr}>
        <div>
          <div style="font-weight:bold; font-size:0.95rem; color:#00f5d4; margin-bottom:4px;">${p.name}</div>
          <div style="font-size:0.8rem; color:#b19cd9; line-height:1.4;">${p.desc}</div>
        </div>
        <div>${badge}</div>
      </div>
    `;
  }).join('');

  openModal(`
    <div style="margin-bottom:10px; font-size:1.1rem; color:#00f5d4;">💻 환경 정책 구매 터미널 (예산: ${budget}억)</div>
    <div class="policy-grid">${cardsHtml}</div>
  `);
}

function confirmPolicy(id) {
  const p = POLICIES.find(item => item.id === id);
  openModal(`
    <div style="text-align:center; padding:10px;">
      <h3 style="font-size:1.1rem; color:#ff758f; margin-bottom:10px;">"${p.name}"을(를) 설치할까요?</h3>
      <p style="font-size:0.9rem; color:#b19cd9; margin-bottom:20px;">비용: ${p.cost}억 | 적용: ${day + 2}일차</p>
      <button class="action-btn" onclick="executePolicy('${p.id}')">설치 승인</button>
    </div>
  `);
}

function executePolicy(id) {
  const p = POLICIES.find(item => item.id === id);
  if (budget >= p.cost && p.status === 'READY') {
    budget -= p.cost;
    p.status = 'PENDING';
    p.applyDay = day + 2;
    renderLaptopModal();
  }
}

function simulateNewDay() {
  POLICIES.forEach(p => {
    if (p.status === 'PENDING' && day >= p.applyDay) {
      p.status = 'ACTIVE';
    }
  });

  const roll = Math.random() * 100;
  if (roll < 15) {
    weather.type = 'DUST';
    activeTasks.sensorDirty = true;
    cleanedSensors = 0;
  } else if (roll < 30) {
    weather.type = 'DROUGHT';
  } else if (roll < 40) {
    weather.type = 'HEAVY_RAIN';
  } else {
    weather.type = 'CLEAR';
  }

  if (!activeTasks.phoneRinging && Math.random() < 0.4) {
    activeTasks.phoneRinging = true;
    activeTasks.currentAudit = AUDIT_SCENARIOS[Math.floor(Math.random() * AUDIT_SCENARIOS.length)];
  }

  updateWeatherHUD();
  updateAlertStrip();
}

function updateWeatherHUD() {
  const hud = document.getElementById('hud-weather');
  const names = {
    'CLEAR': '☀️ 맑음 (사막 건조)',
    'DROUGHT': '🔥 극심한 폭염 가뭄',
    'DUST': '🌪️ 모래바람(황사) 경보',
    'HEAVY_RAIN': '⛈️ 국지성 폭우',
    'RAIN': '🌧️ 인공강우 단비 내리는 중'
  };
  hud.innerHTML = `
    <div style="font-weight:bold; color:#ff758f;">${names[weather.type]}</div>
    <div style="font-size:0.8rem; color:#b19cd9;">습도: ${weather.humidity}% | 기온: ${weather.temp}°C</div>
  `;
}

// --- 1번째 이미지풍 앤티크 만화풍 도시 배경 렌더링 (시간대별/날씨별 변화) ---
function drawCartoonCity(ctx, x, y, w, h, timeHour, weatherType) {
  ctx.save();
  ctx.translate(x, y);

  // 시간대에 따른 하늘 색상 변화 (아침/낮/노을/밤)
  let skyTop = '#e09f63', skyBottom = '#f4d0a1';
  if (timeHour >= 18 || timeHour < 6) {
    skyTop = '#22162b'; skyBottom = '#4a2538'; // 밤/새벽
  } else if (timeHour >= 16) {
    skyTop = '#d9534f'; skyBottom = '#f0ad4e'; // 노을
  }

  // 창밖 전체 배경
  ctx.fillStyle = skyTop;
  ctx.fillRect(0, 0, w, h);

  // 사막 지형 언덕 실루엣
  ctx.fillStyle = '#bfa175';
  ctx.beginPath();
  ctx.moveTo(0, h * 0.6);
  ctx.quadraticCurveTo(w * 0.3, h * 0.45, w * 0.6, h * 0.55);
  ctx.quadraticCurveTo(w * 0.8, h * 0.62, w, h * 0.5);
  ctx.lineTo(w, h);
  ctx.lineTo(0, h);
  ctx.fill();

  // 만화풍 건물들 배치 (1번째 이미지 구도 참고)
  CITY_BUILDINGS.forEach(b => {
    let bx = b.x * w;
    let by = b.y * h;
    let bw = b.w * w;
    let bh = b.h * h;

    ctx.fillStyle = b.color;
    ctx.strokeStyle = '#2b1c14';
    ctx.lineWidth = 3;
    ctx.fillRect(bx, by, bw, bh);
    ctx.strokeRect(bx, by, bw, bh);

    // 굴뚝 및 연기 애니메이션
    ctx.fillStyle = '#4a3b32';
    ctx.fillRect(bx + bw * 0.2, by - bh * 0.3, bw * 0.2, bh * 0.3);
    ctx.strokeRect(bx + bw * 0.2, by - bh * 0.3, bw * 0.2, bh * 0.3);

    // 매연 효과
    if (weatherType !== 'RAIN' && weatherType !== 'HEAVY_RAIN') {
      ctx.fillStyle = 'rgba(180, 170, 160, 0.4)';
      let smokeOffset = Math.sin(Date.now() / 400) * 8;
      ctx.beginPath();
      ctx.arc(bx + bw * 0.3 + smokeOffset, by - bh * 0.4, 12, 0, Math.PI * 2);
      ctx.arc(bx + bw * 0.3 + smokeOffset + 10, by - bh * 0.5, 16, 0, Math.PI * 2);
      ctx.fill();
    }
  });

  // 날씨 이벤트 효과 (모래바람 또는 비)
  if (weatherType === 'DUST') {
    ctx.fillStyle = 'rgba(210, 150, 60, 0.35)';
    ctx.fillRect(0, 0, w, h);
    dustParticles.forEach(p => {
      ctx.fillStyle = 'rgba(255, 220, 150, 0.6)';
      ctx.fillRect((p.x + Date.now() * 0.1) % w, p.y % h, p.size, p.size);
    });
  } else if (weatherType === 'RAIN' || weatherType === 'HEAVY_RAIN') {
    ctx.fillStyle = 'rgba(20, 30, 50, 0.3)';
    ctx.fillRect(0, 0, w, h);
    ctx.strokeStyle = 'rgba(150, 200, 255, 0.7)';
    ctx.lineWidth = 2;
    raindrops.forEach(drop => {
      drop.y += drop.speed;
      if (drop.y > h) drop.y = 0;
      ctx.beginPath();
      ctx.moveTo(drop.x % w, drop.y);
      ctx.lineTo((drop.x % w) - 3, drop.y + drop.len);
      ctx.stroke();
    });
  }

  ctx.restore();
}

// --- 2번째 이미지 감성: 사무실 책상을 화면 정중앙에 배치한 뷰 ---
function drawOfficeScene() {
  // 실내 배경 (어두운 디스토피아 감성)
  ctx.fillStyle = '#121018';
  ctx.fillRect(0, 0, width, height);

  const hrs = Math.floor(gameMinutes / 60);

  // 중앙 통유리창 영역 (가로 65%, 세로 55% 크기로 정중앙 배치)
  const winW = width * 0.68;
  const winH = height * 0.54;
  const winX = (width - winW) / 2;
  const winY = height * 0.05;

  // 통유리창 내부 배경 (만화풍 도시 렌더링)
  drawCartoonCity(ctx, winX, winY, winW, winH, hrs, weather.type);

  // 창틀 (아트워크풍 두꺼운 우드/메탈 프레임)
  ctx.strokeStyle = '#2b1e17';
  ctx.lineWidth = 14;
  ctx.strokeRect(winX, winY, winW, winH);

  // 창틀 내부 격자선
  ctx.beginPath();
  ctx.moveTo(winX + winW * 0.5, winY);
  ctx.lineTo(winX + winW * 0.5, winY + winH);
  ctx.stroke();

  // 2번째 이미지 감성: 정중앙에 배치된 나무 책상
  const deskW = width * 0.75;
  const deskH = height * 0.38;
  const deskX = (width - deskW) / 2;
  const deskY = height * 0.62;

  // 책상 상판 (입체감 있는 목재 톤)
  ctx.fillStyle = '#3d261d';
  ctx.fillRect(deskX, deskY, deskW, deskH);
  ctx.fillStyle = '#261711';
  ctx.fillRect(deskX, deskY, deskW, 14); // 책상 앞면 두께 엣지

  // 책상 위 오브젝트들 렌더링
  drawDeskObjects(deskX, deskY, deskW, deskH);
}

function drawDeskObjects(dx, dy, dw, dh) {
  const blink = Math.floor(Date.now() / 300) % 2 === 0;

  DESK_ITEMS.forEach(item => {
    const ix = dx + dw * item.relX;
    const iy = dy + dh * item.relY;
    const iw = dw * item.relW;
    const ih = dh * item.relH;

    // 만화풍 박스 및 테두리
    ctx.fillStyle = '#1c1622';
    ctx.strokeStyle = '#7928ca';
    ctx.lineWidth = 2;
    ctx.fillRect(ix, iy, iw, ih);
    ctx.strokeRect(ix, iy, iw, ih);

    // 디테일 포인트
    if (item.id === 'beaker') {
      ctx.fillStyle = activeTasks.phPrepared ? '#00f5d4' : '#ff2a5f';
      ctx.fillRect(ix + 4, iy + ih * 0.4, iw - 8, ih * 0.5);
    } else if (item.id === 'phone' && activeTasks.phoneRinging && blink) {
      ctx.fillStyle = '#ff2a5f';
      ctx.fillRect(ix + 6, iy + 6, iw - 12, ih - 12);
    } else if (item.id === 'sensor_pad' && activeTasks.sensorDirty && blink) {
      ctx.fillStyle = '#ffb703';
      ctx.fillRect(ix + 6, iy + 6, iw - 12, ih - 12);
    }
  });
}

// 오프닝 줌인 연출 렌더링 (1번째 이미지 전경에서 사무실 창문으로 줌인)
function drawZoomInBackground() {
  zoomProgress += 0.012;
  if (zoomProgress >= 1.0) {
    zoomProgress = 1.0;
    scene = 'OFFICE';
    document.getElementById('hud-clock').style.display = 'flex';
    document.getElementById('hud-weather').style.display = 'block';
    updateWeatherHUD();
    updateAlertStrip();
    showDialogue('나', '사막 모래바람을 뚫고 사무실 책상 앞에 앉았어. 먼저 [pH 배합기]로 산성비 중화 세팅부터 끝내자!');
    return;
  }

  ctx.save();
  const scale = 1 + zoomProgress * 4.0;
  const targetX = width * 0.5;
  const targetY = height * 0.35;

  ctx.translate(targetX, targetY);
  ctx.scale(scale, scale);
  ctx.translate(-targetX, -targetY);

  drawCartoonCity(ctx, 0, 0, width, height, 7, 'CLEAR');
  ctx.restore();

  ctx.fillStyle = `rgba(18, 16, 24, ${zoomProgress * 0.7})`;
  ctx.fillRect(0, 0, width, height);
}

// 마우스 인터랙션
canvas.addEventListener('mousemove', (e) => {
  if (scene !== 'OFFICE' || isPaused) {
    document.getElementById('hover-tooltip').style.display = 'none';
    canvas.style.cursor = 'default';
    return;
  }
  const mx = e.clientX;
  const my = e.clientY;
  let hovered = null;

  const deskW = width * 0.75;
  const deskH = height * 0.38;
  const deskX = (width - deskW) / 2;
  const deskY = height * 0.62;

  DESK_ITEMS.forEach(item => {
    const ox = deskX + deskW * item.relX;
    const oy = deskY + deskH * item.relY;
    const ow = deskW * item.relW;
    const oh = deskH * item.relH;
    if (mx >= ox && mx <= ox + ow && my >= oy && my <= oy + oh) hovered = item;
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

  const deskW = width * 0.75;
  const deskH = height * 0.38;
  const deskX = (width - deskW) / 2;
  const deskY = height * 0.62;

  for (const item of DESK_ITEMS) {
    const ox = deskX + deskW * item.relX;
    const oy = deskY + deskH * item.relY;
    const ow = deskW * item.relW;
    const oh = deskH * item.relH;
    if (mx >= ox && mx <= ox + ow && my >= oy && my <= oy + oh) {
      handleObjectClick(item.id);
      break;
    }
  }
});

// 메인 루프
function gameLoop(timestamp) {
  if (!lastTimestamp) lastTimestamp = timestamp;
  const deltaSec = (timestamp - lastTimestamp) / 1000;
  lastTimestamp = timestamp;

  ctx.clearRect(0, 0, width, height);

  if (scene === 'TITLE') {
    drawCartoonCity(ctx, 0, 0, width, height, 12, 'CLEAR');
  } else if (scene === 'ZOOM_IN') {
    drawZoomInBackground();
  } else if (scene === 'OFFICE' || scene === 'ENDING') {
    drawOfficeScene();

    if (scene === 'OFFICE' && !isPaused) {
      gameMinutes += deltaSec * 4.67 * timeMultiplier;

      if (gameMinutes >= 21 * 60) {
        day++;
        gameMinutes = 7 * 60;
        simulateNewDay();
      }

      const hrs = Math.floor(gameMinutes / 60);
      const mins = Math.floor(gameMinutes % 60);
      document.getElementById('clock-day-text').innerText = `${day}일차`;
      document.getElementById('clock-time-text').innerText = `${String(hrs).padStart(2, '0')}:${String(mins).padStart(2, '0')}`;
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
