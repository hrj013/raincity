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
<title>Rain City - Enhanced Art Style</title>
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
    background-color: #0d0b12;
    font-family: 'DungGeunMo', monospace;
    color: #f0ece1;
  }

  #game-container {
    position: relative;
    width: 100vw;
    height: 100vh;
    overflow: hidden;
    background: #0d0b12;
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

  /* 고급 레트로 일러스트 윈도우 스타일 */
  .retro-window {
    background: #161224;
    border: 4px solid #ff758f;
    box-shadow: 6px 6px 0px #ff2a5f, 12px 12px 0px #08060a;
    border-radius: 4px;
    padding: 24px;
    position: relative;
  }

  .window-titlebar {
    background: linear-gradient(90deg, #ff758f, #7928ca);
    color: #fff;
    padding: 6px 12px;
    font-size: 0.95rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: -24px -24px 20px -24px;
    border-bottom: 3px solid #ff2a5f;
  }

  .window-controls span {
    display: inline-block;
    width: 14px;
    height: 14px;
    background: #ff2a5f;
    border: 1.5px solid #fff;
    margin-left: 6px;
    text-align: center;
    font-size: 9px;
    line-height: 11px;
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
    background: #0d0b12;
    transition: opacity 1.2s ease;
  }

  .title-logo {
    font-size: clamp(4rem, 8vw, 6.5rem);
    color: #ff758f;
    text-shadow: 5px 5px 0px #7928ca, 10px 10px 0px #08060a;
    margin-bottom: 12px;
    letter-spacing: 4px;
  }

  .title-sub {
    font-size: 1.2rem;
    color: #b19cd9;
    margin-bottom: 45px;
    letter-spacing: 1.5px;
  }

  .start-btn {
    font-family: 'DungGeunMo', monospace;
    font-size: 1.5rem;
    padding: 16px 50px;
    background: #7928ca;
    color: #fff;
    border: 4px solid #ff758f;
    box-shadow: 6px 6px 0px #ff2a5f;
    cursor: pointer;
    transition: 0.1s;
  }

  .start-btn:hover {
    background: #9d4edd;
    transform: translate(-2px, -2px);
    box-shadow: 8px 8px 0px #ff2a5f;
  }

  /* 우측 상단 시계 HUD */
  #hud-clock {
    position: absolute;
    top: 20px;
    right: 24px;
    z-index: 15;
    background: #161224;
    border: 3px solid #00f5d4;
    box-shadow: 4px 4px 0px #08060a;
    padding: 12px 18px;
    display: none;
    align-items: center;
    gap: 14px;
  }

  .clock-day {
    font-size: 1.2rem;
    color: #00f5d4;
  }

  .clock-time {
    font-size: 1.1rem;
    color: #ff758f;
    background: #08060a;
    padding: 4px 10px;
    border: 2px solid #7928ca;
  }

  .speed-btn {
    font-family: 'DungGeunMo', monospace;
    background: #241e38;
    border: 2px solid #00f5d4;
    color: #e2dfd2;
    font-size: 0.85rem;
    padding: 4px 8px;
    cursor: pointer;
  }

  .speed-btn.active {
    background: #00f5d4;
    color: #0d0b12;
    border-color: #fff;
  }

  /* 좌측 상단 기상 HUD */
  #hud-weather {
    position: absolute;
    top: 20px;
    left: 24px;
    z-index: 15;
    background: #161224;
    border: 3px solid #ff758f;
    box-shadow: 4px 4px 0px #08060a;
    padding: 12px 18px;
    display: none;
    font-size: 0.95rem;
    line-height: 1.6;
  }

  /* 긴급 알림 배지 */
  #alert-strip {
    position: absolute;
    top: 115px;
    left: 24px;
    z-index: 15;
    display: none;
    flex-direction: column;
    gap: 10px;
  }

  .alert-pill {
    background: #ff2a5f;
    border: 2px solid #fff;
    color: #fff;
    padding: 8px 14px;
    font-size: 0.9rem;
    cursor: pointer;
    box-shadow: 4px 4px 0px #08060a;
    animation: alertBlink 0.8s infinite alternate;
  }

  @keyframes alertBlink {
    0% { opacity: 0.8; transform: scale(1); }
    100% { opacity: 1; transform: scale(1.02); }
  }

  /* 하단 대화창 */
  #dialogue-box {
    position: absolute;
    bottom: 24px;
    left: 50%;
    transform: translateX(-50%);
    width: min(850px, 92vw);
    z-index: 25;
    background: #161224;
    border: 4px solid #b19cd9;
    box-shadow: 8px 8px 0px #08060a;
    padding: 18px 26px;
    display: none;
    cursor: pointer;
  }

  .speaker-tag {
    display: inline-block;
    background: #ff758f;
    color: #0d0b12;
    font-size: 0.95rem;
    font-weight: bold;
    padding: 4px 12px;
    border: 2px solid #fff;
    margin-bottom: 10px;
  }

  .dialogue-text {
    font-size: 1.1rem;
    line-height: 1.7;
    color: #f0ece1;
  }

  .dialogue-next {
    text-align: right;
    font-size: 0.82rem;
    color: #00f5d4;
    margin-top: 8px;
  }

  /* 모달 오버레이 */
  #modal-backdrop {
    position: absolute;
    inset: 0;
    background: rgba(13, 11, 18, 0.88);
    z-index: 30;
    display: none;
    align-items: center;
    justify-content: center;
  }

  .modal-card {
    width: min(760px, 92vw);
    max-height: 88vh;
    overflow-y: auto;
  }

  .newspaper-sheet {
    background: #e2d7be;
    color: #211c16;
    padding: 26px;
    border: 3px solid #7928ca;
  }

  .news-head {
    text-align: center;
    border-bottom: 3px double #211c16;
    padding-bottom: 10px;
    margin-bottom: 16px;
  }

  .dossier-box {
    background: #161224;
    color: #f0ece1;
    padding: 22px;
    border: 3px solid #7928ca;
  }

  .check-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 14px;
    margin: 10px 0;
    background: #241e38;
    border: 2px solid #b19cd9;
    font-size: 1.05rem;
  }

  .policy-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 14px;
  }

  .policy-card {
    background: #0d0b12;
    border: 2px solid #7928ca;
    padding: 16px;
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
    font-size: 0.8rem;
    padding: 3px 8px;
    margin-top: 10px;
    border: 1px solid #7928ca;
  }

  .badge-active { background: #00f5d4; color: #0d0b12; }
  .badge-pending { background: #ffb703; color: #0d0b12; }
  .badge-ready { background: #7928ca; color: #fff; }

  .mixer-box {
    background: #0d0b12;
    border: 3px solid #00f5d4;
    padding: 22px;
    text-align: center;
    margin-top: 12px;
  }

  .action-btn {
    font-family: 'DungGeunMo', monospace;
    padding: 12px 26px;
    background: #7928ca;
    color: #fff;
    border: 3px solid #ff758f;
    box-shadow: 4px 4px 0px #ff2a5f;
    cursor: pointer;
    font-size: 1.05rem;
  }

  .choice-btn {
    font-family: 'DungGeunMo', monospace;
    display: block;
    width: 100%;
    text-align: left;
    background: #1f1a2d;
    border: 2px solid #7928ca;
    color: #f0ece1;
    padding: 14px 18px;
    margin-bottom: 12px;
    cursor: pointer;
    font-size: 1rem;
  }

  .choice-btn:hover {
    border-color: #00f5d4;
  }

  #hover-tooltip {
    position: absolute;
    pointer-events: none;
    background: #161224;
    border: 2px solid #ff758f;
    color: #00f5d4;
    padding: 6px 12px;
    font-size: 0.85rem;
    z-index: 18;
    display: none;
    transform: translate(-50%, -140%);
    white-space: nowrap;
    box-shadow: 4px 4px 0px #ff2a5f;
  }
</style>
</head>
<body>

<div id="game-container">
  <canvas id="gameCanvas"></canvas>

  <!-- 타이틀 화면 -->
  <div id="title-overlay">
    <div class="title-logo">RAIN CITY</div>
    <div class="title-sub">사막의 잿빛 도시, 내 손으로 되살려보자구!</div>
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

let scene = 'TITLE';
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
let zoomProgress = 0;

let weather = {
  type: 'CLEAR',
  windSpeed: 3.2,
  humidity: 32,
  temp: 36,
  rainProb: 15,
  so2: 75,
  pm25: 80,
  ph: 4.6
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

// 첫 번째 이미지풍 만화풍 디스토피아 도시 구조물
const CITY_BUILDINGS = [
  { x: 0.12, y: 0.38, w: 0.16, h: 0.20, color: '#8b4532' },
  { x: 0.68, y: 0.35, w: 0.15, h: 0.23, color: '#3d6b5c' },
  { x: 0.42, y: 0.48, w: 0.14, h: 0.18, color: '#c49a45' },
  { x: 0.04, y: 0.52, w: 0.11, h: 0.15, color: '#a0523d' },
  { x: 0.82, y: 0.50, w: 0.12, h: 0.16, color: '#9e5a47' }
];

// 두 번째 이미지풍 정중앙 책상 위 오브젝트 배치
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
  }
];

let dustParticles = [];
for (let i = 0; i < 100; i++) {
  dustParticles.push({
    x: Math.random() * 3000, y: Math.random() * 2000,
    speedX: 1.5 + Math.random() * 4, speedY: -0.3 + Math.random() * 1,
    size: 1.5 + Math.random() * 3
  });
}

let raindrops = [];
for (let i = 0; i < 150; i++) {
  raindrops.push({
    x: Math.random() * window.innerWidth, y: Math.random() * window.innerHeight,
    speed: 14 + Math.random() * 8, len: 18 + Math.random() * 15
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
  if (document.getElementById('modal-backdrop').style.display !== 'flex') isPaused = false;
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
  if (document.getElementById('dialogue-box').style.display !== 'block') isPaused = false;
}

function updateAlertStrip() {
  const strip = document.getElementById('alert-strip');
  let alerts = [];
  if (!activeTasks.phPrepared) alerts.push(`<div class="alert-pill" onclick="handleObjectClick('beaker')">🧪 [pH 배합기]로 중화 준비를 해주세요!</div>`);
  if (activeTasks.sensorDirty) alerts.push(`<div class="alert-pill" onclick="handleObjectClick('sensor_pad')">📡 [센서 정비기] 오류 발생!</div>`);
  if (activeTasks.phoneRinging) alerts.push(`<div class="alert-pill" onclick="handleObjectClick('phone')">☎️ [민원 전화기] 수신 중!</div>`);
  strip.innerHTML = alerts.join('');
  strip.style.display = alerts.length > 0 ? 'flex' : 'none';
}

function getChecklistStatus() {
  const acidFreq = totalRainDays === 0 ? 12.0 : (acidRainDays / Math.max(1, day)) * 100;
  return { check1: droughtLevel < 30, check2: acidFreq < 10, acidFreq: acidFreq.toFixed(1) };
}

function handleObjectClick(id) {
  if (id === 'newspaper') {
    openModal(`
      <div style="margin-bottom:10px; font-size:1.1rem; color:#ff758f;">📰 레인 시티 조간신문</div>
      <div class="newspaper-sheet">
        <div class="news-head"><h2 style="font-size:1.3rem;">"비가 오지 않는 사막 도시의 눈물"</h2></div>
        <p style="line-height:1.6; font-size:0.95rem;">과연 30일 안에 이 지독한 가뭄을 끝내고 푸른 하늘을 되찾아줄 수 있을 것인가?</p>
      </div>
    `);
  } else if (id === 'documents') {
    const status = getChecklistStatus();
    openModal(`
      <div style="margin-bottom:10px; font-size:1.1rem; color:#00f5d4;">📁 목표 체크리스트</div>
      <div class="dossier-box">
        <div style="display:flex; justify-content:space-between; margin-bottom:12px;"><span>💰 예산</span><span style="color:#00f5d4; font-weight:bold;">${budget} 억</span></div>
        <div class="check-item"><span>1. 가뭄 진행도 30% 미만 (현재: ${droughtLevel.toFixed(1)}%)</span><span>${status.check1 ? '✅' : '⬜'}</span></div>
        <div class="check-item"><span>2. 산성비 빈도 10% 미만 (현재: ${status.acidFreq}%)</span><span>${status.check2 ? '✅' : '⬜'}</span></div>
      </div>
    `);
  } else if (id === 'laptop') { renderLaptopModal(); }
  else if (id === 'beaker') { openPhMixerMinigame(); }
  else if (id === 'radio') { openSeedingMinigame(); }
  else if (id === 'sensor_pad') { openSensorRepairMinigame(); }
  else if (id === 'phone') { openAuditPhoneModal(); }
  else if (id === 'photo') { showDialogue('나', '지갑 속 가족사진... 버틸 수 있는 원동력이야.'); }
}

function openPhMixerMinigame() {
  if (activeTasks.phPrepared) {
    showDialogue('나', '이미 알칼리 중화제 배합이 완료되어 있어!');
    return;
  }
  openModal(`
    <div style="margin-bottom:10px; font-size:1.1rem; color:#00f5d4;">🧪 pH 배합기 (산성비 중화)</div>
    <div class="mixer-box">
      <p style="font-size:1.1rem; margin-bottom:10px;">투입량: <span id="mix-val" style="color:#00f5d4; font-size:1.3rem;">150</span> kg</p>
      <input type="range" id="mix-slider" min="50" max="250" value="150" style="width:85%; cursor:pointer;" oninput="document.getElementById('mix-val').innerText = this.value">
    </div>
    <div style="text-align:center; margin-top:18px;">
      <button class="action-btn" onclick="executeMixer()">✨ 배합 완료</button>
    </div>
  `);
}

function executeMixer() {
  closeModal();
  activeTasks.phPrepared = true;
  showDialogue('나', '중화 세팅 완료! 안전하게 비를 내릴 수 있어.');
  updateAlertStrip();
}

function openSeedingMinigame() {
  if (!activeTasks.phPrepared) {
    showDialogue('나', '먼저 [pH 배합기]로 중화 세팅을 끝내야 해!');
    return;
  }
  openModal(`
    <div style="margin-bottom:10px; font-size:1.1rem; color:#00f5d4;">🛩️ 인공강우 작전</div>
    <div style="text-align:center;">
      <button class="action-btn" onclick="fireSeeding()">🚀 인공강우 개시! (10억)</button>
    </div>
  `);
}

function fireSeeding() {
  if (budget < 10) { closeModal(); showDialogue('나', '예산이 부족해!'); return; }
  budget -= 10;
  activeTasks.phPrepared = false;
  closeModal();
  weather.type = 'RAIN';
  totalRainDays++;
  droughtLevel = Math.max(5, droughtLevel - 15);
  showDialogue('나', '인공강우 성공! 통유리창 밖에 시원한 비가 내린다!');
  updateWeatherHUD();
  updateAlertStrip();
}

function openSensorRepairMinigame() {
  if (!activeTasks.sensorDirty) { showDialogue('나', '센서가 정상 작동 중이야.'); return; }
  openModal(`
    <div style="margin-bottom:10px; font-size:1.1rem; color:#ff758f;">📡 대기질 센서 정비</div>
    <div style="display:grid; grid-template-columns:repeat(2, 1fr); gap:10px;">
      <div id="sn-1" class="choice-btn" onclick="cleanSensor(1)">⚠️ 1번 센서</div>
      <div id="sn-2" class="choice-btn" onclick="cleanSensor(2)">⚠️ 2번 센서</div>
    </div>
  `);
}

let cleanedSensors = 0;
function cleanSensor(idx) {
  const el = document.getElementById(`sn-${idx}`);
  if (el && !el.dataset.cleaned) {
    el.dataset.cleaned = "true";
    el.style.background = "#00f5d4";
    el.style.color = "#0d0b12";
    el.innerHTML = "✅ 정상";
    cleanedSensors++;
    if (cleanedSensors >= 2) {
      cleanedSensors = 0;
      activeTasks.sensorDirty = false;
      budget += 10;
      setTimeout(() => { closeModal(); updateAlertStrip(); showDialogue('나', '센서 정비 완료! 수당 10억 획득!'); }, 300);
    }
  }
}

function openAuditPhoneModal() {
  if (!activeTasks.phoneRinging || !activeTasks.currentAudit) return;
  const audit = activeTasks.currentAudit;
  openModal(`
    <div style="margin-bottom:10px; font-size:1.1rem; color:#ff758f;">☎️ ${audit.title}</div>
    <p style="margin-bottom:16px;">"${audit.desc}"</p>
    <button class="choice-btn" onclick="resolveAudit(0)">1. ${audit.choices[0].text}</button>
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
  let cardsHtml = POLICIES.map(p => `
    <div class="policy-card" onclick="executePolicy('${p.id}')">
      <div style="font-weight:bold; color:#00f5d4; margin-bottom:4px;">${p.name}</div>
      <div style="font-size:0.8rem; color:#b19cd9;">${p.desc}</div>
      <span class="badge-status badge-ready">설치 (${p.cost}억)</span>
    </div>
  `).join('');
  openModal(`<div style="font-size:1.1rem; color:#00f5d4; margin-bottom:10px;">💻 정책 구매 터미널 (예산: ${budget}억)</div><div class="policy-grid">${cardsHtml}</div>`);
}

function executePolicy(id) {
  const p = POLICIES.find(item => item.id === id);
  if (budget >= p.cost) {
    budget -= p.cost;
    p.status = 'ACTIVE';
    closeModal();
    showDialogue('나', `[${p.name}] 설치가 완료되었습니다!`);
  }
}

function simulateNewDay() {
  const roll = Math.random() * 100;
  if (roll < 20) { weather.type = 'DUST'; activeTasks.sensorDirty = true; cleanedSensors = 0; }
  else if (roll < 40) { weather.type = 'DROUGHT'; }
  else { weather.type = 'CLEAR'; }
  if (!activeTasks.phoneRinging && Math.random() < 0.4) {
    activeTasks.phoneRinging = true;
    activeTasks.currentAudit = AUDIT_SCENARIOS[0];
  }
  updateWeatherHUD();
  updateAlertStrip();
}

function updateWeatherHUD() {
  const hud = document.getElementById('hud-weather');
  const names = { 'CLEAR': '☀️ 맑음', 'DROUGHT': '🔥 폭염 가뭄', 'DUST': '🌪️ 모래바람 경보', 'RAIN': '🌧️ 단비 내리는 중' };
  hud.innerHTML = `<div style="font-weight:bold; color:#ff758f;">${names[weather.type]}</div><div style="font-size:0.85rem; color:#b19cd9;">습도: ${weather.humidity}%</div>`;
}

// 1번째 이미지풍 만화풍 도시 배경 렌더링
function drawCartoonCity(ctx, x, y, w, h, timeHour, weatherType) {
  ctx.save();
  ctx.translate(x, y);

  let skyTop = '#df9257', skyBottom = '#f4d0a1';
  if (timeHour >= 18 || timeHour < 6) { skyTop = '#1a1224'; skyBottom = '#3b1f32'; }

  ctx.fillStyle = skyTop;
  ctx.fillRect(0, 0, w, h);

  // 언덕 실루엣
  ctx.fillStyle = '#bfa175';
  ctx.beginPath();
  ctx.moveTo(0, h * 0.58);
  ctx.quadraticCurveTo(w * 0.4, h * 0.42, w, h * 0.55);
  ctx.lineTo(w, h); ctx.lineTo(0, h); ctx.fill();

  CITY_BUILDINGS.forEach(b => {
    let bx = b.x * w, by = b.y * h, bw = b.w * w, bh = b.h * h;
    ctx.fillStyle = b.color;
    ctx.strokeStyle = '#211610';
    ctx.lineWidth = 3;
    ctx.fillRect(bx, by, bw, bh);
    ctx.strokeRect(bx, by, bw, bh);

    // 굴뚝
    ctx.fillStyle = '#3a2a22';
    ctx.fillRect(bx + bw * 0.25, by - bh * 0.35, bw * 0.2, bh * 0.35);
    ctx.strokeRect(bx + bw * 0.25, by - bh * 0.35, bw * 0.2, bh * 0.35);
  });

  if (weatherType === 'DUST') {
    ctx.fillStyle = 'rgba(210, 150, 60, 0.3)';
    ctx.fillRect(0, 0, w, h);
    dustParticles.forEach(p => {
      ctx.fillStyle = 'rgba(255, 220, 150, 0.7)';
      ctx.fillRect((p.x + Date.now() * 0.1) % w, p.y % h, p.size, p.size);
    });
  } else if (weatherType === 'RAIN') {
    ctx.fillStyle = 'rgba(20, 30, 50, 0.35)';
    ctx.fillRect(0, 0, w, h);
    ctx.strokeStyle = 'rgba(150, 200, 255, 0.75)';
    ctx.lineWidth = 2;
    raindrops.forEach(drop => {
      drop.y += drop.speed;
      if (drop.y > h) drop.y = 0;
      ctx.beginPath();
      ctx.moveTo(drop.x % w, drop.y);
      ctx.lineTo((drop.x % w) - 2, drop.y + drop.len);
      ctx.stroke();
    });
  }
  ctx.restore();
}

// 2번째 이미지풍: 책상 정중앙 배치 뷰
function drawOfficeScene() {
  ctx.fillStyle = '#0d0b12';
  ctx.fillRect(0, 0, width, height);

  const hrs = Math.floor(gameMinutes / 60);

  // 중앙 통유리창
  const winW = width * 0.70;
  const winH = height * 0.52;
  const winX = (width - winW) / 2;
  const winY = height * 0.04;

  drawCartoonCity(ctx, winX, winY, winW, winH, hrs, weather.type);

  // 고급 우드 창틀
  ctx.strokeStyle = '#2b1e17';
  ctx.lineWidth = 14;
  ctx.strokeRect(winX, winY, winW, winH);
  ctx.beginPath();
  ctx.moveTo(winX + winW * 0.5, winY);
  ctx.lineTo(winX + winW * 0.5, winY + winH);
  ctx.stroke();

  // 책상 정중앙 배치
  const deskW = width * 0.78;
  const deskH = height * 0.40;
  const deskX = (width - deskW) / 2;
  const deskY = height * 0.60;

  ctx.fillStyle = '#3d261d';
  ctx.fillRect(deskX, deskY, deskW, deskH);
  ctx.fillStyle = '#261711';
  ctx.fillRect(deskX, deskY, deskW, 16);

  drawDeskObjects(deskX, deskY, deskW, deskH);
}

function drawDeskObjects(dx, dy, dw, dh) {
  const blink = Math.floor(Date.now() / 300) % 2 === 0;

  DESK_ITEMS.forEach(item => {
    const ix = dx + dw * item.relX;
    const iy = dy + dh * item.relY;
    const iw = dw * item.relW;
    const ih = dh * item.relH;

    // 일러스트풍 오브젝트 카드
    ctx.fillStyle = '#1b1624';
    ctx.strokeStyle = '#b19cd9';
    ctx.lineWidth = 3;
    ctx.fillRect(ix, iy, iw, ih);
    ctx.strokeRect(ix, iy, iw, ih);

    if (item.id === 'beaker') {
      ctx.fillStyle = activeTasks.phPrepared ? '#00f5d4' : '#ff2a5f';
      ctx.fillRect(ix + 6, iy + ih * 0.4, iw - 12, ih * 0.45);
    } else if (item.id === 'phone' && activeTasks.phoneRinging && blink) {
      ctx.fillStyle = '#ff2a5f';
      ctx.fillRect(ix + 6, iy + 6, iw - 12, ih - 12);
    } else if (item.id === 'sensor_pad' && activeTasks.sensorDirty && blink) {
      ctx.fillStyle = '#ffb703';
      ctx.fillRect(ix + 6, iy + 6, iw - 12, ih - 12);
    }
  });
}

function drawZoomInBackground() {
  zoomProgress += 0.012;
  if (zoomProgress >= 1.0) {
    zoomProgress = 1.0;
    scene = 'OFFICE';
    document.getElementById('hud-clock').style.display = 'flex';
    document.getElementById('hud-weather').style.display = 'block';
    updateWeatherHUD();
    updateAlertStrip();
    showDialogue('나', '사막 모래바람을 뚫고 사무실에 도착했다. [pH 배합기]로 중화 세팅부터 시작하자!');
    return;
  }

  ctx.save();
  const scale = 1 + zoomProgress * 4.0;
  ctx.translate(width * 0.5, height * 0.35);
  ctx.scale(scale, scale);
  ctx.translate(-width * 0.5, -height * 0.35);
  drawCartoonCity(ctx, 0, 0, width, height, 7, 'CLEAR');
  ctx.restore();

  ctx.fillStyle = `rgba(13, 11, 18, ${zoomProgress * 0.75})`;
  ctx.fillRect(0, 0, width, height);
}

canvas.addEventListener('mousemove', (e) => {
  if (scene !== 'OFFICE' || isPaused) {
    document.getElementById('hover-tooltip').style.display = 'none';
    canvas.style.cursor = 'default';
    return;
  }
  const mx = e.clientX, my = e.clientY;
  let hovered = null;
  const deskW = width * 0.78, deskH = height * 0.40;
  const deskX = (width - deskW) / 2, deskY = height * 0.60;

  DESK_ITEMS.forEach(item => {
    const ox = deskX + deskW * item.relX, oy = deskY + deskH * item.relY;
    const ow = deskW * item.relW, oh = deskH * item.relH;
    if (mx >= ox && mx <= ox + ow && my >= oy && my <= oy + oh) hovered = item;
  });

  const tooltip = document.getElementById('hover-tooltip');
  if (hovered) {
    canvas.style.cursor = 'pointer';
    tooltip.style.display = 'block';
    tooltip.style.left = `${mx}px`; tooltip.style.top = `${my}px`;
    tooltip.innerText = hovered.name;
  } else {
    canvas.style.cursor = 'default';
    tooltip.style.display = 'none';
  }
});

canvas.addEventListener('click', (e) => {
  if (scene !== 'OFFICE' || isPaused) return;
  const mx = e.clientX, my = e.clientY;
  const deskW = width * 0.78, deskH = height * 0.40;
  const deskX = (width - deskW) / 2, deskY = height * 0.60;

  for (const item of DESK_ITEMS) {
    const ox = deskX + deskW * item.relX, oy = deskY + deskH * item.relY;
    const ow = deskW * item.relW, oh = deskH * item.relH;
    if (mx >= ox && mx <= ox + ow && my >= oy && my <= oy + oh) {
      handleObjectClick(item.id);
      break;
    }
  }
});

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
