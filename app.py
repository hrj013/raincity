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

  /* 레이튼 + 할로우 나이트 감성 패널 */
  .hollow-panel {
    background: rgba(18, 20, 28, 0.96);
    border: 2px solid #8c7a5b;
    box-shadow: 0 0 30px rgba(0, 0, 0, 0.9), inset 0 0 18px rgba(140, 122, 91, 0.25);
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
    color: #f7eedc;
    text-shadow: 0 4px 20px rgba(0,0,0,0.8), 0 0 40px rgba(212, 188, 139, 0.45);
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
    background: rgba(20, 22, 30, 0.78);
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

  /* 우측 상단 시계 HUD */
  #hud-clock {
    position: absolute;
    top: 20px;
    right: 24px;
    z-index: 15;
    background: linear-gradient(135deg, #2b241d 0%, #1a1715 100%);
    border: 2px solid #b89f74;
    border-radius: 14px;
    padding: 10px 18px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.65);
    display: none;
    align-items: center;
    gap: 12px;
  }

  .clock-day {
    font-family: 'Gowun Batang', serif;
    font-size: 1.2rem;
    font-weight: 700;
    color: #f3d59b;
  }

  .clock-time {
    font-size: 1.1rem;
    font-weight: 600;
    color: #ffffff;
    background: rgba(255,255,255,0.08);
    padding: 4px 10px;
    border-radius: 8px;
  }

  .speed-btn {
    background: rgba(255,255,255,0.1);
    border: 1px solid #8c7a5b;
    color: #e6d8be;
    font-size: 0.78rem;
    padding: 4px 8px;
    border-radius: 6px;
    cursor: pointer;
  }

  .speed-btn.active {
    background: #c9a66b;
    color: #161512;
    font-weight: 700;
  }

  /* 좌측 상단 기상 및 실시간 알림 배지 */
  #hud-weather {
    position: absolute;
    top: 20px;
    left: 24px;
    z-index: 15;
    background: rgba(22, 24, 33, 0.88);
    border: 1.5px solid #7d7365;
    border-radius: 12px;
    padding: 10px 18px;
    display: none;
    font-size: 0.9rem;
    line-height: 1.55;
    box-shadow: 0 4px 14px rgba(0,0,0,0.5);
  }

  /* 긴급 현장 작업 알림 배너 */
  #alert-strip {
    position: absolute;
    top: 105px;
    left: 24px;
    z-index: 15;
    display: none;
    flex-direction: column;
    gap: 8px;
  }

  .alert-pill {
    background: rgba(158, 42, 43, 0.9);
    border: 1px solid #ffccd5;
    color: #fff;
    padding: 7px 14px;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 600;
    cursor: pointer;
    animation: pulse 1.3s infinite;
    box-shadow: 0 4px 12px rgba(0,0,0,0.5);
  }

  @keyframes pulse {
    0%, 100% { transform: scale(1); opacity: 0.88; }
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
    font-size: 0.88rem;
    padding: 3px 14px;
    border-radius: 20px;
    margin-bottom: 8px;
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
    color: #c7ae80;
    margin-top: 6px;
  }

  /* 모달 오버레이 */
  #modal-backdrop {
    position: absolute;
    inset: 0;
    background: rgba(8, 10, 14, 0.76);
    backdrop-filter: blur(4px);
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
    border-bottom: 1px solid rgba(201, 177, 130, 0.35);
    padding-bottom: 12px;
    margin-bottom: 18px;
  }

  .modal-title {
    font-family: 'Gowun Batang', serif;
    font-size: 1.45rem;
    font-weight: 700;
    color: #f2dfb8;
  }

  .close-btn {
    background: none;
    border: 1px solid #8c7a5b;
    color: #d6c5a7;
    font-size: 0.95rem;
    padding: 4px 12px;
    border-radius: 6px;
    cursor: pointer;
  }

  .close-btn:hover {
    background: #8c7a5b;
    color: #12141c;
  }

  /* 신문 & 서류 더미 */
  .newspaper-sheet {
    background: #e8dec8;
    color: #241f18;
    padding: 26px;
    border-radius: 6px;
    font-family: 'Gowun Batang', serif;
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
    border-radius: 8px;
    font-family: 'Gowun Batang', serif;
  }

  .check-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 13px;
    margin: 10px 0;
    background: #e6decb;
    border-left: 5px solid #7d6844;
    border-radius: 4px;
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
    background: rgba(32, 36, 48, 0.92);
    border: 1px solid #695e4c;
    border-radius: 10px;
    padding: 14px;
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
    opacity: 0.52;
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

  /* 미니게임 UI 컴포넌트 */
  .radar-bar {
    position: relative;
    width: 100%;
    height: 36px;
    background: #1a1e29;
    border: 2px solid #8c7a5b;
    border-radius: 18px;
    overflow: hidden;
    margin: 18px 0;
  }

  .radar-target {
    position: absolute;
    top: 0;
    height: 100%;
    background: rgba(64, 145, 108, 0.65);
    border-left: 2px solid #95d5b2;
    border-right: 2px solid #95d5b2;
  }

  .radar-cursor {
    position: absolute;
    top: 0;
    width: 8px;
    height: 100%;
    background: #ffd166;
    box-shadow: 0 0 12px #ffd166;
  }

  .sensor-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 14px;
    margin: 16px 0;
  }

  .sensor-node {
    background: #232734;
    border: 1.5px solid #6c757d;
    border-radius: 10px;
    padding: 16px;
    text-align: center;
    cursor: pointer;
    transition: all 0.2s;
  }

  .sensor-node.dirty {
    border-color: #e09f3e;
    background: #3b2d1f;
  }

  .sensor-node.clean {
    border-color: #52b788;
    background: #1b3329;
  }

  .action-btn {
    padding: 10px 24px;
    border-radius: 8px;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    border: none;
    transition: 0.2s;
  }

  .btn-yes { background: #c9a66b; color: #161512; }
  .btn-yes:hover { background: #e0be82; }
  .btn-no { background: #3b3e4a; color: #e6e2d8; }
  .btn-no:hover { background: #505463; }

  .choice-btn {
    display: block;
    width: 100%;
    text-align: left;
    background: #252936;
    border: 1px solid #8c7a5b;
    color: #f0ece1;
    padding: 14px 18px;
    border-radius: 8px;
    margin-bottom: 10px;
    cursor: pointer;
    font-size: 0.98rem;
  }

  .choice-btn:hover {
    background: #383e52;
    border-color: #e3c891;
  }

  /* 툴팁 */
  #hover-tooltip {
    position: absolute;
    pointer-events: none;
    background: rgba(18, 20, 28, 0.94);
    border: 1px solid #d4bc8b;
    color: #f7eedc;
    padding: 5px 12px;
    border-radius: 20px;
    font-size: 0.86rem;
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
  width = canvas.width = window.innerWidth;
  height = canvas.height = window.innerHeight;
}
window.addEventListener('resize', resize);
resize();

// --- 게임 상태 변수 ---
let scene = 'TITLE';
let day = 1;
let month = 1;
let gameMinutes = 7 * 60; // 07:00 시작
let timeMultiplier = 1;   // 기본 1배속 (현실 10분 = 게임 1일)
let lastTimestamp = 0;
let isPaused = false;

// 도시 환경 및 시뮬레이션 지표
let budget = 250;
let droughtLevel = 68; // 목표: 30% 미만
let totalRainDays = 0;
let acidRainDays = 0;

let weather = {
  type: 'CLEAR',
  cloudType: 'WARM', // 'WARM'(따뜻한 구름) or 'COLD'(차가운 과냉각 구름)
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

// 실시간 현장 액션 상태 (환경공학자 & 환경평가원 업무)
let activeTasks = {
  seedingReady: true,      // 인공강우 작전 가능 여부 (하루 1회)
  phAlert: false,          // 산성비 중화 작업 필요 여부
  sensorDirty: false,      // 황사 등으로 대기질 센서 오염 여부
  phoneRinging: false,     // 긴급 환경 감사/민원 전화 수신 여부
  currentAudit: null
};

// 정책 데이터 (선택 후 2일 뒤에 적용)
const POLICIES = [
  { id: 'fgd', name: '배연탈황설비 (FGD)', cost: 45, desc: '공장·발전소의 SO₂를 알칼리성 물질로 제거하여 산성비 위험을 크게 낮춥니다.', status: 'READY', applyDay: null },
  { id: 'esp', name: '전기집진기 (ESP)', cost: 40, desc: '미세먼지(PM2.5)와 황산염 입자를 정전기로 포집하여 대기질을 개선합니다.', status: 'READY', applyDay: null },
  { id: 'sensor', name: '정밀 대기질 센서망', cost: 25, desc: 'SO₂, NOₓ, PM2.5, 강수 pH를 실시간 측정해 오염 확산과 산성비 위험을 정밀 분석합니다.', status: 'READY', applyDay: null },
  { id: 'raingarden', name: '빗물정원 조성', cost: 30, desc: '빗물이 토양으로 자연 침투하도록 유도해 홍수를 줄이고 비점오염 유출을 막습니다.', status: 'READY', applyDay: null },
  { id: 'permeable', name: '투수성 포장 도로', cost: 35, desc: '사막 도시의 아스팔트를 투수성 소재로 교체해 빗물 흡수율과 지하수 함양을 높입니다.', status: 'READY', applyDay: null },
  { id: 'reservoir', name: '지하 빗물저류조', cost: 50, desc: '폭우 시 도심 침수를 막고, 저장된 빗물을 활용해 가뭄 진행도를 크게 낮춥니다.', status: 'READY', applyDay: null },
  { id: 'seeding', name: '고출력 인공강우 시딩기', cost: 55, desc: '상공 구름에 촉매제를 대량 살포해 인공강우 작전의 기본 성공률과 강수량을 높입니다.', status: 'READY', applyDay: null }
];

// 창밖 3개 공장
const FACTORIES = [
  { id: 'factory1', name: '제1 화력·담수화 복합발전소', role: '도시 전력 공급과 바닷물 담수화를 담당하는 핵심 에너지 시설입니다.', pollutants: '아황산가스(SO₂), 질소산화물(NOₓ), 온배수', relX: 0.22, relY: 0.42, relW: 0.13, relH: 0.16 },
  { id: 'factory2', name: '제2 석유화학·정제 플랜트', role: '사막 부자도시의 외화를 벌어들이는 주력 석유화학 제품 생산 공장입니다.', pollutants: '휘발성유기화합물(VOCs), 아황산가스(SO₂), 초미세먼지(PM2.5)', relX: 0.44, relY: 0.43, relW: 0.14, relH: 0.15 },
  { id: 'factory3', name: '제3 시멘트·건설자재 제련소', role: '마천루 건설에 필요한 시멘트와 금속 자재를 가공하는 중공업 시설입니다.', pollutants: '고농도 미세먼지(PM10/PM2.5), 질소산화물(NOₓ), 중금속 분진', relX: 0.68, relY: 0.41, relW: 0.13, relH: 0.17 }
];

// 책상 위 오브젝트 (기존 6종 + 환경공학자 전문 장비 4종)
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

// 긴급 환경 감사/민원 시나리오 풀
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

// --- 오브젝트 클릭 핸들러 ---
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
        <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:2px solid #8c7a5b; padding-bottom:12px; margin-bottom:16px;">
          <span style="font-size:1.15rem; font-weight:700;">💰 가용 도시 환경 예산</span>
          <span style="font-size:1.5rem; font-weight:800; color:#1b4332;">${budget} 억 디르함</span>
        </div>
        <h3 style="margin-bottom:10px; color:#3d3122;">📋 30일차 최종 평가 체크리스트 (실시간 갱신)</h3>
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
        <p><strong style="color:#e3c891;">[시설 역할]</strong><br>${f.role}</p><br>
        <p><strong style="color:#ff8fa3;">[주요 배출 오염물질]</strong><br>${f.pollutants}</p>
      </div>
    `);
  }
}

// --- [미니게임 1] 인공강우 작전 지휘 (시딩 타이밍 레이더) ---
function openSeedingMinigame() {
  if (!activeTasks.seedingReady) {
    showDialogue('나', '오늘의 인공강우 시딩 항공기 출격은 이미 완료했어. 내일 기상 관측 데이터를 보고 다시 작전을 세우자.');
    return;
  }
  const cloudDesc = weather.cloudType === 'WARM'
    ? '따뜻한 구름층 (영상 기온 4℃) → 염화나트륨 등 [흡습성 입자] 적합'
    : '차가운 과냉각 구름층 (영하 -8℃) → 요오드화은 등 [빙정핵 입자] 적합';

  openModal(`
    <div class="modal-header">
      <span class="modal-title">🛩️ 인공강우 시딩(Cloud Seeding) 작전 통제</span>
      <button class="close-btn" onclick="closeModal()">닫기</button>
    </div>
    <p style="font-size:0.95rem; color:#e3c891; margin-bottom:8px;">📡 현재 상공 기상 레이더 분석: <strong>${cloudDesc}</strong></p>
    <p style="font-size:0.88rem; color:#cfc9bc; margin-bottom:14px;">
      1) 구름 온도에 맞는 촉매제를 선택한 뒤, 2) 움직이는 레이더 커서가 <strong>초록색 응결 골든타임 구간</strong>에 들어왔을 때 살포 버튼을 누르세요! (작전 비용: 10억)
    </p>
    <div style="margin-bottom:12px;">
      <label style="margin-right:16px; cursor:pointer;">
        <input type="radio" name="seedType" value="WARM" checked> 🧂 흡습성 시딩 입자 (따뜻한 구름용)
      </label>
      <label style="cursor:pointer;">
        <input type="radio" name="seedType" value="COLD"> ❄️ 빙정핵 시딩 입자 (차가운 구름용)
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
    // 완벽 성공 -> 즉시 비 내림
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
      showDialogue('나', `인공강우 작전 대성공! 하늘에서 비가 쏟아지기 시작했어! 하지만 대기 중 오염물질 때문에 강수 pH가 ${weather.ph}로 산성화되고 있어. 빨리 책상 위 [실험 세트]에서 중화 작업을 해야 해!`);
    } else {
      showDialogue('나', `완벽한 타이밍과 촉매제 선택이었어! 깨끗한 단비(pH ${weather.ph})가 내리면서 가뭄 진행도가 크게 떨어졌어!`);
    }
  } else if (isTimingGood || isTypeCorrect) {
    droughtLevel = Math.max(5, droughtLevel - 4);
    showDialogue('나', '구름 조건과 살포 타이밍 중 하나가 어긋나서 약한 이슬비만 내렸어. 다음엔 구름 온도와 레이더 타이밍을 모두 정확히 맞추자.');
  } else {
    showDialogue('나', '시딩 물질과 살포 타이밍이 모두 빗나가서 구름이 흩어져 버렸어... 아까운 예산만 날렸군.');
  }
  updateWeatherHUD();
  updateAlertStrip();
}

// --- [미니게임 2] 산성비 방지 화학 제어 (알칼리 중화제 배합 퍼즐) ---
function openPhNeutralizeMinigame() {
  if (!activeTasks.phAlert && weather.ph >= 5.6) {
    showDialogue('나', `현재 수질 및 강수 pH는 ${weather.ph}로 비교적 안정적이야. 산성비 경보가 울리면 이곳에서 소석회(알칼리 중화제)를 배합해 pH를 조절할 수 있어.`);
    return;
  }

  const currentPh = weather.ph;
  openModal(`
    <div class="modal-header">
      <span class="modal-title">🧪 빗물저류조 및 강수 산성도(pH) 화학 중화 제어</span>
      <button class="close-btn" onclick="closeModal()">닫기</button>
    </div>
    <p style="font-size:0.95rem; color:#ffccd5; margin-bottom:10px;">
      ⚠️ 현재 측정된 강수 산성도: <strong>pH ${currentPh}</strong> (황산·질산 성분 검출)
    </p>
    <p style="font-size:0.9rem; color:#cfc9bc; margin-bottom:16px;">
      알칼리성 중화제(탄산칼슘·소석회 용액)를 투입하여 목표 안전 범위인 <strong>pH 6.2 ~ 6.8</strong> 사이로 맞추세요!
      (힌트: pH 0.1 상승당 약 10kg의 중화제가 필요합니다)
    </p>
    <div style="background:#1b1f2b; padding:16px; border-radius:10px; text-align:center;">
      <label style="font-size:1.05rem; font-weight:700; color:#f3d59b;">
        중화제 투입량: <span id="alkali-val">150</span> kg
      </label><br><br>
      <input type="range" id="alkali-slider" min="20" max="300" value="150" style="width:85%;"
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
    showDialogue('나', `정확한 화학 당량 계산이었어! 수질이 pH ${newPh}로 완벽하게 중화되어 토양과 호수 생태계를 지켜냈어!`);
  } else if (newPh < 6.2) {
    weather.ph = newPh;
    showDialogue('나', `중화제 투입량이 조금 부족해서 pH ${newPh}에 머물렀어. 산성도가 완전히 가시지 않았군.`);
  } else {
    weather.ph = 7.4;
    activeTasks.phAlert = false;
    showDialogue('나', `중화제를 너무 과다 투입해서 오히려 수질이 pH ${newPh}의 강알칼리성이 되어버렸어... 다음엔 조금 더 정밀하게 계산하자.`);
  }
  updateWeatherHUD();
  updateAlertStrip();
}

// --- [미니게임 3] 대기질 센서 정비 단말기 ---
function openSensorRepairMinigame() {
  if (!activeTasks.sensorDirty) {
    showDialogue('나', '도심 전역에 설치된 4개 구역 대기질 센서망이 모두 정상적으로 데이터를 송신하고 있어.');
    return;
  }

  openModal(`
    <div class="modal-header">
      <span class="modal-title">📡 도심 대기질 센서망 원격 정비 단말기</span>
      <button class="close-btn" onclick="closeModal()">닫기</button>
    </div>
    <p style="font-size:0.92rem; color:#cfc9bc; margin-bottom:12px;">
      황사 모래바람으로 인해 광학 미세먼지 센서가 오염되었습니다. <strong>오염된 4개의 센서 노드를 모두 클릭</strong>해 에어로졸 필터를 세척하세요!
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
      setTimeout(() => {
        closeModal();
        updateAlertStrip();
        showDialogue('나', '4개 구역의 대기질 센서를 모두 복구했어! 정확한 오염 확산 데이터 확보 보상으로 10억의 연구 수당을 받았어.');
      }, 350);
    }
  }
}

// --- [미니게임 4] 환경평가원 직통 전화기 (돌발 감사 & 민원) ---
function openAuditPhoneModal() {
  if (!activeTasks.phoneRinging || !activeTasks.currentAudit) {
    showDialogue('나', '지금은 걸려온 환경 감사나 긴급 민원 전화가 없어. 전화벨이 울리면 바로 수화기를 들어보자.');
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
      <span class="modal-title">💻 환경공학 정책 제어 터미널 (잔여 예산: ${budget}억)</span>
      <button class="close-btn" onclick="closeModal()">닫기</button>
    </div>
    <p style="font-size:0.88rem; color:#c9b182; margin-bottom:12px;">
      ※ 선택한 정책은 현장 시공을 거쳐 <strong>2일 후</strong>부터 도시에 적용됩니다.
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

  // 자연재해 확률 (15% 가뭄, 2% 폭우, 30% 황사)
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

  // 매일 45% 확률로 긴급 환경 감사/민원 전화 수신
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
    showDialogue('나', `오늘부터 [${newlyApplied.join(', ')}] 설비가 가동되기 시작했어! 도시 환경이 한층 개선될 거야.`);
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
    ? `SO₂: ${weather.so2.toFixed(0)} | NOₓ: ${weather.nox.toFixed(0)} | PM2.5: ${weather.pm25.toFixed(0)} | 강수 pH: ${weather.ph}`
    : (activeTasks.sensorDirty ? `⚠️ 센서 오염됨 (정비 단말기 클릭 필요)` : `대기질 정밀 데이터: [센서 미설치]`);

  hud.innerHTML = `
    <div style="font-weight:700; color:#f3d59b;">${weatherNames[weather.type]}</div>
    <div style="font-size:0.84rem; color:#ddd;">바람: ${weather.windDir} ${weather.windSpeed}m/s | 습도: ${weather.humidity}% | 강수확률: ${weather.rainProb}%</div>
    <div style="font-size:0.82rem; color:#a8dadc; margin-top:2px;">${sensorInfo}</div>
  `;
}

// --- 30일차 결산 및 엔딩 ---
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
    month++;
    day = 1;
    gameMinutes = 7 * 60;
    budget += 120;
    showDialogue('나', `목표 중 하나를 달성해 계약이 연장되었어! ${month}개월째 임무를 이어가며 추가 예산 120억이 지원되었으니 이번 달엔 꼭 두 목표를 모두 완수하자.`);
  } else {
    scene = 'ENDING';
    isPaused = true;
    openModal(`
      <div style="text-align:center; padding:15px;">
        <h2 style="font-family:'Cinzel', serif; font-size:1.9rem; color:#ff8fa3; margin-bottom:10px;">BAD ENDING : 계약 해지</h2>
        <p style="font-family:'Gowun Batang', serif; font-size:1.1rem; line-height:1.8; color:#f0ece1; margin-bottom:20px;">
          가뭄 진행도 <strong>${droughtLevel.toFixed(1)}%</strong>, 산성비 빈도 <strong>${status.acidFreq}%</strong>...<br>
          도시는 여전히 메마르고 산성비에 신음하고 있습니다.<br>
          결국 환경정책국에서 해고 통지서를 받고 짐을 싸게 되었습니다.
        </p>
        <button class="start-btn" onclick="location.reload()">다시 도전하기</button>
      </div>
    `);
  }
}

// --- 그래픽 렌더링 ---
function drawTitleBackground() {
  const grad = ctx.createLinearGradient(0, 0, 0, height);
  grad.addColorStop(0, '#181424');
  grad.addColorStop(0.45, '#4a3238');
  grad.addColorStop(0.8, '#9e6b43');
  grad.addColorStop(1, '#2b1d16');
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, width, height);

  ctx.save();
  ctx.beginPath();
  ctx.arc(width * 0.5, height * 0.36, Math.min(width, height) * 0.22, 0, Math.PI * 2);
  ctx.fillStyle = 'rgba(247, 238, 220, 0.14)';
  ctx.fill();
  ctx.restore();

  ctx.fillStyle = '#141118';
  const baseY = height * 0.78;
  const buildings = [
    { x: 0.15, w: 0.04, h: 0.22 }, { x: 0.21, w: 0.05, h: 0.32 }, { x: 0.28, w: 0.03, h: 0.19 },
    { x: 0.34, w: 0.06, h: 0.42 }, { x: 0.42, w: 0.04, h: 0.28 }, { x: 0.48, w: 0.05, h: 0.48 },
    { x: 0.55, w: 0.06, h: 0.36 }, { x: 0.63, w: 0.04, h: 0.25 }, { x: 0.69, w: 0.05, h: 0.39 },
    { x: 0.76, w: 0.04, h: 0.21 }
  ];

  buildings.forEach(b => {
    const bx = width * b.x;
    const bw = width * b.w;
    const bh = height * b.h;
    ctx.fillRect(bx, baseY - bh, bw, bh + 40);
    ctx.beginPath();
    ctx.moveTo(bx + bw * 0.5, baseY - bh - 35);
    ctx.lineTo(bx + bw * 0.35, baseY - bh);
    ctx.lineTo(bx + bw * 0.65, baseY - bh);
    ctx.closePath();
    ctx.fill();
  });

  ctx.fillStyle = '#1c1412';
  ctx.beginPath();
  ctx.moveTo(0, height);
  ctx.lineTo(0, height * 0.76);
  ctx.quadraticCurveTo(width * 0.3, height * 0.71, width * 0.6, height * 0.78);
  ctx.quadraticCurveTo(width * 0.85, height * 0.83, width, height * 0.74);
  ctx.lineTo(width, height);
  ctx.fill();

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
  const dayProgress = (gameMinutes - 420) / 840;
  const skyGrad = ctx.createLinearGradient(0, 0, 0, height * 0.68);

  if (weather.type === 'DUST') {
    skyGrad.addColorStop(0, '#8c6239');
    skyGrad.addColorStop(1, '#c9965b');
  } else if (weather.type === 'RAIN' || weather.type === 'HEAVY_RAIN') {
    skyGrad.addColorStop(0, '#222b38');
    skyGrad.addColorStop(1, '#4a5a6e');
  } else if (dayProgress < 0.2) {
    skyGrad.addColorStop(0, '#3a4f7a');
    skyGrad.addColorStop(1, '#e8a87c');
  } else if (dayProgress < 0.7) {
    skyGrad.addColorStop(0, '#2b6cb0');
    skyGrad.addColorStop(1, '#ebd5b3');
  } else if (dayProgress < 0.88) {
    skyGrad.addColorStop(0, '#2d1e3e');
    skyGrad.addColorStop(0.6, '#b85d43');
    skyGrad.addColorStop(1, '#f2b872');
  } else {
    skyGrad.addColorStop(0, '#0b0e17');
    skyGrad.addColorStop(1, '#1d2436');
  }

  ctx.fillStyle = skyGrad;
  ctx.fillRect(0, 0, width, height * 0.68);

  const greenRatio = Math.max(0, (100 - droughtLevel) / 100);
  ctx.fillStyle = greenRatio > 0.6 ? '#4a6b48' : '#b89468';
  ctx.fillRect(0, height * 0.54, width, height * 0.14);

  // 창밖 3개 공장
  FACTORIES.forEach(f => {
    const fx = width * f.relX;
    const fy = height * f.relY;
    const fw = width * f.relW;
    const fh = height * f.relH;

    ctx.fillStyle = '#2b2d38';
    ctx.strokeStyle = '#121318';
    ctx.lineWidth = 2.5;
    ctx.fillRect(fx, fy + fh * 0.35, fw, fh * 0.65);
    ctx.strokeRect(fx, fy + fh * 0.35, fw, fh * 0.65);

    ctx.fillRect(fx + fw * 0.2, fy, fw * 0.14, fh * 0.35);
    ctx.strokeRect(fx + fw * 0.2, fy, fw * 0.14, fh * 0.35);
    ctx.fillRect(fx + fw * 0.65, fy + fh * 0.08, fw * 0.14, fh * 0.27);
    ctx.strokeRect(fx + fw * 0.65, fy + fh * 0.08, fw * 0.14, fh * 0.27);

    ctx.fillStyle = `rgba(90, 85, 80, ${Math.min(0.75, weather.so2 / 140)})`;
    ctx.beginPath();
    ctx.arc(fx + fw * 0.27, fy - 12, 16, 0, Math.PI * 2);
    ctx.arc(fx + fw * 0.35, fy - 26, 22, 0, Math.PI * 2);
    ctx.fill();
  });

  if (weather.type === 'DUST') {
    drawParticles('rgba(218, 165, 95, 0.65)', 12);
  } else if (weather.type === 'RAIN' || weather.type === 'HEAVY_RAIN') {
    ctx.strokeStyle = weather.ph < 5.6 ? 'rgba(180, 220, 160, 0.55)' : 'rgba(175, 215, 255, 0.6)';
    ctx.lineWidth = weather.type === 'HEAVY_RAIN' ? 2.2 : 1.3;
    const count = weather.type === 'HEAVY_RAIN' ? 140 : 65;
    for (let i = 0; i < count; i++) {
      const rx = Math.random() * width;
      const ry = Math.random() * height * 0.65;
      ctx.beginPath();
      ctx.moveTo(rx, ry);
      ctx.lineTo(rx - 6, ry + 18);
      ctx.stroke();
    }
  }

  // 통유리창 프레임
  ctx.strokeStyle = '#181920';
  ctx.lineWidth = 10;
  ctx.strokeRect(0, 0, width, height * 0.65);
  for (let i = 1; i <= 3; i++) {
    ctx.beginPath();
    ctx.moveTo((width / 4) * i, 0);
    ctx.lineTo((width / 4) * i, height * 0.65);
    ctx.stroke();
  }

  // 원목 책상
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

  drawDeskObjects();
}

function drawDeskObjects() {
  ctx.lineWidth = 2;
  ctx.strokeStyle = '#1c1815';
  const blink = Math.floor(Date.now() / 400) % 2 === 0;

  // 1. 인공강우 작전 무전기
  const rad = DESK_ITEMS[0];
  ctx.fillStyle = '#2b303a';
  ctx.fillRect(width * rad.relX, height * rad.relY, width * rad.relW, height * rad.relH);
  ctx.strokeRect(width * rad.relX, height * rad.relY, width * rad.relW, height * rad.relH);
  // 안테나
  ctx.beginPath();
  ctx.moveTo(width * (rad.relX + 0.015), height * rad.relY);
  ctx.lineTo(width * (rad.relX + 0.015), height * (rad.relY - 0.06));
  ctx.stroke();
  // 상태 LED
  ctx.fillStyle = activeTasks.seedingReady ? '#52b788' : '#6c757d';
  ctx.beginPath();
  ctx.arc(width * (rad.relX + 0.035), height * (rad.relY + 0.03), 5, 0, Math.PI * 2);
  ctx.fill();

  // 2. 신문 기사
  const news = DESK_ITEMS[1];
  ctx.fillStyle = '#e6dcc5';
  ctx.fillRect(width * news.relX, height * news.relY, width * news.relW, height * news.relH);
  ctx.strokeRect(width * news.relX, height * news.relY, width * news.relW, height * news.relH);
  ctx.fillStyle = '#3b332b';
  ctx.fillRect(width * (news.relX + 0.015), height * (news.relY + 0.02), width * (news.relW - 0.03), 5);

  // 3. 서류 더미
  const docs = DESK_ITEMS[2];
  for (let i = 2; i >= 0; i--) {
    ctx.fillStyle = i === 0 ? '#f7f3e8' : '#dcd3be';
    ctx.fillRect(width * docs.relX + i * 4, height * docs.relY - i * 4, width * docs.relW, height * docs.relH);
    ctx.strokeRect(width * docs.relX + i * 4, height * docs.relY - i * 4, width * docs.relW, height * docs.relH);
  }

  // 4. 노트북
  const lap = DESK_ITEMS[3];
  ctx.fillStyle = '#252934';
  ctx.fillRect(width * lap.relX, height * lap.relY, width * lap.relW, height * (lap.relH * 0.68));
  ctx.strokeRect(width * lap.relX, height * lap.relY, width * lap.relW, height * (lap.relH * 0.68));
  ctx.fillStyle = '#3b5266';
  ctx.fillRect(width * (lap.relX + 0.01), height * (lap.relY + 0.012), width * (lap.relW - 0.02), height * (lap.relH * 0.52));
  ctx.fillStyle = '#3a3f4d';
  ctx.fillRect(width * (lap.relX - 0.01), height * (lap.relY + lap.relH * 0.68), width * (lap.relW + 0.02), height * (lap.relH * 0.32));
  ctx.strokeRect(width * (lap.relX - 0.01), height * (lap.relY + lap.relH * 0.68), width * (lap.relW + 0.02), height * (lap.relH * 0.32));

  // 5. 대기질 센서 정비 단말기
  const sen = DESK_ITEMS[4];
  ctx.fillStyle = '#1e222b';
  ctx.fillRect(width * sen.relX, height * sen.relY, width * sen.relW, height * sen.relH);
  ctx.strokeRect(width * sen.relX, height * sen.relY, width * sen.relW, height * sen.relH);
  ctx.fillStyle = (activeTasks.sensorDirty && blink) ? '#e09f3e' : '#2b9348';
  ctx.fillRect(width * (sen.relX + 0.01), height * (sen.relY + 0.015), width * (sen.relW - 0.02), height * (sen.relH * 0.55));

  // 6. 수질·강수 pH 중화 실험 세트 (비커)
  const bkr = DESK_ITEMS[5];
  ctx.fillStyle = 'rgba(200, 230, 255, 0.35)';
  ctx.fillRect(width * bkr.relX, height * bkr.relY, width * bkr.relW, height * bkr.relH);
  ctx.strokeRect(width * bkr.relX, height * bkr.relY, width * bkr.relW, height * bkr.relH);
  // 비커 속 용액 색상 (산성 경보 시 붉은빛 점멸)
  ctx.fillStyle = (activeTasks.phAlert && blink) ? '#e63946' : '#4cc9f0';
  ctx.fillRect(width * (bkr.relX + 0.005), height * (bkr.relY + bkr.relH * 0.45), width * (bkr.relW - 0.01), height * (bkr.relH * 0.5));

  // 7. 가족사진
  const pic = DESK_ITEMS[6];
  ctx.fillStyle = '#8c6239';
  ctx.fillRect(width * pic.relX, height * pic.relY, width * pic.relW, height * pic.relH);
  ctx.strokeRect(width * pic.relX, height * pic.relY, width * pic.relW, height * pic.relH);
  ctx.fillStyle = '#d9cbb8';
  ctx.fillRect(width * (pic.relX + 0.008), height * (pic.relY + 0.012), width * (pic.relW - 0.016), height * (pic.relH - 0.024));

  // 8. 펜꽂이
  const pen = DESK_ITEMS[7];
  const px = width * pen.relX;
  const py = height * pen.relY;
  const pw = width * pen.relW;
  const ph = height * pen.relH;
  ['#c94a4a', '#3b6ea5', '#e3b23c'].forEach((col, idx) => {
    ctx.strokeStyle = col;
    ctx.lineWidth = 2.5;
    ctx.beginPath();
    ctx.moveTo(px + pw * (0.25 + idx * 0.25), py + ph * 0.4);
    ctx.lineTo(px + pw * (0.15 + idx * 0.3), py - 12);
    ctx.stroke();
  });
  ctx.strokeStyle = '#1c1815';
  ctx.lineWidth = 2;
  ctx.fillStyle = '#4a4e59';
  ctx.fillRect(px, py + ph * 0.35, pw, ph * 0.65);
  ctx.strokeRect(px, py + ph * 0.35, pw, ph * 0.65);

  // 9. 환경평가원 직통 전화기
  const phn = DESK_ITEMS[8];
  const shakeX = (activeTasks.phoneRinging && blink) ? 3 : 0;
  ctx.fillStyle = activeTasks.phoneRinging ? '#9e2a2b' : '#2b2d42';
  ctx.fillRect(width * phn.relX + shakeX, height * phn.relY, width * phn.relW, height * phn.relH);
  ctx.strokeRect(width * phn.relX + shakeX, height * phn.relY, width * phn.relW, height * phn.relH);

  // 10. 탁상 캘린더
  const cal = DESK_ITEMS[9];
  ctx.fillStyle = '#f5efe2';
  ctx.fillRect(width * cal.relX, height * cal.relY, width * cal.relW, height * cal.relH);
  ctx.strokeRect(width * cal.relX, height * cal.relY, width * cal.relW, height * cal.relH);
  ctx.fillStyle = '#9e2a2b';
  ctx.fillRect(width * cal.relX, height * cal.relY, width * cal.relW, height * (cal.relH * 0.28));
  ctx.fillStyle = '#1c1815';
  ctx.font = 'bold 14px Gowun Batang';
  ctx.fillText(`${day}일`, width * (cal.relX + 0.015), height * (cal.relY + 0.075));
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
