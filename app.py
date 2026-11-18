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
<title>Rain City - Pixel Art Edition</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=DungGeunMo&display=swap');
  @import url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_2107@1.1/Pretendard-Regular.woff2');

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
    background-color: #0c0910;
    font-family: 'DungGeunMo', monospace;
    color: #f7f4eb;
  }

  #game-container {
    position: relative;
    width: 100vw;
    height: 100vh;
    overflow: hidden;
    background: #0c0910;
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

  /* 도트 레트로 윈도우 박스 */
  .pixel-window {
    background: #181425;
    border: 4px solid #ff6b8b;
    box-shadow: 6px 6px 0px #120d1a;
    border-radius: 0px;
    padding: 24px;
    position: relative;
  }

  .pixel-titlebar {
    background: #ff6b8b;
    color: #120d1a;
    padding: 6px 12px;
    font-size: 1rem;
    font-weight: bold;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: -24px -24px 20px -24px;
    border-bottom: 3px solid #120d1a;
  }

  .pixel-controls span {
    display: inline-block;
    width: 14px;
    height: 14px;
    background: #181425;
    border: 2px solid #120d1a;
    margin-left: 4px;
    text-align: center;
    font-size: 9px;
    line-height: 10px;
    cursor: pointer;
    color: #fff;
  }

  /* 시작 화면 (점프킹/인디 게임풍 감성 디자인) */
  #title-overlay {
    position: absolute;
    inset: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    z-index: 20;
    background: linear-gradient(180deg, #1b1226 0%, #0c0910 100%);
    transition: opacity 1.2s ease;
  }

  .title-logo {
    font-size: clamp(4.5rem, 9vw, 7.5rem);
    color: #ff6b8b;
    text-shadow: 6px 6px 0px #5c2c46, 12px 12px 0px #0c0910;
    margin-bottom: 15px;
    letter-spacing: 4px;
  }

  .title-sub {
    font-size: 1.25rem;
    color: #bfa175;
    margin-bottom: 50px;
    letter-spacing: 1.5px;
    text-shadow: 2px 2px 0px #0c0910;
  }

  .pixel-btn {
    font-family: 'DungGeunMo', monospace;
    font-size: 1.5rem;
    padding: 16px 50px;
    background: #5c2c46;
    color: #f7f4eb;
    border: 4px solid #ff6b8b;
    box-shadow: 6px 6px 0px #0c0910;
    cursor: pointer;
    transition: 0.08s;
  }

  .pixel-btn:hover {
    background: #7a3d60;
    transform: translate(-2px, -2px);
    box-shadow: 8px 8px 0px #0c0910;
  }

  .pixel-btn:active {
    transform: translate(3px, 3px);
    box-shadow: 2px 2px 0px #0c0910;
  }

  /* 우측 상단 시계 HUD */
  #hud-clock {
    position: absolute;
    top: 20px;
    right: 24px;
    z-index: 15;
    background: #181425;
    border: 3px solid #00f5d4;
    box-shadow: 4px 4px 0px #0c0910;
    padding: 12px 18px;
    display: none;
    align-items: center;
    gap: 14px;
  }

  .clock-day { font-size: 1.2rem; color: #00f5d4; }
  .clock-time { font-size: 1.1rem; color: #ff6b8b; background: #0c0910; padding: 4px 10px; border: 2px solid #5c2c46; }

  .speed-btn {
    font-family: 'DungGeunMo', monospace;
    background: #2b213a;
    border: 2px solid #00f5d4;
    color: #f7f4eb;
    font-size: 0.85rem;
    padding: 4px 8px;
    cursor: pointer;
  }
  .speed-btn.active { background: #00f5d4; color: #0c0910; border-color: #fff; }

  /* 좌측 상단 기상 HUD */
  #hud-weather {
    position: absolute;
    top: 20px;
    left: 24px;
    z-index: 15;
    background: #181425;
    border: 3px solid #ff6b8b;
    box-shadow: 4px 4px 0px #0c0910;
    padding: 12px 18px;
    display: none;
    font-size: 0.95rem;
    line-height: 1.6;
  }

  /* 알림 배지 */
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
    background: #ff3366;
    border: 2px solid #fff;
    color: #fff;
    padding: 8px 14px;
    font-size: 0.9rem;
    cursor: pointer;
    box-shadow: 4px 4px 0px #0c0910;
  }

  /* 하단 대화창 */
  #dialogue-box {
    position: absolute;
    bottom: 24px;
    left: 50%;
    transform: translateX(-50%);
    width: min(850px, 92vw);
    z-index: 25;
    background: #181425;
    border: 4px solid #bfa175;
    box-shadow: 8px 8px 0px #0c0910;
    padding: 18px 26px;
    display: none;
    cursor: pointer;
  }

  .speaker-tag {
    display: inline-block;
    background: #ff6b8b;
    color: #0c0910;
    font-size: 0.95rem;
    font-weight: bold;
    padding: 4px 12px;
    border: 2px solid #fff;
    margin-bottom: 10px;
  }

  .dialogue-text { font-size: 1.1rem; line-height: 1.7; color: #f7f4eb; }
  .dialogue-next { text-align: right; font-size: 0.82rem; color: #00f5d4; margin-top: 8px; }

  /* 모달 오버레이 */
  #modal-backdrop {
    position: absolute;
    inset: 0;
    background: rgba(12, 9, 16, 0.88);
    z-index: 30;
    display: none;
    align-items: center;
    justify-content: center;
  }

  .modal-card { width: min(760px, 92vw); max-height: 88vh; overflow-y: auto; }

  .newspaper-sheet { background: #e2d7be; color: #211c16; padding: 26px; border: 3px solid #5c2c46; }
  .news-head { text-align: center; border-bottom: 3px double #211c16; padding-bottom: 10px; margin-bottom: 16px; }

  .dossier-box { background: #181425; color: #f7f4eb; padding: 22px; border: 3px solid #5c2c46; }
  .check-item { display: flex; align-items: center; justify-content: space-between; padding: 14px; margin: 10px 0; background: #2b213a; border: 2px solid #bfa175; font-size: 1.05rem; }

  .policy-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 14px; }
  .policy-card { background: #0c0910; border: 2px solid #5c2c46; padding: 16px; cursor: pointer; display: flex; flex-direction: column; justify-content: space-between; }
  .policy-card:hover { border-color: #00f5d4; background: #21182d; }
  
  .badge-status { display: inline-block; font-size: 0.8rem; padding: 3px 8px; margin-top: 10px; border: 1px solid #5c2c46; }
  .badge-ready { background: #5c2c46; color: #fff; }

  .mixer-box { background: #0c0910; border: 3px solid #00f5d4; padding: 22px; text-align: center; margin-top: 12px; }
  .pixel-btn-action { font-family: 'DungGeunMo', monospace; padding: 12px 26px; background: #5c2c46; color: #fff; border: 3px solid #ff6b8b; box-shadow: 4px 4px 0px #0c0910; cursor: pointer; }
  .choice-btn { font-family: 'DungGeunMo', monospace; display: block; width: 100%; text-align: left; background: #21182d; border: 2px solid #5c2c46; color: #f7f4eb; padding: 14px 18px; margin-bottom: 12px; cursor: pointer; }
  .choice-btn:hover { border-color: #00f5d4; }

  #hover-tooltip {
    position: absolute; pointer-events: none; background: #181425; border: 2px solid #ff6b8b; color: #00f5d4; padding: 6px 12px; font-size: 0.85rem; z-index: 18; display: none; transform: translate(-50%, -140%); white-space: nowrap; box-shadow: 4px 4px 0px #0c0910;
  }
</style>
</head>
<body>

<div id="game-container">
  <canvas id="gameCanvas"></canvas>

  <!-- 오직 감성을 살린 세련된 도트풍 타이틀 화면 -->
  <div id="title-overlay">
    <div class="title-logo">RAIN CITY</div>
    <div class="title-sub">디스토피아 사막 도시, 감성 레트로 환경경영 시뮬레이션</div>
    <button class="pixel-btn" onclick="startZoomInSequence()">사무실로 출근하기 ▶</button>
  </div>

  <div id="hud-weather"></div>
  <div id="alert-strip"></div>
  <div id="hud-clock">
    <span class="clock-day" id="clock-day-text">1일차</span>
    <span class="clock-time" id="clock-time-text">07:00</span>
    <div>
      <button class="speed-btn active" id="spd-1" onclick="setSpeed(1)">1x</button>
      <button class="speed-btn" id="spd-3" onclick="setSpeed(3)">3x</button>
      <button class="speed-btn" id="spd-10" onclick="setSpeed(10)">10x</button>
    </div>
  </div>

  <div id="hover-tooltip"></div>

  <div id="dialogue-box" onclick="closeDialogue()">
    <div class="speaker-tag" id="dialogue-speaker">나</div>
    <div class="dialogue-text" id="dialogue-text"></div>
    <div class="dialogue-next">▼ 클릭해서 계속</div>
  </div>

  <div id="modal-backdrop">
    <div class="pixel-window modal-card" id="modal-content"></div>
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

let weather = { type: 'CLEAR', humidity: 32, temp: 36, so2: 75, pm25: 80 };
let activeTasks = { phPrepared: false, sensorDirty: false, phoneRinging: false, currentAudit: null };

const POLICIES = [
  { id: 'fgd', name: '배연탈황설비 (FGD)', cost: 45, desc: '공장 SO₂를 줄여 산성비 위험을 낮춰줍니다.', status: 'READY' },
  { id: 'esp', name: '전기집진기 (ESP)', cost: 40, desc: '초미세먼지(PM2.5)를 잡아서 공기를 맑게 해줘요.', status: 'READY' },
  { id: 'sensor', name: '정밀 대기질 센서망', cost: 25, desc: '도시 대기 상태와 강수 pH를 실시간으로 보여줍니다.', status: 'READY' },
  { id: 'seeding', name: '인공강우 시딩 장비', cost: 55, desc: '구름에 촉매를 뿌려 강수 확률을 확 높여줍니다.', status: 'READY' }
];

// 아기자기한 도트풍 도시 건물 배열
const PIXEL_BUILDINGS = [
  { rx: 0.1, ry: 0.35, w: 120, h: 180, color: '#8b4532', roof: '#5c2c46' },
  { rx: 0.35, ry: 0.30, w: 140, h: 220, color: '#3d6b5c', roof: '#233d34' },
  { rx: 0.62, ry: 0.38, w: 110, h: 160, color: '#c49a45', roof: '#7a5f2a' },
  { rx: 0.82, ry: 0.32, w: 130, h: 200, color: '#a0523d', roof: '#613225' }
];

// 정중앙 책상 위 도트 오브젝트
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

let dustParticles = Array.from({length: 80}, () => ({
  x: Math.random() * 2000, y: Math.random() * 1200,
  speed: 1.5 + Math.random() * 3, size: 2 + Math.random() * 2
}));

let raindrops = Array.from({length: 120}, () => ({
  x: Math.random() * window.innerWidth, y: Math.random() * window.innerHeight,
  speed: 16 + Math.random() * 8, len: 15 + Math.random() * 12
}));

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
    <div class="pixel-titlebar">
      <span>SYSTEM DIALOG</span>
      <div class="pixel-controls"><span onclick="closeModal()">×</span></div>
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
  if (!activeTasks.phPrepared) alerts.push(`<div class="alert-pill" onclick="handleObjectClick('beaker')">🧪 [pH 배합기] 중화 세팅을 해주세요!</div>`);
  if (activeTasks.sensorDirty) alerts.push(`<div class="alert-pill" onclick="handleObjectClick('sensor_pad')">📡 [센서 정비기] 모래바람으로 오류 발생!</div>`);
  if (activeTasks.phoneRinging) alerts.push(`<div class="alert-pill" onclick="handleObjectClick('phone')">☎️ [민원 전화기] 수신 중!</div>`);
  strip.innerHTML = alerts.join('');
  strip.style.display = alerts.length > 0 ? 'flex' : 'none';
}

function handleObjectClick(id) {
  if (id === 'newspaper') {
    openModal(`
      <div style="margin-bottom:10px; color:#ff6b8b; font-weight:bold;">📰 조간신문</div>
      <div class="newspaper-sheet">
        <div class="news-head"><h2>"비가 오지 않는 사막 도시의 눈물"</h2></div>
        <p style="margin-top:10px;">과연 30일 안에 이 지독한 가뭄을 끝낼 수 있을 것인가?</p>
      </div>
    `);
  } else if (id === 'documents') {
    openModal(`
      <div style="margin-bottom:10px; color:#00f5d4; font-weight:bold;">📁 체크리스트</div>
      <div class="dossier-box">
        <div style="margin-bottom:10px;">💰 남은 예산: <strong style="color:#00f5d4;">${budget}억</strong></div>
        <div class="check-item"><span>1. 가뭄 진행도 30% 미만</span><span>${droughtLevel < 30 ? '✅' : '⬜'} (${droughtLevel.toFixed(1)}%)</span></div>
      </div>
    `);
  } else if (id === 'laptop') { renderLaptopModal(); }
  else if (id === 'beaker') { openPhMixerMinigame(); }
  else if (id === 'radio') { openSeedingMinigame(); }
  else if (id === 'sensor_pad') { openSensorRepairMinigame(); }
  else if (id === 'phone') { showDialogue('나', '지금은 민원 전화가 끊겼어.'); }
  else if (id === 'photo') { showDialogue('나', '지갑 속 가족사진... 힘내자.'); }
}

function openPhMixerMinigame() {
  if (activeTasks.phPrepared) { showDialogue('나', '이미 중화 세팅이 완료되어 있어!'); return; }
  openModal(`
    <div style="margin-bottom:10px; color:#00f5d4; font-weight:bold;">🧪 pH 배합기</div>
    <div class="mixer-box">
      <p style="margin-bottom:10px;">중화제 투입량: <span id="mix-val" style="color:#00f5d4; font-size:1.2rem;">150</span> kg</p>
      <input type="range" id="mix-slider" min="50" max="250" value="150" style="width:85%; cursor:pointer;" oninput="document.getElementById('mix-val').innerText = this.value">
    </div>
    <div style="text-align:center; margin-top:18px;">
      <button class="pixel-btn-action" onclick="executeMixer()">✨ 배합 완료</button>
    </div>
  `);
}

function executeMixer() {
  closeModal();
  activeTasks.phPrepared = true;
  showDialogue('나', '완벽한 비율로 중화 세팅 완료! 안전하게 비를 내릴 수 있어.');
  updateAlertStrip();
}

function openSeedingMinigame() {
  if (!activeTasks.phPrepared) { showDialogue('나', '먼저 [pH 배합기]로 중화 세팅을 끝내야 해!'); return; }
  openModal(`
    <div style="margin-bottom:10px; color:#00f5d4; font-weight:bold;">🛩️ 인공강우 작전 무전기</div>
    <div style="text-align:center; padding:15px;">
      <button class="pixel-btn-action" onclick="fireSeeding()">🚀 인공강우 개시! (10억)</button>
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
  if (!activeTasks.sensorDirty) { showDialogue('나', '센서가 모두 정상 작동 중이야.'); return; }
  openModal(`
    <div style="margin-bottom:10px; color:#ff6b8b; font-weight:bold;">📡 대기질 센서 정비</div>
    <div style="display:grid; grid-template-columns:repeat(2, 1fr); gap:10px;">
      <div id="sn-1" class="choice-btn" onclick="cleanSensor(1)">⚠️ 1번 센서 정비</div>
      <div id="sn-2" class="choice-btn" onclick="cleanSensor(2)">⚠️ 2번 센서 정비</div>
    </div>
  `);
}

let cleanedSensors = 0;
function cleanSensor(idx) {
  const el = document.getElementById(`sn-${idx}`);
  if (el && !el.dataset.cleaned) {
    el.dataset.cleaned = "true";
    el.style.background = "#00f5d4";
    el.style.color = "#0c0910";
    el.innerHTML = "✅ 정상 작동";
    cleanedSensors++;
    if (cleanedSensors >= 2) {
      cleanedSensors = 0;
      activeTasks.sensorDirty = false;
      budget += 10;
      setTimeout(() => { closeModal(); updateAlertStrip(); showDialogue('나', '센서 정비 완료! 수당 10억 획득!'); }, 300);
    }
  }
}

function renderLaptopModal() {
  let cardsHtml = POLICIES.map(p => `
    <div class="policy-card" onclick="executePolicy('${p.id}')">
      <div style="font-weight:bold; color:#00f5d4; margin-bottom:6px;">${p.name}</div>
      <div style="font-size:0.8rem; color:#bfa175; margin-bottom:8px;">${p.desc}</div>
      <span class="badge-status badge-ready">설치 (${p.cost}억)</span>
    </div>
  `).join('');
  openModal(`<div style="margin-bottom:10px; color:#00f5d4; font-weight:bold;">💻 정책 구매 터미널 (예산: ${budget}억)</div><div class="policy-grid">${cardsHtml}</div>`);
}

function executePolicy(id) {
  const p = POLICIES.find(item => item.id === id);
  if (budget >= p.cost) {
    budget -= p.cost;
    p.status = 'ACTIVE';
    closeModal();
    showDialogue('나', `[${p.name}] 설치 완료!`);
  }
}

function simulateNewDay() {
  const roll = Math.random() * 100;
  if (roll < 20) { weather.type = 'DUST'; activeTasks.sensorDirty = true; cleanedSensors = 0; }
  else if (roll < 40) { weather.type = 'DROUGHT'; }
  else { weather.type = 'CLEAR'; }
  updateWeatherHUD();
  updateAlertStrip();
}

function updateWeatherHUD() {
  const hud = document.getElementById('hud-weather');
  const names = { 'CLEAR': '☀️ 맑음', 'DROUGHT': '🔥 폭염 가뭄', 'DUST': '🌪️ 모래바람 경보', 'RAIN': '🌧️ 단비 내리는 중' };
  hud.innerHTML = `<div style="font-weight:bold; color:#ff6b8b;">${names[weather.type]}</div><div style="font-size:0.85rem; color:#bfa175;">습도: ${weather.humidity}%</div>`;
}

// 귀여운 도트풍 도시 배경 그리기
function drawPixelCity(ctx, x, y, w, h, timeHour, weatherType) {
  ctx.save();
  ctx.translate(x, y);

  let skyColor = '#df9257';
  if (timeHour >= 18 || timeHour < 6) skyColor = '#161022';
  else if (timeHour >= 16) skyColor = '#d9534f';

  ctx.fillStyle = skyColor;
  ctx.fillRect(0, 0, w, h);

  // 사막 언덕 실루엣
  ctx.fillStyle = '#9c7c51';
  ctx.beginPath();
  ctx.moveTo(0, h * 0.6);
  ctx.quadraticCurveTo(w * 0.4, h * 0.45, w, h * 0.58);
  ctx.lineTo(w, h); ctx.lineTo(0, h); ctx.fill();

  // 도트풍 건물들 렌더링
  PIXEL_BUILDINGS.forEach(b => {
    let bx = b.rx * w, by = b.ry * h;
    // 본체
    ctx.fillStyle = b.color;
    ctx.strokeStyle = '#120d1a';
    ctx.lineWidth = 4;
    ctx.fillRect(bx, by, b.w, b.h);
    ctx.strokeRect(bx, by, b.w, b.h);

    // 지붕
    ctx.fillStyle = b.roof;
    ctx.fillRect(bx - 6, by - 14, b.w + 12, 14);
    ctx.strokeRect(bx - 6, by - 14, b.w + 12, 14);

    // 창문 도트 디테일
    ctx.fillStyle = (timeHour >= 18 || timeHour < 6) ? '#00f5d4' : '#2b213a';
    for (let wx = bx + 14; wx < bx + b.w - 14; wx += 22) {
      for (let wy = by + 16; wy < by + b.h - 16; wy += 28) {
        ctx.fillRect(wx, wy, 10, 14);
      }
    }
  });

  if (weatherType === 'DUST') {
    ctx.fillStyle = 'rgba(210, 140, 40, 0.35)';
    ctx.fillRect(0, 0, w, h);
    dustParticles.forEach(p => {
      ctx.fillStyle = '#ffcc66';
      ctx.fillRect((p.x + Date.now() * 0.1) % w, p.y % h, p.size, p.size);
    });
  } else if (weatherType === 'RAIN') {
    ctx.fillStyle = 'rgba(15, 25, 45, 0.4)';
    ctx.fillRect(0, 0, w, h);
    ctx.strokeStyle = '#88ccff';
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

// 정중앙 책상 배치 뷰
function drawOfficeScene() {
  ctx.fillStyle = '#0c0910';
  ctx.fillRect(0, 0, width, height);

  const hrs = Math.floor(gameMinutes / 60);

  // 중앙 통유리창
  const winW = width * 0.70;
  const winH = height * 0.52;
  const winX = (width - winW) / 2;
  const winY = height * 0.04;

  drawPixelCity(ctx, winX, winY, winW, winH, hrs, weather.type);

  // 아기자기한 레트로 우드 창틀
  ctx.strokeStyle = '#3d251e';
  ctx.lineWidth = 14;
  ctx.strokeRect(winX, winY, winW, winH);
  ctx.beginPath();
  ctx.moveTo(winX + winW * 0.5, winY); ctx.lineTo(winX + winW * 0.5, winY + winH);
  ctx.stroke();

  // 정중앙 배치된 책상
  const deskW = width * 0.78;
  const deskH = height * 0.40;
  const deskX = (width - deskW) / 2;
  const deskY = height * 0.60;

  ctx.fillStyle = '#4a2c23';
  ctx.fillRect(deskX, deskY, deskW, deskH);
  ctx.fillStyle = '#2b1914';
  ctx.fillRect(deskX, deskY, deskW, 16);

  // 책상 위 도트 오브젝트들
  DESK_ITEMS.forEach(item => {
    const ix = deskX + deskW * item.relX;
    const iy = deskY + deskH * item.relY;
    const iw = deskW * item.relW;
    const ih = deskH * item.relH;

    ctx.fillStyle = '#181425';
    ctx.strokeStyle = '#bfa175';
    ctx.lineWidth = 3;
    ctx.fillRect(ix, iy, iw, ih);
    ctx.strokeRect(ix, iy, iw, ih);

    if (item.id === 'beaker') {
      ctx.fillStyle = activeTasks.phPrepared ? '#00f5d4' : '#ff6b8b';
      ctx.fillRect(ix + 6, iy + ih * 0.4, iw - 12, ih * 0.45);
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
  drawPixelCity(ctx, 0, 0, width, height, 7, 'CLEAR');
  ctx.restore();

  ctx.fillStyle = `rgba(12, 9, 16, ${zoomProgress * 0.8})`;
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
    drawPixelCity(ctx, 0, 0, width, height, 12, 'CLEAR');
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
