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
<title>Rain City - Omori x Needy Girl Style</title>
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
    background-color: #0b0a10;
    font-family: 'DungGeunMo', monospace;
    color: #f0ece1;
  }

  #game-container {
    position: relative;
    width: 100vw;
    height: 100vh;
    overflow: hidden;
    background: #0b0a10;
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

  /* 니디걸 + 오모리 감성 윈도우 패널 */
  .retro-window {
    background: #14121c;
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
    background: #0b0a10;
    transition: opacity 1.2s ease;
  }

  .title-logo {
    font-size: clamp(3.5rem, 7vw, 6rem);
    color: #ff758f;
    text-shadow: 4px 4px 0px #7928ca, 8px 8px 0px #0b0a10;
    margin-bottom: 10px;
    letter-spacing: 3px;
    animation: titleGlow 2s infinite alternate;
  }

  @keyframes titleGlow {
    0% { text-shadow: 4px 4px 0px #7928ca, 8px 8px 0px #0b0a10; }
    100% { text-shadow: 4px 4px 0px #ff2a5f, 0px 0px 20px rgba(255,117,143,0.6); }
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

  .start-btn:active {
    transform: translate(2px, 2px);
    box-shadow: 2px 2px 0px #ff2a5f;
  }

  /* 우측 상단 시계 HUD (네디걸 테마) */
  #hud-clock {
    position: absolute;
    top: 16px;
    right: 20px;
    z-index: 15;
    background: #14121c;
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
    background: #14121c;
    border: 3px solid #ff758f;
    box-shadow: 3px 3px 0px #0b0a10;
    padding: 10px 16px;
    display: none;
    font-size: 0.9rem;
    line-height: 1.5;
  }

  /* 알림 배지 (네디걸 채팅 스타일) */
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
    animation: alertBlink 0.8s infinite alternate;
  }

  @keyframes alertBlink {
    0% { opacity: 0.85; transform: scale(1); }
    100% { opacity: 1; transform: scale(1.03); }
  }

  /* 하단 오모리 스타일 대화창 */
  #dialogue-box {
    position: absolute;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    width: min(820px, 92vw);
    z-index: 25;
    background: #14121c;
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

  .close-btn:hover {
    background: #ff758f;
  }

  /* 신문 & 서류 */
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
    background: #1e1b29;
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

  /* 노트북 정책 카드 그리드 */
  .policy-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 12px;
  }

  .policy-card {
    background: #0b0a10;
    border: 2px solid #7928ca;
    padding: 14px;
    cursor: pointer;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    transition: 0.15s;
  }

  .policy-card:hover:not(.disabled) {
    border-color: #00f5d4;
    background: #191428;
    transform: translateY(-2px);
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

  .badge-active { background: #00f5d4; color: #0b0a10; }
  .badge-pending { background: #ffb703; color: #0b0a10; }
  .badge-ready { background: #7928ca; color: #fff; }

  .mixer-box {
    background: #0b0a10;
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

  .action-btn:hover {
    background: #9d4edd;
  }

  .choice-btn {
    font-family: 'DungGeunMo', monospace;
    display: block;
    width: 100%;
    text-align: left;
    background: #191428;
    border: 2px solid #7928ca;
    color: #f0ece1;
    padding: 12px 16px;
    margin-bottom: 10px;
    cursor: pointer;
    font-size: 0.95rem;
  }

  .choice-btn:hover {
    background: #2b223d;
    border-color: #00f5d4;
  }

  #hover-tooltip {
    position: absolute;
    pointer-events: none;
    background: #14121c;
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

// 줌인 애니메이션 변수
let zoomProgress = 0; // 0.0 ~ 1.0

let weather = {
  type: 'CLEAR',
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
  phAlert: false,          
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

const FACTORIES = [
  { id: 'factory1', name: '제1 화력·담수화 발전소', role: '전기와 물을 공급하는 거대한 에너지 공장이야.', pollutants: 'SO₂, NOₓ', relX: 0.22, relY: 0.42, relW: 0.13, relH: 0.16 },
  { id: 'factory2', name: '제2 석유화학 플랜트', role: '외화를 벌어다 준다지만 매연을 어마어마하게 뿜어내지.', pollutants: 'VOCs, SO₂, PM2.5', relX: 0.44, relY: 0.43, relW: 0.14, relH: 0.15 },
  { id: 'factory3', name: '제3 시멘트 제련소', role: '건물 올리느라 쉴 새 없이 돌아가는 시멘트 공장이야.', pollutants: '고농도 미세먼지, 중금속 분진', relX: 0.68, relY: 0.41, relW: 0.13, relH: 0.17 }
];

const DESK_ITEMS = [
  { id: 'beaker', name: '🧪 pH 배합기 (산성비 중화 준비)', relX: 0.04, relY: 0.65, relW: 0.08, relH: 0.14 },
  { id: 'radio', name: '🛩️ 인공강우 무전기 (비 내리기)', relX: 0.14, relY: 0.65, relW: 0.07, relH: 0.13 },
  { id: 'newspaper', name: '📰 조간신문', relX: 0.23, relY: 0.74, relW: 0.12, relH: 0.12 },
  { id: 'documents', name: '📁 서류 더미 (목표 체크리스트)', relX: 0.37, relY: 0.70, relW: 0.12, relH: 0.14 },
  { id: 'laptop', name: '💻 업무용 노트북 (정책 구매)', relX: 0.51, relY: 0.64, relW: 0.15, relH: 0.17 },
  { id: 'sensor_pad', name: '📡 대기질 센서 정비기', relX: 0.68, relY: 0.67, relW: 0.07, relH: 0.12 },
  { id: 'photo', name: '🖼️ 가족사진', relX: 0.77, relY: 0.73, relW: 0.06, relH: 0.10 },
  { id: 'penholder', name: '✏️ 펜꽂이', relX: 0.84, relY: 0.72, relW: 0.04, relH: 0.10 },
  { id: 'phone', name: '☎️ 민원 전화기', relX: 0.83, relY: 0.61, relW: 0.07, relH: 0.09 },
  { id: 'calendar', name: '📅 캘린더', relX: 0.91, relY: 0.71, relW: 0.06, relH: 0.11 }
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
  },
  {
    title: "주민들의 미세먼지 성토 대란",
    desc: "기침하는 주민들이 시청 앞으로 몰려왔어! 비상 조치가 필요해!",
    choices: [
      { text: "차량 2부제랑 공장 가동 일시 중지 때리기! (예산 -10억)", effect: () => { budget = Math.max(0, budget - 10); weather.pm25 = Math.max(10, weather.pm25 - 20); return "지갑은 좀 털렸지만 공기는 확실히 맑아졌어!"; } },
      { text: "마스크 나눠주면서 마인드 컨트롤 권고하기", effect: () => { weather.pm25 = Math.max(10, weather.pm25 - 5); return "주민들 불만은 남았지만 뭐 어쩌겠어, 다 먹고살자고 하는 짓인데."; } }
    ]
  }
];

// 모래바람 파티클 생성
let dustParticles = [];
for (let i = 0; i < 120; i++) {
  dustParticles.push({
    x: Math.random() * 3000,
    y: Math.random() * 2000,
    speedX: 2 + Math.random() * 5,
    speedY: -0.5 + Math.random() * 1.2,
    size: 1.5 + Math.random() * 3,
    alpha: 0.2 + Math.random() * 0.5
  });
}

function setSpeed(spd) {
  timeMultiplier = spd;
  document.querySelectorAll('.speed-btn').forEach(b => b.classList.remove('active'));
  document.getElementById(`spd-${spd}`).classList.add('active');
}

// 오프닝 줌인 연출 트리거
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

// 오브젝트 상호작용
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
  else if (id === 'laptop') {
    renderLaptopModal();
  }
  else if (id === 'beaker') {
    openPhMixerMinigame();
  }
  else if (id === 'radio') {
    openSeedingMinigame();
  }
  else if (id === 'sensor_pad') {
    openSensorRepairMinigame();
  }
  else if (id === 'phone') {
    openAuditPhoneModal();
  }
  else if (id === 'photo') {
    showDialogue('나', '지갑 속 가족사진... 힘들 때마다 이거 보면서 버티는 거지 뭐.');
  }
  else if (id === 'penholder') {
    showDialogue('나', '볼펜 촉이 다 닳았네. 오늘 밤에도 계산기 두드리려면 펜 좀 깎아야겠어.');
  }
  else if (id === 'calendar') {
    showDialogue('나', `벌써 ${month}개월째 ${day}일이야. 평가일까지 앞으로 ${30 - day}일 남았네!`);
  }
  else if (id.startsWith('factory')) {
    const f = FACTORIES.find(item => item.id === id);
    openModal(`
      <div style="margin-bottom:10px; font-size:1.1rem; color:#ff758f;">🏭 ${f.name}</div>
      <div style="line-height:1.7; font-size:0.95rem; background:#191428; padding:15px; border:2px solid #7928ca;">
        <p><strong style="color:#00f5d4;">[역할]</strong><br>${f.role}</p><br>
        <p><strong style="color:#ff758f;">[배출 물질]</strong><br>${f.pollutants}</p>
      </div>
    `);
  }
}

// pH 배합기 미니게임
function openPhMixerMinigame() {
  if (activeTasks.phPrepared) {
    showDialogue('나', '이미 알칼리 중화제 배합을 깔끔하게 끝내놨지! 언제든 비가 와도 산성비 걱정은 붙들어 메라구.');
    return;
  }
  openModal(`
    <div style="margin-bottom:10px; font-size:1.1rem; color:#00f5d4;">🧪 pH 배합기 (산성비 사전 중화)</div>
    <p style="font-size:0.9rem; color:#ff758f; margin-bottom:12px;">슬라이더를 움직여 알칼리 중화제를 딱 맞는 양으로 배합해봐.</p>
    <div class="mixer-box">
      <p style="font-size:1.1rem; margin-bottom:10px;">소석회/탄산칼슘 투입량: <span id="mix-val" style="color:#00f5d4; font-size:1.3rem;">150</span> kg</p>
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
  if (val >= 120 && val <= 180) {
    showDialogue('나', `크 완벽한 황금 비율이야! (${val}kg) pH 6.5 이상의 깨끗한 단비가 내려줄 거야!`);
  } else {
    showDialogue('나', `약간 오차가 있지만(${val}kg) 일단 중화 세팅은 완료했어.`);
  }
  updateAlertStrip();
}

// 인공강우 미니게임
function openSeedingMinigame() {
  if (!activeTasks.phPrepared) {
    showDialogue('나', '어허, 순서가 있지! 먼저 책상 위 [pH 배합기]로 중화 세팅부터 끝내야 산성비 피해를 막을 수 있어.');
    return;
  }
  const cloudDesc = weather.cloudType === 'WARM' ? '따뜻한 구름 (흡습성 입자 적합)' : '차가운 과냉각 구름 (빙정핵 입자 적합)';
  openModal(`
    <div style="margin-bottom:10px; font-size:1.1rem; color:#00f5d4;">🛩️ 인공강우 작전 무전기</div>
    <p style="font-size:0.9rem; color:#ff758f; margin-bottom:10px;">구름 상태: <strong>${cloudDesc}</strong></p>
    <div style="margin-bottom:12px; background:#191428; padding:12px; border:2px solid #7928ca;">
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
  const selected = document.querySelector('input[name="seedChoice"]:checked').value;
  budget -= 10;
  activeTasks.phPrepared = false;
  closeModal();

  const isCorrect = (selected === weather.cloudType);
  if (isCorrect || weather.rainProb > 40) {
    weather.type = 'RAIN';
    totalRainDays++;
    weather.ph = +(6.3 + Math.random() * 0.5).toFixed(2);
    droughtLevel = Math.max(5, droughtLevel - 12);
    showDialogue('나', `대성공이야! pH 배합기로 산성비를 막고 깨끗한 단비(pH ${weather.ph})가 내려 가뭄이 해소되었어!`);
  } else {
    showDialogue('나', '촉매가 맞지 않아 구름이 흩어져버렸어... 아까운 내 10억!');
  }
  updateWeatherHUD();
  updateAlertStrip();
}

// 센서 정비 미니게임
function openSensorRepairMinigame() {
  if (!activeTasks.sensorDirty) {
    showDialogue('나', '센서 모두 아주 정상적으로 작동 중이야.');
    return;
  }
  openModal(`
    <div style="margin-bottom:10px; font-size:1.1rem; color:#ff758f;">📡 대기질 센서 정비기</div>
    <p style="font-size:0.9rem; color:#f0ece1; margin-bottom:12px;">모래바람으로 먹통이 된 <strong>4개의 센서</strong>를 클릭해서 먼지를 털어내줘!</p>
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
    el.style.color = "#0b0a10";
    el.innerHTML = "✅ 정상 작동 중";
    cleanedSensors++;
    if (cleanedSensors >= 4) {
      cleanedSensors = 0;
      activeTasks.sensorDirty = false;
      budget += 10;
      setTimeout(() => {
        closeModal();
        updateAlertStrip();
        showDialogue('나', '모든 센서 청소 완료! 보상으로 연구 수당 10억 획득!');
      }, 300);
    }
  }
}

// 민원 전화 미니게임
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

// 노트북 정책 터미널
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
      <button class="action-btn" style="background:#191428; margin-left:10px;" onclick="renderLaptopModal()">돌아가기</button>
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

// 일일 시뮬레이션
function simulateNewDay() {
  let newlyApplied = [];
  POLICIES.forEach(p => {
    if (p.status === 'PENDING' && day >= p.applyDay) {
      p.status = 'ACTIVE';
      newlyApplied.push(p.name);
    }
  });

  const activeIds = POLICIES.filter(p => p.status === 'ACTIVE').map(p => p.id);

  const roll = Math.random() * 100;
  if (roll < 2) weather.type = 'HEAVY_RAIN';
  else if (roll < 17) weather.type = 'DROUGHT';
  else if (roll < 47) {
    weather.type = 'DUST';
    activeTasks.sensorDirty = true;
    cleanedSensors = 0;
  }
  else weather.type = 'CLEAR';

  weather.cloudType = Math.random() < 0.5 ? 'WARM' : 'COLD';

  if (!activeTasks.phoneRinging && Math.random() < 0.4) {
    activeTasks.phoneRinging = true;
    activeTasks.currentAudit = AUDIT_SCENARIOS[Math.floor(Math.random() * AUDIT_SCENARIOS.length)];
  }

  const dirs = ['북풍', '북서풍', '서풍', '남서풍', '남동풍', '동풍'];
  weather.windDir = dirs[Math.floor(Math.random() * dirs.length)];
  weather.windSpeed = +(1.2 + Math.random() * 6).toFixed(1);
  weather.temp = weather.type === 'DROUGHT' ? 42 : 32;
  weather.humidity = weather.type === 'HEAVY_RAIN' ? 90 : (weather.type === 'DROUGHT' ? 18 : 30);
  if (activeIds.includes('seeding')) weather.humidity += 15;

  let so2Gen = activeIds.includes('fgd') ? 4 : 16;
  let pmGen = activeIds.includes('esp') ? 4 : 15;
  if (weather.type === 'DUST') pmGen += 25;

  weather.so2 = Math.max(8, weather.so2 + so2Gen - (weather.windSpeed * 2));
  weather.pm25 = Math.max(10, weather.pm25 + pmGen - (weather.windSpeed * 2));

  let rainProb = (weather.humidity * 0.5) - (weather.temp * 0.25);
  if (activeIds.includes('seeding')) rainProb += 25;
  weather.rainProb = Math.max(5, Math.min(90, Math.round(rainProb)));

  const didRain = (Math.random() * 100) < weather.rainProb;
  if (didRain) {
    weather.type = 'RAIN';
    totalRainDays++;
    droughtLevel = Math.max(5, droughtLevel - 9);
  } else {
    droughtLevel = Math.min(100, droughtLevel + (weather.type === 'DROUGHT' ? 5 : 2));
  }

  updateWeatherHUD();
  updateAlertStrip();

  if (newlyApplied.length > 0) {
    showDialogue('나', `[${newlyApplied.join(', ')}] 설치 공사가 완료되었습니다!`);
  }
}

function updateWeatherHUD() {
  const hud = document.getElementById('hud-weather');
  const names = {
    'CLEAR': '☀️ 맑음 (사막 건조)',
    'DROUGHT': '🔥 극심한 폭염 가뭄',
    'DUST': '🌪️ 모래바람(황사) 경보',
    'HEAVY_RAIN': '⛈️ 국지성 폭우',
    'RAIN': '🌧️ 단비 내리는 중'
  };
  const hasSensor = POLICIES.find(p => p.id === 'sensor').status === 'ACTIVE';
  const sensorText = (hasSensor && !activeTasks.sensorDirty) ? `SO₂: ${weather.so2.toFixed(0)} | PM2.5: ${weather.pm25.toFixed(0)}` : `센서 점검 필요`;

  hud.innerHTML = `
    <div style="font-weight:bold; color:#ff758f;">${names[weather.type]}</div>
    <div style="font-size:0.8rem; color:#b19cd9;">바람: ${weather.windDir} | 습도: ${weather.humidity}%</div>
    <div style="font-size:0.8rem; color:#00f5d4; margin-top:2px;">${sensorText}</div>
  `;
}

// 30일차 결산
function checkMonthEnd() {
  const status = getChecklistStatus();
  if (status.check1 && status.check2) {
    scene = 'ENDING';
    isPaused = true;
    openModal(`
      <div style="text-align:center; padding:15px;">
        <h2 style="font-size:1.6rem; color:#00f5d4; margin-bottom:12px;">🌟 HAPPY ENDING : 푸른 레인 시티</h2>
        <p style="font-size:1rem; line-height:1.7; color:#f0ece1; margin-bottom:20px;">
          가뭄도 잡고 환경 오염도 완벽하게 막아냈어!<br>도시를 푸르게 되살린 영웅으로 인정받았다!
        </p>
        <button class="start-btn" onclick="location.reload()">처음부터 다시하기</button>
      </div>
    `);
  } else if (status.check1 || status.check2) {
    month++;
    day = 1;
    gameMinutes = 7 * 60;
    budget += 100;
    showDialogue('나', `절반의 성과로 계약 연장! ${month}개월째 추가 예산 100억을 받고 마저 달린다!`);
  } else {
    scene = 'ENDING';
    isPaused = true;
    openModal(`
      <div style="text-align:center; padding:15px;">
        <h2 style="font-size:1.6rem; color:#ff2a5f; margin-bottom:12px;">💀 BAD ENDING : 해고 통지서</h2>
        <p style="font-size:1rem; line-height:1.7; color:#f0ece1; margin-bottom:20px;">
          결국 사막 도시를 살리지 못하고 쓸쓸히 쫓겨나고 말았다...
        </p>
        <button class="start-btn" onclick="location.reload()">다시 도전하기</button>
      </div>
    `);
  }
}

// --- 오모리 & 니디걸 감성 그래픽 렌더링 ---
function drawTitleBackground() {
  // 암울하면서도 레트로한 사막 도시 전경
  ctx.fillStyle = '#0b0a10';
  ctx.fillRect(0, 0, width, height);

  ctx.fillStyle = '#191428';
  ctx.fillRect(0, height * 0.5, width, height * 0.5);

  // 실루엣 건물들
  const buildings = [0.1, 0.22, 0.35, 0.48, 0.62, 0.75, 0.88];
  buildings.forEach((bx, idx) => {
    ctx.fillStyle = idx % 2 === 0 ? '#241e38' : '#1c162b';
    const bw = width * 0.08;
    const bh = height * (0.3 + (idx % 3) * 0.09);
    ctx.fillRect(width * bx, height * 0.5 - bh, bw, bh);

    // 니디걸풍 네온 창문 불빛
    ctx.fillStyle = idx === 3 ? '#00f5d4' : '#ff758f';
    for(let wy = height * 0.5 - bh + 15; wy < height * 0.5 - 20; wy += 25) {
      ctx.fillRect(width * bx + 10, wy, 8, 12);
      ctx.fillRect(width * bx + bw - 18, wy, 8, 12);
    }
  });

  // 모래바람 입자
  ctx.fillStyle = 'rgba(255, 183, 3, 0.35)';
  dustParticles.forEach(p => {
    ctx.fillRect(p.x % width, p.y % height, p.size, p.size);
    p.x += p.speedX * 1.5;
    p.y += p.speedY;
  });
}

// 줌인 연출 렌더링
function drawZoomInBackground() {
  zoomProgress += 0.012; // 줌인 속도
  if (zoomProgress >= 1.0) {
    zoomProgress = 1.0;
    scene = 'OFFICE';
    document.getElementById('hud-clock').style.display = 'flex';
    document.getElementById('hud-weather').style.display = 'block';
    updateWeatherHUD();
    updateAlertStrip();
    showDialogue('나', '휴, 사막 모래바람을 뚫고 드디어 사무실에 도착했어. 먼저 책상 위 [pH 배합기]로 중화 세팅을 끝내고 기상을 체크해보자!');
    return;
  }

  // 줌인 스케일 계산 (중앙 4번 건물 창문으로 줌인)
  ctx.save();
  const scale = 1 + zoomProgress * 4.5;
  const targetX = width * 0.52;
  const targetY = height * 0.35;

  ctx.translate(targetX, targetY);
  ctx.scale(scale, scale);
  ctx.translate(-targetX, -targetY);

  drawTitleBackground();
  ctx.restore();

  // 줌인될 때 화면 암전 페이드
  ctx.fillStyle = `rgba(11, 10, 16, ${zoomProgress * 0.6})`;
  ctx.fillRect(0, 0, width, height);
}

function drawOfficeScene() {
  // 오모리풍 차분하고 감성적인 실내 배경 + 네디걸 포인트 네온
  ctx.fillStyle = '#14121c';
  ctx.fillRect(0, 0, width, height * 0.65);

  // 창밖 풍경 (사막 도시와 노을)
  const skyGrad = ctx.createLinearGradient(0, 0, 0, height * 0.65);
  skyGrad.addColorStop(0, '#241e38');
  skyGrad.addColorStop(0.7, '#4a2838');
  skyGrad.addColorStop(1, '#7928ca');
  ctx.fillStyle = skyGrad;
  ctx.fillRect(0, 0, width, height * 0.62);

  // 창밖 공장 실루엣
  FACTORIES.forEach(f => {
    const fx = width * f.relX;
    const fy = height * f.relY;
    const fw = width * f.relW;
    const fh = height * f.relH;
    ctx.fillStyle = '#0b0a10';
    ctx.fillRect(fx, fy, fw, fh);
    ctx.fillStyle = '#ff2a5f';
    ctx.fillRect(fx + fw * 0.3, fy - 15, fw * 0.1, 15);
  });

  // 창틀 (네디걸 핑크 테두리)
  ctx.strokeStyle = '#ff758f';
  ctx.lineWidth = 6;
  ctx.strokeRect(0, 0, width, height * 0.62);

  // 원목 책상
  ctx.fillStyle = '#2b1f3d';
  ctx.fillRect(0, height * 0.62, width, height * 0.38);
  ctx.fillStyle = '#191226';
  ctx.fillRect(0, height * 0.62, width, 14);

  drawDeskObjects();
}

function drawDeskObjects() {
  const blink = Math.floor(Date.now() / 300) % 2 === 0;

  DESK_ITEMS.forEach(item => {
    const ix = width * item.relX;
    const iy = height * item.relY;
    const iw = width * item.relW;
    const ih = height * item.relH;

    ctx.fillStyle = '#1e192b';
    ctx.strokeStyle = '#b19cd9';
    ctx.lineWidth = 2;
    ctx.fillRect(ix, iy, iw, ih);
    ctx.strokeRect(ix, iy, iw, ih);

    // 오브젝트별 디테일
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

// 메인 60fps 델타타임 루프
function gameLoop(timestamp) {
  if (!lastTimestamp) lastTimestamp = timestamp;
  const deltaSec = (timestamp - lastTimestamp) / 1000;
  lastTimestamp = timestamp;

  ctx.clearRect(0, 0, width, height);

  if (scene === 'TITLE') {
    drawTitleBackground();
  } else if (scene === 'ZOOM_IN') {
    drawZoomInBackground();
  } else if (scene === 'OFFICE' || scene === 'ENDING') {
    drawOfficeScene();

    if (scene === 'OFFICE' && !isPaused) {
      gameMinutes += deltaSec * 4.67 * timeMultiplier;

      if (gameMinutes >= 21 * 60) {
        if (day >= 30) {
          checkMonthEnd();
        } else {
          day++;
          gameMinutes = 7 * 60;
          simulateNewDay();
        }
      }

      const hrs = Math.floor(gameMinutes / 60);
      const mins = Math.floor(gameMinutes % 60);
      const prefix = month > 1 ? `${month}개월째 ` : '';
      document.getElementById('clock-day-text').innerText = `${prefix}${day}일차`;
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
