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
          <div style="font-weight:700; font-size:1.08rem; color:#f5e6c8; margin-bottom:6px;">${p.name}</div>
          <div style="font-size:0.88rem; color:#cfc9bc; line-height:1.5;">${p.desc}</div>
        </div>
        <div>${badge}</div>
      </div>
    `;
  }).join('');

  openModal(`
    <div class="modal-header">
      <span class="modal-title">💻 환경공학 정책 제어 터미널 (잔여 예산: ${budget}억)</span>
      <button class="close-btn" onclick="closeModal()">닫기</button>
    </div>
    <p style="font-size:0.9rem; color:#c9b182; margin-bottom:14px;">
      ※ 선택한 정책은 현장 시공 및 장비 반입을 거쳐 <strong>2일 후</strong>부터 도시에 적용됩니다.
    </p>
    <div class="policy-grid">${cardsHtml}</div>
  `);
}

function confirmPolicy(policyId) {
  const p = POLICIES.find(item => item.id === policyId);
  openModal(`
    <div class="confirm-box">
      <h3 style="font-family:'Gowun Batang', serif; font-size:1.45rem; color:#f5e6c8; margin-bottom:12px;">
        "${p.name}"을(를) 선택하시겠습니까?
      </h3>
      <p style="color:#cfc9bc; font-size:0.98rem;">
        소요 예산: <strong>${p.cost}억</strong> | 적용 시점: <strong>${day + 2}일차 아침</strong>
      </p>
      <div class="btn-group">
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
    p.status = 'PENDING';
    p.applyDay = day + 2;
    renderLaptopModal();
  }
}

// --- 일일 환경 & 대기화학 시뮬레이션 ---
function simulateNewDay() {
  // 1. 예약된 정책 적용 체크 (2일 후 적용)
  let newlyApplied = [];
  POLICIES.forEach(p => {
    if (p.status === 'PENDING' && day >= p.applyDay) {
      p.status = 'ACTIVE';
      newlyApplied.push(p.name);
    }
  });

  const activeIds = POLICIES.filter(p => p.status === 'ACTIVE').map(p => p.id);

  // 2. 자연재해 확률 판정 (15% 가뭄, 2% 폭우, 30% 황사)
  const roll = Math.random() * 100;
  if (roll < 2) {
    weather.type = 'HEAVY_RAIN';
  } else if (roll < 17) {
    weather.type = 'DROUGHT';
  } else if (roll < 47) {
    weather.type = 'DUST';
  } else {
    weather.type = 'CLEAR';
  }

  // 3. 바람, 습도, 기온, 강수 확률 갱신
  const dirs = ['북풍', '북서풍', '서풍', '남서풍', '남동풍', '동풍'];
  weather.windDir = dirs[Math.floor(Math.random() * dirs.length)];
  weather.windSpeed = +(1.2 + Math.random() * 6.5).toFixed(1);
  weather.temp = weather.type === 'DROUGHT' ? Math.floor(41 + Math.random() * 6) : Math.floor(29 + Math.random() * 9);
  weather.humidity = weather.type === 'HEAVY_RAIN' ? 88 : (weather.type === 'DROUGHT' ? 16 : Math.floor(25 + Math.random() * 35));
  if (activeIds.includes('seeding')) weather.humidity = Math.min(95, weather.humidity + 18);

  // 4. 오염물질 배출 및 확산 계산
  let so2Gen = activeIds.includes('fgd') ? 4 : 16;
  let noxGen = 13;
  let pmGen = activeIds.includes('esp') ? 4 : 15;
  if (weather.type === 'DUST') pmGen += 28;

  const dispersion = weather.windSpeed * 2.1;
  weather.so2 = Math.max(8, Math.min(150, weather.so2 + so2Gen - dispersion));
  weather.nox = Math.max(8, Math.min(140, weather.nox + noxGen - dispersion));
  weather.pm25 = Math.max(10, Math.min(200, weather.pm25 + pmGen - dispersion));

  // 5. 구름방울 형성 및 강수 시뮬레이션
  let rainProb = (weather.humidity * 0.55) - (weather.temp * 0.3);
  if (activeIds.includes('seeding')) rainProb += 28;
  if (weather.type === 'HEAVY_RAIN') rainProb = 95;
  if (weather.type === 'DROUGHT') rainProb = 3;
  weather.rainProb = Math.max(2, Math.min(95, Math.round(rainProb)));

  const didRain = (Math.random() * 100) < weather.rainProb;
  if (didRain) {
    if (weather.type !== 'HEAVY_RAIN') weather.type = 'RAIN';
    totalRainDays++;

    // 산화 반응 및 구름방울 흡수에 따른 강수 pH 계산
    const acidLoad = (weather.so2 * 0.021) + (weather.nox * 0.015);
    weather.ph = +(Math.max(3.9, Math.min(6.8, 6.5 - acidLoad))).toFixed(2);

    // 대기 세정 효과
    weather.so2 *= 0.65;
    weather.nox *= 0.7;
    weather.pm25 *= 0.6;

    // 가뭄 완화 (빗물정원, 투수성 포장, 저류조 시너지)
    let droughtReduce = 7;
    if (activeIds.includes('raingarden')) droughtReduce += 4;
    if (activeIds.includes('permeable')) droughtReduce += 4;
    if (activeIds.includes('reservoir')) droughtReduce += 7;
    if (weather.type === 'HEAVY_RAIN') droughtReduce += 6;
    droughtLevel = Math.max(5, droughtLevel - droughtReduce);

    if (weather.ph < 5.6) {
      acidRainDays++;
      weather.ecoHealth = Math.max(10, weather.ecoHealth - 6);
    } else {
      weather.ecoHealth = Math.min(100, weather.ecoHealth + 5);
    }
  } else {
    // 비가 안 올 경우 가뭄 심화
    let droughtInc = weather.type === 'DROUGHT' ? 5.5 : 2.2;
    if (activeIds.includes('reservoir')) droughtInc *= 0.65;
    droughtLevel = Math.min(100, droughtLevel + droughtInc);
  }

  updateWeatherHUD();

  if (newlyApplied.length > 0) {
    showDialogue('나', `오늘부터 [${newlyApplied.join(', ')}] 설비가 본격적으로 가동되기 시작했어! 도시의 공기가 달라질 거야.`);
  }
}

function updateWeatherHUD() {
  const hud = document.getElementById('hud-weather');
  const weatherNames = {
    'CLEAR': '☀️ 맑음 (사막 건조기후)',
    'DROUGHT': '🔥 자연재해: 극심한 폭염·가뭄',
    'DUST': '🌪️ 자연재해: 고농도 황사 발생',
    'HEAVY_RAIN': '⛈️ 자연재해: 국지성 폭우',
    'RAIN': '🌧️ 단비 내리는 중'
  };
  const hasSensor = POLICIES.find(p => p.id === 'sensor').status === 'ACTIVE';
  const sensorInfo = hasSensor
    ? `SO₂: ${weather.so2.toFixed(0)} | NOₓ: ${weather.nox.toFixed(0)} | PM2.5: ${weather.pm25.toFixed(0)} | 예상 pH: ${weather.ph}`
    : `대기질 정밀 데이터: [센서 미설치]`;

  hud.innerHTML = `
    <div style="font-weight:700; color:#f3d59b;">${weatherNames[weather.type]}</div>
    <div style="font-size:0.85rem; color:#ddd;">바람: ${weather.windDir} ${weather.windSpeed}m/s | 습도: ${weather.humidity}% | 강수확률: ${weather.rainProb}%</div>
    <div style="font-size:0.82rem; color:#a8dadc; margin-top:2px;">${sensorInfo}</div>
  `;
}

// --- 30일차 결산 및 엔딩 ---
function checkMonthEnd() {
  const status = getChecklistStatus();
  if (status.check1 && status.check2) {
    // 둘 다 달성 -> 부자가 되어 고향으로 가는 비행기 엔딩
    scene = 'ENDING';
    isPaused = true;
    document.getElementById('hud-clock').style.display = 'none';
    document.getElementById('hud-weather').style.display = 'none';
    openModal(`
      <div style="text-align:center; padding:15px;">
        <h2 style="font-family:'Cinzel', serif; font-size:2rem; color:#f3d59b; margin-bottom:10px;">HAPPY ENDING : 푸른 하늘의 귀환</h2>
        <p style="font-family:'Gowun Batang', serif; font-size:1.12rem; line-height:1.8; color:#f0ece1; margin-bottom:20px;">
          가뭄 진행도 <strong>${droughtLevel.toFixed(1)}%</strong>, 산성비 빈도 <strong>${status.acidFreq}%</strong>!<br>
          당신은 사막의 회색 도시에 맑은 비와 푸른 녹지를 되찾아주었습니다.<br>
          두둑한 외화 보너스를 손에 쥔 채, 창밖으로 펼쳐진 푸른 도시를 내려다보며 고향행 비행기에 오릅니다.
        </p>
        <button class="start-btn" onclick="location.reload()">처음부터 다시하기</button>
      </div>
    `);
  } else if (status.check1 || status.check2) {
    // 둘 중 하나 달성 -> 2달째 이어서 진행
    month++;
    day = 1;
    gameMinutes = 7 * 60;
    budget += 120; // 추가 지원 예산
    showDialogue('나', `목표 중 하나는 달성했지만 아직 도시를 완전히 살리지 못했어... 다행히 계약이 연장되어 ${month}개월째 임무를 이어가게 됐어! 추가 예산 120억이 지원되었으니 이번 달엔 꼭 끝내자.`);
  } else {
    // 둘 다 미달성 -> 해고 엔딩
    scene = 'ENDING';
    isPaused = true;
    openModal(`
      <div style="text-align:center; padding:15px;">
        <h2 style="font-family:'Cinzel', serif; font-size:1.9rem; color:#ff8fa3; margin-bottom:10px;">BAD ENDING : 계약 해지</h2>
        <p style="font-family:'Gowun Batang', serif; font-size:1.1rem; line-height:1.8; color:#f0ece1; margin-bottom:20px;">
          가뭄 진행도 <strong>${droughtLevel.toFixed(1)}%</strong>, 산성비 빈도 <strong>${status.acidFreq}%</strong>...<br>
          도시는 여전히 메마르고 산성비에 신음하고 있습니다.<br>
          결국 환경정책국에서 해고 통지서를 받고 빈손으로 짐을 싸게 되었습니다.
        </p>
        <button class="start-btn" onclick="location.reload()">다시 도전하기</button>
      </div>
    `);
  }
}

// --- 그래픽 렌더링 (레이튼 + 할로우 나이트 + 도넛홀 감성) ---
function drawTitleBackground() {
  // 몽환적인 황혼 사막 하늘 그라데이션
  const grad = ctx.createLinearGradient(0, 0, 0, height);
  grad.addColorStop(0, '#181424');
  grad.addColorStop(0.45, '#4a3238');
  grad.addColorStop(0.8, '#9e6b43');
  grad.addColorStop(1, '#2b1d16');
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, width, height);

  // 거대한 창백한 달 (할로우 나이트 감성)
  ctx.save();
  ctx.beginPath();
  ctx.arc(width * 0.5, height * 0.36, Math.min(width, height) * 0.22, 0, Math.PI * 2);
  ctx.fillStyle = 'rgba(247, 238, 220, 0.14)';
  ctx.fill();
  ctx.restore();

  // 도넛홀 스타일의 섬세하고 고독한 사막 마천루 실루엣
  ctx.fillStyle = '#141118';
  const baseY = height * 0.78;
  const buildings = [
    { x: 0.15, w: 0.04, h: 0.22 },
    { x: 0.21, w: 0.05, h: 0.32 },
    { x: 0.28, w: 0.03, h: 0.19 },
    { x: 0.34, w: 0.06, h: 0.42 },
    { x: 0.42, w: 0.04, h: 0.28 },
    { x: 0.48, w: 0.05, h: 0.48 }, // 주인공 사무실이 위치한 중앙 타워
    { x: 0.55, w: 0.06, h: 0.36 },
    { x: 0.63, w: 0.04, h: 0.25 },
    { x: 0.69, w: 0.05, h: 0.39 },
    { x: 0.76, w: 0.04, h: 0.21 }
  ];

  buildings.forEach(b => {
    const bx = width * b.x;
    const bw = width * b.w;
    const bh = height * b.h;
    ctx.fillRect(bx, baseY - bh, bw, bh + 40);
    // 첨탑 디테일
    ctx.beginPath();
    ctx.moveTo(bx + bw * 0.5, baseY - bh - 35);
    ctx.lineTo(bx + bw * 0.35, baseY - bh);
    ctx.lineTo(bx + bw * 0.65, baseY - bh);
    ctx.closePath();
    ctx.fill();
  });

  // 완만한 사막 모래 언덕
  ctx.fillStyle = '#1c1412';
  ctx.beginPath();
  ctx.moveTo(0, height);
  ctx.lineTo(0, height * 0.76);
  ctx.quadraticCurveTo(width * 0.3, height * 0.71, width * 0.6, height * 0.78);
  ctx.quadraticCurveTo(width * 0.85, height * 0.83, width, height * 0.74);
  ctx.lineTo(width, height);
  ctx.fill();

  // 날리는 모래바람 입자
  drawParticles('#e6c288', 6);
}

function drawParticles(color, speedMult) {
  ctx.fillStyle = color;
  particles.forEach(p => {
    p.x += p.speedX * speedMult * 0.3;
    p.y += p.speedY;
    if (p.x > width) p.x = 0;
    if (p.y > height) p.y = 0;
    if (p.y < 0) p.y = height;

    ctx.globalAlpha = p.alpha;
    ctx.beginPath();
    ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
    ctx.fill();
  });
  ctx.globalAlpha = 1.0;
}

function drawOfficeScene() {
  // 1. 통유리창 밖 하늘색 (시간대: 07:00 ~ 21:00 및 날씨 반영)
  const dayProgress = (gameMinutes - 420) / 840; // 0(아침 7시) ~ 1(밤 9시)
  const skyGrad = ctx.createLinearGradient(0, 0, 0, height * 0.68);

  if (weather.type === 'DUST') {
    skyGrad.addColorStop(0, '#8c6239');
    skyGrad.addColorStop(1, '#c9965b');
  } else if (weather.type === 'RAIN' || weather.type === 'HEAVY_RAIN') {
    skyGrad.addColorStop(0, '#222b38');
    skyGrad.addColorStop(1, '#4a5a6e');
  } else if (dayProgress < 0.2) {
    // 아침 7~9시 여명
    skyGrad.addColorStop(0, '#3a4f7a');
    skyGrad.addColorStop(1, '#e8a87c');
  } else if (dayProgress < 0.7) {
    // 낮 사막 하늘
    skyGrad.addColorStop(0, '#2b6cb0');
    skyGrad.addColorStop(1, '#ebd5b3');
  } else if (dayProgress < 0.88) {
    // 해질녘 노을
    skyGrad.addColorStop(0, '#2d1e3e');
    skyGrad.addColorStop(0.6, '#b85d43');
    skyGrad.addColorStop(1, '#f2b872');
  } else {
    // 밤 8~9시
    skyGrad.addColorStop(0, '#0b0e17');
    skyGrad.addColorStop(1, '#1d2436');
  }

  ctx.fillStyle = skyGrad;
  ctx.fillRect(0, 0, width, height * 0.68);

  // 사막 지평선 & 녹지 변화 (가뭄 진행도가 낮아질수록 푸른 녹지가 넓어짐)
  const greenRatio = Math.max(0, (100 - droughtLevel) / 100);
  ctx.fillStyle = greenRatio > 0.6 ? '#4a6b48' : '#b89468';
  ctx.fillRect(0, height * 0.54, width, height * 0.14);

  // 통유리창 너머 3가지 공장 그리기 (레이튼 스타일 깔끔한 외곽선)
  FACTORIES.forEach(f => {
    const fx = width * f.relX;
    const fy = height * f.relY;
    const fw = width * f.relW;
    const fh = height * f.relH;

    // 공장 본체
    ctx.fillStyle = '#2b2d38';
    ctx.strokeStyle = '#121318';
    ctx.lineWidth = 2.5;
    ctx.fillRect(fx, fy + fh * 0.35, fw, fh * 0.65);
    ctx.strokeRect(fx, fy + fh * 0.35, fw, fh * 0.65);

    // 굴뚝 2개
    ctx.fillRect(fx + fw * 0.2, fy, fw * 0.14, fh * 0.35);
    ctx.strokeRect(fx + fw * 0.2, fy, fw * 0.14, fh * 0.35);
    ctx.fillRect(fx + fw * 0.65, fy + fh * 0.08, fw * 0.14, fh * 0.27);
    ctx.strokeRect(fx + fw * 0.65, fy + fh * 0.08, fw * 0.14, fh * 0.27);

    // 굴뚝 연기 (대기질에 따라 농도 변화)
    ctx.fillStyle = `rgba(90, 85, 80, ${Math.min(0.75, weather.so2 / 140)})`;
    ctx.beginPath();
    ctx.arc(fx + fw * 0.27, fy - 12, 16, 0, Math.PI * 2);
    ctx.arc(fx + fw * 0.35, fy - 26, 22, 0, Math.PI * 2);
    ctx.fill();
  });

  // 창밖 날씨 이펙트 (황사 / 비 / 폭우)
  if (weather.type === 'DUST') {
    drawParticles('rgba(218, 165, 95, 0.65)', 12);
  } else if (weather.type === 'RAIN' || weather.type === 'HEAVY_RAIN') {
    ctx.strokeStyle = weather.ph < 5.6 ? 'rgba(180, 220, 160, 0.55)' : 'rgba(175, 215, 255, 0.6)';
    ctx.lineWidth = weather.type === 'HEAVY_RAIN' ? 2.2 : 1.3;
    const count = weather.type === 'HEAVY_RAIN' ? 140 : 65;
    for (let i = 0; i < count; i++) {
      const rx = (Math.random() * width);
      const ry = (Math.random() * height * 0.65);
      ctx.beginPath();
      ctx.moveTo(rx, ry);
      ctx.lineTo(rx - 6, ry + 18);
      ctx.stroke();
    }
  }

  // 통유리창 프레임 (할로우 나이트 + 레이튼풍 아치형 철제 창틀)
  ctx.strokeStyle = '#181920';
  ctx.lineWidth = 10;
  ctx.strokeRect(0, 0, width, height * 0.65);
  for (let i = 1; i <= 3; i++) {
    ctx.beginPath();
    ctx.moveTo((width / 4) * i, 0);
    ctx.lineTo((width / 4) * i, height * 0.65);
    ctx.stroke();
  }

  // 2. 사무실 긴 원목 책상 (전경)
  const deskGrad = ctx.createLinearGradient(0, height * 0.63, 0, height);
  deskGrad.addColorStop(0, '#59412e');
  deskGrad.addColorStop(0.2, '#422f20');
  deskGrad.addColorStop(1, '#241911');
  ctx.fillStyle = deskGrad;
  ctx.fillRect(0, height * 0.63, width, height * 0.37);

  ctx.strokeStyle = '#1a110b';
  ctx.lineWidth = 4;
  ctx.beginPath();
  ctx.moveTo(0, height * 0.63);
  ctx.lineTo(width, height * 0.63);
  ctx.stroke();

  // 3. 책상 위 오브젝트 그리기 (손그림 스타일)
  drawDeskObjects();
}

function drawDeskObjects() {
  ctx.lineWidth = 2;
  ctx.strokeStyle = '#1c1815';

  // (1) 신문 기사
  const news = DESK_ITEMS[0];
  ctx.fillStyle = '#e6dcc5';
  ctx.fillRect(width * news.relX, height * news.relY, width * news.relW, height * news.relH);
  ctx.strokeRect(width * news.relX, height * news.relY, width * news.relW, height * news.relH);
  ctx.fillStyle = '#3b332b';
  ctx.fillRect(width * (news.relX + 0.015), height * (news.relY + 0.02), width * (news.relW - 0.03), 6);

  // (2) 서류 더미
  const docs = DESK_ITEMS[1];
  for (let i = 2; i >= 0; i--) {
    ctx.fillStyle = i === 0 ? '#f7f3e8' : '#dcd3be';
    ctx.fillRect(width * docs.relX + i * 5, height * docs.relY - i * 5, width * docs.relW, height * docs.relH);
    ctx.strokeRect(width * docs.relX + i * 5, height * docs.relY - i * 5, width * docs.relW, height * docs.relH);
  }

  // (3) 노트북
  const lap = DESK_ITEMS[2];
  // 모니터 부분
  ctx.fillStyle = '#252934';
  ctx.fillRect(width * lap.relX, height * lap.relY, width * lap.relW, height * (lap.relH * 0.68));
  ctx.strokeRect(width * lap.relX, height * lap.relY, width * lap.relW, height * (lap.relH * 0.68));
  // 화면 빛
  ctx.fillStyle = '#3b5266';
  ctx.fillRect(width * (lap.relX + 0.01), height * (lap.relY + 0.012), width * (lap.relW - 0.02), height * (lap.relH * 0.52));
  // 키보드 하판
  ctx.fillStyle = '#3a3f4d';
  ctx.fillRect(width * (lap.relX - 0.01), height * (lap.relY + lap.relH * 0.68), width * (lap.relW + 0.02), height * (lap.relH * 0.32));
  ctx.strokeRect(width * (lap.relX - 0.01), height * (lap.relY + lap.relH * 0.68), width * (lap.relW + 0.02), height * (lap.relH * 0.32));

  // (4) 가족사진 액자
  const pic = DESK_ITEMS[3];
  ctx.fillStyle = '#8c6239';
  ctx.fillRect(width * pic.relX, height * pic.relY, width * pic.relW, height * pic.relH);
  ctx.strokeRect(width * pic.relX, height * pic.relY, width * pic.relW, height * pic.relH);
  ctx.fillStyle = '#d9cbb8';
  ctx.fillRect(width * (pic.relX + 0.01), height * (pic.relY + 0.015), width * (pic.relW - 0.02), height * (pic.relH - 0.03));

  // (5) 펜꽂이 (볼펜, 샤프 다수)
  const pen = DESK_ITEMS[4];
  const px = width * pen.relX;
  const py = height * pen.relY;
  const pw = width * pen.relW;
  const ph = height * pen.relH;
  // 꽂힌 펜들
  const penColors = ['#c94a4a', '#3b6ea5', '#e3b23c', '#2b2d42'];
  penColors.forEach((col, idx) => {
    ctx.strokeStyle = col;
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(px + pw * (0.2 + idx * 0.2), py + ph * 0.4);
    ctx.lineTo(px + pw * (0.1 + idx * 0.25), py - 14);
    ctx.stroke();
  });
  ctx.strokeStyle = '#1c1815';
  ctx.lineWidth = 2;
  ctx.fillStyle = '#4a4e59';
  ctx.fillRect(px, py + ph * 0.35, pw, ph * 0.65);
  ctx.strokeRect(px, py + ph * 0.35, pw, ph * 0.65);

  // (6) 탁상 캘린더
  const cal = DESK_ITEMS[5];
  ctx.fillStyle = '#f5efe2';
  ctx.fillRect(width * cal.relX, height * cal.relY, width * cal.relW, height * cal.relH);
  ctx.strokeRect(width * cal.relX, height * cal.relY, width * cal.relW, height * cal.relH);
  ctx.fillStyle = '#9e2a2b';
  ctx.fillRect(width * cal.relX, height * cal.relY, width * cal.relW, height * (cal.relH * 0.28));
  ctx.fillStyle = '#1c1815';
  ctx.font = 'bold 16px Gowun Batang';
  ctx.fillText(`${day}일`, width * (cal.relX + 0.025), height * (cal.relY + 0.085));
}

// --- 마우스 호버 및 클릭 이벤트 ---
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
    if (mx >= ox && mx <= ox + ow && my >= oy && my <= oy + oh) {
      hovered = obj;
    }
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

// --- 메인 게임 루프 (10분 = 1일 시간 경과) ---
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
      // 현실 600초(10분) = 게임 840분(07:00 ~ 21:00) -> 초당 1.4분 진행
      gameMinutes += deltaSec * 1.4;

      if (gameMinutes >= 21 * 60) {
        // 밤 9시 도달 -> 다음 날 아침 7시로 전환
        if (day >= 30) {
          checkMonthEnd();
        } else {
          day++;
          gameMinutes = 7 * 60;
          simulateNewDay();
        }
      }

      // 우측 상단 시계 업데이트
      const hrs = Math.floor(gameMinutes / 60);
      const mins = Math.floor(gameMinutes % 60);
      const padH = String(hrs).padStart(2, '0');
      const padM = String(mins).padStart(2, '0');
      const prefix = month > 1 ? `${month}개월째 ` : '';
      document.getElementById('clock-day-text').innerText = `${prefix}${day}일차`;
      document.getElementById('clock-time-text').innerText = `${padH}시 ${padM}분`;
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
