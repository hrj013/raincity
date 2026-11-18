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
  @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;800&family=Gowun+Batang:wght@400;700&family=Noto+Sans+KR:wght@300;400;600;700&display=swap');

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
    background-color: #150b38;
    font-family: 'Noto Sans KR', sans-serif;
    color: #f0ece1;
  }

  #game-container {
    position: relative;
    width: 100vw;
    height: 100vh;
    overflow: hidden;
    background: #2b1580;
  }

  canvas {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: block;
  }

  /* 고감도 팝아트 네온 패널 */
  .hollow-panel {
    background: rgba(34, 18, 92, 0.97);
    border: 3px solid #150b38;
    border-radius: 16px;
    box-shadow: 6px 6px 0 #ff8cc6, 0 0 0 3px #b69cff, 0 15px 35px rgba(21, 11, 56, 0.6);
    padding: 24px;
    position: relative;
  }

  .hollow-panel::before {
    content: "★";
    position: absolute;
    top: -16px;
    left: 50%;
    transform: translateX(-50%);
    background: #2b1580;
    padding: 0 12px;
    color: #ffd95e;
    font-size: 16px;
    border-radius: 10px;
    border: 2px solid #150b38;
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
    color: #fff4d6;
    text-shadow: 4px 4px 0 #ff8cc6, 8px 8px 0 #150b38;
    margin-bottom: 10px;
  }

  .title-sub {
    font-family: 'Gowun Batang', serif;
    font-size: 1.15rem;
    letter-spacing: 0.25em;
    color: #d8c9ff;
    margin-bottom: 45px;
    text-shadow: 2px 2px 0 #150b38;
  }

  .start-btn {
    font-family: 'Cinzel', serif;
    font-size: 1.3rem;
    letter-spacing: 0.2em;
    padding: 14px 48px;
    background: #7bf0c8;
    color: #150b38;
    border: 3px solid #150b38;
    border-radius: 14px;
    cursor: pointer;
    transition: all 0.2s ease;
    box-shadow: 5px 5px 0 #150b38;
    font-weight: 800;
  }

  .start-btn:hover {
    background: #ff8cc6;
    color: #150b38;
    box-shadow: 2px 2px 0 #150b38;
    transform: translate(3px, 3px);
  }

  /* 우측 상단 시계 HUD */
  #hud-clock {
    position: absolute;
    top: 20px;
    right: 24px;
    z-index: 15;
    background: #fff4d6;
    border: 3px solid #150b38;
    border-radius: 14px;
    padding: 10px 18px;
    box-shadow: 4px 4px 0 #ff8cc6;
    display: none;
    align-items: center;
    gap: 12px;
  }

  .clock-day {
    font-family: 'Gowun Batang', serif;
    font-size: 1.2rem;
    font-weight: 700;
    color: #150b38;
  }

  .clock-time {
    font-size: 1.1rem;
    font-weight: 800;
    color: #150b38;
    background: #7bf0c8;
    padding: 4px 10px;
    border-radius: 8px;
    border: 2px solid #150b38;
  }

  .speed-btn {
    background: #fff;
    border: 2px solid #150b38;
    color: #150b38;
    font-size: 0.78rem;
    padding: 4px 8px;
    border-radius: 6px;
    cursor: pointer;
    font-weight: 700;
  }

  .speed-btn.active {
    background: #ffd95e;
    color: #150b38;
  }

  /* 좌측 상단 기상 및 실시간 알림 배지 */
  #hud-weather {
    position: absolute;
    top: 20px;
    left: 24px;
    z-index: 15;
    background: rgba(34, 18, 92, 0.95);
    border: 3px solid #150b38;
    border-radius: 14px;
    padding: 10px 18px;
    display: none;
    font-size: 0.9rem;
    line-height: 1.55;
    box-shadow: 4px 4px 0 #59d2ff;
    color: #f0ece1;
  }

  /* 긴급 현장 작업 알림 배너 */
  #alert-strip {
    position: absolute;
    top: 110px;
    left: 24px;
    z-index: 15;
    display: none;
    flex-direction: column;
    gap: 8px;
  }

  .alert-pill {
    background: #ff5fa2;
    border: 2px solid #150b38;
    color: #150b38;
    padding: 7px 14px;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 800;
    cursor: pointer;
    animation: pulse 1.3s infinite;
    box-shadow: 3px 3px 0 #150b38;
  }

  @keyframes pulse {
    0%, 100% { transform: scale(1); opacity: 0.9; }
    50% { transform: scale(1.03); opacity: 1; }
  }

  /* 하단 대화창 */
  #dialogue-box {
    position: absolute;
    bottom: 22px;
    left: 50%;
    transform: translateX(-50%);
    width: min(820px, 90vw);
    z-index: 25;
    background: #2b1580;
    border: 3px solid #150b38;
    border-radius: 16px;
    padding: 18px 26px;
    box-shadow: 6px 6px 0 #ff8cc6;
    display: none;
    cursor: pointer;
  }

  .speaker-tag {
    display: inline-block;
    background: #ff8cc6;
    color: #150b38;
    font-weight: 800;
    font-size: 0.88rem;
    padding: 3px 14px;
    border-radius: 20px;
    margin-bottom: 8px;
    border: 2px solid #150b38;
  }

  .dialogue-text {
    font-family: 'Gowun Batang', serif;
    font-size: 1.1rem;
    line-height: 1.65;
    color: #f5efe2;
  }

  .dialogue-next {
    text-align: right;
    font-size: 0.8rem;
    color: #7bf0c8;
    margin-top: 6px;
    font-weight: 700;
  }

  /* 모달 오버레이 */
  #modal-backdrop {
    position: absolute;
    inset: 0;
    background: rgba(21, 11, 56, 0.78);
    backdrop-filter: blur(6px);
    z-index: 30;
    display: none;
    align-items: center;
    justify-content: center;
  }

  .modal-card {
    width: min(780px, 92vw);
    max-height: 86vh;
    overflow-y: auto;
  }

  .modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 2px solid #b69cff;
    padding-bottom: 12px;
    margin-bottom: 18px;
  }

  .modal-title {
    font-family: 'Gowun Batang', serif;
    font-size: 1.45rem;
    font-weight: 700;
    color: #fff4d6;
  }

  .close-btn {
    background: none;
    border: 2px solid #b69cff;
    color: #fff4d6;
    font-size: 0.95rem;
    padding: 4px 12px;
    border-radius: 8px;
    cursor: pointer;
    font-weight: 700;
  }

  .close-btn:hover {
    background: #ff8cc6;
    color: #150b38;
  }

  /* 신문 & 서류 더미 */
  .newspaper-sheet {
    background: #fff4d6;
    color: #150b38;
    padding: 26px;
    border-radius: 10px;
    font-family: 'Gowun Batang', serif;
    border: 2px solid #150b38;
  }

  .news-head {
    text-align: center;
    border-top: 3px double #150b38;
    border-bottom: 3px double #150b38;
    padding: 10px 0;
    margin-bottom: 16px;
  }

  .dossier-box {
    background: #fff4d6;
    color: #150b38;
    padding: 22px;
    border-radius: 10px;
    font-family: 'Gowun Batang', serif;
    border: 2px solid #150b38;
  }

  .check-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 13px;
    margin: 10px 0;
    background: #e8deff;
    border: 2px solid #150b38;
    border-radius: 8px;
    font-size: 1.05rem;
    font-weight: 700;
  }

  /* 노트북 정책 카드 */
  .policy-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(290px, 1fr));
    gap: 12px;
  }

  .policy-card {
    background: rgba(60, 35, 150, 0.95);
    border: 2px solid #150b38;
    box-shadow: 3px 3px 0 #b69cff;
    border-radius: 12px;
    padding: 14px;
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }

  .policy-card:hover:not(.disabled) {
    border-color: #7bf0c8;
    transform: translateY(-2px);
    background: rgba(80, 50, 190, 0.95);
  }

  .policy-card.disabled {
    opacity: 0.52;
    cursor: not-allowed;
  }

  .badge-status {
    display: inline-block;
    font-size: 0.78rem;
    padding: 3px 10px;
    border-radius: 10px;
    margin-top: 8px;
    font-weight: 700;
  }

  .badge-active { background: #7bf0c8; color: #150b38; }
  .badge-pending { background: #ffd95e; color: #150b38; }
  .badge-ready { background: #b69cff; color: #150b38; }

  /* 미니게임 UI 컴포넌트 */
  .radar-bar {
    position: relative;
    width: 100%;
    height: 36px;
    background: #150b38;
    border: 3px solid #150b38;
    border-radius: 18px;
    overflow: hidden;
    margin: 18px 0;
  }

  .radar-target {
    position: absolute;
    top: 0;
    height: 100%;
    background: rgba(123, 240, 200, 0.5);
    border-left: 2px solid #7bf0c8;
    border-right: 2px solid #7bf0c8;
  }

  .radar-cursor {
    position: absolute;
    top: 0;
    width: 8px;
    height: 100%;
    background: #ffd95e;
    box-shadow: 0 0 12px #ffd95e;
  }

  .sensor-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 14px;
    margin: 16px 0;
  }

  .sensor-node {
    background: #3c2399;
    border: 2px solid #150b38;
    border-radius: 10px;
    padding: 16px;
    text-align: center;
    cursor: pointer;
    transition: all 0.2s;
    font-weight: 700;
  }

  .sensor-node.dirty {
    background: #5a1836;
    color: #ffccde;
  }

  .sensor-node.clean {
    background: #1a4d3e;
    color: #bbf7d0;
  }

  .action-btn {
    padding: 10px 24px;
    border-radius: 10px;
    font-size: 1rem;
    font-weight: 800;
    cursor: pointer;
    border: 2px solid #150b38;
    transition: 0.2s;
    box-shadow: 3px 3px 0 #150b38;
  }

  .btn-yes { background: #7bf0c8; color: #150b38; }
  .btn-yes:hover { background: #9effdf; }
  .btn-no { background: #ff8cc6; color: #150b38; }
  .btn-no:hover { background: #ffb3d9; }

  .choice-btn {
    display: block;
    width: 100%;
    text-align: left;
    background: #3c2399;
    border: 2px solid #150b38;
    box-shadow: 3px 3px 0 #ff8cc6;
    color: #f0ece1;
    padding: 14px 18px;
    border-radius: 10px;
    margin-bottom: 12px;
    cursor: pointer;
    font-size: 0.98rem;
    font-weight: 600;
  }

  .choice-btn:hover {
    background: #5a3ad8;
    border-color: #7bf0c8;
  }

  /* 툴팁 */
  #hover-tooltip {
    position: absolute;
    pointer-events: none;
    background: #fff4d6;
    color: #150b38;
    border: 2px solid #150b38;
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 0.86rem;
    font-weight: 700;
    z-index: 18;
    display: none;
    transform: translate(-50%, -140%);
    white-space: nowrap;
    box-shadow: 3px 3px 0 #150b38;
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

  <!-- 긴급 현장 작업 알림 배너 -->
  <div id="alert-strip"></div>

  <!-- 우측 상단 시간 HUD -->
  <div id="hud-clock">
    <span class="clock-day" id="clock-day-text">1일차</span>
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
function resize() {
  const dpr = window.devicePixelRatio || 1;
  width = window.innerWidth;
  height = window.innerHeight;
  
  canvas.width = width * dpr;
  canvas.height = height * dpr;
  canvas.style.width = width + 'px';
  canvas.style.height = height + 'px';
  
  ctx.scale(dpr, dpr);
}
window.addEventListener('resize', resize);
resize();

// --- 게임 상태 변수 ---
let scene = 'TITLE';
let day = 1;
let month = 1;
let gameMinutes = 7 * 60; // 07:00 시작
let timeMultiplier = 1;   // 기본 1배속
let lastTimestamp = 0;
let isPaused = false;

// 도시 환경 및 시뮬레이션 지표
let budget = 250;
let droughtLevel = 68; // 목표: 30% 미만
let totalRainDays = 0;
let acidRainDays = 0;

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
  seedingReady: true,
  phAlert: false,
  sensorDirty: false,
  phoneRinging: false,
  currentAudit: null
};

const POLICIES = [
  { id: 'fgd', name: '배연탈황설비 (FGD)', cost: 45, desc: '공장·발전소의 SO₂를 알칼리성 물질로 제거하여 산성비 위험을 크게 낮춥니다.', status: 'READY', applyDay: null },
  { id: 'esp', name: '전기집진기 (ESP)', cost: 40, desc: '미세먼지(PM2.5)와 황산염 입자를 정전기로 포집하여 대기질을 개선합니다.', status: 'READY', applyDay: null },
  { id: 'sensor', name: '정밀 대기질 센서망', cost: 25, desc: 'SO₂, NOₓ, PM2.5, 강수 pH를 실시간 측정해 오염 확산과 산성비 위험을 정밀 분석합니다.', status: 'READY', applyDay: null },
  { id: 'raingarden', name: '빗물정원 조성', cost: 30, desc: '빗물이 토양으로 자연 침투하도록 유도해 홍수를 줄이고 비점오염 유출을 막습니다.', status: 'READY', applyDay: null },
  { id: 'permeable', name: '투수성 포장 도로', cost: 35, desc: '사막 도시의 아스팔트를 투수성 소재로 교체해 빗물 흡수율과 지하수 함양을 높입니다.', status: 'READY', applyDay: null },
  { id: 'reservoir', name: '지하 빗물저류조', cost: 50, desc: '폭우 시 도심 침수를 막고, 저장된 빗물을 활용해 가뭄 진행도를 크게 낮춥니다.', status: 'READY', applyDay: null },
  { id: 'seeding', name: '고출력 인공강우 시딩기', cost: 55, desc: '상공 구름에 촉매제를 대량 살포해 인공강우 작전의 기본 성공률과 강수량을 높입니다.', status: 'READY', applyDay: null }
];

const FACTORIES = [
  { id: 'factory1', name: '제1 화력·담수화 복합발전소', role: '도시 전력 공급과 바닷물 담수화를 담당하는 핵심 에너지 시설입니다.', pollutants: '아황산가스(SO₂), 질소산화물(NOₓ), 온배수', relX: 0.22, relY: 0.42, relW: 0.13, relH: 0.16 },
  { id: 'factory2', name: '제2 석유화학·정제 플랜트', role: '사막 부자도시의 외화를 벌어들이는 주력 석유화학 제품 생산 공장입니다.', pollutants: '휘발성유기화합물(VOCs), 아황산가스(SO₂), 초미세먼지(PM2.5)', relX: 0.44, relY: 0.43, relW: 0.14, relH: 0.15 },
  { id: 'factory3', name: '제3 시멘트·건설자재 제련소', role: '마천루 건설에 필요한 시멘트와 금속 자재를 가공하는 중공업 시설입니다.', pollutants: '고농도 미세먼지(PM10/PM2.5), 질소산화물(NOₓ), 중금속 분진', relX: 0.68, relY: 0.41, relW: 0.13, relH: 0.17 }
];

const DESK_ITEMS = [
  { id: 'radio', name: '🛩️ 인공강우 작전 무전기 (시딩 지휘)', relX: 0.04, relY: 0.65, relW: 0.07, relH: 0.13 },
  { id: 'newspaper', name: '📰 신문 기사', relX: 0.13, relY: 0.74, relW: 0.14, relH: 0.12 },
  { id: 'documents', name: '📁 서류 더미 (예산 & 체크리스트)', relX: 0.29, relY: 0.70, relW: 0.13, relH: 0.14 },
  { id: 'laptop', name: '💻 업무용 노트북 (환경 정책)', relX: 0.44, relY: 0.64, relW: 0.16, relH: 0.17 },
  { id: 'sensor_pad', name: '📡 대기질 센서 정비 단말기', relX: 0.62, relY: 0.67, relW: 0.08, relH: 0.12 },
  { id: 'beaker', name: '🧪 수질·강수 pH 중화 실험 세트', relX: 0.72, relY: 0.66, relW: 0.07, relH: 0.14 },
  { id: 'photo', name: '🖼️ 고향의 가족사진', relX: 0.80, relY: 0.73, relW: 0.06, relH: 0.10 },
  { id: 'penholder', name: '✏️ 필기구 꽂이 (볼펜·샤프)', relX: 0.87, relY: 0.72, relW: 0.04, relH: 0.10 },
  { id: 'phone', name: '☎️ 환경평가원 직통 전화기', relX: 0.85, relY: 0.61, relW: 0.07, relH: 0.09 },
  { id: 'calendar', name: '📅 탁상 캘린더', relX: 0.92, relY: 0.71, relW: 0.06, relH: 0.11 }
];

const AUDIT_SCENARIOS = [
  {
    title: "제2 석유화학 플랜트 야간 불법 배출 제보",
    desc: "시민 환경단체에서 제2 플랜트가 탈황 필터를 끄고 아황산가스(SO₂)를 무단 배출하고 있다는 익명 제보를 보내왔습니다.",
    choices: [
      { text: "즉시 불시 환경 감사를 실시해 과태료를 징수한다 (+25억 예산, SO₂ -15)", effect: () => { budget += 25; weather.so2 = Math.max(10, weather.so2 - 15); return "불법 배출 현장을 적발하여 25억의 환경부담금을 징수하고 배출을 차단했습니다!"; } },
      { text: "경고 공문만 발송하고 시설 개선 권고를 내린다 (SO₂ -5)", effect: () => { weather.so2 = Math.max(10, weather.so2 - 5); return "공장 측에서 재발 방지를 약속하며 배출량을 소폭 줄였습니다."; } }
    ]
  },
  {
    title: "왕실 도시개발청의 긴급 수자원 브리핑 요청",
    desc: "사막 신도시 건설에 필요한 공업용수가 부족하다며 인공강우 예산을 건설국으로 전용하자는 압력이 들어왔습니다.",
    choices: [
      { text: "과학적 가뭄 및 산성비 리스크 보고서를 제출해 예산을 사수한다 (+15억 추가 지원)", effect: () => { budget += 15; return "정밀 데이터에 설득된 왕실 위원회가 오히려 환경국에 15억을 추가 지원했습니다!"; } },
      { text: "일부 예산을 양보하는 대신 도로 살수차 지원을 받는다 (가뭄 -3%)", effect: () => { droughtLevel = Math.max(5, droughtLevel - 3); return "살수차 지원으로 도심 지열과 가뭄이 소폭 완화되었습니다."; } }
    ]
  },
  {
    title: "주거지구 호흡기 질환 민원 급증",
    desc: "고농도 미세먼지로 인해 도심 병원에 호흡기 환자가 늘어나고 있습니다. 환경평가원으로서 비상 조치를 결정해야 합니다.",
    choices: [
      { text: "비상 차량 2부제 및 공장 가동률 일시 단축 발령 (PM2.5 -20, 예산 -10억)", effect: () => { budget = Math.max(0, budget - 10); weather.pm25 = Math.max(10, weather.pm25 - 20); return "긴급 저감 조치로 도심 미세먼지 농도가 빠르게 안정되었습니다!"; } },
      { text: "시민들에게 실내 대기 권고 및 마스크 보급만 진행한다 (PM2.5 -5)", effect: () => { weather.pm25 = Math.max(10, weather.pm25 - 5); return "시민들의 불만은 일부 진정되었으나 대기질 개선 폭은 크지 않았습니다."; } }
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
    size: 1 + Math.random() * 3,
    alpha: 0.3 + Math.random() * 0.6
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
    showDialogue('나', '드디어 사막의 거대 도시에 부임했어... 책상 위의 노트북으로 환경 정책을 세우는 것뿐만 아니라, 무전기로 직접 인공강우 작전을 지휘하고 실험 세트로 산성비를 중화해야 해!');
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
    alerts.push(`<div class="alert-pill" onclick="handleObjectClick('beaker')">🧪 경고: 강수 산성화 위험! [실험 세트]에서 pH 중화 필요</div>`);
  }
  if (activeTasks.sensorDirty) {
    alerts.push(`<div class="alert-pill" onclick="handleObjectClick('sensor_pad')">📡 경고: 황사로 대기질 센서 오류 발생! [정비 단말기] 클릭</div>`);
  }
  if (activeTasks.phoneRinging) {
    alerts.push(`<div class="alert-pill" onclick="handleObjectClick('phone')">☎️ 수신 중: 긴급 환경 감사/민원 전화 도착! [전화기] 클릭</div>`);
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
      <div class="modal-header">
        <span class="modal-title">📰 레인 시티 조간신문</span>
        <button class="close-btn" onclick="closeModal()">닫기</button>
      </div>
      <div class="newspaper-sheet">
        <div class="news-head">
          <div style="font-size:0.85rem; letter-spacing:0.2em;">THE RAIN CITY CHRONICLE</div>
          <h2 style="font-size:1.55rem; margin-top:4px;">"비가 내리지 않는 황금의 도시에 희망의 단비를"</h2>
        </div>
        <p style="line-height:1.8; font-size:1.05rem;">
          끝없는 모래바람과 극심한 가뭄, 그리고 무분별한 산업화로 인한 산성비 위협이 우리 도시를 덮치고 있다.
          정부는 이 위기를 타개하기 위해 해외에서 초빙한 환경공학 전문가에게 도시의 미래를 맡겼다.
        </p>
      </div>
    `);
    setTimeout(() => {
      document.getElementById('dialogue-speaker').innerText = '나';
      document.getElementById('dialogue-text').innerText = '이 도시를 살려야 한다.. 내 기술과 판단으로 이 메마른 하늘에 맑은 비를 내리게 할 거야.';
      document.getElementById('dialogue-box').style.display = 'block';
    }, 250);
  }
  else if (id === 'documents') {
    const status = getChecklistStatus();
    openModal(`
      <div class="modal-header">
        <span class="modal-title">📁 환경정책국 기밀 서류 더미</span>
        <button class="close-btn" onclick="closeModal()">닫기</button>
      </div>
      <div class="dossier-box">
        <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:2px solid #150b38; padding-bottom:12px; margin-bottom:16px;">
          <span style="font-size:1.15rem; font-weight:700;">💰 가용 도시 환경 예산</span>
          <span style="font-size:1.5rem; font-weight:800; color:#1b4332;">${budget} 억 디르함</span>
        </div>
        <h3 style="margin-bottom:10px; color:#150b38;">📋 30일차 최종 평가 체크리스트 (실시간 갱신)</h3>
        <div class="check-item">
          <span>1. 가뭄 진행도가 30% 미만인가? (현재: ${droughtLevel.toFixed(1)}%)</span>
          <span style="font-size:1.25rem;">${status.check1 ? '✅ 달성' : '⬜ 미달성'}</span>
        </div>
        <div class="check-item">
          <span>2. 산성비 발생 빈도가 10% 미만인가? (현재: ${status.acidFreq}%)</span>
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
    showDialogue('나', '지갑 속 낡은 가족사진... 내가 타국에서 묵묵히 버티는 이유야. 꼭 부자가 되어서 당당하게 돌아갈게.');
  }
  else if (id === 'penholder') {
    showDialogue('나', '볼펜, 샤프, 제도용 연필이 빽빽하게 꽂혀 있다. 매일 밤 대기 확산 수식을 계산하느라 닳아버린 흔적들이다.');
  }
  else if (id === 'calendar') {
    showDialogue('나', `오늘은 ${month}개월째 ${day}일차야. 이번 달 평가일까지 앞으로 ${30 - day}일 남았어.`);
  }
  else if (id.startsWith('factory')) {
    const f = FACTORIES.find(item => item.id === id);
    openModal(`
      <div class="modal-header">
        <span class="modal-title">🏭 ${f.name}</span>
        <button class="close-btn" onclick="closeModal()">닫기</button>
      </div>
      <div style="line-height:1.8; font-size:1.05rem;">
        <p><strong style="color:#ffd95e;">[시설 역할]</strong><br>${f.role}</p><br>
        <p><strong style="color:#ff8cc6;">[주요 배출 오염물질]</strong><br>${f.pollutants}</p>
      </div>
    `);
  }
}

function openSeedingMinigame() {
  if (!activeTasks.seedingReady) {
    showDialogue('나', '오늘의 인공강우 시딩 항공기 출격은 이미 완료했어. 내일 기상 관측 데이터를 보고 다시 작전을 세우자.');
    return;
  }
  const cloudDesc = weather.cloudType === 'WARM'
    ? '따뜻한 구름층 (영상 기온 4℃) → 흡습성 입자 [염화나트륨] 적합'
    : '차가운 과냉각 구름층 (영하 -8℃) → 빙정핵 입자 [요오드화은] 적합';

  openModal(`
    <div class="modal-header">
      <span class="modal-title">🛩️ 인공강우 시딩(Cloud Seeding) 작전 통제</span>
      <button class="close-btn" onclick="closeModal()">닫기</button>
    </div>
    <p style="font-size:0.95rem; color:#ffd95e; margin-bottom:8px;">📡 현재 상공 기상 레이더 분석: <strong>${cloudDesc}</strong></p>
    <p style="font-size:0.88rem; color:#d8c9ff; margin-bottom:14px;">
      1) 구름 온도에 맞는 촉매제를 선택한 뒤, 2) 레이더 커서가 <strong>초록색 응결 골든타임 구간</strong>에 들어왔을 때 살포 버튼을 누르세요! (작전 비용: 10억)
    </p>
    <div style="margin-bottom:12px; font-weight:700;">
      <label style="margin-right:16px; cursor:pointer;">
        <input type="radio" name="seedType" value="WARM" checked> 🧂 흡습성 시딩 입자
      </label>
      <label style="cursor:pointer;">
        <input type="radio" name="seedType" value="COLD"> ❄️ 빙정핵 시딩 입자
      </label>
    </div>
    <div class="radar-bar">
      <div class="radar-target" style="left: 38%; width: 24%;"></div>
      <div class="radar-cursor" id="radar-cursor" style="left: 0%;"></div>
    </div>
    <div style="text-align:center; margin-top:16px;">
      <button class="action-btn btn-yes" onclick="fireSeeding()">🚀 지금 촉매제 살포 실행! (10억)</button>
    </div>
  `);

  let pos = 0;
  let dir = 1;
  radarInterval = setInterval(() => {
    pos += dir * 3.2;
    if (pos >= 98) { pos = 98; dir = -1; }
    if (pos <= 0) { pos = 0; dir = 1; }
    const cursor = document.getElementById('radar-cursor');
    if (cursor) cursor.style.left = pos + '%';
  }, 25);
}

function fireSeeding() {
  if (budget < 10) {
    closeModal();
    showDialogue('나', '예산이 부족해서 항공기 출격 비용(10억)을 감당할 수 없어...');
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
      showDialogue('나', `인공강우 작전 대성공! 단비가 내렸지만 대기 오염물질로 인해 강수 pH가 ${weather.ph}로 산성화되었어. 책상 위 [실험 세트]에서 중화 작업을 해야 해!`);
    } else {
      showDialogue('나', `완벽한 타이밍과 촉매제 선택! 깨끗한 단비(pH ${weather.ph})가 내리며 가뭄 해갈에 크게 기여했습니다!`);
    }
  } else if (isTimingGood || isTypeCorrect) {
    droughtLevel = Math.max(5, droughtLevel - 4);
    showDialogue('나', '조건이 일부만 맞아떨어져 약한 이슬비만 내렸습니다. 다음엔 더 정밀하게 맞춰보자.');
  } else {
    showDialogue('나', '시딩 물질과 타이밍이 모두 빗나가 구름이 흩어져 버렸습니다... 예산만 낭비했군요.');
  }
  updateWeatherHUD();
  updateAlertStrip();
}

function openPhNeutralizeMinigame() {
  if (!activeTasks.phAlert && weather.ph >= 5.6) {
    showDialogue('나', `현재 수질 및 강수 pH는 ${weather.ph}로 안전합니다. 산성비 경보 시 이곳에서 알칼리 중화제를 투입할 수 있습니다.`);
    return;
  }

  const currentPh = weather.ph;
  openModal(`
    <div class="modal-header">
      <span class="modal-title">🧪 빗물저류조 및 강수 산성도(pH) 화학 중화 제어</span>
      <button class="close-btn" onclick="closeModal()">닫기</button>
    </div>
    <p style="font-size:0.95rem; color:#ff8cc6; margin-bottom:10px;">
      ⚠️ 현재 측정된 강수 산성도: <strong>pH ${currentPh}</strong> (황산·질산 성분 검출)
    </p>
    <p style="font-size:0.9rem; color:#d8c9ff; margin-bottom:16px;">
      알칼리성 중화제를 투입하여 안전 범위인 <strong>pH 6.2 ~ 6.8</strong>로 맞추세요!
    </p>
    <div style="background:#150b38; padding:18px; border-radius:12px; text-align:center; border:2px solid #b69cff;">
      <label style="font-size:1.1rem; font-weight:800; color:#ffd95e;">
        중화제 투입량: <span id="alkali-val">150</span> kg
      </label><br><br>
      <input type="range" id="alkali-slider" min="20" max="300" value="150" style="width:85%; accent-color:#7bf0c8;"
             oninput="document.getElementById('alkali-val').innerText = this.value">
    </div>
    <div style="text-align:center; margin-top:18px;">
      <button class="action-btn btn-yes" onclick="executePhNeutralize()">⚗️ 중화 용액 살포 및 pH 측정</button>
    </div>
  `);
}

function executePhNeutralize() {
  const dose = parseInt(document.getElementById('alkali-slider').value);
  const newPh = +(weather.ph + (dose * 0.01)).toFixed(2);
  closeModal();

  if (newPh >= 6.2 && newPh <= 6.8) {
    weather.ph = newPh;
    activeTasks.phAlert = false;
    weather.ecoHealth = Math.min(100, weather.ecoHealth + 6);
    if (acidRainDays > 0) acidRainDays--;
    showDialogue('나', `정확한 화학 당량 계산! 수질이 pH ${newPh}로 완벽하게 중화되어 생태계를 보호했습니다.`);
  } else if (newPh < 6.2) {
    weather.ph = newPh;
    showDialogue('나', `중화제가 부족하여 pH ${newPh}에 머물렀습니다. 산성도가 완전히 가시지 않았네요.`);
  } else {
    weather.ph = 7.4;
    activeTasks.phAlert = false;
    showDialogue('나', `중화제 과다 투입으로 수질이 pH ${newPh} 강알칼리성이 되어버렸습니다...`);
  }
  updateWeatherHUD();
  updateAlertStrip();
}

function openSensorRepairMinigame() {
  if (!activeTasks.sensorDirty) {
    showDialogue('나', '도심 4개 구역 대기질 센서망이 모두 정상 가동 중입니다.');
    return;
  }

  openModal(`
    <div class="modal-header">
      <span class="modal-title">📡 도심 대기질 센서망 원격 정비 단말기</span>
      <button class="close-btn" onclick="closeModal()">닫기</button>
    </div>
    <p style="font-size:0.92rem; color:#d8c9ff; margin-bottom:12px;">
      황사로 인해 센서가 오염되었습니다. <strong>4개의 오염된 센서 노드를 모두 클릭</strong>해 필터를 세척하세요!
    </p>
    <div class="sensor-grid">
      <div class="sensor-node dirty" id="node-1" onclick="cleanNode(1)">⚠️ 제1 발전소 구역 센서<br><small>[모래 막힘 - 클릭 세척]</small></div>
      <div class="sensor-node dirty" id="node-2" onclick="cleanNode(2)">⚠️ 제2 석유화학 구역 센서<br><small>[모래 막힘 - 클릭 세척]</small></div>
      <div class="sensor-node dirty" id="node-3" onclick="cleanNode(3)">⚠️ 제3 제련소 구역 센서<br><small>[모래 막힘 - 클릭 세척]</small></div>
      <div class="sensor-node dirty" id="node-4" onclick="cleanNode(4)">⚠️ 중앙 호수·주거지 센서<br><small>[모래 막힘 - 클릭 세척]</small></div>
    </div>
  `);
}

let cleanedCount = 0;
function cleanNode(idx) {
  const el = document.getElementById(`node-${idx}`);
  if (el && el.classList.contains('dirty')) {
    el.classList.remove('dirty');
    el.classList.add('clean');
    el.innerHTML = `✅ 센서 정상 가동<br><small>[교정 완료]</small>`;
    cleanedCount++;
    if (cleanedCount >= 4) {
      cleanedCount = 0;
      activeTasks.sensorDirty = false;
      budget += 10;
      setTimeout(() => {
        closeModal();
        updateAlertStrip();
        showDialogue('나', '4개 구역 센서 복구 완료! 정확한 오염 데이터 확보 보상으로 10억의 연구 수당을 획득했습니다.');
      }, 350);
    }
  }
}

function openAuditPhoneModal() {
  if (!activeTasks.phoneRinging || !activeTasks.currentAudit) {
    showDialogue('나', '현재 걸려온 긴급 환경 감사나 민원 전화가 없습니다.');
    return;
  }

  const audit = activeTasks.currentAudit;
  openModal(`
    <div class="modal-header">
      <span class="modal-title">☎️ [긴급 수신] ${audit.title}</span>
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
  const resultMsg = activeTasks.currentAudit.choices[choiceIdx].effect();
  activeTasks.phoneRinging = false;
  activeTasks.currentAudit = null;
  closeModal();
  updateWeatherHUD();
  updateAlertStrip();
  showDialogue('나', resultMsg);
}

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
      badge = `<span class="badge-status badge-pending">⏳ 설치 중 (${p.applyDay}일차 적용)</span>`;
      disabledClass = 'disabled';
      onClickAttr = '';
    } else if (budget < p.cost) {
      badge = `<span class="badge-status badge-ready">예산 부족 (${p.cost}억)</span>`;
      disabledClass = 'disabled';
      onClickAttr = '';
    } else {
      badge = `<span class="badge-status badge-ready">시행 가능 (${p.cost}억)</span>`;
    }

    return `
      <div class="policy-card ${disabledClass}" ${onClickAttr}>
        <div>
          <div style="font-weight:800; font-size:1.05rem; color:#fff4d6; margin-bottom:5px;">${p.name}</div>
          <div style="font-size:0.86rem; color:#d8c9ff; line-height:1.45;">${p.desc}</div>
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
    <p style="font-size:0.88rem; color:#ffd95e; margin-bottom:12px;">
      ※ 선택한 정책은 현장 시공을 거쳐 <strong>2일 후</strong>부터 도시에 적용됩니다.
    </p>
    <div class="policy-grid">${cardsHtml}</div>
  `);
}

function confirmPolicy(policyId) {
  const p = POLICIES.find(item => item.id === policyId);
  openModal(`
    <div style="text-align:center; padding:20px 10px;">
      <h3 style="font-family:'Gowun Batang', serif; font-size:1.45rem; color:#fff4d6; margin-bottom:12px;">
        "${p.name}"을(를) 선택하시겠습니까?
      </h3>
      <p style="color:#d8c9ff; font-size:0.98rem; margin-bottom:20px;">
        소요 예산: <strong>${p.cost}억</strong> | 적용 시점: <strong>${day + 2}일차 아침</strong>
      </p>
      <div style="display:flex; justify-content:center; gap:16px;">
        <button class="action-btn btn-yes" onclick="executePolicy('${p.id}')">확인</button>
        <button class="action-btn btn-no" onclick="renderLaptopModal()">취소</button>
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
    showDialogue('나', `오늘부터 [${newlyApplied.join(', ')}] 설비 가동 개시! 도시 환경이 개선되기 시작합니다.`);
  }
}

function updateWeatherHUD() {
  const hud = document.getElementById('hud-weather');
  const weatherNames = {
    'CLEAR': '☀️ 맑음 (사막 건조기후)',
    'DROUGHT': '🔥 자연재해: 극심한 폭염·가뭄',
    'DUST': '🌪️ 자연재해: 고농도 황사 발생',
    'HEAVY_RAIN': '⛈️ 자연재해: 국지성 폭우',
    'RAIN': '🌧️ 비 내리는 중'
  };
  const hasSensor = POLICIES.find(p => p.id === 'sensor').status === 'ACTIVE';
  const sensorInfo = (hasSensor && !activeTasks.sensorDirty)
    ? `SO₂: ${weather.so2.toFixed(0)} | NOₓ: ${weather.nox.toFixed(0)} | PM2.5: ${weather.pm25.toFixed(0)} | pH: ${weather.ph}`
    : (activeTasks.sensorDirty ? `⚠️ 센서 오염됨 (정비 단말기 클릭)` : `대기질 데이터: [센서 미설치]`);

  hud.innerHTML = `
    <div style="font-weight:800; color:#ffd95e; font-size:0.95rem;">${weatherNames[weather.type]}</div>
    <div style="font-size:0.84rem; color:#fff4d6;">바람: ${weather.windDir} ${weather.windSpeed}m/s | 습도: ${weather.humidity}% | 강수확률: ${weather.rainProb}%</div>
    <div style="font-size:0.82rem; color:#7bf0c8; margin-top:3px; font-weight:700;">${sensorInfo}</div>
  `;
}

function checkMonthEnd() {
  const status = getChecklistStatus();
  if (status.check1 && status.check2) {
    scene = 'ENDING';
    isPaused = true;
    document.getElementById('hud-clock').style.display = 'none';
    document.getElementById('hud-weather').style.display = 'none';
    document.getElementById('alert-strip').style.display = 'none';
    openModal(`
      <div style="text-align:center; padding:15px;">
        <h2 style="font-family:'Cinzel', serif; font-size:2rem; color:#ffd95e; margin-bottom:10px;">HAPPY ENDING : 푸른 하늘의 귀환</h2>
        <p style="font-family:'Gowun Batang', serif; font-size:1.12rem; line-height:1.8; color:#f0ece1; margin-bottom:20px;">
          가뭄 진행도 <strong>${droughtLevel.toFixed(1)}%</strong>, 산성비 빈도 <strong>${status.acidFreq}%</strong>!<br>
          당신은 사막 도시에 맑은 비와 푸른 녹지를 되찾아주었습니다. 위대한 업적을 축하합니다!
        </p>
        <button class="start-btn" onclick="location.reload()">다시 시작하기</button>
      </div>
    `);
  } else if (status.check1 || status.check2) {
    month++;
    day = 1;
    gameMinutes = 7 * 60;
    budget += 120;
    showDialogue('나', `목표 중 하나를 달성해 계약이 연장되었습니다! ${month}개월째 임무 개시 (추가 예산 120억 지원).`);
  } else {
    scene = 'ENDING';
    isPaused = true;
    openModal(`
      <div style="text-align:center; padding:15px;">
        <h2 style="font-family:'Cinzel', serif; font-size:1.9rem; color:#ff8cc6; margin-bottom:10px;">BAD ENDING : 계약 해지</h2>
        <p style="font-family:'Gowun Batang', serif; font-size:1.1rem; line-height:1.8; color:#f0ece1; margin-bottom:20px;">
          가뭄 진행도 <strong>${droughtLevel.toFixed(1)}%</strong>, 산성비 빈도 <strong>${status.acidFreq}%</strong>...<br>
          도시는 여전히 메마르고 오염되어 결국 해고 통지서를 받게 되었습니다.
        </p>
        <button class="start-btn" onclick="location.reload()">재도전하기</button>
      </div>
    `);
  }
}

// --- 고해상도 벡터 일러스트 패치 ---
const PAL = { ink: '#150b38', violet: '#6a3df0', deep: '#2b1580', mint: '#7bf0c8', pink: '#ff8cc6', sky: '#59d2ff', cream: '#fff4d6', yellow: '#ffd95e' };

function rr(x, y, w, h, fill, r, lw) {
  ctx.beginPath();
  if (ctx.roundRect) {
    ctx.roundRect(x, y, w, h, r === undefined ? 8 : r);
  } else {
    ctx.rect(x, y, w, h);
  }
  if (fill) { ctx.fillStyle = fill; ctx.fill(); }
  ctx.lineWidth = lw || 3;
  ctx.strokeStyle = PAL.ink;
  ctx.stroke();
}

function star(x, y, r, col) {
  ctx.fillStyle = col;
  ctx.beginPath();
  for (let i = 0; i < 8; i++) {
    const a = i * Math.PI / 4, rad = i % 2 ? r * 0.4 : r;
    ctx.lineTo(x + Math.cos(a) * rad, y + Math.sin(a) * rad);
  }
  ctx.closePath();
  ctx.fill();
}

function planet(x, y, r, col, ring) {
  if (ring) {
    ctx.strokeStyle = PAL.cream; ctx.lineWidth = 3;
    ctx.beginPath(); ctx.ellipse(x, y, r * 1.7, r * 0.5, -0.4, 0, Math.PI * 2); ctx.stroke();
  }
  ctx.beginPath(); ctx.arc(x, y, r, 0, Math.PI * 2);
  ctx.fillStyle = col; ctx.fill();
  ctx.lineWidth = 3; ctx.strokeStyle = PAL.ink; ctx.stroke();
  ctx.fillStyle = 'rgba(255,255,255,0.4)';
  ctx.beginPath(); ctx.arc(x - r * 0.3, y - r * 0.3, r * 0.28, 0, Math.PI * 2); ctx.fill();
}

const DOODLES = [
  [0.07, 0.14, 18, 's'], [0.20, 0.32, 24, 'm', 0], [0.33, 0.10, 14, 's'], [0.50, 0.22, 28, 'p', 1],
  [0.62, 0.08, 16, 's'], [0.78, 0.28, 22, 'm', 0], [0.90, 0.12, 20, 's'], [0.14, 0.52, 12, 's'], [0.88, 0.48, 14, 's']
];

function drawDoodles(h, alpha) {
  const t = Date.now() / 900;
  ctx.save();
  ctx.globalAlpha = alpha;
  DOODLES.forEach((d, i) => {
    const x = width * d[0], y = h * d[1] + Math.sin(t + i * 1.7) * 4;
    if (d[3] === 's') star(x, y, d[2], PAL.cream);
    else planet(x, y, d[2], d[3] === 'm' ? PAL.mint : PAL.pink, d[4] === 1);
  });
  ctx.restore();
}

function drawBushes(y, size) {
  for (let x = -size * 0.4, i = 0; x < width + size; x += size * 0.85, i++) {
    const cy = y + Math.sin(i * 2.3) * size * 0.12;
    ctx.beginPath(); ctx.arc(x, cy, size * 0.55, 0, Math.PI * 2);
    ctx.fillStyle = i % 3 === 0 ? PAL.sky : PAL.mint; ctx.fill();
    ctx.lineWidth = 3; ctx.strokeStyle = PAL.ink; ctx.stroke();
  }
}

function drawTitleBackground() {
  const g = ctx.createLinearGradient(0, 0, 0, height);
  g.addColorStop(0, '#7a4bff'); g.addColorStop(1, '#2a1480');
  ctx.fillStyle = g; ctx.fillRect(0, 0, width, height);

  ctx.fillStyle = 'rgba(255,255,255,0.05)';
  const s = 60;
  for (let y = 0; y < height; y += s) for (let x = ((y / s) % 2) * s; x < width; x += s * 2) ctx.fillRect(x, y, s, s);

  drawDoodles(height * 0.8, 1);

  const base = height * 0.8;
  for (let i = 0; i < 12; i++) {
    const bw = width * 0.05, bx = width * (0.1 + i * 0.07), bh = height * (0.18 + ((i * 37) % 5) * 0.06);
    rr(bx, base - bh, bw, bh + 60, i % 2 ? '#3a1fa0' : '#4b2cc4', 6);
    for (let wy = base - bh + 14; wy < base - 8; wy += 22) {
      ctx.fillStyle = (wy / 22 + i) % 3 < 1 ? PAL.yellow : 'rgba(255,244,214,0.25)';
      ctx.fillRect(bx + bw * 0.3, wy, bw * 0.4, 8);
    }
  }
  drawBushes(height * 0.9, 64);
  drawParticles('#ffffff', 3);
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
  const dp = (gameMinutes - 420) / 840, wh = height * 0.65;
  let a, b;
  if (weather.type === 'DUST') { a = '#b4579c'; b = '#ffb86b'; }
  else if (weather.type === 'RAIN' || weather.type === 'HEAVY_RAIN') { a = '#2a2a7a'; b = '#5b7fe0'; }
  else if (dp < 0.2) { a = '#5a3ad8'; b = '#ff9ec4'; }
  else if (dp < 0.7) { a = '#6a3df0'; b = '#8fe3ff'; }
  else if (dp < 0.88) { a = '#3a1d94'; b = '#ff7fb0'; }
  else { a = '#150b48'; b = '#3a2a9a'; }

  const g = ctx.createLinearGradient(0, 0, 0, wh);
  g.addColorStop(0, a); g.addColorStop(1, b);
  ctx.fillStyle = g; ctx.fillRect(0, 0, width, wh);
  if (weather.type !== 'DUST') drawDoodles(wh * 0.55, dp > 0.88 ? 1 : 0.8);

  const gr = Math.max(0, (100 - droughtLevel) / 100), gy = height * 0.56;
  ctx.fillStyle = gr > 0.6 ? '#3fd6a4' : '#e9c7a0';
  ctx.fillRect(0, gy, width, wh - gy);
  ctx.fillStyle = PAL.ink; ctx.fillRect(0, gy, width, 3);
  if (gr > 0.3) drawBushes(gy + 8, 30 + gr * 26);

  const t = Date.now() / 700;
  FACTORIES.forEach((f, idx) => {
    const fx = width * f.relX, fy = height * f.relY, fw = width * f.relW, fh = height * f.relH;
    rr(fx + fw * 0.2, fy, fw * 0.16, fh * 0.4, '#a98bff', 4);
    rr(fx + fw * 0.64, fy + fh * 0.1, fw * 0.16, fh * 0.3, '#a98bff', 4);
    rr(fx, fy + fh * 0.35, fw, fh * 0.65, idx % 2 ? '#8a6bff' : '#6a4be0', 8);
    for (let wx = 0; wx < 4; wx++) {
      ctx.fillStyle = PAL.yellow;
      ctx.fillRect(fx + fw * (0.1 + wx * 0.22), fy + fh * 0.55, fw * 0.12, fh * 0.14);
    }
    const sa = Math.min(0.85, weather.so2 / 140);
    for (let k = 0; k < 3; k++) {
      const sx = fx + fw * 0.28 + k * 7 + Math.sin(t + idx + k) * 5, sy = fy - 10 - k * 15;
      ctx.beginPath(); ctx.arc(sx, sy, 12 + k * 5, 0, Math.PI * 2);
      ctx.fillStyle = 'rgba(255,244,214,' + sa + ')'; ctx.fill();
      ctx.lineWidth = 2; ctx.strokeStyle = 'rgba(21,11,56,' + sa + ')'; ctx.stroke();
    }
  });

  if (weather.type === 'DUST') {
    drawParticles('rgba(255,217,94,0.7)', 12);
  } else if (weather.type === 'RAIN' || weather.type === 'HEAVY_RAIN') {
    ctx.lineCap = 'round';
    ctx.strokeStyle = weather.ph < 5.6 ? 'rgba(123,240,200,0.85)' : 'rgba(143,227,255,0.85)';
    ctx.lineWidth = weather.type === 'HEAVY_RAIN' ? 3 : 2;
    const count = weather.type === 'HEAVY_RAIN' ? 120 : 55;
    for (let i = 0; i < count; i++) {
      const rx = Math.random() * width, ry = Math.random() * wh;
      ctx.beginPath(); ctx.moveTo(rx, ry); ctx.lineTo(rx - 5, ry + 16); ctx.stroke();
    }
  }

  // 선명한 이중 창틀 프레임
  ctx.strokeStyle = PAL.ink; ctx.lineWidth = 12;
  ctx.strokeRect(0, 0, width, wh);
  for (let i = 1; i <= 3; i++) {
    ctx.beginPath(); ctx.moveTo((width / 4) * i, 0); ctx.lineTo((width / 4) * i, wh); ctx.stroke();
  }
  ctx.strokeStyle = PAL.pink; ctx.lineWidth = 3;
  ctx.strokeRect(8, 8, width - 16, wh - 16);

  // 책상 영역
  const dy = height * 0.63;
  const dg = ctx.createLinearGradient(0, dy, 0, height);
  dg.addColorStop(0, '#3c2399'); dg.addColorStop(1, '#1a0f55');
  ctx.fillStyle = dg; ctx.fillRect(0, dy, width, height - dy);
  const cols = [PAL.mint, PAL.pink, PAL.sky, PAL.yellow], cs = 26;
  for (let x = 0, i = 0; x < width; x += cs, i++) {
    ctx.fillStyle = cols[i % 4]; ctx.fillRect(x, dy, cs, cs);
    ctx.fillStyle = 'rgba(21,11,56,0.18)'; if (i % 2) ctx.fillRect(x, dy, cs, cs);
  }
  ctx.fillStyle = PAL.ink; ctx.fillRect(0, dy - 2, width, 4); ctx.fillRect(0, dy + cs, width, 4);

  drawDeskObjects();
}

function drawDeskObjects() {
  const I = id => DESK_ITEMS.find(o => o.id === id);
  const X = o => width * o.relX, Y = o => height * o.relY, W = o => width * o.relW, H = o => height * o.relH;
  const blink = Math.floor(Date.now() / 400) % 2 === 0;
  ctx.lineCap = 'round';

  // 무전기
  let o = I('radio');
  ctx.strokeStyle = PAL.ink; ctx.lineWidth = 4;
  ctx.beginPath(); ctx.moveTo(X(o) + W(o) * 0.3, Y(o)); ctx.lineTo(X(o) + W(o) * 0.3, Y(o) - H(o) * 0.55); ctx.stroke();
  rr(X(o), Y(o), W(o), H(o), '#5a3ad8', 10);
  for (let i = 0; i < 3; i++) { ctx.fillStyle = PAL.cream; ctx.beginPath(); ctx.arc(X(o) + W(o) * 0.3, Y(o) + H(o) * (0.45 + i * 0.16), 3.5, 0, Math.PI * 2); ctx.fill(); }
  ctx.fillStyle = activeTasks.seedingReady ? PAL.mint : '#8479b8';
  ctx.beginPath(); ctx.arc(X(o) + W(o) * 0.72, Y(o) + H(o) * 0.2, 6, 0, Math.PI * 2); ctx.fill();
  ctx.lineWidth = 2; ctx.stroke();

  // 신문
  o = I('newspaper');
  rr(X(o), Y(o), W(o), H(o), PAL.cream, 4);
  ctx.fillStyle = PAL.ink; ctx.fillRect(X(o) + W(o) * 0.08, Y(o) + H(o) * 0.14, W(o) * 0.84, 6);
  for (let i = 0; i < 3; i++) ctx.fillRect(X(o) + W(o) * 0.08, Y(o) + H(o) * (0.38 + i * 0.2), W(o) * (0.84 - i * 0.2), 3);

  // 서류 더미
  o = I('documents');
  for (let i = 2; i >= 0; i--) rr(X(o) + i * 5, Y(o) - i * 5, W(o), H(o), i === 0 ? PAL.cream : (i === 1 ? '#ffd0e8' : '#bfeaff'), 4);
  ctx.fillStyle = PAL.ink; ctx.fillRect(X(o) + W(o) * 0.12, Y(o) + H(o) * 0.25, W(o) * 0.5, 4);
  ctx.fillRect(X(o) + W(o) * 0.12, Y(o) + H(o) * 0.5, W(o) * 0.7, 3);

  // 노트북
  o = I('laptop');
  rr(X(o), Y(o), W(o), H(o) * 0.68, PAL.ink, 8);
  rr(X(o) + 7, Y(o) + 7, W(o) - 14, H(o) * 0.68 - 14, PAL.sky, 4, 2);
  star(X(o) + W(o) * 0.5, Y(o) + H(o) * 0.33, 11, PAL.cream);
  rr(X(o) - W(o) * 0.06, Y(o) + H(o) * 0.68, W(o) * 1.12, H(o) * 0.3, PAL.pink, 6);

  // 센서 단말기
  o = I('sensor_pad');
  rr(X(o), Y(o), W(o), H(o), '#3c2399', 8);
  rr(X(o) + 6, Y(o) + 6, W(o) - 12, H(o) * 0.55, (activeTasks.sensorDirty && blink) ? PAL.yellow : PAL.mint, 4, 2);
  ctx.fillStyle = PAL.pink; ctx.beginPath(); ctx.arc(X(o) + W(o) * 0.5, Y(o) + H(o) * 0.82, 5, 0, Math.PI * 2); ctx.fill();

  // 비커
  o = I('beaker');
  ctx.fillStyle = (activeTasks.phAlert && blink) ? '#ff5fa2' : PAL.sky;
  ctx.fillRect(X(o) + 3, Y(o) + H(o) * 0.45, W(o) - 6, H(o) * 0.5);
  rr(X(o), Y(o), W(o), H(o), 'rgba(255,244,214,0.25)', 6);
  ctx.fillStyle = PAL.cream; ctx.beginPath(); ctx.arc(X(o) + W(o) * 0.35, Y(o) + H(o) * 0.65, 4, 0, Math.PI * 2); ctx.fill();

  // 가족사진
  o = I('photo');
  rr(X(o), Y(o), W(o), H(o), PAL.yellow, 6);
  rr(X(o) + 5, Y(o) + 5, W(o) - 10, H(o) - 10, '#9a7bff', 3, 2);
  [0.32, 0.68].forEach((fx, k) => {
    ctx.fillStyle = k ? PAL.pink : PAL.mint; ctx.beginPath(); ctx.arc(X(o) + W(o) * fx, Y(o) + H(o) * 0.5, W(o) * 0.17, 0, Math.PI * 2); ctx.fill();
    ctx.lineWidth = 2; ctx.strokeStyle = PAL.ink; ctx.stroke();
  });

  // 펜꽂이
  o = I('penholder');
  ['#ff5fa2', PAL.sky, PAL.yellow].forEach((col, k) => {
    ctx.strokeStyle = PAL.ink; ctx.lineWidth = 6;
    ctx.beginPath(); ctx.moveTo(X(o) + W(o) * (0.25 + k * 0.25), Y(o) + H(o) * 0.4); ctx.lineTo(X(o) + W(o) * (0.1 + k * 0.32), Y(o) - 12); ctx.stroke();
    ctx.strokeStyle = col; ctx.lineWidth = 3; ctx.stroke();
  });
  rr(X(o), Y(o) + H(o) * 0.35, W(o), H(o) * 0.65, '#5a3ad8', 6);

  // 전화기
  o = I('phone');
  const sh = (activeTasks.phoneRinging && blink) ? 4 : 0;
  rr(X(o) + sh, Y(o), W(o), H(o), activeTasks.phoneRinging ? '#ff5fa2' : PAL.mint, 10);
  rr(X(o) + sh + W(o) * 0.1, Y(o) - H(o) * 0.2, W(o) * 0.8, H(o) * 0.3, PAL.cream, 8);
  ctx.fillStyle = PAL.ink;
  for (let i = 0; i < 3; i++) { ctx.beginPath(); ctx.arc(X(o) + sh + W(o) * (0.25 + i * 0.25), Y(o) + H(o) * 0.6, 3, 0, Math.PI * 2); ctx.fill(); }

  // 캘린더
  o = I('calendar');
  rr(X(o), Y(o), W(o), H(o), PAL.cream, 5);
  ctx.fillStyle = '#ff5fa2'; ctx.fillRect(X(o) + 2, Y(o) + 2, W(o) - 4, H(o) * 0.28);
  ctx.fillStyle = PAL.ink; ctx.font = 'bold 15px Gowun Batang';
  ctx.fillText(day + '일', X(o) + W(o) * 0.15, Y(o) + H(o) * 0.72);
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
      gameMinutes += deltaSec * 1.4 * timeMultiplier;

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
