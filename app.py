import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Rain City",
    page_icon="🌧️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Streamlit 기본 여백 및 헤더 숨김 처리 (풀스크린 게임 몰입감 확보)
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .block-container {
            padding-top: 0rem;
            padding-bottom: 0rem;
            padding-left: 0rem;
            padding-right: 0rem;
            max-width: 100%;
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
  @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;800&family=Gowun+Batang:wght@400;700&family=Noto+Sans+KR:wght@300;400;600&display=swap');

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
    background-color: #0d0f14;
    font-family: 'Noto Sans KR', sans-serif;
    color: #f0ece1;
  }

  #game-container {
    position: relative;
    width: 100vw;
    height: 100vh;
    overflow: hidden;
    background: #141218;
  }

  canvas {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: block;
  }

  /* 레이튼 + 할로우 나이트 감성 UI 테두리 */
  .hollow-panel {
    background: rgba(18, 20, 28, 0.94);
    border: 2px solid #8c7a5b;
    box-shadow: 0 0 25px rgba(0, 0, 0, 0.85), inset 0 0 15px rgba(140, 122, 91, 0.25);
    border-radius: 12px;
    padding: 24px;
    position: relative;
  }

  .hollow-panel::before {
    content: "✧";
    position: absolute;
    top: -12px;
    left: 50%;
    transform: translateX(-50%);
    background: #12141c;
    padding: 0 10px;
    color: #d4bc8b;
    font-size: 16px;
  }

  /* 타이틀 화면 오버레이 */
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

  #title-overlay.zooming {
    transform: scale(4.5) translate(5%, -5%);
    opacity: 0;
    pointer-events: none;
  }

  .title-logo {
    font-family: 'Cinzel', serif;
    font-size: clamp(3.5rem, 7vw, 6rem);
    font-weight: 800;
    letter-spacing: 0.18em;
    color: #f7eedc;
    text-shadow: 0 4px 20px rgba(0,0,0,0.8), 0 0 40px rgba(212, 188, 139, 0.4);
    margin-bottom: 10px;
  }

  .title-sub {
    font-family: 'Gowun Batang', serif;
    font-size: 1.15rem;
    letter-spacing: 0.25em;
    color: #d6c5a7;
    margin-bottom: 45px;
    text-shadow: 0 2px 10px rgba(0,0,0,0.9);
  }

  .start-btn {
    font-family: 'Cinzel', serif;
    font-size: 1.3rem;
    letter-spacing: 0.2em;
    padding: 14px 48px;
    background: rgba(20, 22, 30, 0.75);
    color: #f5ebd6;
    border: 1.5px solid #c9b182;
    border-radius: 30px;
    cursor: pointer;
    transition: all 0.35s ease;
    box-shadow: 0 0 20px rgba(0,0,0,0.6);
  }

  .start-btn:hover {
    background: #c9b182;
    color: #14151c;
    box-shadow: 0 0 30px rgba(201, 177, 130, 0.7);
    transform: translateY(-2px);
  }

  /* 우측 상단 시계 HUD (좋은 피자, 위대한 피자 스타일) */
  #hud-clock {
    position: absolute;
    top: 22px;
    right: 26px;
    z-index: 15;
    background: linear-gradient(135deg, #2b241d 0%, #1a1715 100%);
    border: 2px solid #b89f74;
    border-radius: 14px;
    padding: 12px 22px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.65);
    display: none;
    align-items: center;
    gap: 14px;
  }

  .clock-day {
    font-family: 'Gowun Batang', serif;
    font-size: 1.25rem;
    font-weight: 700;
    color: #f3d59b;
  }

  .clock-time {
    font-family: 'Noto Sans KR', sans-serif;
    font-size: 1.15rem;
    font-weight: 600;
    color: #ffffff;
    background: rgba(255,255,255,0.08);
    padding: 4px 10px;
    border-radius: 8px;
  }

  /* 좌측 상단 간략 기상/환경 배지 */
  #hud-weather {
    position: absolute;
    top: 22px;
    left: 26px;
    z-index: 15;
    background: rgba(22, 24, 33, 0.85);
    border: 1.5px solid #7d7365;
    border-radius: 12px;
    padding: 10px 18px;
    display: none;
    font-size: 0.92rem;
    line-height: 1.5;
    box-shadow: 0 4px 14px rgba(0,0,0,0.5);
  }

  /* 하단 대화창 (레이튼 스타일) */
  #dialogue-box {
    position: absolute;
    bottom: 24px;
    left: 50%;
    transform: translateX(-50%);
    width: min(820px, 90vw);
    z-index: 25;
    background: linear-gradient(180deg, rgba(28, 25, 23, 0.96) 0%, rgba(17, 16, 18, 0.98) 100%);
    border: 2px solid #c7ae80;
    border-radius: 14px;
    padding: 18px 26px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.85);
    display: none;
    cursor: pointer;
  }

  .speaker-tag {
    display: inline-block;
    background: #8f7449;
    color: #fff9ed;
    font-weight: 700;
    font-size: 0.9rem;
    padding: 3px 14px;
    border-radius: 20px;
    margin-bottom: 8px;
    letter-spacing: 0.05em;
  }

  .dialogue-text {
    font-family: 'Gowun Batang', serif;
    font-size: 1.12rem;
    line-height: 1.65;
    color: #f5efe2;
  }

  .dialogue-next {
    text-align: right;
    font-size: 0.82rem;
    color: #c7ae80;
    margin-top: 6px;
    animation: pulse 1.4s infinite;
  }

  @keyframes pulse {
    0%, 100% { opacity: 0.4; }
    50% { opacity: 1; }
  }

  /* 모달 오버레이 (신문, 서류더미, 노트북, 공장정보, 엔딩) */
  #modal-backdrop {
    position: absolute;
    inset: 0;
    background: rgba(8, 10, 14, 0.72);
    backdrop-filter: blur(4px);
    z-index: 30;
    display: none;
    align-items: center;
    justify-content: center;
  }

  .modal-card {
    width: min(760px, 92vw);
    max-height: 85vh;
    overflow-y: auto;
  }

  .modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid rgba(201, 177, 130, 0.35);
    padding-bottom: 12px;
    margin-bottom: 18px;
  }

  .modal-title {
    font-family: 'Gowun Batang', serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: #f2dfb8;
  }

  .close-btn {
    background: none;
    border: 1px solid #8c7a5b;
    color: #d6c5a7;
    font-size: 1rem;
    padding: 4px 12px;
    border-radius: 6px;
    cursor: pointer;
  }

  .close-btn:hover {
    background: #8c7a5b;
    color: #12141c;
  }

  /* 신문 스타일 */
  .newspaper-sheet {
    background: #e8dec8;
    color: #241f18;
    padding: 28px;
    border-radius: 6px;
    font-family: 'Gowun Batang', serif;
    box-shadow: inset 0 0 30px rgba(110, 88, 55, 0.35);
  }

  .news-head {
    text-align: center;
    border-top: 3px double #241f18;
    border-bottom: 3px double #241f18;
    padding: 10px 0;
    margin-bottom: 16px;
  }

  /* 서류 더미 스타일 */
  .dossier-box {
    background: #f4efe4;
    color: #222;
    padding: 24px;
    border-radius: 8px;
    font-family: 'Gowun Batang', serif;
  }

  .check-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 14px;
    margin: 10px 0;
    background: #e6decb;
    border-left: 5px solid #7d6844;
    border-radius: 4px;
    font-size: 1.08rem;
    font-weight: 700;
  }

  /* 노트북 정책 UI */
  .policy-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(290px, 1fr));
    gap: 14px;
  }

  .policy-card {
    background: rgba(32, 36, 48, 0.9);
    border: 1px solid #695e4c;
    border-radius: 10px;
    padding: 15px;
    cursor: pointer;
    transition: all 0.25s ease;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }

  .policy-card:hover:not(.disabled) {
    border-color: #e3c891;
    transform: translateY(-2px);
    background: rgba(45, 50, 66, 0.95);
  }

  .policy-card.disabled {
    opacity: 0.55;
    cursor: not-allowed;
  }

  .badge-status {
    display: inline-block;
    font-size: 0.78rem;
    padding: 2px 8px;
    border-radius: 10px;
    margin-top: 8px;
  }

  .badge-active { background: #2d6a4f; color: #d8f3dc; }
  .badge-pending { background: #b58328; color: #fff3b0; }
  .badge-ready { background: #3d405b; color: #e0e1dd; }

  /* 확인 다이얼로그 */
  .confirm-box {
    text-align: center;
    padding: 20px 10px;
  }

  .btn-group {
    display: flex;
    justify-content: center;
    gap: 16px;
    margin-top: 24px;
  }

  .action-btn {
    padding: 10px 28px;
    border-radius: 8px;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    border: none;
  }

  .btn-yes { background: #c9a66b; color: #161512; }
  .btn-yes:hover { background: #e0be82; }
  .btn-no { background: #3b3e4a; color: #e6e2d8; }
  .btn-no:hover { background: #505463; }

  /* 툴팁 (마우스 호버 시 오브젝트 이름 표시) */
  #hover-tooltip {
    position: absolute;
    pointer-events: none;
    background: rgba(18, 20, 28, 0.92);
    border: 1px solid #d4bc8b;
    color: #f7eedc;
    padding: 5px 12px;
    border-radius: 20px;
    font-size: 0.88rem;
    z-index: 18;
    display: none;
    transform: translate(-50%, -140%);
    white-space: nowrap;
    box-shadow: 0 4px 12px rgba(0,0,0,0.6);
  }
</style>
</head>
<body>

<div id="game-container">
  <canvas id="gameCanvas"></canvas>

  <!-- 타이틀 화면 -->
  <div id="title-overlay">
    <div class="title-logo">RAIN CITY</div>
    <div class="title-sub">사막 위에 내리는 첫 번째 비의 기록</div>
    <button class="start-btn" onclick="startGame()">START</button>
  </div>

  <!-- 좌측 상단 기상 및 대기질 현황 -->
  <div id="hud-weather"></div>

  <!-- 우측 상단 시간 HUD -->
  <div id="hud-clock">
    <span class="clock-day" id="clock-day-text">1일차</span>
    <span class="clock-time" id="clock-time-text">07시 00분</span>
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
function resize() {
  width = canvas.width = window.innerWidth;
  height = canvas.height = window.innerHeight;
}
window.addEventListener('resize', resize);
resize();

// --- 게임 상태 변수 ---
let scene = 'TITLE'; // 'TITLE', 'ZOOMING', 'OFFICE', 'ENDING'
let zoomProgress = 0;

// 시간 시스템: 1일 = 07:00 ~ 21:00 (14시간 = 840분)
// 현실 10분(600초) = 게임 1일(840분) => 현실 1초 = 게임 1.4분
let day = 1;
let month = 1;
let gameMinutes = 7 * 60; // 07:00 시작 (420분)
let lastTimestamp = 0;
let isPaused = false;

// 도시 환경 및 시뮬레이션 변수
let budget = 250; // 초기 예산 (억 단위)
let droughtLevel = 68; // 가뭄 진행도 (%) - 목표: 30% 미만
let totalRainDays = 0;
let acidRainDays = 0;

// 대기질 및 기상 변수 (매일 변화)
let weather = {
  type: 'CLEAR', // 'CLEAR', 'DROUGHT', 'DUST', 'HEAVY_RAIN', 'RAIN'
  windDir: '북서풍',
  windSpeed: 3.2,
  humidity: 28,
  temp: 36,
  rainProb: 15,
  so2: 75,
  nox: 65,
  pm25: 80,
  ph: 4.6,
  ecoHealth: 45
};

// 정책 데이터 (선택 후 2일 뒤에 적용)
const POLICIES = [
  {
    id: 'fgd',
    name: '배연탈황설비 (FGD)',
    cost: 45,
    desc: '공장·발전소에서 배출되는 SO₂를 알칼리성 물질과 반응시켜 제거하여 산성비 위험을 크게 낮춥니다.',
    status: 'READY', // READY, PENDING, ACTIVE
    applyDay: null
  },
  {
    id: 'esp',
    name: '전기집진기 (ESP)',
    cost: 40,
    desc: '미세먼지(PM2.5)와 황산염 입자를 정전기로 포집하여 대기질을 획기적으로 개선합니다.',
    status: 'READY',
    applyDay: null
  },
  {
    id: 'sensor',
    name: '정밀 대기질 센서망',
    cost: 25,
    desc: 'SO₂, NOₓ, PM2.5, 강수 pH를 실시간 측정해 오염 확산과 산성비 위험을 정밀 분석합니다.',
    status: 'READY',
    applyDay: null
  },
  {
    id: 'raingarden',
    name: '빗물정원 조성',
    cost: 30,
    desc: '빗물이 토양으로 자연 침투하도록 유도해 홍수를 줄이고 오염물질의 하천 유입을 막습니다.',
    status: 'READY',
    applyDay: null
  },
  {
    id: 'permeable',
    name: '투수성 포장 도로',
    cost: 35,
    desc: '사막 도시의 아스팔트를 투수성 소재로 교체하여 빗물 흡수율과 지하수 함양을 높입니다.',
    status: 'READY',
    applyDay: null
  },
  {
    id: 'reservoir',
    name: '지하 빗물저류조',
    cost: 50,
    desc: '폭우 시 도심 침수를 막고, 저장된 빗물을 활용해 가뭄 진행도를 크게 낮춥니다.',
    status: 'READY',
    applyDay: null
  },
  {
    id: 'seeding',
    name: '인공강우 시딩 장비',
    cost: 55,
    desc: '구름에 흡습성 입자 및 빙정핵을 살포해 강수 확률과 강수량을 높여 가뭄을 해소합니다.',
    status: 'READY',
    applyDay: null
  }
];

// 공장 데이터 (통유리창 너머 3개 공장)
const FACTORIES = [
  {
    id: 'factory1',
    name: '제1 화력·담수화 복합발전소',
    role: '도시 전체의 전력 공급과 바닷물 담수화를 담당하는 핵심 에너지 시설입니다.',
    pollutants: '아황산가스(SO₂), 질소산화물(NOₓ), 온배수',
    relX: 0.22, relY: 0.42, relW: 0.13, relH: 0.16
  },
  {
    id: 'factory2',
    name: '제2 석유화학·정제 플랜트',
    role: '사막 부자도시의 외화를 벌어들이는 주력 석유화학 제품 생산 공장입니다.',
    pollutants: '휘발성유기화합물(VOCs), 아황산가스(SO₂), 초미세먼지(PM2.5)',
    relX: 0.44, relY: 0.43, relW: 0.14, relH: 0.15
  },
  {
    id: 'factory3',
    name: '제3 시멘트·건설자재 제련소',
    role: '마천루 건설에 필요한 시멘트와 금속 자재를 가공하는 중공업 시설입니다.',
    pollutants: '고농도 미세먼지(PM10/PM2.5), 질소산화물(NOₓ), 중금속 분진',
    relX: 0.68, relY: 0.41, relW: 0.13, relH: 0.17
  }
];

// 책상 위 오브젝트 정의
const DESK_ITEMS = [
  { id: 'newspaper', name: '신문 기사', relX: 0.12, relY: 0.72, relW: 0.16, relH: 0.13 },
  { id: 'documents', name: '서류 더미 (예산 & 체크리스트)', relX: 0.31, relY: 0.69, relW: 0.14, relH: 0.15 },
  { id: 'laptop', name: '업무용 노트북 (환경 정책)', relX: 0.48, relY: 0.64, relW: 0.18, relH: 0.18 },
  { id: 'photo', name: '고향의 가족사진', relX: 0.69, relY: 0.67, relW: 0.08, relH: 0.12 },
  { id: 'penholder', name: '필기구 꽂이 (볼펜·샤프)', relX: 0.79, relY: 0.68, relW: 0.06, relH: 0.11 },
  { id: 'calendar', name: '탁상 캘린더', relX: 0.87, relY: 0.69, relW: 0.09, relH: 0.12 }
];

// 파티클 (모래바람 & 빗방울)
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

// --- 시작 연출 ---
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
    showDialogue('나', '드디어 이 사막의 거대 도시에 도착했어... 고향에 있는 가족들을 위해서라도, 반드시 이 도시의 가뭄과 산성비 문제를 해결하고 성공해야 해.');
  }, 1800);
}

// --- 대화창 제어 ---
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

// --- 모달 제어 ---
function openModal(htmlContent) {
  isPaused = true;
  document.getElementById('modal-content').innerHTML = htmlContent;
  document.getElementById('modal-backdrop').style.display = 'flex';
}

function closeModal() {
  document.getElementById('modal-backdrop').style.display = 'none';
  if (document.getElementById('dialogue-box').style.display !== 'block') {
    isPaused = false;
  }
}

// --- 체크리스트 달성 판정 ---
function getChecklistStatus() {
  const acidFreq = totalRainDays === 0 ? 12.0 : (acidRainDays / Math.max(1, day)) * 100;
  const check1 = droughtLevel < 30;
  const check2 = acidFreq < 10;
  return { check1, check2, acidFreq: acidFreq.toFixed(1) };
}

// --- 오브젝트 클릭 상호작용 ---
function handleObjectClick(id) {
  if (id === 'newspaper') {
    openModal(`
      <div class="modal-header">
        <span class="modal-title">📰 레인 시티 조간신문</span>
        <button class="close-btn" onclick="closeModal()">닫기</button>
      </div>
      <div class="newspaper-sheet">
        <div class="news-head">
          <div style="font-size:0.85rem; letter-spacing:0.2em;">THE RAIN CITY CHRONICLE</div>
          <h2 style="font-size:1.6rem; margin-top:4px;">"비가 내리지 않는 황금의 도시에 희망의 단비를"</h2>
        </div>
        <p style="line-height:1.8; font-size:1.05rem;">
          끝없는 모래바람과 극심한 가뭄, 그리고 무분별한 산업화로 인한 산성비 위협이 우리 도시를 덮치고 있다.
          정부는 이 위기를 타개하기 위해 해외에서 초빙한 환경공학 전문가에게 도시의 미래를 맡겼다.
          과연 30일 안에 사막의 하늘에서 맑은 비를 내리게 하고 생태계를 되살릴 수 있을 것인가...
        </p>
      </div>
    `);
    setTimeout(() => {
      document.getElementById('dialogue-speaker').innerText = '나';
      document.getElementById('dialogue-text').innerText = '이 도시를 살려야 한다.. 내 손에 이 도시의 하늘과 고향으로 돌아갈 미래가 달려 있어.';
      document.getElementById('dialogue-box').style.display = 'block';
    }, 300);
  }
  else if (id === 'documents') {
    const status = getChecklistStatus();
    openModal(`
      <div class="modal-header">
        <span class="modal-title">📁 환경정책국 기밀 서류 더미</span>
        <button class="close-btn" onclick="closeModal()">닫기</button>
      </div>
      <div class="dossier-box">
        <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:2px solid #8c7a5b; padding-bottom:12px; margin-bottom:16px;">
          <span style="font-size:1.15rem; font-weight:700;">💰 가용 도시 환경 예산</span>
          <span style="font-size:1.5rem; font-weight:800; color:#1b4332;">${budget} 억 디르함</span>
        </div>
        <h3 style="margin-bottom:10px; color:#3d3122;">📋 30일차 최종 평가 체크리스트 (실시간 갱신)</h3>
        <div class="check-item">
          <span>1. 가뭄 진행도가 30% 미만인가? (현재: ${droughtLevel.toFixed(1)}%)</span>
          <span style="font-size:1.3rem;">${status.check1 ? '✅ 달성' : '⬜ 미달성'}</span>
        </div>
        <div class="check-item">
          <span>2. 산성비 발생 빈도가 10% 미만인가? (현재: ${status.acidFreq}%)</span>
          <span style="font-size:1.3rem;">${status.check2 ? '✅ 달성' : '⬜ 미달성'}</span>
        </div>
        <p style="margin-top:16px; font-size:0.92rem; color:#555;">
          * 30일차 종료 시 두 조건을 모두 달성하면 막대한 보너스와 함께 고향으로 귀국합니다.<br>
          * 한 가지만 달성할 경우 계약이 1개월 연장되며, 모두 실패 시 해고됩니다.
        </p>
      </div>
    `);
  }
  else if (id === 'laptop') {
    renderLaptopModal();
  }
  else if (id === 'photo') {
    showDialogue('나', '지갑 속 낡은 가족사진... 내가 타국에서 묵묵히 버티는 이유야. 꼭 부자가 되어서 당당하게 돌아갈게.');
  }
  else if (id === 'penholder') {
    showDialogue('나', '볼펜, 샤프, 제도용 연필이 빽빽하게 꽂혀 있다. 매일 밤 대기 확산 수식을 계산하느라 닳아버린 흔적들이다.');
  }
  else if (id === 'calendar') {
    const remain = 30 - day;
    showDialogue('나', `오늘은 ${month}개월째 ${day}일차야. 이번 달 평가일까지 앞으로 ${remain}일 남았어.`);
  }
  else if (id.startsWith('factory')) {
    const f = FACTORIES.find(item => item.id === id);
    openModal(`
      <div class="modal-header">
        <span class="modal-title">🏭 ${f.name}</span>
        <button class="close-btn" onclick="closeModal()">닫기</button>
      </div>
      <div style="line-height:1.8; font-size:1.05rem;">
        <p><strong style="color:#e3c891;">[시설 역할]</strong><br>${f.role}</p>
        <br>
        <p><strong style="color:#ff8fa3;">[주요 배출 오염물질]</strong><br>${f.pollutants}</p>
        <br>
        <p style="font-size:0.92rem; color:#b8b0a2;">
          ※ 배출된 SO₂와 NOₓ는 바람을 타고 확산되어 대기 중에서 황산과 질산으로 산화되며, 강수 시 산성비의 주원인이 됩니다.
        </p>
      </div>
    `);
  }
}

// --- 노트북 정책 화면 & 확인 창 ---
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
      badge = `<span class="badge-status badge-pending">⏳ 설치 중 (${p.applyDay}
