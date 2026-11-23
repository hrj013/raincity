import streamlit as st
import streamlit.components.v1 as components

GAME_TITLE = "내일의 도시"

st.set_page_config(
    page_title=GAME_TITLE,
    page_icon="🌙",
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

game_html = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>내일의 도시</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Cinzel:wght@600;800&family=Gowun+Batang:wght@400;700&family=Noto+Sans+KR:wght@300;400;600;700;800&display=swap');

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

  * { box-sizing: border-box; user-select: none; margin: 0; padding: 0; }

  body, html {
    width: 100%; height: 100%; overflow: hidden;
    background-color: #070a1c;
    font-family: 'Noto Sans KR', sans-serif;
    color: #f0ece1;
  }

  #game-container { position: relative; width: 100vw; height: 100vh; overflow: hidden; background: #0b0f2a; }

  canvas {
    position: absolute; top: 0; left: 0; width: 100%; height: 100%; display: block;
    image-rendering: pixelated; image-rendering: crisp-edges;
  }

  /* 미니게임용 캔버스: 모달 안에서 비율 유지 */
  canvas.mg {
    position: relative !important; width: 100% !important; height: auto !important;
    display: block; margin: 0 auto; border: 3px solid var(--edge);
    box-shadow: 0 0 0 3px var(--ink), 0 8px 0 3px var(--ink);
    image-rendering: pixelated; background: #0d163b; cursor: pointer; touch-action: none;
  }

  .hollow-panel, #dialogue-box, #hud-clock, #hud-weather {
    border: none; border-radius: 0;
    box-shadow:
      -4px 0 0 0 var(--edge), 4px 0 0 0 var(--edge), 0 -4px 0 0 var(--edge), 0 4px 0 0 var(--edge),
      -8px 0 0 0 var(--ink), 8px 0 0 0 var(--ink), 0 -8px 0 0 var(--ink), 0 8px 0 0 var(--ink),
      0 14px 0 0 rgba(0, 0, 0, 0.35);
  }

  .hollow-panel { background: linear-gradient(180deg, #16215a 0%, #0f1744 100%); padding: 24px; position: relative; }
  .hollow-panel::before {
    content: "🌙"; position: absolute; top: -16px; left: 50%; transform: translateX(-50%);
    background: #14205a; padding: 0 10px; color: var(--gold); font-size: 14px;
  }

  #title-overlay {
    position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center;
    z-index: 20; transition: opacity 1.2s ease, transform 2.2s cubic-bezier(0.25, 0.8, 0.25, 1);
  }
  #title-overlay::before {
    content: ''; position: absolute; inset: 0; z-index: -1;
    background: radial-gradient(ellipse 42% 30% at 50% 50%, rgba(6, 8, 28, 0.78) 0%, rgba(6, 8, 28, 0.45) 55%, rgba(6, 8, 28, 0) 100%);
    pointer-events: none;
  }
  #title-overlay.zooming { transform: scale(4.5) translate(5%, -5%); opacity: 0; pointer-events: none; }

  .title-eng {
    font-family: 'Press Start 2P', monospace; font-size: clamp(0.55rem, 1.3vw, 0.9rem); letter-spacing: 0.3em;
    color: #9ab0e8; margin-bottom: 18px; text-shadow: 2px 2px 0 #0a0d24;
  }
  .title-logo {
    font-family: 'Noto Sans KR', sans-serif; font-size: clamp(2.6rem, 8vw, 5.4rem); font-weight: 800; letter-spacing: 0.1em;
    color: #ffe9a8; text-shadow: 4px 4px 0 #b4533a, 8px 8px 0 #0a0d24; margin-bottom: 24px;
  }
  .title-sub {
    font-weight: 600; font-size: 1.1rem; letter-spacing: 0.22em; color: #d6e4ff;
    margin-bottom: 45px; text-shadow: 2px 2px 0 #0a0d24;
  }

  .start-btn {
    font-family: 'Press Start 2P', 'Cinzel', monospace; font-size: 1.05rem; letter-spacing: 0.15em;
    padding: 16px 44px; background: var(--gold); color: #1a1030; border: none; border-radius: 0; cursor: pointer;
    transition: transform 0.08s steps(2), box-shadow 0.08s steps(2);
    box-shadow: -4px 0 0 0 var(--ink), 4px 0 0 0 var(--ink), 0 -4px 0 0 var(--ink), 0 4px 0 0 var(--ink), 0 10px 0 0 var(--gold-dk), 0 10px 0 4px var(--ink);
  }
  .start-btn:hover { background: #ffd978; transform: translateY(-2px); }
  .start-btn:active {
    transform: translateY(6px);
    box-shadow: -4px 0 0 0 var(--ink), 4px 0 0 0 var(--ink), 0 -4px 0 0 var(--ink), 0 4px 0 0 var(--ink), 0 4px 0 0 var(--gold-dk), 0 4px 0 4px var(--ink);
  }

  #hud-clock {
    position: absolute; top: 24px; right: 28px; z-index: 15;
    background: linear-gradient(180deg, #1a2766 0%, #101847 100%);
    padding: 10px 18px; display: none; align-items: center; gap: 12px;
  }
  .clock-day { font-size: 1.1rem; font-weight: 700; color: #ffe08a; }
  .clock-time { font-size: 1.05rem; font-weight: 700; color: #ffffff; background: rgba(0, 0, 0, 0.35); padding: 4px 10px; letter-spacing: 0.04em; }
  .speed-btn {
    background: #26357f; border: none; color: #cfdcff; font-size: 0.78rem; padding: 5px 9px; border-radius: 0; cursor: pointer;
    box-shadow: 0 0 0 2px var(--ink), 0 4px 0 2px var(--ink); margin-right: 3px;
  }
  .speed-btn.active { background: var(--gold); color: #1a1030; font-weight: 700; }

  #hud-weather {
    position: absolute; top: 24px; left: 28px; z-index: 15;
    background: linear-gradient(180deg, #16215a 0%, #0f1744 100%);
    padding: 10px 18px; display: none; font-size: 0.9rem; line-height: 1.55;
  }

  #alert-strip { position: absolute; top: 120px; left: 28px; z-index: 15; display: none; flex-direction: column; gap: 12px; }
  .alert-pill {
    background: #b3262e; border: none; border-radius: 0; color: #fff; padding: 7px 14px; font-size: 0.85rem; font-weight: 700;
    cursor: pointer; animation: pulse 1.3s steps(2) infinite;
    box-shadow: -3px 0 0 0 #ffccd5, 3px 0 0 0 #ffccd5, 0 -3px 0 0 #ffccd5, 0 3px 0 0 #ffccd5, -6px 0 0 0 var(--ink), 6px 0 0 0 var(--ink), 0 -6px 0 0 var(--ink), 0 6px 0 0 var(--ink);
  }
  @keyframes pulse { 0%, 100% { transform: translateY(0); filter: brightness(0.92); } 50% { transform: translateY(-2px); filter: brightness(1.15); } }

  #dialogue-box {
    position: absolute; bottom: 30px; left: 50%; transform: translateX(-50%); width: min(820px, 88vw); z-index: 25;
    background: linear-gradient(180deg, #17235f 0%, #0d1540 100%); padding: 18px 26px; display: none; cursor: pointer;
  }
  .speaker-tag {
    display: inline-block; background: var(--gold); color: #1a1030; font-weight: 700; font-size: 0.88rem; padding: 3px 14px;
    margin-bottom: 10px; box-shadow: 0 0 0 2px var(--ink), 0 4px 0 2px var(--ink);
  }
  .dialogue-text { font-size: 1.05rem; font-weight: 400; line-height: 1.7; letter-spacing: 0.01em; color: #f4f1e6; }
  .dialogue-next { text-align: right; font-size: 0.8rem; color: var(--gold); margin-top: 6px; animation: blink 1s steps(2) infinite; }
  @keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0.25; } }

  #modal-backdrop { position: absolute; inset: 0; background: rgba(4, 6, 20, 0.78); z-index: 30; display: none; align-items: center; justify-content: center; }
  .modal-card { width: min(820px, 92vw); max-height: 88vh; overflow-y: auto; }
  .modal-header {
    display: flex; justify-content: space-between; align-items: center;
    border-bottom: 4px solid rgba(233, 239, 255, 0.25); padding-bottom: 12px; margin-bottom: 16px;
  }
  .modal-title { font-size: 1.25rem; font-weight: 700; color: #ffe08a; text-shadow: 2px 2px 0 var(--ink); }
  .close-btn {
    background: #26357f; border: none; color: #dbe6ff; font-size: 0.95rem; padding: 5px 14px; border-radius: 0; cursor: pointer;
    box-shadow: 0 0 0 3px var(--ink), 0 5px 0 3px var(--ink);
  }
  .close-btn:hover { background: var(--gold); color: #1a1030; }

  .newspaper-sheet { background: #e8dec8; color: #241f18; padding: 26px; font-family: 'Gowun Batang', serif; box-shadow: 0 0 0 3px var(--ink), 0 6px 0 3px var(--ink); }
  .news-head { text-align: center; border-top: 3px double #241f18; border-bottom: 3px double #241f18; padding: 10px 0; margin-bottom: 16px; }
  .dossier-box { background: #f4efe4; color: #222; padding: 20px; font-family: 'Gowun Batang', serif; box-shadow: 0 0 0 3px var(--ink), 0 6px 0 3px var(--ink); }
  .check-item {
    display: flex; align-items: center; justify-content: space-between; padding: 12px; margin: 9px 0;
    background: #e6decb; border-left: 6px solid #7d6844; font-size: 1.02rem; font-weight: 700;
  }

  .policy-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(290px, 1fr)); gap: 16px; }
  .policy-card {
    background: #1b2766; border: none; padding: 14px; cursor: pointer; transition: transform 0.08s steps(2);
    display: flex; flex-direction: column; justify-content: space-between;
    box-shadow: 0 0 0 3px #4b63c9, 0 0 0 6px var(--ink), 0 9px 0 6px var(--ink);
  }
  .policy-card:hover:not(.disabled) {
    box-shadow: 0 0 0 3px var(--gold), 0 0 0 6px var(--ink), 0 9px 0 6px var(--ink); transform: translateY(-3px); background: #25348a;
  }
  .policy-card.disabled { opacity: 0.52; cursor: not-allowed; }
  .badge-status { display: inline-block; font-size: 0.78rem; padding: 2px 8px; margin-top: 8px; }
  .badge-active { background: #2d6a4f; color: #d8f3dc; }
  .badge-pending { background: #b58328; color: #fff3b0; }
  .badge-ready { background: #3d405b; color: #e0e1dd; }

  .sensor-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 18px; margin: 16px 0; }
  .sensor-node {
    background: #1b2250; padding: 16px; text-align: center; cursor: pointer; transition: transform 0.08s steps(2);
    box-shadow: 0 0 0 3px #6c757d, 0 0 0 6px var(--ink);
  }
  .sensor-node.dirty { background: #4a3420; box-shadow: 0 0 0 3px #e09f3e, 0 0 0 6px var(--ink); }
  .sensor-node.clean { background: #17402f; box-shadow: 0 0 0 3px #52b788, 0 0 0 6px var(--ink); }

  .action-btn {
    padding: 10px 22px; font-size: 0.98rem; font-weight: 700; cursor: pointer; border: none;
    transition: transform 0.08s steps(2); box-shadow: 0 0 0 3px var(--ink), 0 7px 0 3px var(--ink);
  }
  .action-btn:active { transform: translateY(4px); }
  .btn-yes { background: var(--gold); color: #1a1030; }
  .btn-yes:hover { background: #ffd978; }
  .btn-no { background: #3b4a9a; color: #e6e9f8; }
  .btn-no:hover { background: #4d5fbd; }

  .choice-btn {
    display: block; width: 100%; text-align: left; background: #1d2a70; border: none; color: #f0ece1;
    padding: 13px 16px; margin-bottom: 12px; cursor: pointer; font-size: 0.96rem;
    box-shadow: 0 0 0 3px #4b63c9, 0 0 0 6px var(--ink);
  }
  .choice-btn:hover { background: #2a3a94; box-shadow: 0 0 0 3px var(--gold), 0 0 0 6px var(--ink); }

  /* 평가서 검토 미니게임 */
  .timebar { height: 12px; background: #0b1236; border: 3px solid var(--ink); margin: 6px 0 12px; }
  .timebar > div { height: 100%; background: var(--gold); width: 100%; }
  .rv-line {
    position: relative; padding: 11px 86px 11px 14px; margin: 9px 0; background: #e6decb; border-left: 6px solid #7d6844;
    font-size: 0.98rem; font-weight: 700; line-height: 1.5; cursor: pointer; color: #241f18;
  }
  .rv-line:hover { background: #f3ead2; }
  .rv-line.hit { background: #f4d3cf; border-left-color: #b3262e; cursor: default; }
  .rv-line.hit::after {
    content: '반려'; position: absolute; right: 12px; top: 50%; transform: translateY(-50%) rotate(-8deg);
    border: 3px solid #b3262e; color: #b3262e; padding: 2px 8px; font-weight: 800; animation: stamp .25s steps(3);
  }
  .rv-line.miss { animation: shake .3s steps(4); background: #f1e0a8; }
  @keyframes stamp { 0% { transform: translateY(-50%) rotate(-8deg) scale(3); opacity: 0; } 100% { transform: translateY(-50%) rotate(-8deg) scale(1); opacity: 1; } }
  @keyframes shake { 0%, 100% { transform: translateX(0); } 25% { transform: translateX(-5px); } 75% { transform: translateX(5px); } }

  #hover-tooltip {
    position: absolute; pointer-events: none; background: #101846; color: #fff4d2; padding: 5px 12px;
    font-size: 0.86rem; font-weight: 600; z-index: 18; display: none; transform: translate(-50%, -140%); white-space: nowrap;
    box-shadow: 0 0 0 3px var(--edge), 0 0 0 6px var(--ink);
  }
</style>
</head>
<body>

<div id="game-container">
  <canvas id="gameCanvas"></canvas>

  <div id="title-overlay">
    <div class="title-eng">TOMORROW'S CITY</div>
    <div class="title-logo">내일의 도시</div>
    <div class="title-sub">대전의 밤, 지속 가능한 내일을 평가하다</div>
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

let dailyWork = { tasks: [], budgetAtStart: 250 };
let pendingFinalDay = false;
let pendingDayNotice = '';
let previousCo2Emission = 280;

let budget = 250;
let pollutionRisk = 38;

let weather = {
  type: 'CLEAR', windDir: '서풍', windSpeed: 2.4, humidity: 55, temp: 19,
  so2: 18, nox: 24, pm25: 32, ecoHealth: 72, co2: 280
};

let activeTasks = { seedingReady: true, phAlert: false, sensorDirty: false, phoneRinging: false, currentAudit: null };

const POLICIES = [
  { id: 'fgd', name: '저NOx 연소·배출가스 방지시설', cost: 45, desc: '연소 효율을 높이고 질소산화물·황산화물 저감시설을 설치하도록 사업계획에 반영합니다.', risk: 0.55, perks: ['측정 SO₂ -12 · NOx -14', '온실가스 -22tCO₂e/일'], fit: ['FINE_DUST'], tip: '시설이 많이 들어설수록 효과가 커요. 미세먼지 낀 날에 특히 든든해요.', status: 'READY', applyDay: null },
  { id: 'esp', name: '고효율 설비 및 전력 사용 최적화', cost: 40, desc: '고효율 모터·전기화 설비와 에너지 관리 시스템을 적용해 온실가스와 대기오염 배출을 줄입니다.', risk: 0.55, perks: ['온실가스 -30tCO₂e/일 (가장 큼)'], fit: ['HEATWAVE'], tip: '온실가스를 가장 크게 줄여요. 폭염이 잦을 때 추천!', status: 'READY', applyDay: null },
  { id: 'sensor', name: '대기질·소음 통합 측정망', cost: 25, desc: '사업지 경계와 주거지역에 측정망을 설치해 미세먼지와 소음 영향을 지속적으로 확인합니다.', risk: 0, perks: ['화면 왼쪽 위에 SO₂·NOx·PM2.5 수치가 공개돼요', 'PM2.5 -4'], fit: [], tip: '다른 정책의 효과를 눈으로 확인할 수 있어요. (최종 평가 지수에는 반영되지 않아요)', noScore: true, status: 'READY', applyDay: null },
  { id: 'raingarden', name: '완충녹지 및 생태 연결축 확보', cost: 30, desc: '주거지와 사업시설 사이에 완충녹지를 두고 기존 녹지·하천 생태축을 연결하도록 권고합니다.', risk: 0.45, perks: ['생태 건강도 +1.5/일'], fit: ['HEAVY_RAIN', 'HEATWAVE'], tip: '가성비가 좋은 정책이에요. 생태 건강도도 함께 올라가요.', status: 'READY', applyDay: null },
  { id: 'permeable', name: '저영향개발(LID)·빗물관리', cost: 35, desc: '투수성 포장과 빗물정원, 저류시설을 반영해 불투수면 증가와 집중호우 때의 유출 영향을 줄입니다.', risk: 0.35, perks: [], fit: ['HEAVY_RAIN'], tip: '집중호우가 잦은 해에 유리해요.', status: 'READY', applyDay: null },
  { id: 'reservoir', name: '폐수 재이용 및 비점오염 저감', cost: 50, desc: '폐수 재이용, 초기우수 처리, 유출수 관리계획을 마련해 하천과 토양에 미치는 영향을 줄입니다.', risk: 0.3, perks: [], fit: ['HEAVY_RAIN'], tip: '비용이 큰 편이라 예산이 넉넉할 때 고르세요.', status: 'READY', applyDay: null },
  { id: 'seeding', name: '공사차량·비산먼지 관리계획', cost: 30, desc: '공사차량 동선과 운행시간을 조정하고 살수·세륜·덮개 등 비산먼지 저감대책을 마련합니다.', risk: 0.25, perks: [], fit: ['FINE_DUST'], tip: '저렴해서 최종 평가 지수를 싸게 낮추는 데 좋아요.', status: 'READY', applyDay: null }
];

const FACTORIES = [
  { id: 'factory1', name: '제1 에너지 공급시설 부지 (갑천변)', facility: 'LNG 열병합발전소', benefit: '대전 도심과 산업시설에 안정적인 전력과 열을 공급합니다.', role: '전력 공급은 필요하지만 연료 연소 과정에서 온실가스와 질소산화물 등이 발생할 수 있습니다. 주거지와의 이격거리, 배출구 높이, 저NOx 연소기술, 방지시설, 대체 에너지 입지를 비교해야 합니다.', pollutants: '온실가스(CO₂), 질소산화물(NOx), 황산화물(SOx), 소음 및 냉각수 영향', relX: 0.22, relY: 0.42, relW: 0.13, relH: 0.16 },
  { id: 'factory2', name: '제2 자원순환시설 부지 (대전천변)', facility: '폐기물 소각·자원회수시설', benefit: '대전에서 발생하는 폐기물을 처리하고 열과 자원을 회수합니다.', role: '폐기물 처리시설은 도시 운영에 필요하지만 대기배출, 악취, 폐수, 폐기물 운반차량과 주민 수용성 문제가 발생할 수 있습니다. 재활용·감량 대안, 배출가스 처리, 밀폐형 반입시설, 교통 동선을 함께 비교해야 합니다.', pollutants: '질소산화물(NOx), 먼지, 악취, 폐수, 운반차량 배출가스 및 소음', relX: 0.44, relY: 0.43, relW: 0.14, relH: 0.15 },
  { id: 'factory3', name: '제3 물류지원시설 부지 (유등천변)', facility: '대형 물류센터', benefit: '생활물자와 산업 원료를 공급하고 지역 일자리와 물류 기능을 지원합니다.', role: '물류시설은 지역경제와 생활에 필요하지만 대형 화물차 통행, 야간 소음, 대기오염, 넓은 불투수면과 녹지 훼손을 유발할 수 있습니다. 기존 도로 활용, 대중교통·친환경 차량, 완충녹지, 빗물관리 대안을 검토해야 합니다.', pollutants: '화물차 배출가스(PM2.5·NOx), 교통소음, 불투수면 증가, 녹지 훼손', relX: 0.68, relY: 0.41, relW: 0.13, relH: 0.17 }
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
  { id: 'radio', name: '📟 배출허용기준 판정 계측기 (대기오염 측정값)', relX: 0.04, relY: 0.65, relW: 0.07, relH: 0.13 },
  { id: 'newspaper', name: '📰 대전시 개발사업 환경영향평가 공고', relX: 0.13, relY: 0.74, relW: 0.14, relH: 0.12 },
  { id: 'documents', name: '📁 환경영향평가서·조사 체크리스트', relX: 0.29, relY: 0.70, relW: 0.13, relH: 0.14 },
  { id: 'laptop', name: '💻 환경 데이터 분석 노트북', relX: 0.44, relY: 0.64, relW: 0.16, relH: 0.17 },
  { id: 'sensor_pad', name: '📡 대기질·소음 측정자료 점검 단말기', relX: 0.62, relY: 0.67, relW: 0.08, relH: 0.12 },
  { id: 'beaker', name: '📝 평가서 초안 검토 (오류 찾기)', relX: 0.72, relY: 0.66, relW: 0.07, relH: 0.14 },
  { id: 'photo', name: '⛰️ 보문산 자락 사면·완충대 현장 조사 지도', relX: 0.80, relY: 0.73, relW: 0.06, relH: 0.10 },
  { id: 'penholder', name: '🏭 배출허용기준 점검 수첩', relX: 0.87, relY: 0.72, relW: 0.04, relH: 0.10 },
  { id: 'phone', name: '☎️ 주민 민원 전화 (말풍선 고르기)', relX: 0.85, relY: 0.61, relW: 0.07, relH: 0.09 },
  { id: 'calendar', name: '📅 환경조사 및 평가 일정 캘린더', relX: 0.92, relY: 0.71, relW: 0.06, relH: 0.11 },
  { id: 'ecology_game', name: '🌙 야간 보호종 현장 조사', relX: 0.04, relY: 0.85, relW: 0.10, relH: 0.09 },
  { id: 'noise_game', name: '🔊 최대소음도(Lmax) 측정', relX: 0.36, relY: 0.85, relW: 0.11, relH: 0.09 },
  { id: 'mitigation_game', name: '🧱 완충·저감시설 배치 시뮬레이터', relX: 0.68, relY: 0.85, relW: 0.11, relH: 0.09 },
  { id: 'wind_game', name: '💨 풍향·대기확산 예측', relX: 0.86, relY: 0.85, relW: 0.10, relH: 0.09 }
];

// ---- 주민 민원 전화: 말풍선 3개 중 평가에 반영할 근거를 고르는 시나리오 ----
function wrongFx(msg, riskUp) {
  return () => { if (riskUp) pollutionRisk = Math.min(100, pollutionRisk + riskUp); return msg; };
}
const AUDIT_SCENARIOS = [
  {
    title: '주민 민원 · 갑천변 발전소 대기확산 우려',
    situation: '갑천변 아파트 단지 주민들이 발전소 연기가 단지로 들어올까 걱정하며 전화했습니다. 세 분 모두 그럴듯하게 말하고 있어요. 평가에 반영할 만한 근거는 누구의 말일까요?',
    speakers: [
      { name: '아파트 주민', look: { hair: '#d8d8e0', hs: 'bun', shirt: '#8a5a9a', shirt2: '#74487f', pants: '#3b3550', cane: true },
        bubble: '굴뚝 높이만 충분히 높으면 연기가 멀리 퍼져서 사라지니까, 따로 확산 예측은 안 해도 되지 않을까요?', correct: false,
        effect: wrongFx('굴뚝이 높으면 도움이 되지만, 어느 계절·풍향에 어느 단지로 얼마나 오는지는 예측해 봐야 알아. 높이만으로 안심할 수는 없어.', 1.5) },
      { name: '동네 청년', look: { hair: '#3a2a1a', hs: 'cap', cap: '#2b6cb0', shirt: '#4b9a6b', shirt2: '#3a7e56', pants: '#2b2d42' },
        bubble: '연평균 미세먼지 농도가 기준 안이면, 하루 몇 시간 높아지는 건 크게 상관없는 거죠?', correct: false,
        effect: wrongFx('연평균이 기준 이내여도 단기(일·시간) 기준을 넘는 날이 생길 수 있어. 짧게 높아지는 때도 따로 봐야 해.', 1.5) },
      { name: '학부모', look: { hair: '#4a2c20', hs: 'long', shirt: '#d98aa0', shirt2: '#bd6f86', pants: '#3d3a52', bag: '#a8603c' },
        bubble: '여름과 겨울은 바람 방향이 달라요. 계절별 풍향 자료로 단지 높이까지 연기가 오는 날을 예측해 주세요.', correct: true,
        effect: () => { budget = Math.max(0, budget - 5); weather.co2 = Math.max(180, weather.co2 - 10); pollutionRisk = Math.max(5, pollutionRisk - 2); return '정확해! 계절별 풍향·풍속과 배출량을 함께 넣어야 오염물질이 어디로 얼마나 오는지 예측할 수 있어.'; } }
    ]
  },
  {
    title: '주민 민원 · 유등천변 물류센터 새벽 소음과 통학로',
    situation: '학부모들이 새벽 대형 화물차 소음과 등굣길을 걱정하며 전화했습니다. 소음 측정 방식에 대한 제안 중 평가 근거가 되는 말은 무엇일까요?',
    speakers: [
      { name: '상가 주인', look: { hair: '#5a5a66', hs: 'perm', shirt: '#7a8a4a', shirt2: '#667439', pants: '#4a3c30' },
        bubble: '부지 경계에서 잰 소음이 기준 이하면, 학교 앞도 당연히 괜찮은 거 아닌가요?', correct: false,
        effect: wrongFx('소음은 거리와 지형에 따라 달라져. 학교처럼 민감한 지점에서 따로 측정해야 해.', 1.5) },
      { name: '학부모', look: { hair: '#4a2c20', hs: 'long', shirt: '#d98aa0', shirt2: '#bd6f86', pants: '#3d3a52', bag: '#a8603c' },
        bubble: '등교 시간과 새벽 화물차 시간대에 학교 담장에서 소음을 재서, 환경기준과 비교해 주세요.', correct: true,
        effect: () => { budget = Math.max(0, budget - 6); pollutionRisk = Math.max(5, pollutionRisk - 2); return '맞아! 민감한 지점·시간대의 소음을 현장에서 측정해 환경기준과 비교해야 방음 대책의 근거가 생겨.'; } },
      { name: '택시 기사', look: { hair: '#2b2230', hs: 'short', shirt: '#e0b13e', shirt2: '#c4982a', pants: '#2b2d42' },
        bubble: '화물차 소음은 어차피 도로 소음이니, 물류센터가 아니라 도로 관리 쪽 문제 아닌가요?', correct: false,
        effect: wrongFx('사업이 새로 유발하는 통행량도 평가에 포함돼. 도로 관리 문제로만 넘길 수는 없어.', 1.5) }
    ]
  },
  {
    title: '주민 민원 · 대전천변 호우 시 오염수 유입',
    situation: '하천 산책로 주민들이 집중호우 때 부지에서 흘러나오는 물이 하천을 오염시킬까 걱정합니다. 비슷하게 들리는 세 의견 중 근거가 되는 말을 고르세요.',
    speakers: [
      { name: '산책 주민', look: { hair: '#2b2230', hs: 'cap', cap: '#c0392b', shirt: '#3b6ea5', shirt2: '#2f5985', pants: '#35384f' },
        bubble: '하수관이 이미 깔려 있으니까 비 오는 날도 다 하수관으로 처리될 텐데, 새 계산은 필요 없어 보여요.', correct: false,
        effect: wrongFx('집중호우에는 관로 용량을 넘칠 수 있고, 초기 빗물은 오염 부하가 커. 유출량을 새로 예측해야 해.', 1.5) },
      { name: '낚시 어르신', look: { hair: '#d8d8e0', hs: 'bald', shirt: '#6a7a5a', shirt2: '#566448', pants: '#4a4036', cane: true },
        bubble: '하천이 원래 탁하니까, 공사로 조금 더 나빠져도 눈에 띄지 않을 거예요.', correct: false,
        effect: wrongFx('이미 탁하다고 추가 오염을 허용할 순 없어. 현재 수질을 기준으로 증가분을 평가해야 해.', 1.5) },
      { name: '조깅하던 주민', look: { hair: '#3a2a1a', hs: 'short', shirt: '#6ad0c8', shirt2: '#52b0a8', pants: '#2b3a5a', glasses: true },
        bubble: '비가 쏟아질 때 부지에서 하천으로 나가는 물의 양과 오염 정도를 예측해서 저류시설 용량을 정해 주세요.', correct: true,
        effect: () => { budget = Math.max(0, budget - 7); weather.ecoHealth = Math.min(100, weather.ecoHealth + 7); pollutionRisk = Math.max(5, pollutionRisk - 2); return '정확해! 유출량·오염 부하를 예측해야 저류시설과 완충녹지를 알맞은 크기와 위치로 둘 수 있어.'; } }
    ]
  },
  {
    title: '주민 민원 · 습지 인근 야간 공사와 서식지',
    situation: '천변 습지 근처에서 야간 공사가 계획되자 주민들이 전화했습니다. 서식지 조사에 관한 세 의견 중 평가에 반영할 만한 말은 누구의 것일까요?',
    speakers: [
      { name: '근처 주민', look: { hair: '#5a5a66', hs: 'short', shirt: '#8a6a4a', shirt2: '#74583b', pants: '#2b2d42' },
        bubble: '낮에 한 번 가서 살펴봤는데 아무것도 안 보였으니까, 보호종은 없는 걸로 봐도 되지 않을까요?', correct: false,
        effect: wrongFx('야행성·번식기 종은 낮에 한 번 본 것으로는 알 수 없어. 시기와 시간대를 바꿔 반복 조사해야 해.', 1.5) },
      { name: '생태 모임 회원', look: { hair: '#4a2c20', hs: 'long', shirt: '#4b9a6b', shirt2: '#3a7e56', pants: '#3b3a52', glasses: true },
        bubble: '맹꽁이는 비 온 뒤 밤에 울어요. 그 시기에 야간 조사를 하고, 번식기를 피해 공사 시기를 정해 주세요.', correct: true,
        effect: () => { budget = Math.max(0, budget - 6); weather.ecoHealth = Math.min(100, weather.ecoHealth + 8); pollutionRisk = Math.max(5, pollutionRisk - 2); return '맞아! 종의 활동 시기에 맞춰 조사하고, 번식기를 피해 공사 시기를 조정해야 해.'; } },
      { name: '편의점 직원', look: { hair: '#2b2230', hs: 'short', shirt: '#6ad0c8', shirt2: '#52b0a8', pants: '#3a3a4a' },
        bubble: '보호종이 나온 자리만 울타리로 막고, 나머지 구역은 계획대로 공사하면 충분하지 않을까요?', correct: false,
        effect: wrongFx('그 자리만 막아도 주변 소음·조명과 이동 경로 단절로 서식이 어려워질 수 있어. 생태축 연결도 봐야 해.', 1.5) }
    ]
  },
  {
    title: '주민 민원 · 공사 비산먼지와 아파트 창문',
    situation: '공사장 바로 옆 아파트 주민들이 먼지 때문에 창문을 못 연다고 전화했습니다. 먼지 측정과 관리에 대한 세 제안 중 근거가 되는 말은 무엇일까요?',
    speakers: [
      { name: '건너편 상인', look: { hair: '#2b2230', hs: 'perm', shirt: '#7a8ab4', shirt2: '#64739a', pants: '#4a3c30' },
        bubble: '공사장 안쪽에 먼지 측정기를 한 대 두면, 주민 피해도 충분히 알 수 있지 않을까요?', correct: false,
        effect: wrongFx('공사장 안쪽 수치는 주민이 실제로 마시는 농도와 달라. 주거지 쪽 민감 지점에서 재야 해.', 1.5) },
      { name: '저층 주민', look: { hair: '#d8d8e0', hs: 'bun', shirt: '#c0613a', shirt2: '#a24f2e', pants: '#3b3550', cane: true },
        bubble: '공사 구간과 가까운 창문 높이에서 먼지 농도를 재고, 바람 부는 날 살수·세륜을 하는지 확인해 주세요.', correct: true,
        effect: () => { budget = Math.max(0, budget - 5); pollutionRisk = Math.max(5, pollutionRisk - 2.5); return '정확해! 민감한 지점에서 농도를 재고, 바람 센 날의 살수·세륜 같은 저감 이행을 확인해야 해.'; } },
      { name: '중학생', look: { hair: '#3a2a1a', hs: 'short', shirt: '#e0505a', shirt2: '#c0404a', pants: '#2b3a5a', bag: '#2b6cb0' },
        bubble: '먼지는 주로 도로에서 날리는 거니까, 공사장 관리와는 따로 생각해야 하지 않을까요?', correct: false,
        effect: wrongFx('도로 먼지도 있지만 공사 자체가 만드는 먼지가 있어. 공사장의 발생원 관리도 평가 대상이야.', 1.5) }
    ]
  },
  {
    title: '주민 민원 · 자원순환시설 악취',
    situation: '시설 주변 아파트 주민들이 여름 저녁마다 냄새가 난다고 전화했습니다. 악취 평가 방법에 관한 세 의견 중 근거가 되는 말은 누구의 것일까요?',
    speakers: [
      { name: '아파트 주민', look: { hair: '#4a2c20', hs: 'long', shirt: '#8a5a9a', shirt2: '#74487f', pants: '#3b3550' },
        bubble: '냄새는 사람마다 느끼는 게 달라서 측정이 어렵잖아요. 민원 건수로 판단하면 되지 않을까요?', correct: false,
        effect: wrongFx('악취는 공기 중 악취물질·희석배수로 측정할 수 있어. 민원 건수만으로는 정확한 판단이 어려워.', 1.5) },
      { name: '시설 관계자', look: { hair: '#2b2230', hs: 'helmet', shirt: '#e07a2f', shirt2: '#c4651f', pants: '#35384f', vest: '#f2c14e' },
        bubble: '탈취제를 더 많이 뿌리면 악취 수치가 내려가니까, 그걸 저감 계획에 넣어 주세요.', correct: false,
        effect: wrongFx('탈취제는 냄새를 가릴 뿐 발생원을 줄이지 못해. 밀폐·포집·처리 같은 근본 대책이 필요해.', 1.5) },
      { name: '저녁 산책 주민', look: { hair: '#d8d8e0', hs: 'bald', shirt: '#6a7a5a', shirt2: '#566448', pants: '#4a4036', cane: true },
        bubble: '바람 방향이 바뀌는 여름 저녁에 시설 주변 아파트에서 악취를 재고, 밀폐·탈취 계획을 보여 주세요.', correct: true,
        effect: () => { budget = Math.max(0, budget - 6); pollutionRisk = Math.max(5, pollutionRisk - 2); return '맞아! 악취가 심한 시간대·풍향 조건에서 민감 지점의 농도를 재고, 발생원 저감 계획을 확인해야 해.'; } }
    ]
  }
];

let particles = [];
for (let i = 0; i < 120; i++) {
  particles.push({ x: Math.random() * 2000, y: Math.random() * 1200, speedX: 2 + Math.random() * 5, speedY: -0.5 + Math.random() * 1.5, size: 1 + Math.random() * 2.5, alpha: 0.2 + Math.random() * 0.5 });
}

let activeMinigameCleanup = null;
function stopActiveMinigame() {
  if (typeof activeMinigameCleanup === 'function') activeMinigameCleanup();
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
    showDialogue('나', '기후 위기로 폭염과 집중호우, 미세먼지 문제가 심해진 대전이야. 환경평가원 실무자로서 배출기준 판정, 사면 현장조사, 평가서 검토, 야간 보호종 조사, 소음 측정, 저감시설 배치, 주민 민원 응대를 해 나가 보자!');
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
  if (document.getElementById('modal-backdrop').style.display !== 'flex') isPaused = false;
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
  if (document.getElementById('dialogue-box').style.display !== 'block') isPaused = false;
}

function updateAlertStrip() {
  const strip = document.getElementById('alert-strip');
  let alerts = [];
  if (activeTasks.phAlert) alerts.push(`<div class="alert-pill" onclick="handleObjectClick('beaker')">📝 호우 영향 검토: 평가서 초안 검토 필요 [서류] 클릭</div>`);
  if (activeTasks.sensorDirty) alerts.push(`<div class="alert-pill" onclick="handleObjectClick('sensor_pad')">📡 경고: 환경 측정장비 데이터 오류 발생! [점검 단말기] 클릭</div>`);
  if (activeTasks.phoneRinging) alerts.push(`<div class="alert-pill" onclick="handleObjectClick('phone')">☎️ 수신 중: 주민 민원 전화가 왔습니다! [전화기] 클릭</div>`);
  strip.innerHTML = alerts.join('');
  strip.style.display = alerts.length > 0 ? 'flex' : 'none';
}

function recordDailyTask(title, detail) { dailyWork.tasks.push({ title, detail }); }

function calculateFinalScores() {
  const builtCount = facilityDecisions.filter(d => d && d !== 'reject').length;
  const utilityScore = builtCount === 3 ? 3 : (builtCount >= 2 ? 2 : 1);
  const activePolicyCount = POLICIES.filter(p => p.status === 'ACTIVE' && p.id !== 'sensor').length;
  const netImpact = Math.max(0, projectImpactScore - activePolicyCount * 0.65 - assessmentQuality * 0.25);
  const risk = pollutionRisk;
  const environmentScore = (netImpact <= 1.5 && risk <= 48) ? 3 : ((netImpact <= 5 && risk <= 72) ? 2 : 1);
  return { utilityScore, environmentScore, builtCount, netImpact: +netImpact.toFixed(1), risk: +risk.toFixed(1) };
}

function scoreMark(score) { return score === 3 ? 'O' : (score === 2 ? '△' : 'x'); }

function handleObjectClick(id) {
  if (id === 'newspaper') {
    recordDailyTask('개발사업 평가 공고 및 사업계획 확인', '사업 목적, 규모, 입지, 공사·운영 계획과 환경영향평가 대상 항목을 확인했습니다.');
    openModal(`
      <div class="modal-header"><span class="modal-title">📰 대전시 개발사업 환경영향평가 공고</span><button class="close-btn" onclick="closeModal()">닫기</button></div>
      <div class="newspaper-sheet"><div class="news-head"><div style="font-size:0.85rem; letter-spacing:0.2em;">대전 환경영향평가팀</div>
      <h2 style="font-size:1.45rem; margin-top:4px;">"필요한 개발과 환경 보전, 두 가지를 함께 검토합니다"</h2></div>
      <p style="line-height:1.8; font-size:1.02rem;">기후 위기로 폭염과 집중호우, 대기오염 위험이 커진 대전. 갑천과 대전천, 유등천변에 에너지 공급시설, 자원순환시설, 물류지원시설의 입지가 제안되었다. 세 시설은 도시 운영에 필요하지만 온실가스와 대기오염, 소음, 교통량 증가, 녹지 훼손 등의 영향을 일으킬 수 있다.</p></div>
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

// ===== 센서 점검 =====
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

// ===== 노트북 정책 =====
function policyInfoHtml(p) {
  const remain = Math.max(0, TOTAL_GAME_DAYS - (day + 2) + 1);
  const lines = [];
  if (p.risk > 0) lines.push(`📉 하루 환경오염 위험도 <strong>-${p.risk.toFixed(2)}%p</strong> <span style="color:#a8c8ff;">(남은 기간 누적 약 -${(p.risk * remain).toFixed(1)}%p)</span>`);
  p.perks.forEach(t => lines.push(`✨ ${t}`));
  if (!p.noScore) lines.push(`⚖️ 최종 평가 <strong>잔여 영향 지수 -0.65</strong>`);
  lines.push(`💡 ${p.tip}`);
  return `<div style="font-size:0.82rem; line-height:1.65; color:#d9e4ff; margin-top:8px; padding:8px 10px; background:rgba(0,0,0,0.28);">${lines.join('<br>')}</div>`;
}

function renderLaptopModal() {
  const order = POLICIES.map((p, i) => ({ p, i })).sort((a, b) => {
    const fa = a.p.fit.includes(weather.type) ? 0 : 1, fb = b.p.fit.includes(weather.type) ? 0 : 1;
    return fa - fb || a.i - b.i;
  }).map(o => o.p);
  let cardsHtml = order.map(p => {
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
    const rec = (p.status === 'READY' && p.fit.includes(weather.type)) ? `<span class="badge-status" style="background:#b3262e; color:#fff; margin-left:6px;">🔥 오늘 날씨 추천</span>` : '';
    return `
      <div class="policy-card ${disabledClass}" ${onClickAttr}>
        <div>
          <div style="font-weight:700; font-size:1.05rem; color:#f5e6c8; margin-bottom:5px;">${p.name}</div>
          <div style="font-size:0.86rem; color:#cfc9bc; line-height:1.45;">${p.desc}</div>
          ${policyInfoHtml(p)}
        </div>
        <div>${badge}${rec}</div>
      </div>
    `;
  }).join('');

  openModal(`
    <div class="modal-header"><span class="modal-title">💻 환경영향 저감방안 검토 시스템 (잔여 예산: ${budget}억)</span><button class="close-btn" onclick="closeModal()">닫기</button></div>
    <div style="background:#1d2a70; padding:10px 14px; margin-bottom:12px; font-size:0.88rem; line-height:1.65; color:#e6ecff; box-shadow:0 0 0 3px #4b63c9, 0 0 0 6px var(--ink);">
      📘 <strong>정책 고르는 법</strong> — 정책은 <strong>2일 뒤</strong>부터 적용돼요. 적용된 정책 1개마다 <strong>최종 평가의 잔여 영향 지수가 0.65</strong> 낮아지고(측정망 제외), 하루 오염 위험도도 매일 줄어요. <strong>일찍 고를수록 누적 효과가 커요.</strong> 예산은 조건부 동의(18억)에도 쓰이니 아껴 쓰세요. 오늘 날씨에 맞는 정책이 맨 위에 올라와요.
    </div>
    <div class="policy-grid">${cardsHtml}</div>
  `);
}

function confirmPolicy(policyId) {
  const p = POLICIES.find(item => item.id === policyId);
  openModal(`
    <div style="text-align:center; padding:20px 10px;">
      <h3 style="font-family:'Gowun Batang', serif; font-size:1.45rem; color:#f5e6c8; margin-bottom:12px;">"${p.name}"을(를) 선택하시겠습니까?</h3>
      <p style="color:#cfc9bc; font-size:0.98rem;">소요 예산: <strong>${p.cost}억</strong> | 적용 시점: <strong>${day + 2}일차 아침</strong></p>
      <div style="max-width:520px; margin:12px auto 0; text-align:left;">${policyInfoHtml(p)}</div>
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
  if (pendingMilestoneIndex !== null) showSiteDecisionModal(pendingMilestoneIndex);
  else if (pendingFinalDay) { pendingFinalDay = false; showFinalAssessmentSummary(); }
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
    title = 'GOOD ENDING : 달빛이 맑은 대전';
    message = '15일의 평가가 끝났어. 꼭 필요한 시설은 들어섰고, 갑천에는 다시 달빛이 비쳐. 주민들은 한빛탑 아래에서 환경평가원에게 손을 흔들었어. 내일의 도시는 이렇게 지켜졌어.';
  } else if (hasTriangle) {
    title = 'PARTIAL ENDING : 버텨내는 대전';
    message = '대전은 유지되고 있지만, 일부 개발사업의 환경 부담이 남아 있어. 하늘엔 옅은 연무가 끼었지만 아직 늦지 않았어. 내일의 도시를 위해 할 일이 남았어.';
  } else {
    title = 'BAD ENDING : 사막이 된 대전';
    message = '필요한 시설과 환경 보전, 두 가지 모두 놓치고 말았어. 비가 줄고 숲이 사라지자 갑천은 말라 갈라졌고, 도시는 모래바람 속에 묻혀 갔어. 다음에는 다른 선택을 해 보자.';
  }
  const names = { standard: '협의 동의', conditional: '조건부 동의', reject: '부동의' };
  const summary = '<div style="font-size:0.88rem; color:#a8c8ff; margin-bottom:16px; line-height:1.8;">' +
    FACTORIES.map((f, i) => `${f.facility}: <strong>${names[facilityDecisions[i]] || '-'}</strong>`).join(' · ') + '</div>';
  openEndingScene(endingType, title, message, summary);
}

// =====================================================================
//  픽셀 미니게임 공용 도우미 (점프킹 · 투더문 풍의 도트 그래픽)
// =====================================================================
const MG_INK = '#0a0d24';

function mgR(c, x, y, w, h, col) {
  c.fillStyle = col;
  c.fillRect(Math.round(x), Math.round(y), Math.round(w), Math.round(h));
}

function mgDisc(c, cx, cy, r, col, s) {
  s = s || 4;
  c.fillStyle = col;
  for (let yy = -r; yy <= r; yy += s) {
    const half = Math.round(Math.sqrt(Math.max(0, r * r - yy * yy)) / s) * s;
    c.fillRect(Math.round(cx - half), Math.round(cy + yy), half * 2 + s, s);
  }
}

function mgPt(e, cv) {
  const rect = cv.getBoundingClientRect();
  return { x: (e.clientX - rect.left) / rect.width * cv.width, y: (e.clientY - rect.top) / rect.height * cv.height };
}

// 투더문 풍 밤하늘 + 달
function mgSky(c, W, horizon, moon) {
  const n = Math.ceil(horizon / 8);
  for (let i = 0; i < n; i++) {
    c.fillStyle = colorAt(SKY_STOPS.night, n === 1 ? 0 : i / (n - 1));
    c.fillRect(0, i * 8, W, 8);
  }
  const r = makeRng(9);
  for (let i = 0; i < 50; i++) {
    const x = Math.floor(r() * W / 4) * 4, y = Math.floor(r() * horizon * 0.8 / 4) * 4;
    c.fillStyle = r() < 0.2 ? '#fff6c8' : '#c9d3f5';
    c.fillRect(x, y, r() < 0.2 ? 4 : 2, r() < 0.2 ? 4 : 2);
  }
  if (moon) {
    c.globalAlpha = 0.10; mgDisc(c, moon.x, moon.y, moon.r + 22, '#cfe0ff');
    c.globalAlpha = 0.18; mgDisc(c, moon.x, moon.y, moon.r + 10, '#cfe0ff');
    c.globalAlpha = 1;
    mgDisc(c, moon.x, moon.y, moon.r, '#f6f0cf');
    mgDisc(c, moon.x - moon.r * 0.35, moon.y - moon.r * 0.25, Math.max(2, moon.r * 0.2), '#dcd5ab', 2);
    mgDisc(c, moon.x + moon.r * 0.3, moon.y + moon.r * 0.3, Math.max(2, moon.r * 0.26), '#e3dcb4', 2);
  }
}

// 대전 아파트 스카이라인
function mgSkyline(c, W, baseY, seed, col, win, scale) {
  const r = makeRng(seed);
  scale = scale || 1;
  let x = 0;
  while (x < W) {
    const bw = 24 + Math.floor(r() * 5) * 8;
    const bh = Math.round((40 + Math.floor(r() * 6) * 10) * scale);
    mgR(c, x, baseY - bh, bw, bh, col);
    if (win) {
      for (let wy = baseY - bh + 8; wy < baseY - 6; wy += 12) {
        for (let wx = x + 6; wx < x + bw - 8; wx += 10) if (r() < 0.35) mgR(c, wx, wy, 4, 6, win);
      }
    }
    x += bw + (r() < 0.4 ? 8 : 0);
  }
}

// 대전 엑스포과학공원 한빛탑
function mgHanbit(c, x, baseY, col, k) {
  k = k || 1;
  const R = (gx, gy, w, h, cc) => mgR(c, x + gx * k, baseY + gy * k, w * k, h * k, cc || col);
  R(-14, -4, 28, 4);
  R(-3, -70, 6, 66);
  R(-9, -80, 18, 10);
  R(-12, -84, 24, 3);
  R(-6, -96, 12, 12);
  R(-1, -122, 2, 26);
  R(-1, -124, 2, 2, '#e0505a');
  R(-7, -78, 2, 3, '#ffd36b'); R(-1, -78, 2, 3, '#ffd36b'); R(5, -78, 2, 3, '#ffd36b');
  R(-3, -92, 2, 3, '#ffd36b'); R(1, -92, 2, 3, '#ffd36b');
}

function mgHeart(c, x, y, s, on) {
  const rows = [[0, 1, 0, 1, 0], [1, 1, 1, 1, 1], [0, 1, 1, 1, 0], [0, 0, 1, 0, 0]];
  rows.forEach((row, j) => row.forEach((v, i) => { if (v) mgR(c, x + i * s, y + j * s, s, s, on ? '#e0505a' : '#3b3f5c'); }));
}

function mgHouse(c, x, y, s, wall, roof) {
  mgR(c, x - 1, y + 3 * s - 1, 8 * s + 2, 5 * s + 2, MG_INK);
  mgR(c, x, y + 3 * s, 8 * s, 5 * s, wall);
  for (let i = 0; i < 3; i++) mgR(c, x + (3 - i) * s - 1, y + i * s, (2 + 2 * i) * s + 2, s, i === 0 ? MG_INK : roof);
  mgR(c, x + s, y + 4 * s, 2 * s, 2 * s, '#ffd166');
  mgR(c, x + 5 * s, y + 5 * s, 2 * s, 3 * s, '#5b3a22');
}

// 파라미터형 도트 사람 (12 x 22 격자)
function mgPerson(c, x, y, s, o) {
  const skin = o.skin || '#f1c7a0', hair = o.hair || '#2b2230', shirt = o.shirt || '#4b6fb5';
  const sh2 = o.shirt2 || shirt, pants = o.pants || '#35384f';
  const R = (gx, gy, w, h, col) => mgR(c, x + gx * s, y + gy * s, w * s, h * s, col);
  R(2, 0, 8, 10, MG_INK); R(0, 9, 12, 9, MG_INK); R(2, 17, 8, 5, MG_INK);
  R(3, 17, 3, 4, pants); R(6, 17, 3, 4, pants); R(3, 21, 3, 1, '#1a1a24'); R(6, 21, 3, 1, '#1a1a24');
  R(2, 10, 8, 7, shirt); R(0, 10, 2, 6, sh2); R(10, 10, 2, 6, sh2); R(0, 16, 2, 2, skin); R(10, 16, 2, 2, skin);
  if (o.vest) { R(2, 10, 2, 7, o.vest); R(8, 10, 2, 7, o.vest); }
  if (o.bag) { R(8, 12, 4, 5, o.bag); R(8, 12, 4, 1, MG_INK); }
  if (o.cane) R(11, 13, 1, 9, '#8a5a2b');
  R(3, 3, 6, 6, skin);
  const hs = o.hs || 'short';
  if (hs === 'bald') { R(3, 2, 6, 1, skin); R(4, 2, 2, 1, '#fff4e0'); }
  else if (hs === 'cap') { R(3, 1, 6, 3, o.cap || '#c0392b'); R(2, 3, 9, 1, o.cap || '#c0392b'); }
  else if (hs === 'helmet') { R(2, 1, 8, 3, '#f2c14e'); R(2, 3, 8, 1, '#c99a2e'); }
  else {
    R(3, 1, 6, 3, hair); R(3, 3, 1, 2, hair); R(8, 3, 1, 2, hair);
    if (hs === 'long') { R(2, 3, 2, 7, hair); R(8, 3, 2, 7, hair); }
    if (hs === 'bun') { R(5, 0, 2, 1, hair); R(4, 1, 4, 1, hair); }
    if (hs === 'perm') { R(2, 1, 8, 4, hair); R(2, 3, 2, 3, hair); R(8, 3, 2, 3, hair); }
  }
  if (o.glasses) { R(3, 5, 3, 2, '#a8dadc'); R(6, 5, 3, 2, '#a8dadc'); }
  R(4, 5, 1, 1, MG_INK); R(7, 5, 1, 1, MG_INK);
  if (o.talk) { R(5, 7, 2, 2, '#7a2c3a'); R(5, 7, 2, 1, '#e0605e'); } else R(5, 8, 2, 1, '#a8606a');
}

// 도트 말풍선 (계단형 모서리 + 꼬리)
function mgBubble(c, x, y, w, h, fill, line, tailX) {
  const s = 4;
  mgR(c, x + s, y, w - 2 * s, h, line); mgR(c, x, y + s, w, h - 2 * s, line);
  mgR(c, x + s, y + 3, w - 2 * s, h - 6, fill); mgR(c, x + 3, y + s, w - 6, h - 2 * s, fill);
  for (let i = 0; i < 4; i++) { const ww = (7 - 2 * i) * 4; mgR(c, tailX - ww / 2, y + h - 2 + i * 4, ww, 4, line); }
  for (let i = 0; i < 3; i++) { const ww = (5 - 2 * i) * 4 - 2; mgR(c, tailX - ww / 2, y + h - 3 + i * 4, ww, 4, fill); }
}

function mgWrap(c, text, maxW) {
  const words = text.split(' ');
  const lines = [];
  let cur = '';
  words.forEach(w => {
    const t = cur ? cur + ' ' + w : w;
    if (c.measureText(t).width > maxW && cur) { lines.push(cur); cur = w; } else cur = t;
  });
  if (cur) lines.push(cur);
  return lines;
}

function mgCreature(c, k, x, y, s) {
  const R = (gx, gy, w, h, col) => mgR(c, x + gx * s, y + gy * s, w * s, h * s, col);
  if (k === 'frog') {
    R(-3, -4, 6, 4, '#4f9a52'); R(-2, -5, 4, 2, '#6fbf6a'); R(-3, -6, 1, 1, '#fff'); R(2, -6, 1, 1, '#fff');
    R(-4, -1, 2, 1, '#3a7a3e'); R(2, -1, 2, 1, '#3a7a3e'); R(-1, -3, 2, 1, '#e0e8a0');
  } else if (k === 'otter') {
    R(-5, -3, 8, 3, '#7a5230'); R(2, -5, 4, 4, '#8b6038'); R(5, -3, 2, 2, '#d8c3a0'); R(3, -4, 1, 1, MG_INK);
    R(-8, -2, 3, 1, '#5e3e22'); R(-4, 0, 1, 1, '#5e3e22'); R(0, 0, 1, 1, '#5e3e22');
  } else if (k === 'owl') {
    R(-3, -8, 6, 8, '#a8793e'); R(-3, -9, 1, 2, '#7a5230'); R(2, -9, 1, 2, '#7a5230');
    R(-2, -6, 2, 2, '#f2c14e'); R(0, -6, 2, 2, '#f2c14e'); R(-1, -5, 1, 1, MG_INK); R(1, -5, 1, 1, MG_INK);
    R(-1, -4, 2, 1, '#e07a2f'); R(-2, -3, 4, 3, '#d8b890');
  } else if (k === 'duck') {
    R(-4, -3, 7, 3, '#e6e6e6'); R(1, -6, 3, 3, '#2b7a4a'); R(4, -5, 2, 1, '#f2c14e'); R(2, -5, 1, 1, MG_INK);
  } else if (k === 'pigeon') {
    R(-3, -3, 6, 3, '#8a8fa0'); R(1, -5, 3, 3, '#6a6f80'); R(4, -4, 1, 1, '#e0b13e'); R(3, -4, 1, 1, '#e0505a');
    R(-1, 0, 1, 1, '#e0b13e'); R(1, 0, 1, 1, '#e0b13e');
  } else {
    R(-4, -2, 7, 2, '#8a7a6e'); R(2, -4, 3, 3, '#9a8a7e'); R(3, -5, 1, 1, '#d8a0a0'); R(-8, -1, 4, 1, '#c9a0a0'); R(4, -3, 1, 1, MG_INK);
  }
}

// =====================================================================
// [업무 1] 대기오염물질 배출허용기준 판정 (계측기 바늘 vs 기준선)
// =====================================================================
function openEmissionInspectionGame() {
  if (!activeTasks.seedingReady) {
    showDialogue('나', '오늘의 배출시설 현장 점검은 이미 마쳤어. 내일 다시 점검해 보자.');
    return;
  }
  const NEED = 5;
  const GASES = [['NOx', 100], ['SOx', 80], ['PM2.5', 35], ['먼지', 60], ['CO', 120], ['NH₃', 50]];
  let ok = 0, lives = 3, combo = 0, running = true, lock = false, over = false;
  let reading = null, left = 7, needle = 0, flashT = 0, flashGood = true, flashTxt = '';

  openModal(`
    <div class="modal-header"><span class="modal-title" id="em-title">📟 배출허용기준 판정 (0/${NEED})</span><button class="close-btn" onclick="closeModal()">닫기</button></div>
    <p style="line-height:1.65; color:#d9d1bd; margin-bottom:10px;">
      굴뚝 계측기의 <strong>측정값이 붉은 기준선을 넘었는지</strong> 판단하세요. 기준 초과면 <strong>개선 조치</strong>, 이내면 <strong>적합</strong>! ${NEED}번 맞히면 점검 완료 (하트 3개) <span style="color:#a89f88;">※ 모의 수치입니다</span>
    </p>
    <canvas id="emCanvas" class="mg" width="700" height="280"></canvas>
    <div style="display:flex; gap:14px; justify-content:center; margin-top:16px;">
      <button class="action-btn btn-yes" id="em-ok">✅ 기준 이내 · 적합 (←)</button>
      <button class="action-btn btn-no" id="em-bad">🚨 기준 초과 · 개선 조치 (→)</button>
    </div>
    <p id="em-status" style="min-height:24px; color:#ffd166; font-weight:700; margin-top:12px; text-align:center;">바늘이 붉은 구간에 들어갔는지 확인하세요!</p>
  `);

  const cv = document.getElementById('emCanvas'), cx = cv.getContext('2d'), W = cv.width, H = cv.height;
  const GCX = 470, GCY = 250, GR = 150;

  const bg = document.createElement('canvas'); bg.width = W; bg.height = H;
  const b = bg.getContext('2d');
  mgSky(b, W, 220, { x: 205, y: 40, r: 18 });
  mgSkyline(b, W, 232, 5, '#1b2358', '#f3c76a', 0.7);
  mgR(b, 0, 232, W, H - 232, '#141a3a'); mgR(b, 0, 232, W, 3, '#3a456e');
  mgR(b, 14, 176, 150, 60, MG_INK); mgR(b, 16, 178, 146, 56, '#3a3f58');
  for (let wx = 24; wx < 150; wx += 18) { mgR(b, wx, 190, 10, 8, '#f3c76a'); mgR(b, wx, 208, 10, 8, '#6f80a6'); }
  mgR(b, 60, 86, 30, 96, MG_INK); mgR(b, 62, 88, 26, 92, '#4a4f6a');
  [96, 118, 140].forEach((yy, i) => mgR(b, 62, yy, 26, 10, i % 2 ? '#e8e2d0' : '#c0392b'));
  mgR(b, 62, 88, 3, 92, '#6a708c');
  mgR(b, 236, 62, 458, 210, MG_INK); mgR(b, 240, 66, 450, 202, '#101847');
  mgR(b, 240, 66, 450, 4, '#26357f');

  function newReading() {
    const gs = GASES[Math.floor(Math.random() * GASES.length)];
    const exceed = Math.random() < 0.5, hard = ok >= 3;
    const ratio = exceed ? (hard ? 1.04 + Math.random() * 0.16 : 1.12 + Math.random() * 0.45) : (hard ? 0.78 + Math.random() * 0.18 : 0.45 + Math.random() * 0.4);
    reading = { gas: gs[0], limit: gs[1], value: Math.round(gs[1] * ratio), exceed };
    left = 7; lock = false; needle = 0;
  }
  function updTitle() { const t = document.getElementById('em-title'); if (t) t.innerText = `📟 배출허용기준 판정 (${ok}/${NEED})`; }
  function setStatus(s) { const e = document.getElementById('em-status'); if (e) e.innerText = s; }

  function finish() {
    running = false;
    activeTasks.seedingReady = false;
    assessmentQuality += 1.5;
    pollutionRisk = Math.max(5, pollutionRisk - 2.5);
    recordDailyTask('배출허용기준 판정 점검 완료', `측정값과 기준을 비교해 ${NEED}건을 정확히 판정하고, 기준 초과 사업장에 개선 조치를 기록했습니다.`);
    closeModal();
    updateWeatherHUD();
    showDialogue('나 · 배출기준 판정 완료', '측정값을 기준과 정확히 비교해 판정했어! 기준 초과 사업장에는 개선 조치를 내렸고, 대기오염 관리 실적이 올랐어.');
  }

  function answer(guess) {
    if (lock || over || !running || !reading) return;
    lock = true;
    const good = (guess === reading.exceed);
    if (good) { ok++; combo++; flashTxt = combo >= 2 ? `정답! COMBO x${combo}` : '정답!'; }
    else { lives--; combo = 0; flashTxt = guess === null ? '시간 초과!' : '오답!'; }
    flashGood = good; flashT = 0.9;
    setStatus(`${reading.gas} 측정값 ${reading.value} / 기준 ${reading.limit} → ${reading.exceed ? '기준 초과 (개선 조치 대상)' : '기준 이내 (적합)'}`);
    updTitle();
    setTimeout(() => {
      if (!running) return;
      if (ok >= NEED) finish();
      else if (lives <= 0) { over = true; setStatus('하트를 모두 잃었어요. 화면을 클릭해 다시 점검하세요!'); }
      else newReading();
    }, 900);
  }

  document.getElementById('em-ok').onclick = () => answer(false);
  document.getElementById('em-bad').onclick = () => answer(true);
  cv.onclick = () => { if (over) { over = false; ok = 0; lives = 3; combo = 0; updTitle(); setStatus('다시 시작! 바늘이 붉은 구간에 들어갔는지 확인하세요.'); newReading(); } };
  const onKey = (e) => {
    if (e.key === 'ArrowLeft') answer(false);
    else if (e.key === 'ArrowRight') answer(true);
  };
  window.addEventListener('keydown', onKey);

  newReading();
  let prevT = performance.now();
  function frame(now) {
    if (!running) return;
    const dt = Math.min(0.05, (now - prevT) / 1000); prevT = now;
    const T = now / 1000;
    if (!lock && !over && reading) { left -= dt; if (left <= 0) answer(null); }
    cx.drawImage(bg, 0, 0);

    // 굴뚝 연기: 기준 초과 사업장이면 검은 연기
    for (let k = 0; k < 7; k++) {
      const prog = (T * 0.4 + k / 7) % 1;
      const px = 76 + prog * 44 + Math.sin(k * 2) * 4, py = 86 - prog * 70, sz = 8 + prog * 18;
      cx.globalAlpha = (1 - prog) * 0.75;
      mgR(cx, px - sz / 2, py - sz / 2, sz, sz, (reading && reading.exceed) ? '#3a3640' : '#aab0c4');
    }
    cx.globalAlpha = 1;

    if (reading) {
      const maxV = reading.limit * 1.8;
      const ang = (v) => Math.PI - Math.min(v, maxV) / maxV * Math.PI;
      const limA = ang(reading.limit);
      for (let d = 0; d <= 180; d += 2) {
        const a = Math.PI * d / 180;
        for (let rr = GR - 16; rr <= GR; rr += 5) {
          mgR(cx, GCX + Math.cos(a) * rr - 2, GCY - Math.sin(a) * rr - 2, 5, 5, a > limA ? '#52b788' : '#e0505a');
        }
      }
      // 기준선
      for (let rr = 40; rr <= GR + 12; rr += 5) mgR(cx, GCX + Math.cos(limA) * rr - 3, GCY - Math.sin(limA) * rr - 3, 6, 6, '#ffffff');
      cx.fillStyle = '#ffe9a8'; cx.font = '700 13px "Noto Sans KR", sans-serif'; cx.textAlign = 'center';
      cx.fillText(`기준 ${reading.limit}`, GCX + Math.cos(limA) * (GR + 34), GCY - Math.sin(limA) * (GR + 24));
      cx.fillStyle = '#9ab0e8'; cx.fillText('0', GCX - GR + 8, GCY + 18);
      // 바늘
      needle += (reading.value - needle) * Math.min(1, dt * 5);
      const nv = needle + Math.sin(T * 18) * maxV * 0.006;
      const na = ang(nv);
      for (let i = 0; i < GR - 22; i += 4) mgR(cx, GCX + Math.cos(na) * i - 3, GCY - Math.sin(na) * i - 3, 6, 6, '#ffd166');
      mgDisc(cx, GCX, GCY, 12, '#f2c14e', 4);
      // 정보창
      cx.fillStyle = '#f4f1e6'; cx.font = '800 19px "Noto Sans KR", sans-serif'; cx.textAlign = 'center';
      cx.fillText(`${reading.gas}  측정값 ${reading.value}  /  기준 ${reading.limit}`, 465, 96);
      mgR(cx, 262, 108, 406, 10, MG_INK);
      mgR(cx, 264, 110, 402 * Math.max(0, left / 7), 6, left < 2 ? '#e0505a' : '#f2c14e');
    }
    for (let i = 0; i < 3; i++) mgHeart(cx, 252 + i * 28, 132, 4, i < lives);
    cx.fillStyle = '#9ab0e8'; cx.font = '700 13px "Noto Sans KR", sans-serif'; cx.textAlign = 'right';
    cx.fillText(`조치 ${ok}/${NEED}`, 676, 30);
    if (flashT > 0) {
      flashT -= dt;
      cx.fillStyle = flashGood ? '#7bf0b0' : '#ff7b7b'; cx.font = '800 34px "Noto Sans KR", sans-serif'; cx.textAlign = 'center';
      cx.fillText(flashTxt, 465, 190);
    }
    if (over) {
      cx.fillStyle = 'rgba(5,8,28,0.78)'; cx.fillRect(0, 0, W, H);
      cx.fillStyle = '#ffd166'; cx.font = '800 26px "Noto Sans KR", sans-serif'; cx.textAlign = 'center';
      cx.fillText('점검 실패! 클릭해서 다시 도전', W / 2, H / 2);
    }
    requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);

  activeMinigameCleanup = () => { running = false; window.removeEventListener('keydown', onKey); };
}

// =====================================================================
// [업무 2] 보문산 자락 사면·완충대 현장 조사 (점프킹 풍 드래그 점프)
// =====================================================================
function openDragClimbMinigame() {
  const idx = Math.min(2, Math.floor((day - 1) / 5));
  const f = FACTORIES[idx];

  openModal(`
    <div class="modal-header">
      <span class="modal-title">⛰️ 사면·완충대 현장 조사 · ${f.facility}</span>
      <button class="close-btn" onclick="closeModal()">닫기</button>
    </div>
    <p style="line-height:1.65; color:#d9d1bd; margin-bottom:10px;">
      조사원을 <strong>뒤로 당겼다 놓아</strong> 점프하세요! 당긴 길이는 <strong>세기</strong>, 반대 방향은 <strong>각도</strong>가 됩니다. 가는 길의 <strong>⭐ 조사 지점 3곳</strong>에서 표본을 채취하고 꼭대기 관측 지점에 도달하세요.
    </p>
    <div style="display:flex; justify-content:space-between; background:#0d1438; padding:8px 14px; border:2px solid #4b63c9; margin-bottom:10px; font-size:0.9rem;">
      <span>도달 고도: <strong id="drag-climb-pct" style="color:#ffd166;">0%</strong></span>
      <span>표본 채취: <strong id="drag-climb-sample" style="color:#6ad0c8;">0/3</strong></span>
      <span>상태: <strong id="drag-climb-status" style="color:#a8e6cf;">현장 조사 중</strong></span>
    </div>
    <canvas id="dragClimbCanvas" class="mg" width="700" height="360" style="cursor:grab;"></canvas>
    <div style="text-align:right; margin-top:14px;">
      <button class="action-btn btn-no" id="drag-reset-btn">출발 지점 복귀</button>
    </div>
  `);

  const c = document.getElementById('dragClimbCanvas');
  const dctx = c.getContext('2d');
  const W = c.width, H = c.height;

  const platforms = [
    { x: 0, y: H - 26, w: W, h: 26, type: 'ground' },
    { x: 85, y: H - 82, w: 150, h: 14, type: 'plat' },
    { x: 300, y: H - 134, w: 145, h: 14, type: 'plat' },
    { x: 495, y: H - 188, w: 145, h: 14, type: 'plat' },
    { x: 265, y: H - 242, w: 155, h: 14, type: 'plat' },
    { x: 75, y: H - 294, w: 140, h: 14, type: 'plat' },
    { x: 450, y: H - 332, w: 185, h: 16, type: 'goal' }
  ];
  const samples = [
    { x: 160, y: H - 100, got: false },
    { x: 567, y: H - 206, got: false },
    { x: 342, y: H - 260, got: false }
  ];

  // 정적 배경: 달빛이 드는 돌탑 내부 + 이끼 낀 돌 발판
  const bg = document.createElement('canvas'); bg.width = W; bg.height = H;
  const b = bg.getContext('2d');
  for (let y = 0; y < H; y += 8) { b.fillStyle = colorAt(SKY_STOPS.night, y / H); b.fillRect(0, y, W, 8); }
  for (let y = 0; y < H; y += 14) {
    const off = ((y / 14) | 0) % 2 ? 18 : 0;
    b.fillStyle = 'rgba(6,8,30,0.5)'; b.fillRect(0, y, W, 2);
    for (let x = -off; x < W; x += 36) b.fillRect(x, y, 2, 14);
  }
  mgR(b, 548, 20, 120, 112, MG_INK); mgR(b, 552, 24, 112, 104, '#16225a');
  mgDisc(b, 608, 76, 28, '#f6f0cf', 2); mgDisc(b, 598, 68, 6, '#dcd5ab', 2);
  mgR(b, 606, 24, 4, 104, MG_INK); mgR(b, 552, 74, 112, 4, MG_INK);
  const rw = makeRng(3);
  [[0, 14], [W - 14, 14]].forEach(([x0, ww]) => {
    mgR(b, x0, 0, ww, H, '#2a2942');
    for (let y = 0; y < H; y += 14) mgR(b, x0, y, ww, 2, '#14132a');
    for (let i = 0; i < 40; i++) mgR(b, x0 + Math.floor(rw() * ww), Math.floor(rw() * H), 3, 2, rw() < 0.5 ? '#3f7a4a' : '#4a4965');
  });
  platforms.forEach(p => {
    const goal = p.type === 'goal', gr = p.type === 'ground';
    mgR(b, p.x, p.y, p.w, p.h, MG_INK);
    mgR(b, p.x + 2, p.y + 2, p.w - 4, p.h - 4, goal ? '#7a6a3a' : '#5d6080');
    for (let x = p.x + 10; x < p.x + p.w - 2; x += 14) mgR(b, x, p.y + 2, 2, p.h - 4, 'rgba(10,13,36,.45)');
    mgR(b, p.x + 2, p.y + 2, p.w - 4, 4, goal ? '#e9c46a' : (gr ? '#5a8f4e' : '#58a05a'));
    for (let x = p.x + 4; x < p.x + p.w - 4; x += 8) mgR(b, x, p.y + 6, 3, 2, goal ? '#e9c46a' : '#3f7a4a');
  });
  const goal = platforms[platforms.length - 1];
  mgR(b, goal.x + goal.w - 34, goal.y - 26, 4, 26, '#c9ccd8');
  mgR(b, goal.x + goal.w - 30, goal.y - 26, 20, 12, '#2d6a4f');
  mgR(b, goal.x + goal.w - 24, goal.y - 22, 8, 4, '#95d5b2');

  const player = { x: 120, y: H - 52, w: 22, h: 26, vx: 0, vy: 0, grounded: true, dir: 1 };
  let dragging = false, dragStart = { x: 0, y: 0 }, dragCurr = { x: 0, y: 0 };
  let maxPct = 0, cleared = false, running = true, sampleCount = 0;
  const trail = [];
  const GRAVITY = 1150, MAX_DRAG = 160;

  function computeLaunchVelocity() {
    const pullX = dragStart.x - dragCurr.x, pullY = dragStart.y - dragCurr.y;
    const rawDist = Math.hypot(pullX, pullY);
    if (rawDist < 8) return null;
    const ratio = Math.min(MAX_DRAG, rawDist) / MAX_DRAG;
    const nx = pullX / rawDist, ny = pullY / rawDist;
    const speed = 140 + ratio * 520;
    let vx = nx * speed, vy = ny * speed;
    if (vy > -110 && ratio > 0.25) vy = -110 - ratio * 260;
    return { vx, vy, powerPct: Math.round(ratio * 100) };
  }

  c.onpointerdown = (evt) => {
    if (!running || !player.grounded) return;
    dragging = true;
    dragStart = { x: player.x + player.w / 2, y: player.y + player.h / 2 };
    dragCurr = mgPt(evt, c);
    c.style.cursor = 'grabbing';
  };
  const onDragMove = (evt) => { if (dragging) dragCurr = mgPt(evt, c); };
  const onDragRelease = () => {
    if (!dragging) return;
    dragging = false;
    c.style.cursor = 'grab';
    if (!player.grounded) return;
    const vel = computeLaunchVelocity();
    if (!vel) return;
    player.vx = vel.vx; player.vy = vel.vy; player.grounded = false;
    if (Math.abs(vel.vx) > 20) player.dir = vel.vx > 0 ? 1 : -1;
  };
  window.addEventListener('pointermove', onDragMove);
  window.addEventListener('pointerup', onDragRelease);

  document.getElementById('drag-reset-btn').onclick = () => {
    player.x = 120; player.y = H - 52; player.vx = 0; player.vy = 0; player.grounded = true; dragging = false; trail.length = 0;
  };

  let prevT = performance.now();
  function loop(now) {
    if (!running) return;
    const dt = Math.min(0.033, (now - prevT) / 1000);
    prevT = now;

    if (!player.grounded) player.vy += GRAVITY * dt;
    const prevBottom = player.y + player.h;
    player.x += player.vx * dt;
    player.y += player.vy * dt;
    if (player.x < 14) { player.x = 14; player.vx = Math.abs(player.vx) * 0.5; }
    if (player.x + player.w > W - 14) { player.x = W - 14 - player.w; player.vx = -Math.abs(player.vx) * 0.5; }
    if (player.y < 0) { player.y = 0; player.vy = 0; }

    let landed = false;
    if (player.vy >= 0) {
      for (const p of platforms) {
        const overlapX = (player.x + player.w - 2) > p.x && (player.x + 2) < (p.x + p.w);
        if (overlapX && prevBottom <= p.y + 12 && (player.y + player.h) >= p.y) {
          player.y = p.y - player.h; player.vy = 0; player.vx = 0; player.grounded = true; landed = true;
          if (p.type === 'goal' && !cleared) {
            cleared = true;
            dragClimbCompleted[idx] = true;
            assessmentQuality += 2 + (sampleCount >= 3 ? 0.5 : 0);
            pollutionRisk = Math.max(5, pollutionRisk - 3);
            weather.ecoHealth = Math.min(100, weather.ecoHealth + 5);
            recordDailyTask('현장 사면·완충대 조사 완료', `${f.facility} 주변 상부 완충녹지 관측 지점에 도달해 표본 ${sampleCount}/3곳을 채취했습니다.`);
            updateWeatherHUD();
            const stEl = document.getElementById('drag-climb-status');
            if (stEl) stEl.innerText = sampleCount >= 3 ? '관측 지점 도달! 표본 완비 (+2.5 평가품질)' : '관측 지점 도달! (+2 평가품질)';
          }
          break;
        }
      }
    }
    if (!landed) player.grounded = false;
    if (!player.grounded) { trail.push({ x: player.x + 11, y: player.y + 13 }); if (trail.length > 9) trail.shift(); }
    else if (trail.length) trail.shift();

    samples.forEach(s => {
      if (!s.got && Math.hypot(player.x + 11 - s.x, player.y + 13 - s.y) < 22) {
        s.got = true; sampleCount++;
        const el = document.getElementById('drag-climb-sample'); if (el) el.innerText = `${sampleCount}/3`;
      }
    });

    const pct = Math.max(0, Math.min(100, Math.round(((H - 26 - (player.y + player.h)) / (H - 358)) * 100)));
    if (pct > maxPct) maxPct = pct;
    const pctEl = document.getElementById('drag-climb-pct');
    if (pctEl) pctEl.innerText = `${pct}% (최고 ${maxPct}%)`;

    dctx.drawImage(bg, 0, 0);
    const blink = Math.floor(now / 350) % 2 === 0;
    samples.forEach(s => {
      if (s.got) { mgR(dctx, s.x - 4, s.y - 4, 8, 8, '#2d6a4f'); mgR(dctx, s.x - 2, s.y - 2, 4, 4, '#95d5b2'); return; }
      const k = blink ? 1 : 0;
      mgR(dctx, s.x - 2, s.y - 10 - k, 4, 20 + 2 * k, '#f2c14e');
      mgR(dctx, s.x - 10 - k, s.y - 2, 20 + 2 * k, 4, '#f2c14e');
      mgR(dctx, s.x - 4, s.y - 4, 8, 8, '#fff4c0');
    });
    trail.forEach((t, i) => { dctx.globalAlpha = (i + 1) / trail.length * 0.45; mgR(dctx, t.x - 3, t.y - 3, 6, 6, '#f2c14e'); });
    dctx.globalAlpha = 1;

    if (dragging && player.grounded) {
      const cx0 = player.x + player.w / 2, cy0 = player.y + player.h / 2;
      const vel = computeLaunchVelocity();
      if (vel) {
        for (let i = 1; i <= 10; i++) {
          const tS = i * 0.065;
          mgR(dctx, cx0 + vel.vx * tS - 2, cy0 + vel.vy * tS + 0.5 * GRAVITY * tS * tS - 2, 4, 4, '#6ad0c8');
        }
        for (let i = 1; i <= 6; i++) mgR(dctx, cx0 + (dragCurr.x - cx0) * i / 6 - 2, cy0 + (dragCurr.y - cy0) * i / 6 - 2, 4, 4, '#ffd166');
        dctx.fillStyle = '#ffe9a8'; dctx.font = '700 12px "Noto Sans KR", sans-serif'; dctx.textAlign = 'left';
        dctx.fillText(`출력 ${vel.powerPct}%`, cx0 + 12, cy0 - 14);
      }
    }

    // 조사원 (안전모 + 형광 조끼)
    const crouch = dragging && player.grounded;
    const px = Math.round(player.x), py = Math.round(player.y) + (crouch ? 4 : 0);
    const S = (gx, gy, w, h, col) => mgR(dctx, px + gx * 2, py + gy * 2, w * 2, h * 2, col);
    mgR(dctx, px - 2, py - 2, 26, crouch ? 26 : 30, MG_INK);
    S(1, 0, 9, 3, '#f2c14e'); S(0, 2, 11, 1, '#c99a2e');
    S(2, 3, 7, 4, '#f1c7a0'); S(3, 4, 1, 1, MG_INK); S(7, 4, 1, 1, MG_INK);
    S(1, 7, 9, 4, '#e07a2f'); S(3, 7, 1, 4, '#f6efd8'); S(7, 7, 1, 4, '#f6efd8');
    if (!crouch) { S(2, 11, 3, 2, '#35384f'); S(6, 11, 3, 2, '#35384f'); }
    S(player.dir > 0 ? 9 : 0, 8, 2, 3, '#f1c7a0');

    requestAnimationFrame(loop);
  }
  requestAnimationFrame(loop);

  activeMinigameCleanup = () => {
    running = false;
    window.removeEventListener('pointermove', onDragMove);
    window.removeEventListener('pointerup', onDragRelease);
  };
}

// =====================================================================
// [업무 3] 환경영향평가서 초안 검토 — 잘못된 문장 찾아 '반려' 도장 찍기
// =====================================================================
const REVIEW_SETS = [
  [
    { t: '사업지 반경 3km의 대기질을 계절별로 나누어 측정한 자료를 현황으로 제시함.', bad: false },
    { t: '현황조사는 맑은 날 하루 한 번만 측정한 값을 연평균으로 대표함.', bad: true, why: '하루치 측정값은 계절·기상 변화를 반영하지 못해 대표성이 부족해요.' },
    { t: '풍향·풍속 자료를 확산 모델에 입력해 주거지의 농도 증가분을 예측함.', bad: false },
    { t: '방지시설을 설치할 예정이므로 영향 예측 없이 "영향 없음"으로 결론 내림.', bad: true, why: '저감시설이 있어도 예측과 검증 없이 영향이 없다고 단정할 수는 없어요.' },
    { t: '주민 의견 수렴 결과와 반영 여부를 표로 정리함.', bad: false },
    { t: '기준 초과가 예상되는 지점은 "적합"으로 기재하고 사유는 생략함.', bad: true, why: '기준 초과 예상 지점은 사유와 저감방안을 반드시 밝혀야 해요.' }
  ],
  [
    { t: '반입 차량 동선과 소음 영향을 시간대별로 예측함.', bad: false },
    { t: '악취는 민원이 생기면 그때 조사하기로 하고 평가서에는 넣지 않음.', bad: true, why: '악취는 사전에 예측하고 저감방안을 평가서에 담아야 해요.' },
    { t: '폐수 처리 계획과 방류 수질 기준 비교표를 제시함.', bad: false },
    { t: '재활용 확대 등 대안은 비교하지 않고 단일안만 제시함.', bad: true, why: '평가에는 입지·규모·공법 대안 비교가 포함되어야 해요.' },
    { t: '배출가스 연속측정 자료를 사후 모니터링 계획에 포함함.', bad: false },
    { t: '인근 학교는 지도에서 눈에 띄지 않아 보전 대상에서 제외함.', bad: true, why: '학교 같은 민감 시설은 현장 확인을 거쳐 보호 대상에 반드시 포함해야 해요.' }
  ],
  [
    { t: '새벽 시간대 화물차 통행량을 현장에서 직접 계수해 소음 예측에 입력함.', bad: false },
    { t: '불투수면이 늘어도 빗물은 땅속으로 흡수되므로 유출 증가는 없다고 봄.', bad: true, why: '포장면이 늘면 빗물이 스며들지 못해 유출량이 늘어나요.' },
    { t: '통학로와 인접한 구간에 방음벽·완충녹지 설치안을 제시함.', bad: false },
    { t: '하천변 식생 훼손은 공사 후 풀을 심으면 되므로 영향 항목에서 삭제함.', bad: true, why: '훼손은 서식지 기능 손실과 복원 기간까지 함께 평가해야 해요.' },
    { t: '법정보호종 서식 여부를 계절별 현장조사로 확인함.', bad: false },
    { t: '저감 대책의 효과는 검증하지 않고 설치했다는 사실만 기재함.', bad: true, why: '저감 대책은 효과를 예측하고 사후 모니터링 계획까지 제시해야 해요.' }
  ]
];

function openTypingChallengeGame() {
  const idx = Math.min(2, Math.floor((day - 1) / 5));
  const set = REVIEW_SETS[idx].slice().sort(() => Math.random() - 0.5);
  const badTotal = set.filter(s => s.bad).length;
  let found = 0, timeLeft = 40, done = false;

  openModal(`
    <div class="modal-header">
      <span class="modal-title">📝 평가서 초안 검토 · ${FACTORIES[idx].facility}</span>
      <button class="close-btn" onclick="closeModal()">닫기</button>
    </div>
    <p style="line-height:1.65; color:#d9d1bd; margin-bottom:12px;">
      사업자가 제출한 평가서 초안에서 <strong>잘못된 문장 ${badTotal}개</strong>를 찾아 클릭해 <strong>반려 도장</strong>을 찍으세요. 멀쩡한 문장을 누르면 시간이 3초 줄어요!
    </p>
    <div class="dossier-box">
      <div style="display:flex; justify-content:space-between; font-weight:700;">
        <span>남은 시간: <strong id="rv-time" style="color:#b3262e;">40.0초</strong></span>
        <span>찾은 오류: <strong id="rv-found" style="color:#1b4332;">0/${badTotal}</strong></span>
      </div>
      <div class="timebar"><div id="rv-bar"></div></div>
      ${set.map((s, i) => `<div class="rv-line" data-i="${i}">${s.t}</div>`).join('')}
      <p id="rv-status" style="min-height:24px; margin-top:10px; font-weight:700; color:#5a3a1a; line-height:1.5;">문장을 읽고 이상한 부분을 찾아보세요.</p>
    </div>
  `);

  const status = (s) => { const e = document.getElementById('rv-status'); if (e) e.innerText = s; };

  function finish(success) {
    if (done) return;
    done = true;
    clearInterval(iv);
    activeTasks.phAlert = false;
    typingGameCompleted[idx] = true;
    if (success) {
      assessmentQuality += 1.5;
      pollutionRisk = Math.max(5, pollutionRisk - 2.5);
      recordDailyTask('환경영향평가서 초안 검토 완료', `초안의 오류 ${badTotal}건을 모두 찾아 보완 요구 의견을 달았습니다.`);
    } else {
      if (found > 0) assessmentQuality += 0.5;
      recordDailyTask('환경영향평가서 초안 검토', `시간 안에 오류 ${found}/${badTotal}건을 찾아 보완을 요구했습니다.`);
    }
    closeModal();
    updateWeatherHUD();
    updateAlertStrip();
    showDialogue(success ? '나 · 초안 검토 완료' : '나 · 초안 검토 종료',
      success ? '잘못된 문장을 전부 찾아냈어! 보완 요구 의견을 달아 평가서의 신뢰도가 올라갔어.' : `오류를 ${found}/${badTotal}건 찾았어. 놓친 부분은 보완 협의에서 다시 확인해야 해.`);
  }

  document.querySelectorAll('.rv-line').forEach(el => {
    el.onclick = () => {
      if (done || el.classList.contains('hit')) return;
      const s = set[+el.dataset.i];
      if (s.bad) {
        el.classList.add('hit');
        found++;
        document.getElementById('rv-found').innerText = `${found}/${badTotal}`;
        status('✅ ' + s.why);
        if (found >= badTotal) finish(true);
      } else {
        timeLeft = Math.max(0, timeLeft - 3);
        el.classList.add('miss');
        setTimeout(() => el.classList.remove('miss'), 320);
        status('⚠️ 이 문장은 문제가 없어요. (시간 -3초)');
      }
    };
  });

  const iv = setInterval(() => {
    if (done) return;
    timeLeft = Math.max(0, +(timeLeft - 0.1).toFixed(1));
    const t = document.getElementById('rv-time'); if (t) t.innerText = `${timeLeft.toFixed(1)}초`;
    const bar = document.getElementById('rv-bar'); if (bar) bar.style.width = `${timeLeft / 40 * 100}%`;
    if (timeLeft <= 0) finish(false);
  }, 100);

  activeMinigameCleanup = () => { done = true; clearInterval(iv); };
}

// =====================================================================
// [업무 4] 야간 보호종 현장 조사 — 손전등 불빛으로 보호종만 기록하기
// =====================================================================
function openHabitatShieldArcadeGame() {
  const idx = Math.min(2, Math.floor((day - 1) / 5));
  if (ecologyGameCompleted[idx]) {
    showDialogue('나', '이 부지의 야간 보호종 조사는 이미 마쳤어.');
    return;
  }
  const NEED = 4;
  let found = 0, mistakes = 0, running = true, mx = 350, my = 160, msg = '', msgT = 0;

  openModal(`
    <div class="modal-header"><span class="modal-title" id="hb-title">🌙 야간 보호종 현장 조사 (0/${NEED})</span><button class="close-btn" onclick="closeModal()">닫기</button></div>
    <p style="line-height:1.65; color:#d9d1bd; margin-bottom:10px;">
      어두운 습지에서 <strong>손전등(마우스)</strong>을 비춰 <strong>법정보호종 ${NEED}마리</strong>를 찾아 클릭해 기록하세요. 오리·비둘기·쥐 같은 <strong>일반종</strong>은 기록하면 안 돼요. 동물은 잠깐 나타났다 사라져요!
    </p>
    <canvas id="habitatCanvas" class="mg" width="700" height="300" style="cursor:none;"></canvas>
    <p id="hb-status" style="min-height:24px; color:#ffd166; font-weight:700; margin-top:12px;">불빛 속에 나타난 동물을 확인하세요.</p>
  `);

  const cv = document.getElementById('habitatCanvas'), cx = cv.getContext('2d'), W = cv.width, H = cv.height;
  const LR = 78;

  const bg = document.createElement('canvas'); bg.width = W; bg.height = H;
  const b = bg.getContext('2d');
  mgSky(b, W, 170, { x: 590, y: 42, r: 22 });
  mgSkyline(b, W, 170, 21, '#141a44', '#f3c76a', 0.55);
  const rm = makeRng(5);
  for (let x = 0; x < W; x += 4) {
    const h = Math.round(34 + 22 * Math.sin(x * 0.012 + 1) + 12 * Math.sin(x * 0.04));
    mgR(b, x, 170 - h, 4, h, '#1d2560'); mgR(b, x, 170 - h, 4, 2, '#3a4a90');
  }
  mgSkyline(b, W, 176, 21, '#101640', '#f3c76a', 0.4);
  mgR(b, 0, 176, W, 44, '#1d2f66');
  for (let i = 0; i < 70; i++) mgR(b, Math.floor(rm() * W / 4) * 4, 178 + Math.floor(rm() * 40 / 4) * 4, 8, 2, '#4a66b0');
  for (let y = 178; y < 214; y += 6) mgR(b, 560 + Math.sin(y) * 6, y, 30 - (y - 178) * 0.4, 2, '#f6f0cf');
  mgR(b, 0, 220, W, 80, '#1a3a2c'); mgR(b, 0, 220, W, 3, '#2d6a4f');
  for (let i = 0; i < 90; i++) {
    const x = Math.floor(rm() * W), y = 226 + Math.floor(rm() * 68), hh = 10 + Math.floor(rm() * 14);
    mgR(b, x, y - hh, 2, hh, rm() < 0.5 ? '#2d6a4f' : '#3f7a4a');
    if (rm() < 0.15) mgR(b, x - 1, y - hh - 6, 4, 8, '#7a5230');
  }

  const ov = document.createElement('canvas'); ov.width = W; ov.height = H;
  const o = ov.getContext('2d');

  const KINDS = [
    { k: 'frog', n: '맹꽁이', prot: true }, { k: 'otter', n: '수달', prot: true },
    { k: 'owl', n: '수리부엉이', prot: true }, { k: 'frog', n: '맹꽁이', prot: true },
    { k: 'duck', n: '청둥오리', prot: false }, { k: 'pigeon', n: '집비둘기', prot: false }, { k: 'rat', n: '집쥐', prot: false }
  ];
  const place = (cr) => { cr.x = 60 + Math.random() * 580; cr.y = 150 + Math.random() * 130; };
  const cr = KINDS.map(k => {
    const c0 = { ...k, x: 0, y: 0, vis: false, t: Math.random() * 2, done: false };
    place(c0);
    return c0;
  });

  cv.onpointermove = (e) => { const p = mgPt(e, cv); mx = p.x; my = p.y; };
  cv.onpointerdown = (e) => {
    if (!running) return;
    const p = mgPt(e, cv); mx = p.x; my = p.y;
    const hit = cr.find(c0 => c0.vis && !c0.done && Math.hypot(mx - c0.x, my - (c0.y - 14)) < 28 && Math.hypot(mx - c0.x, my - c0.y) < LR);
    const st = document.getElementById('hb-status');
    if (!hit) { return; }
    if (hit.prot) {
      hit.done = true; found++;
      msg = `📸 ${hit.n} 기록! (${found}/${NEED})`; msgT = 2.5;
      const t = document.getElementById('hb-title'); if (t) t.innerText = `🌙 야간 보호종 현장 조사 (${found}/${NEED})`;
      if (st) st.innerText = `✅ 보호종 ${hit.n}을(를) 현황조사 자료로 기록했어요.`;
      if (found >= NEED) finish();
    } else {
      mistakes++;
      msg = `${hit.n}은(는) 일반종이에요. 기록 낭비!`; msgT = 2.5;
      if (st) st.innerText = `⚠️ ${hit.n}은(는) 법정보호종이 아니에요. (잘못 기록 ${mistakes}회)`;
    }
  };

  function finish() {
    running = false;
    ecologyGameCompleted[idx] = true;
    assessmentQuality += 1;
    pollutionRisk = Math.max(5, pollutionRisk - 2);
    weather.ecoHealth = Math.min(100, weather.ecoHealth + 5);
    recordDailyTask('야간 보호종 현장 조사 완료', `습지 일대에서 법정보호종 ${NEED}개체를 확인·기록했습니다. (일반종 오기록 ${mistakes}회)`);
    closeModal();
    updateWeatherHUD();
    showDialogue('나 · 보호종 조사 완료', '보호종 4개체를 모두 기록했어! 서식지 보전 대책과 공사 시기 조정의 근거 자료가 확보됐어.');
  }

  let prevT = performance.now();
  function frame(now) {
    if (!running) return;
    const dt = Math.min(0.05, (now - prevT) / 1000); prevT = now;
    cr.forEach(c0 => {
      if (c0.done) return;
      c0.t -= dt;
      if (c0.t <= 0) {
        if (c0.vis) { c0.vis = false; c0.t = 1 + Math.random() * 2; place(c0); }
        else { c0.vis = true; c0.t = 2.4 + Math.random() * 1.2; }
      }
    });
    cx.drawImage(bg, 0, 0);

    // 손전등 범위 안에서만 동물이 보임
    cx.save();
    cx.beginPath(); cx.arc(mx, my, LR, 0, Math.PI * 2); cx.clip();
    cr.forEach(c0 => {
      if (!c0.vis || c0.done) return;
      const hop = Math.abs(Math.sin(now / 220 + c0.x)) * 4;
      mgCreature(cx, c0.k, c0.x, c0.y - hop, 4);
    });
    cx.restore();

    // 어둠 덮개 (손전등 구멍)
    o.globalCompositeOperation = 'source-over';
    o.clearRect(0, 0, W, H);
    o.fillStyle = 'rgba(3,5,22,0.9)'; o.fillRect(0, 0, W, H);
    o.globalCompositeOperation = 'destination-out';
    const gr = o.createRadialGradient(mx, my, LR * 0.35, mx, my, LR);
    gr.addColorStop(0, 'rgba(0,0,0,1)'); gr.addColorStop(1, 'rgba(0,0,0,0)');
    o.fillStyle = gr; o.beginPath(); o.arc(mx, my, LR, 0, Math.PI * 2); o.fill();
    cx.drawImage(ov, 0, 0);

    // 조준점
    mgR(cx, mx - 1, my - 8, 2, 6, '#ffd166'); mgR(cx, mx - 1, my + 3, 2, 6, '#ffd166');
    mgR(cx, mx - 8, my - 1, 6, 2, '#ffd166'); mgR(cx, mx + 3, my - 1, 6, 2, '#ffd166');

    // HUD
    mgR(cx, 8, 8, 208, 26, 'rgba(5,8,28,0.8)');
    cx.fillStyle = '#ffe9a8'; cx.font = '800 14px "Noto Sans KR", sans-serif'; cx.textAlign = 'left';
    cx.fillText(`📸 보호종 기록 ${found}/${NEED}`, 16, 27);
    if (msgT > 0) {
      msgT -= dt;
      mgR(cx, 150, 262, 400, 28, 'rgba(5,8,28,0.85)');
      cx.fillStyle = '#f4f1e6'; cx.textAlign = 'center'; cx.fillText(msg, 350, 281);
    }
    requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);

  activeMinigameCleanup = () => { running = false; };
}

// =====================================================================
// [업무 5] 최대소음도(Lmax) 측정 — 기준을 넘는 소음 피크를 측정 창에서 포착
// =====================================================================
function openNoisePeakTimingGame() {
  const idx = Math.min(2, Math.floor((day - 1) / 5));
  if (noiseGameCompleted[idx]) {
    showDialogue('나', '이 부지의 최대소음도 측정은 이미 완료했어.');
    return;
  }
  const NEED = 3;
  let caps = 0, misses = 0, running = true, msg = '', msgT = 0;

  openModal(`
    <div class="modal-header"><span class="modal-title" id="ns-title">🔊 최대소음도(Lmax) 측정 (0/${NEED})</span><button class="close-btn" onclick="closeModal()">닫기</button></div>
    <p style="line-height:1.65; color:#d9d1bd; margin-bottom:10px;">
      화물차가 지나갈 때마다 소음 파형에 피크가 생겨요. <strong>붉은 기준선(예시 65dB)을 넘는 피크</strong>가 <strong>노란 측정 창</strong>에 들어왔을 때 <strong>[측정!]</strong> (또는 Space)을 눌러 ${NEED}번 기록하세요. 기준 이하의 피크는 평가 대상이 아니에요.
    </p>
    <canvas id="noiseCanvas" class="mg" width="700" height="250"></canvas>
    <div style="text-align:center; margin-top:16px;"><button class="action-btn btn-yes" id="ns-btn">🎯 최대소음도 측정!</button></div>
    <p id="ns-status" style="min-height:24px; color:#ffd166; font-weight:700; margin-top:12px; text-align:center;">기준선을 넘는 피크가 측정 창에 들어오면 누르세요!</p>
  `);

  const cv = document.getElementById('noiseCanvas'), cx = cv.getContext('2d'), W = cv.width;
  const BASE = 48, STD = 65, WINX = 150, SPEED = 150;
  const Y = (db) => 200 - (db - 40) * 3.5;

  const bg = document.createElement('canvas'); bg.width = W; bg.height = 250;
  const b = bg.getContext('2d');
  mgR(b, 0, 0, W, 250, '#0d163b');
  for (let x = 0; x < W; x += 35) mgR(b, x, 0, 1, 205, '#18275c');
  for (let db = 40; db <= 85; db += 5) {
    mgR(b, 0, Y(db), W, 1, '#18275c');
    b.fillStyle = '#6f80b8'; b.font = '700 11px "Noto Sans KR", sans-serif'; b.fillText(db + '', 4, Y(db) - 2);
  }
  for (let x = 0; x < W; x += 10) mgR(b, x, Y(STD), 6, 2, '#e0505a');
  b.fillStyle = '#ff9a9a'; b.font = '800 12px "Noto Sans KR", sans-serif'; b.fillText('환경기준(예시) 65dB', W - 150, Y(STD) - 4);
  mgR(b, 0, 214, W, 36, '#1a1f3c'); mgR(b, 0, 214, W, 3, '#3a456e');
  for (let x = 6; x < W; x += 36) mgR(b, x, 236, 16, 3, '#d9cda4');

  const spikes = [];
  let spawnIn = 0.6, T = 0;
  const level = (px) => {
    let db = BASE + 1.6 * Math.sin(px * 0.09 + T * 3) + 1.0 * Math.sin(px * 0.23);
    spikes.forEach(s => { const d = px - s.x; db += s.amp * Math.exp(-(d * d) / (2 * 20 * 20)); });
    return db;
  };

  function finish() {
    running = false;
    noiseGameCompleted[idx] = true;
    assessmentQuality += 1;
    pollutionRisk = Math.max(5, pollutionRisk - 2);
    recordDailyTask('최대소음도(Lmax) 측정 완료', `기준을 넘는 소음 피크 ${NEED}회를 측정해 방음 대책의 근거 자료를 확보했습니다.`);
    closeModal();
    updateWeatherHUD();
    showDialogue('나 · 소음 측정 완료', '기준을 넘는 최대소음도를 3번 측정했어! 방음벽과 운행시간 조정의 근거가 생겼어.');
  }

  function capture() {
    if (!running) return;
    const s = spikes.find(q => !q.hit && Math.abs(q.x - WINX) <= 18);
    const st = document.getElementById('ns-status');
    if (s && s.exceed) {
      s.hit = true; caps++;
      msg = `✅ ${Math.round(BASE + s.amp)}dB 기록!`; msgT = 1.5;
      if (st) st.innerText = `✅ 기준 초과 최대소음도 ${Math.round(BASE + s.amp)}dB를 포착했어요! (${caps}/${NEED})`;
      const t = document.getElementById('ns-title'); if (t) t.innerText = `🔊 최대소음도(Lmax) 측정 (${caps}/${NEED})`;
      if (caps >= NEED) finish();
    } else if (s) {
      s.hit = true; misses++;
      msg = '기준 이하 소음'; msgT = 1.5;
      if (st) st.innerText = '⚠️ 기준 이하의 소음이에요. 측정 대상이 아니에요!';
    } else {
      misses++;
      msg = '피크 없음'; msgT = 1.5;
      if (st) st.innerText = '❌ 측정 창에 피크가 없어요. 타이밍을 다시 보세요!';
    }
  }
  document.getElementById('ns-btn').onclick = capture;
  const onKey = (e) => { if (e.code === 'Space') { e.preventDefault(); capture(); } };
  window.addEventListener('keydown', onKey);

  let prevT = performance.now();
  function frame(now) {
    if (!running) return;
    const dt = Math.min(0.05, (now - prevT) / 1000); prevT = now;
    T += dt; spawnIn -= dt;
    if (spawnIn <= 0) {
      const ex = Math.random() < 0.6;
      spikes.push({ x: W + 40, amp: (ex ? 72 + Math.random() * 10 : 55 + Math.random() * 7) - BASE, exceed: ex, hit: false });
      spawnIn = 1.1 + Math.random() * 1.0;
    }
    spikes.forEach(s => { s.x -= SPEED * dt; });
    while (spikes.length && spikes[0].x < -60) spikes.shift();

    cx.drawImage(bg, 0, 0);
    // 화물차
    spikes.forEach(s => {
      const tx = Math.round(s.x) - 18;
      mgR(cx, tx, 218, 38, 16, MG_INK); mgR(cx, tx + 2, 220, 26, 11, s.hit ? '#6a708c' : '#c8ccd8');
      mgR(cx, tx + 28, 224, 8, 8, '#e0505a'); mgR(cx, tx + 5, 232, 6, 4, MG_INK); mgR(cx, tx + 26, 232, 6, 4, MG_INK);
    });
    // 소음 파형
    for (let px = 0; px < W; px += 3) {
      const db = level(px), y = Y(db);
      cx.globalAlpha = 0.14; mgR(cx, px, y + 3, 3, 203 - y, db > STD ? '#ff6b6b' : '#6ad0c8');
      cx.globalAlpha = 1; mgR(cx, px, y, 3, 3, db > STD ? '#ff6b6b' : '#6ad0c8');
    }
    // 측정 창
    cx.globalAlpha = 0.18; mgR(cx, WINX - 18, 0, 36, 205, '#ffd166'); cx.globalAlpha = 1;
    mgR(cx, WINX - 18, 0, 2, 205, '#ffd166'); mgR(cx, WINX + 16, 0, 2, 205, '#ffd166');
    // 현재 레벨 표시
    mgR(cx, W - 140, 8, 130, 28, MG_INK);
    cx.fillStyle = '#7bf0b0'; cx.font = '800 15px "Noto Sans KR", sans-serif'; cx.textAlign = 'center';
    cx.fillText(`현재 ${level(WINX).toFixed(1)} dB`, W - 75, 28);
    cx.textAlign = 'left'; cx.fillStyle = '#ffe9a8'; cx.font = '800 12px "Noto Sans KR", sans-serif';
    cx.fillText('측정 창', WINX - 18, 16);
    if (msgT > 0) {
      msgT -= dt;
      cx.fillStyle = '#ffd166'; cx.font = '800 22px "Noto Sans KR", sans-serif'; cx.textAlign = 'center';
      cx.fillText(msg, 350, 60);
    }
    requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);

  activeMinigameCleanup = () => { running = false; window.removeEventListener('keydown', onKey); };
}

// =====================================================================
// [업무 6] 완충·저감시설 배치 — 문제 유형에 맞는 시설을 알맞은 구역에
// =====================================================================
function openMitigationPlacementGame() {
  const idx = Math.min(2, Math.floor((day - 1) / 5));
  if (mitigationGameCompleted[idx]) {
    showDialogue('나', '이 부지의 완충·저감시설 배치는 이미 마쳤어.');
    return;
  }
  const tools = [
    { id: 'buffer', label: '🌳 완충녹지' },
    { id: 'rain', label: '💧 투수·저류시설' },
    { id: 'wall', label: '🧱 방음벽' }
  ];
  const slots = [
    { name: '주거지 경계', issue: '단지로 먼지와 소음이 들어와요', kind: 'home', hz: ['dust', 'noise'], ok: ['buffer', 'wall'] },
    { name: '하천 수변부', issue: '호우 때 오염된 물이 하천으로 흘러요', kind: 'river', hz: ['rain'], ok: ['rain', 'buffer'] },
    { name: '학교 통학로 옆', issue: '새벽 화물차 소음이 등굣길에 전달돼요', kind: 'school', hz: ['noise'], ok: ['wall'] },
    { name: '도로변 완충대', issue: '차량 먼지와 소음이 도로변으로 퍼져요', kind: 'road', hz: ['dust', 'noise'], ok: ['buffer', 'wall'] }
  ];
  const why = {
    rain: '투수·저류시설은 빗물 유출을 줄이는 시설이에요. 먼지·소음 문제에는 맞지 않아요.',
    wall: '방음벽은 소음을 막는 시설이에요. 빗물·오염수 문제에는 투수·저류시설이나 수변 완충녹지가 맞아요.',
    buffer: '완충녹지는 먼지에는 좋지만 학교 앞 소음을 직접 막기엔 부족해요. 방음벽이 필요해요.'
  };
  let sel = 'buffer', placed = [null, null, null, null], badFlash = [0, 0, 0, 0], running = true;
  const MAXP = 3;

  openModal(`
    <div class="modal-header"><span class="modal-title" id="mt-title">🧱 완충·저감시설 배치 (0/${MAXP} 설치)</span><button class="close-btn" onclick="closeModal()">닫기</button></div>
    <p style="line-height:1.65; color:#d9d1bd; margin-bottom:12px;">
      아래 <strong>저감 시설</strong>을 고른 뒤, 각 구역의 <strong>문제 유형</strong>에 맞는 곳 <strong>${MAXP}곳</strong>에 설치하세요. 설치한 곳을 다시 클릭하면 철거돼요.
    </p>
    <div id="mt-tools" style="display:flex; gap:8px; margin-bottom:12px; flex-wrap:wrap;"></div>
    <canvas id="mtCanvas" class="mg" width="700" height="250"></canvas>
    <p id="place-fb" style="color:#ffd166; min-height:24px; margin-top:12px; font-weight:700; line-height:1.5;"></p>
    <div style="text-align:center; margin-top:10px;"><button class="action-btn btn-yes" id="place-confirm-btn">배치안 적용</button></div>
  `);

  const renderTools = () => {
    document.getElementById('mt-tools').innerHTML = tools.map(t => `<button class="action-btn ${sel === t.id ? 'btn-yes' : 'btn-no'}" onclick="pickPlaceTool('${t.id}')">${t.label}</button>`).join('');
  };
  window.pickPlaceTool = (tid) => { sel = tid; renderTools(); };
  renderTools();

  const cv = document.getElementById('mtCanvas'), cx = cv.getContext('2d');
  const PW = 164, PX = (i) => 10 + i * 172;
  const fb = (s) => { const e = document.getElementById('place-fb'); if (e) e.innerText = s; };
  const count = () => placed.filter(Boolean).length;
  const setTitle = () => { const t = document.getElementById('mt-title'); if (t) t.innerText = `🧱 완충·저감시설 배치 (${count()}/${MAXP} 설치)`; };

  cv.onpointerdown = (e) => {
    const p = mgPt(e, cv);
    const i = Math.floor((p.x - 6) / 172);
    if (i < 0 || i > 3) return;
    if (placed[i]) placed[i] = null;
    else if (count() < MAXP) placed[i] = sel;
    badFlash[i] = 0;
    setTitle(); fb('');
  };

  document.getElementById('place-confirm-btn').onclick = () => {
    if (count() < MAXP) { fb(`저감시설 ${MAXP}곳을 모두 배치해야 합니다.`); return; }
    let firstWrong = null;
    placed.forEach((t, i) => { if (t && !slots[i].ok.includes(t)) { badFlash[i] = 1.2; if (firstWrong === null) firstWrong = i; } });
    if (firstWrong !== null) {
      fb(`❌ '${slots[firstWrong].name}'에는 맞지 않는 시설이에요. ${why[placed[firstWrong]]}`);
      return;
    }
    running = false;
    mitigationGameCompleted[idx] = true;
    assessmentQuality += 1;
    pollutionRisk = Math.max(5, pollutionRisk - 3);
    weather.ecoHealth = Math.min(100, weather.ecoHealth + 4);
    const done = placed.map((t, i) => t ? `${slots[i].name}: ${tools.find(x => x.id === t).label}` : null).filter(Boolean);
    recordDailyTask('완충·저감시설 공간 배치 완료', `문제 유형에 맞춰 ${done.join(', ')} 에 저감시설을 배치했습니다.`);
    closeModal();
    updateWeatherHUD();
    showDialogue('나 · 시설 배치 완료', '구역별 문제에 딱 맞는 저감시설을 배치했어! 영향 저감 효과가 높아졌어.');
  };

  function hazard(kind, x, y, T) {
    if (kind === 'dust') {
      for (let k = 0; k < 9; k++) mgR(cx, x + ((k * 17 + T * 22) % 70), y + ((k * 11) % 26) + Math.sin(T * 2 + k) * 3, 4, 4, '#9a9aa8');
    } else if (kind === 'rain') {
      for (let k = 0; k < 9; k++) mgR(cx, x + k * 8, y + ((k * 7 + T * 50) % 34), 2, 6, '#6ab0e8');
    } else {
      cx.globalAlpha = 0.5 + 0.5 * Math.sin(T * 6);
      for (let k = 0; k < 3; k++) mgR(cx, x + 40 + k * 10, y + 6 - k * 3, 3, 10 + k * 6, '#ffd166');
      cx.globalAlpha = 1;
    }
  }
  function treeRow(x, y, n) {
    for (let k = 0; k < n; k++) {
      const tx = x + k * 34;
      mgR(cx, tx + 8, y + 12, 6, 14, '#5b3a22');
      mgR(cx, tx, y, 22, 14, MG_INK); mgR(cx, tx + 2, y + 2, 18, 10, '#2f6b3a'); mgR(cx, tx + 4, y + 2, 8, 4, '#4f9a52');
    }
  }

  let prevT = performance.now();
  function frame(now) {
    if (!running) return;
    const dt = Math.min(0.05, (now - prevT) / 1000); prevT = now;
    const T = now / 1000;
    cx.fillStyle = '#0d163b'; cx.fillRect(0, 0, 700, 250);
    slots.forEach((s, i) => {
      const x = PX(i), y = 8;
      mgR(cx, x - 2, y - 2, PW + 4, 238, badFlash[i] > 0 ? '#e0505a' : (placed[i] ? '#52b788' : MG_INK));
      mgR(cx, x, y, PW, 234, '#141a44');
      for (let k = 0; k < 8; k++) mgR(cx, x + 10 + k * 19, y + 6 + (k * 13) % 30, 2, 2, '#c9d3f5');
      mgR(cx, x, y + 138, PW, 30, '#1a3a2c');
      // 장면
      if (s.kind === 'home') {
        [[12, 76, 52, 62, '#5a6a9a'], [78, 92, 40, 46, '#6a7aaa'], [124, 80, 34, 58, '#4a5a8a']].forEach(a => {
          mgR(cx, x + a[0], y + a[1], a[2], a[3], MG_INK); mgR(cx, x + a[0] + 2, y + a[1] + 2, a[2] - 4, a[3] - 4, a[4]);
          for (let wy = y + a[1] + 8; wy < y + a[1] + a[3] - 8; wy += 12) for (let wx = x + a[0] + 6; wx < x + a[0] + a[2] - 8; wx += 12) mgR(cx, wx, wy, 5, 6, '#ffd166');
        });
      } else if (s.kind === 'river') {
        mgR(cx, x, y + 108, PW, 56, '#1d4f8a');
        for (let k = 0; k < 6; k++) mgR(cx, x + ((k * 29 + T * 14) % 150), y + 116 + (k % 3) * 14, 14, 2, '#7fb0d8');
        mgHouse(cx, x + 8, y + 78, 3, '#6a7aaa', '#a8603c');
      } else if (s.kind === 'school') {
        mgR(cx, x + 12, y + 78, 84, 60, MG_INK); mgR(cx, x + 14, y + 80, 80, 56, '#8a6a4a');
        for (let wx = x + 22; wx < x + 90; wx += 16) mgR(cx, wx, y + 90, 8, 10, '#ffd166');
        mgR(cx, x + 44, y + 112, 16, 24, '#5b3a22'); mgR(cx, x + 100, y + 54, 3, 36, '#c9ccd8'); mgR(cx, x + 103, y + 54, 14, 8, '#e0505a');
        mgPerson(cx, x + 112, y + 104, 2, { hs: 'short', shirt: '#e0b13e', pants: '#2b3a5a', bag: '#2b6cb0' });
      } else {
        mgR(cx, x, y + 128, PW, 22, '#2a2e44'); for (let k = 0; k < 6; k++) mgR(cx, x + k * 30 + 4, y + 138, 16, 2, '#d9cda4');
        const tx = x + ((T * 40) % (PW + 40)) - 30;
        mgR(cx, tx, y + 118, 40, 18, MG_INK); mgR(cx, tx + 2, y + 120, 28, 12, '#c8ccd8'); mgR(cx, tx + 30, y + 124, 8, 8, '#e0505a');
        mgR(cx, tx + 6, y + 134, 6, 4, MG_INK); mgR(cx, tx + 28, y + 134, 6, 4, MG_INK);
      }
      if (!placed[i]) s.hz.forEach((h, hi) => hazard(h, x + 10 + hi * 64, y + 22, T));
      // 설치된 시설
      const t = placed[i];
      if (t === 'buffer') treeRow(x + 14, y + 112, 4);
      else if (t === 'wall') {
        mgR(cx, x + 8, y + 104, PW - 16, 30, MG_INK); mgR(cx, x + 10, y + 106, PW - 20, 26, '#8a8fa0');
        for (let k = 0; k < 7; k++) mgR(cx, x + 14 + k * 20, y + 106, 2, 26, '#6a6f80'); mgR(cx, x + 10, y + 118, PW - 20, 2, '#6a6f80');
      } else if (t === 'rain') {
        mgR(cx, x + 14, y + 116, PW - 28, 24, MG_INK); mgR(cx, x + 16, y + 118, PW - 32, 20, '#3d7fb5');
        for (let k = 0; k < 5; k++) mgR(cx, x + 24 + k * 26, y + 108, 2, 14, '#4f9a52');
      }
      cx.fillStyle = '#ffe9a8'; cx.font = '800 14px "Noto Sans KR", sans-serif'; cx.textAlign = 'center';
      cx.fillText(s.name, x + PW / 2, y + 190);
      cx.fillStyle = '#c9d3f5'; cx.font = '600 12px "Noto Sans KR", sans-serif';
      mgWrap(cx, s.issue, PW - 16).forEach((ln, li) => cx.fillText(ln, x + PW / 2, y + 208 + li * 15));
      if (badFlash[i] > 0) badFlash[i] -= dt;
      if (placed[i]) { cx.fillStyle = '#95d5b2'; cx.font = '800 12px "Noto Sans KR", sans-serif'; cx.fillText('설치됨', x + PW / 2, y + 14); }
    });
    requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);

  activeMinigameCleanup = () => { running = false; };
}

// =====================================================================
// [업무 7] 풍향·대기확산 예측 — 바람이 '불어오는' 방향을 읽고 오염 기둥이 향할 구역 맞히기
// =====================================================================
function openWindPlumeDefenseGame() {
  const idx = Math.min(2, Math.floor((day - 1) / 5));
  if (windGameCompleted[idx]) {
    showDialogue('나', '이 부지의 대기확산 예측은 이미 마쳤어.');
    return;
  }
  const NEED = 3;
  const DIRS = ['북', '북동', '동', '남동', '남', '남서', '서', '북서'];
  let round = 0, lives = 3, running = true, lock = false, from = 0, windSpd = 2.4, hover = -1, flash = { k: -1, t: 0 }, plume = null, msg = '';

  openModal(`
    <div class="modal-header"><span class="modal-title" id="wd-title">💨 풍향·대기확산 예측 (0/${NEED})</span><button class="close-btn" onclick="closeModal()">닫기</button></div>
    <p style="line-height:1.65; color:#d9d1bd; margin-bottom:10px;">
      풍향은 바람이 <strong>불어오는 쪽</strong>의 이름이에요 (북풍 = 북쪽에서 남쪽으로). 오늘의 바람을 읽고 <strong>배출구의 오염 기둥이 흘러갈 주거 구역</strong>을 클릭하세요. ${NEED}번 맞히면 완료 (하트 3개)
    </p>
    <canvas id="windCanvas" class="mg" width="700" height="300"></canvas>
    <p id="wd-status" style="min-height:24px; color:#ffd166; font-weight:700; margin-top:12px;">바람 방향을 읽고 영향받는 구역을 고르세요!</p>
  `);

  const cv = document.getElementById('windCanvas'), cx = cv.getContext('2d'), W = cv.width, H = cv.height;
  const CX = 350, CY = 150;
  const zones = DIRS.map((n, k) => { const a = k * Math.PI / 4; return { n, x: CX + Math.sin(a) * 250, y: CY - Math.cos(a) * 108 }; });

  const bg = document.createElement('canvas'); bg.width = W; bg.height = H;
  const b = bg.getContext('2d');
  mgSky(b, W, 120, { x: 70, y: 36, r: 18 });
  mgR(b, 0, 96, W, H - 96, '#162a3a');
  for (let y = 96; y < H; y += 12) mgR(b, 0, y, W, 2, '#1d3a4a');
  for (let x = 0; x < W; x += 40) mgR(b, x, 96, 2, H - 96, '#1d3a4a');
  mgSkyline(b, W, 100, 44, '#141a44', '#f3c76a', 0.5);

  const setStatus = (s) => { const e = document.getElementById('wd-status'); if (e) e.innerText = s; };
  function newRound() {
    let nf; do { nf = Math.floor(Math.random() * 8); } while (nf === from && round > 0);
    from = nf; windSpd = +(1 + Math.random() * 5).toFixed(1); lock = false; plume = null;
  }
  newRound();

  function finish() {
    running = false;
    windGameCompleted[idx] = true;
    assessmentQuality += 1;
    pollutionRisk = Math.max(5, pollutionRisk - 2);
    recordDailyTask('풍향·대기확산 예측 완료', `풍향 자료를 읽고 오염 기둥의 이동 방향과 영향 구역을 ${NEED}회 정확히 예측했습니다.`);
    closeModal();
    updateWeatherHUD();
    showDialogue('나 · 확산 예측 완료', '풍향을 정확히 읽고 영향 구역을 예측했어! 어디에 측정망과 저감시설을 둘지 근거가 생겼어.');
  }

  cv.onpointermove = (e) => {
    const p = mgPt(e, cv);
    hover = zones.findIndex(z => Math.hypot(p.x - z.x, p.y - z.y) < 46);
  };
  cv.onpointerdown = (e) => {
    if (lock || !running) return;
    const p = mgPt(e, cv);
    const k = zones.findIndex(z => Math.hypot(p.x - z.x, p.y - z.y) < 46);
    if (k < 0) return;
    const target = (from + 4) % 8;
    if (k === target) {
      lock = true; round++;
      plume = { k, t: 0 };
      const t = document.getElementById('wd-title'); if (t) t.innerText = `💨 풍향·대기확산 예측 (${round}/${NEED})`;
      setStatus(`✅ ${DIRS[from]}풍은 ${DIRS[from]}쪽에서 불어와 ${DIRS[target]}쪽 구역으로 오염물질을 실어 가요!`);
      setTimeout(() => { if (!running) return; if (round >= NEED) finish(); else { msg = ''; newRound(); } }, 1300);
    } else {
      lives--;
      flash = { k, t: 0.8 };
      setStatus(`❌ ${DIRS[from]}풍은 ${DIRS[from]}쪽에서 불어와 반대편인 ${DIRS[target]}쪽으로 흘러가요. 다시 읽어 보세요!`);
      if (lives <= 0) { lock = true; setTimeout(() => { if (!running) return; round = 0; lives = 3; const t = document.getElementById('wd-title'); if (t) t.innerText = `💨 풍향·대기확산 예측 (0/${NEED})`; setStatus('하트를 모두 잃어 처음부터 다시 도전해요!'); newRound(); }, 1200); }
    }
  };

  let prevT = performance.now();
  function frame(now) {
    if (!running) return;
    const dt = Math.min(0.05, (now - prevT) / 1000); prevT = now;
    const T = now / 1000;
    cx.drawImage(bg, 0, 0);

    // 구역(주거지 3채 + 라벨)
    zones.forEach((z, k) => {
      const hot = hover === k && !lock;
      if (hot) mgR(cx, z.x - 44, z.y - 30, 88, 64, 'rgba(255,209,102,0.25)');
      if (flash.k === k && flash.t > 0) mgR(cx, z.x - 44, z.y - 30, 88, 64, 'rgba(224,80,90,0.45)');
      mgHouse(cx, z.x - 38, z.y - 16, 3, '#8a6a4a', '#a8603c');
      mgHouse(cx, z.x - 6, z.y - 8, 3, '#7a8ab4', '#5a6a9a');
      cx.fillStyle = hot ? '#ffe9a8' : '#c9d3f5'; cx.font = '800 13px "Noto Sans KR", sans-serif'; cx.textAlign = 'center';
      cx.fillText(z.n + ' 구역', z.x, z.y + 38);
    });
    if (flash.t > 0) flash.t -= dt;

    // 배출원(굴뚝)
    mgR(cx, CX - 34, CY - 6, 68, 44, MG_INK); mgR(cx, CX - 32, CY - 4, 64, 40, '#3a3f58');
    mgR(cx, CX - 8, CY - 44, 16, 42, MG_INK); mgR(cx, CX - 6, CY - 42, 12, 38, '#4a4f6a'); mgR(cx, CX - 6, CY - 30, 12, 6, '#c0392b'); mgR(cx, CX - 6, CY - 18, 12, 6, '#c0392b');
    for (let wx = CX - 26; wx < CX + 24; wx += 14) mgR(cx, wx, CY + 8, 8, 8, '#f3c76a');

    // 오염 기둥
    const tgt = plume ? zones[plume.k] : null;
    for (let k = 0; k < 10; k++) {
      let px, py, al;
      if (plume) {
        const prog = Math.min(1, plume.t + k * 0.03);
        px = CX + (tgt.x - CX) * prog + Math.sin(k + T * 3) * 4;
        py = CY - 40 + (tgt.y - (CY - 40)) * prog + Math.cos(k + T * 2) * 4;
        al = 0.75;
      } else {
        const prog = (T * 0.35 + k / 10) % 1;
        px = CX + Math.sin(k * 2 + T) * 6; py = CY - 46 - prog * 44; al = (1 - prog) * 0.8;
      }
      cx.globalAlpha = al; mgR(cx, px - 7, py - 7, 14, 14, '#6a625c');
    }
    cx.globalAlpha = 1;
    if (plume) plume.t = Math.min(1, plume.t + dt * 0.9);

    // 바람 정보 패널
    mgR(cx, 8, 8, 232, 56, MG_INK); mgR(cx, 10, 10, 228, 52, '#101847');
    cx.fillStyle = '#ffe9a8'; cx.font = '800 19px "Noto Sans KR", sans-serif'; cx.textAlign = 'left';
    cx.fillText(`🌬️ ${DIRS[from]}풍  ${windSpd}m/s`, 20, 34);
    cx.fillStyle = '#9ab0e8'; cx.font = '700 12px "Noto Sans KR", sans-serif';
    cx.fillText(`(${DIRS[from]}쪽에서 불어오는 바람)`, 20, 54);
    for (let i = 0; i < 3; i++) mgHeart(cx, W - 96 + i * 28, 12, 4, i < lives);

    requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);

  activeMinigameCleanup = () => { running = false; };
}

// =====================================================================
// [업무 8] 주민 민원 전화 — 마을 주민 세 명의 말풍선 중 알맞은 근거 고르기 (제한시간 + 그럴듯한 오답)
// =====================================================================
function openAuditPhoneModal() {
  const audit = (activeTasks.phoneRinging && activeTasks.currentAudit)
    ? activeTasks.currentAudit
    : AUDIT_SCENARIOS[(day + Math.floor(gameMinutes / 60)) % AUDIT_SCENARIOS.length];
  const cards = audit.speakers.slice().sort(() => Math.random() - 0.5);
  const LIMIT = 30;

  openModal(`
    <div class="modal-header">
      <span class="modal-title">☎️ ${audit.title}</span>
      <button class="close-btn" onclick="closeModal()">닫기</button>
    </div>
    <p style="line-height:1.65; color:#d9d1bd; margin-bottom:10px;">${audit.situation}<br><strong>주민이나 말풍선을 클릭</strong>해서 고르세요. <strong>${LIMIT}초</strong> 안에 판단하지 못하면 민원인이 전화를 끊어요!</p>
    <canvas id="callCanvas" class="mg" width="720" height="380"></canvas>
    <p id="call-status" style="min-height:24px; color:#ffd166; font-weight:700; margin-top:12px; text-align:center;">누구의 말이 평가에 반영할 만한 근거일까요?</p>
  `);

  const cv = document.getElementById('callCanvas'), cx = cv.getContext('2d'), W = cv.width, H = cv.height;
  const COLW = W / 3, GROUND = 318, SP_Y = 186, S = 6;
  cx.font = '700 14px "Noto Sans KR", sans-serif';
  const lay = cards.map(sp => ({ sp, lines: mgWrap(cx, sp.bubble, COLW - 52) }));
  const maxLines = Math.max(...lay.map(l => l.lines.length));
  const BH = maxLines * 19 + 24;

  // 정적 배경: 대전의 저녁 골목 + 한빛탑
  const bg = document.createElement('canvas'); bg.width = W; bg.height = H;
  const b = bg.getContext('2d');
  mgSky(b, W, 250, { x: 664, y: 40, r: 16 });
  for (let x = 0; x < W; x += 4) {
    const h = Math.round(46 + 20 * Math.sin(x * 0.011 + 2) + 10 * Math.sin(x * 0.037));
    mgR(b, x, 250 - h, 4, h, '#1d2560'); mgR(b, x, 250 - h, 4, 2, '#3a4a90');
  }
  mgHanbit(b, 640, 250, '#9aa6cc', 0.8);
  mgSkyline(b, W, 262, 14, '#141a44', '#f3c76a', 0.9);
  mgR(b, 0, 262, W, H - 262, '#1a1f3c'); mgR(b, 0, GROUND - 6, W, 5, '#3a456e'); mgR(b, 0, 262, W, 6, '#2a3270');
  for (let x = 8; x < W; x += 40) mgR(b, x, 350, 20, 3, '#d9cda4');
  [240, 480].forEach(lx => {
    mgR(b, lx - 2, 196, 4, 124, '#2a2e44'); mgR(b, lx - 12, 190, 24, 8, '#2a2e44');
    b.globalAlpha = 0.18; mgR(b, lx - 30, 198, 60, 80, '#ffd166'); b.globalAlpha = 1; mgR(b, lx - 8, 196, 16, 4, '#ffe9a8');
  });

  let hover = -1, chosen = -1, locked = false, running = true, left = LIMIT;

  const colAt = (p) => (p.y < 340 && p.x >= 0 && p.x < W) ? Math.floor(p.x / COLW) : -1;
  cv.onpointermove = (e) => { hover = locked ? hover : colAt(mgPt(e, cv)); cv.style.cursor = (hover >= 0 && !locked) ? 'pointer' : 'default'; };
  cv.onpointerdown = (e) => {
    if (locked) return;
    const i = colAt(mgPt(e, cv));
    if (i < 0) return;
    locked = true; chosen = i; hover = i;
    const sp = lay[i].sp;
    const st = document.getElementById('call-status');
    if (st) st.innerText = sp.correct ? `✔ ${sp.name}의 말을 평가 근거로 채택합니다!` : `✘ ${sp.name}의 말은 평가 근거로 부족해 보여요…`;
    setTimeout(() => { if (running) pickSpeakerBubble(sp, audit); }, 1000);
  };

  function timeout() {
    locked = true;
    const st = document.getElementById('call-status');
    if (st) st.innerText = '⏰ 시간이 다 되어 민원인이 전화를 끊었어요…';
    const fake = { name: '시간 초과', bubble: '(통화 종료)', correct: false,
      effect: () => { pollutionRisk = Math.min(100, pollutionRisk + 1.5); return '판단이 늦어져 민원인이 전화를 끊었어. 민원은 근거를 빠르게 가려내는 일이 중요해.'; } };
    setTimeout(() => { if (running) pickSpeakerBubble(fake, audit); }, 900);
  }

  let prevT = performance.now();
  function frame(now) {
    if (!running) return;
    const dt = Math.min(0.05, (now - prevT) / 1000); prevT = now;
    const T = now / 1000;
    if (!locked) { left -= dt; if (left <= 0) { left = 0; timeout(); } }
    cx.drawImage(bg, 0, 0);
    lay.forEach((l, i) => {
      const x0 = i * COLW, mid = x0 + COLW / 2;
      const isHover = hover === i && chosen < 0;
      const isChosen = chosen === i;
      const dim = chosen >= 0 && !isChosen;
      const jump = Math.sin(T * 3 + i * 1.7) > 0.7 ? -3 : 0;
      cx.globalAlpha = dim ? 0.45 : 1;
      mgR(cx, mid - 36, GROUND - 4, 72, 6, 'rgba(0,0,0,0.4)');
      mgPerson(cx, mid - 6 * S, SP_Y + jump + (isHover ? -4 : 0), S, Object.assign({}, l.sp.look, { talk: chosen < 0 && Math.floor(T * 4 + i * 3) % 3 === 0 }));
      cx.font = '800 13px "Noto Sans KR", sans-serif'; cx.textAlign = 'center';
      const nw = cx.measureText(l.sp.name).width + 22;
      mgR(cx, mid - nw / 2 - 3, GROUND + 8, nw + 6, 26, MG_INK); mgR(cx, mid - nw / 2, GROUND + 11, nw, 20, isHover || isChosen ? '#f2c14e' : '#26357f');
      cx.fillStyle = isHover || isChosen ? '#1a1030' : '#dbe6ff'; cx.fillText(l.sp.name, mid, GROUND + 26);
      let fill = '#f6efd8', line = MG_INK;
      if (isHover) { fill = '#fff8e3'; line = '#f2c14e'; }
      if (isChosen) { fill = l.sp.correct ? '#cfeedd' : '#f6d4d4'; line = l.sp.correct ? '#2d6a4f' : '#b3262e'; }
      mgBubble(cx, x0 + 14, 12 + (isHover ? -2 : 0), COLW - 28, BH, fill, line, mid);
      cx.fillStyle = '#221d17'; cx.font = '700 14px "Noto Sans KR", sans-serif'; cx.textAlign = 'left';
      l.lines.forEach((ln, li) => cx.fillText(ln, x0 + 26, 12 + (isHover ? -2 : 0) + 24 + li * 19));
      if (isChosen) {
        mgR(cx, x0 + 18, 4, 64, 20, l.sp.correct ? '#2d6a4f' : '#b3262e');
        cx.fillStyle = '#fff'; cx.font = '800 12px "Noto Sans KR", sans-serif'; cx.textAlign = 'center';
        cx.fillText(l.sp.correct ? '✔ 채택' : '✘ 부족', x0 + 50, 19);
      }
      cx.globalAlpha = 1;
    });
    // 전화기 + 남은 시간
    const ring = Math.floor(T * 6) % 2 === 0;
    mgR(cx, 14, 352, 30, 20, MG_INK); mgR(cx, 16, 354, 26, 16, '#b3262e'); mgR(cx, 20, 358, 18, 4, '#14131f'); mgR(cx, 22, 364, 4, 4, '#c9c2b0'); mgR(cx, 30, 364, 4, 4, '#c9c2b0');
    if (chosen < 0 && ring) { mgR(cx, 50, 352, 3, 8, '#ffd166'); mgR(cx, 58, 348, 3, 14, '#ffd166'); }
    mgR(cx, 90, 356, 614, 14, MG_INK);
    mgR(cx, 92, 358, 610 * (left / LIMIT), 10, left < 8 ? '#e0505a' : '#f2c14e');
    cx.fillStyle = '#ffe9a8'; cx.font = '800 12px "Noto Sans KR", sans-serif'; cx.textAlign = 'left';
    cx.fillText(`통화 가능 ${Math.ceil(left)}초`, 96, 349);
    requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);

  activeMinigameCleanup = () => { running = false; };
}

function pickSpeakerBubble(sp, audit) {
  const msg = sp.effect();
  if (sp.correct) {
    assessmentQuality += 1;
    recordDailyTask('주민 민원 근거 선택 성공', `${audit.title} — ${sp.name}: ${sp.bubble}`);
  } else if (sp.name === '시간 초과') {
    recordDailyTask('주민 민원 전화 놓침', `${audit.title} — 시간 안에 근거를 가려내지 못했습니다.`);
  } else {
    recordDailyTask('주민 민원 검토 및 재확인', `${audit.title} — ${sp.name}의 발언은 평가 근거로 부족해 다시 확인했습니다.`);
  }
  activeTasks.phoneRinging = false;
  activeTasks.currentAudit = null;
  closeModal();
  updateWeatherHUD();
  updateAlertStrip();
  showDialogue(sp.correct ? `나 · ${sp.name} 근거 채택` : `나 · ${sp.name} 발언 검토`, msg);
}

// =====================================================================
// 엔딩 — 대전의 15일 뒤 풍경 (도트 그림)
// =====================================================================
function openEndingScene(kind, title, message, summaryHtml) {
  openModal(`
    <div class="modal-header"><span class="modal-title">${title}</span></div>
    <canvas id="endCanvas" class="mg" width="720" height="400" style="cursor:default;"></canvas>
    <div style="text-align:center; padding:16px 8px 0;">
      <div style="font-size:1.05rem; line-height:1.85; color:#f0ece1; margin-bottom:14px;">${message}</div>
      ${summaryHtml}
      <button class="start-btn" onclick="location.reload()">처음부터 다시하기</button>
    </div>
  `);

  const cv = document.getElementById('endCanvas'), cx = cv.getContext('2d'), W = cv.width, H = cv.height;
  const SK = {
    green: [[0, '#3a7fc0'], [0.55, '#9ad0f0'], [1, '#f8e3b4']],
    partial: [[0, '#2d1e3e'], [0.6, '#b85d43'], [1, '#f2b872']],
    desert: [[0, '#9a6a3e'], [0.55, '#d9a566'], [1, '#f2dba2']]
  }[kind];
  const PAL = {
    green:   { ridge: '#4a8a6a', sky: '#6a7aa8', win: null,      land: '#4d9a52', landHi: '#7bc46e', river: '#3d82c0', rip: '#a8d8f8', bank: '#3f8a46', tower: '#fff1d0' },
    partial: { ridge: '#5a4a6a', sky: '#3a3560', win: '#f3c76a', land: '#4a6a46', landHi: '#6f8a5a', river: '#35629a', rip: '#7fb0d8', bank: '#3d5a3e', tower: '#c9ccd8' },
    desert:  { ridge: '#b08a5a', sky: '#a08060', win: null, land: '#d2b078', landHi: '#e8cf98', river: '#8a6a48', rip: '#5e4630', bank: '#c29c64', tower: '#b89a70' }
  }[kind];

  const bg = document.createElement('canvas'); bg.width = W; bg.height = H;
  const b = bg.getContext('2d');
  for (let y = 0; y < 262; y += 8) { b.fillStyle = colorAt(SK, y / 262); b.fillRect(0, y, W, 8); }
  const rs = makeRng(17);
  if (kind === 'green') {
    b.globalAlpha = 0.25; mgDisc(b, 150, 70, 52, '#fff4c0'); b.globalAlpha = 1; mgDisc(b, 150, 70, 30, '#fff4c0');
    [[300, 50], [460, 90], [60, 130], [560, 40]].forEach(([x, y]) => { mgR(b, x, y, 70, 14, '#ffffff'); mgR(b, x + 14, y - 10, 36, 12, '#ffffff'); mgR(b, x + 6, y + 14, 58, 4, '#c9d9ea'); });
  } else if (kind === 'partial') {
    for (let i = 0; i < 24; i++) { b.fillStyle = '#f4f1d8'; b.fillRect(Math.floor(rs() * W / 4) * 4, Math.floor(rs() * 90 / 4) * 4, 2, 2); }
    b.globalAlpha = 0.3; mgDisc(b, 150, 240, 56, '#ff9a5a'); b.globalAlpha = 1; mgDisc(b, 150, 240, 34, '#ffcf7a');
  } else {
    b.globalAlpha = 0.22; mgDisc(b, 150, 76, 78, '#fff0c0'); b.globalAlpha = 0.3; mgDisc(b, 150, 76, 52, '#fff0c0'); b.globalAlpha = 1; mgDisc(b, 150, 76, 30, '#fff4c8');
  }
  // 보문산 능선
  for (let x = 0; x < W; x += 4) {
    const h = Math.round(44 + 22 * Math.sin(x * 0.012 + 1) + 10 * Math.sin(x * 0.04));
    mgR(b, x, 258 - h, 4, h + 6, PAL.ridge);
  }
  mgSkyline(b, W, 264, 33, PAL.sky, PAL.win, 0.8);
  // 한빛탑
  mgHanbit(b, 626, 266, PAL.tower, 1.1);
  // 모래언덕이 도시 아래를 덮음
  if (kind === 'desert') for (let x = 0; x < W; x += 4) { const hd = Math.round(16 + 12 * Math.sin(x * 0.018 + 0.5) + 6 * Math.sin(x * 0.05)); mgR(b, x, 262 - hd, 4, hd + 6, '#dcbd84'); mgR(b, x, 262 - hd, 4, 2, '#f0dba8'); }
  // 육지 · 갑천 · 둑
  mgR(b, 0, 262, W, 56, PAL.land); mgR(b, 0, 262, W, 4, PAL.landHi);
  for (let i = 0; i < 120; i++) mgR(b, Math.floor(rs() * W), 268 + Math.floor(rs() * 48), 4, 2, rs() < 0.5 ? PAL.landHi : PAL.bank);
  mgR(b, 0, 318, W, 40, PAL.river);
  if (kind === 'desert') for (let i = 0; i < 46; i++) { let x = Math.floor(rs() * W), y = 320 + Math.floor(rs() * 34); for (let k = 0; k < 7; k++) { mgR(b, x, y, 3, 2, PAL.rip); x += Math.floor(rs() * 7) - 2; y += Math.floor(rs() * 5) - 2; if (y < 319) y = 319; if (y > 352) y = 352; } }
  mgR(b, 0, 354, W, 46, PAL.bank); mgR(b, 0, 354, W, 4, PAL.landHi);
  mgR(b, 0, 316, W, 3, '#9a9b91');
  function tree(x, y, i) {
    mgR(b, x + 8, y + 18, 6, 22, '#5b3a22');
    if (kind === 'desert') {
      mgR(b, x + 2, y + 12, 8, 3, '#5b3a22'); mgR(b, x + 12, y + 6, 8, 3, '#5b3a22'); mgR(b, x + 5, y + 4, 3, 10, '#5b3a22');
    } else {
      const lush = kind === 'green' || i % 2 === 0;
      mgR(b, x, y, 22, 20, MG_INK);
      mgR(b, x + 2, y + 2, 18, 16, lush ? '#2f6b3a' : '#8a8a4a');
      mgR(b, x + 4, y + 2, 8, 6, lush ? '#4f9a52' : '#a8a860');
    }
  }
  [14, 92, 176, 262, 414, 492, 570, 668].forEach((x, i) => tree(x, 340 - 4 * (i % 2), i));

  const LOOK = {
    assessor: { hs: 'helmet', shirt: '#e07a2f', shirt2: '#c4651f', pants: '#35384f', vest: '#f2c14e' },
    v1: { hair: '#d8d8e0', hs: 'bun', shirt: '#8a5a9a', shirt2: '#74487f', pants: '#3b3550', cane: true },
    v2: { hair: '#4a2c20', hs: 'long', shirt: '#d98aa0', shirt2: '#bd6f86', pants: '#3d3a52', bag: '#a8603c' },
    v3: { hair: '#3a2a1a', hs: 'cap', cap: '#2b6cb0', shirt: '#4b9a6b', shirt2: '#3a7e56', pants: '#2b2d42' }
  };
  const crowd = kind === 'green'
    ? [['assessor', 290], ['v1', 350], ['v2', 410], ['v3', 470]]
    : (kind === 'partial' ? [['assessor', 320], ['v2', 390]] : [['assessor', 340]]);
  const slots = [34, 150, 266];

  function facility(x, baseY, decision, T, idx) {
    if (decision === 'reject' || !decision) {
      if (kind !== 'desert') {
        mgR(cx, x + 4, baseY - 30, 6, 24, '#5b3a22'); mgR(cx, x, baseY - 46, 22, 20, MG_INK); mgR(cx, x + 2, baseY - 44, 18, 16, '#2f6b3a'); mgR(cx, x + 4, baseY - 44, 8, 6, '#4f9a52');
        for (let k = 0; k < 6; k++) mgR(cx, x + 28 + k * 6, baseY - 6 - (k % 2) * 2, 3, 3, k % 2 ? '#ffd166' : '#ff9ab8');
        mgR(cx, x + 30, baseY - 30, 30, 12, MG_INK); mgR(cx, x + 32, baseY - 28, 26, 8, '#8a6a4a');
        cx.fillStyle = '#fff4c0'; cx.font = '800 9px "Noto Sans KR", sans-serif'; cx.textAlign = 'center'; cx.fillText('보전', x + 45, baseY - 21);
      } else {
        mgR(cx, x + 8, baseY - 22, 4, 20, '#5b3a22'); mgR(cx, x + 4, baseY - 16, 6, 2, '#5b3a22');
        mgR(cx, x + 24, baseY - 4, 36, 4, '#3a2f26');
      }
      return;
    }
    const cond = decision === 'conditional';
    mgR(cx, x, baseY - 30, 64, 30, MG_INK); mgR(cx, x + 2, baseY - 28, 60, 26, cond ? '#4a5a78' : '#3a3f58');
    for (let wx = x + 8; wx < x + 58; wx += 12) { mgR(cx, wx, baseY - 22, 6, 5, '#ffd36b'); mgR(cx, wx, baseY - 12, 6, 5, '#6f80a6'); }
    [[x + 8, 26], [x + 40, 20]].forEach(([cxp, ch], ci) => {
      mgR(cx, cxp, baseY - 30 - ch, 10, ch + 2, MG_INK); mgR(cx, cxp + 2, baseY - 28 - ch, 6, ch, '#4a4f6a');
      mgR(cx, cxp + 2, baseY - 24 - ch, 6, 3, '#c0392b'); mgR(cx, cxp + 2, baseY - 16 - ch, 6, 3, '#c0392b');
      for (let k = 0; k < 6; k++) {
        const prog = (T * 0.35 + k / 6 + ci * 0.3 + idx * 0.17) % 1;
        const px = cxp + 5 + prog * 34, py = baseY - 34 - ch - prog * 64, sz = 6 + prog * 16;
        cx.globalAlpha = (cond ? 0.22 : 0.8) * (1 - prog);
        mgR(cx, px - sz / 2, py - sz / 2, sz, sz, cond ? '#c9ccd8' : (kind === 'desert' ? '#2a252c' : '#6a625c'));
      }
      cx.globalAlpha = 1;
    });
    if (cond) {
      for (let k = 0; k < 3; k++) { mgR(cx, x + 2 + k * 22, baseY + 2, 6, 6, '#5b3a22'); mgR(cx, x + k * 22, baseY - 10, 16, 12, MG_INK); mgR(cx, x + 2 + k * 22, baseY - 8, 12, 8, '#2f6b3a'); }
      mgR(cx, x + 66, baseY - 22, 2, 22, '#c9ccd8'); mgR(cx, x + 64, baseY - 26, 6, 5, '#52b788');
    }
  }

  let prevT = performance.now(), running = true;
  function frame(now) {
    if (!running) return;
    prevT = now;
    const T = now / 1000;
    cx.drawImage(bg, 0, 0);
    // 갑천 물결
    if (kind !== 'desert') for (let k = 0; k < 18; k++) mgR(cx, ((k * 47 + T * 18) % (W + 20)) - 10, 322 + (k % 5) * 7, 16, 2, PAL.rip);
    if (kind === 'green') for (let k = 0; k < 6; k++) if (Math.sin(T * 3 + k * 2) > 0.7) mgR(cx, 60 + k * 110, 326 + (k % 3) * 8, 3, 3, '#ffffff');
    // 시설 3곳 (평가 결과에 따라 달라짐)
    slots.forEach((sx, i) => facility(sx, 316, facilityDecisions[i], T, i));
    // 주민과 평가원
    crowd.forEach(([k, x], i) => {
      const bob = kind === 'green' ? (Math.sin(T * 4 + i * 1.3) > 0.55 ? -6 : 0) : (kind === 'partial' ? (Math.sin(T * 2 + i) > 0.9 ? -2 : 0) : 0);
      mgR(cx, x - 4, 392, 56, 5, 'rgba(0,0,0,0.35)');
      mgPerson(cx, x, 304 + bob + (kind === 'desert' ? 6 : 0), 4, Object.assign({}, LOOK[k], { talk: kind === 'green' && Math.floor(T * 3 + i) % 2 === 0 }));
    });
    // 분위기 효과
    if (kind === 'green') {
      for (let i = 0; i < 4; i++) {
        const bx = ((T * 36 + i * 190) % (W + 80)) - 40, by = 70 + i * 22 + Math.sin(T * 2 + i) * 8, f = Math.floor(T * 6 + i) % 2;
        mgR(cx, bx, by, 6, 2, MG_INK); mgR(cx, bx + 6, by - (f ? 3 : -1), 6, 2, MG_INK); mgR(cx, bx - 6, by - (f ? 3 : -1), 6, 2, MG_INK);
      }
      for (let i = 0; i < 22; i++) { cx.globalAlpha = 0.85; mgR(cx, (i * 37 + T * 14 + Math.sin(T + i) * 10) % W, (T * 26 + i * 53) % H, 3, 3, '#ffc8dc'); }
      cx.globalAlpha = 1;
    } else if (kind === 'partial') {
      for (let i = 0; i < 18; i++) { cx.globalAlpha = 0.16; mgR(cx, (i * 71 + T * 10) % W, 150 + (i * 29) % 120, 46, 12, '#b8aab0'); }
      cx.globalAlpha = 1;
    } else {
      cx.fillStyle = 'rgba(210,160,80,0.2)'; cx.fillRect(0, 0, W, H);
      for (let i = 0; i < 70; i++) { cx.globalAlpha = 0.6; mgR(cx, ((i * 61 + T * (160 + (i % 5) * 30)) % (W + 20)) - 10, (i * 37) % H, 3 + (i % 3), 2, '#efd69a'); }
      cx.globalAlpha = 1;
      const tx = (T * 70) % (W + 60) - 30;
      mgDisc(cx, tx, 380 - Math.abs(Math.sin(T * 6)) * 6, 10, '#8a6a40', 2); mgDisc(cx, tx, 380 - Math.abs(Math.sin(T * 6)) * 6, 5, '#b08a58', 2);
    }
    // 제목표
    const label = kind === 'green' ? 'GOOD ENDING' : (kind === 'partial' ? 'PARTIAL ENDING' : 'BAD ENDING');
    mgR(cx, 10, 10, 250, 34, MG_INK); mgR(cx, 13, 13, 244, 28, '#101847');
    cx.fillStyle = kind === 'green' ? '#7bf0b0' : (kind === 'partial' ? '#ffd166' : '#ff7b7b');
    cx.font = '12px "Press Start 2P", monospace'; cx.textAlign = 'left'; cx.fillText(label, 22, 33);
    requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);

  activeMinigameCleanup = () => { running = false; };
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
    drawMoon(Math.round(lw * 0.78), Math.round(lh * 0.2), Math.max(6, Math.round(lh * 0.095)));
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

// 대전 도시 레이어: 보문산 능선 · 아파트 스카이라인 · 엑스포과학공원 한빛탑 · 갑천
function drawCityLayer(variant, green) {
  const r = makeRng(11);
  const groundY = Math.round(lh * 0.54);
  const groundH = Math.round(lh * 0.14);
  const towerLights = [];
  const desert = endingType === 'desert';

  // 보문산 능선 (원경)
  for (let xx = 0; xx < lw; xx++) {
    const ridge = Math.round(groundY - lh * 0.22 - Math.abs(Math.sin(xx * 0.045 + 0.6)) * lh * 0.06 - Math.sin(xx * 0.013) * lh * 0.04);
    pr(xx, ridge, 1, groundY - ridge, '#6d7aa3');
    pr(xx, ridge, 1, 1, '#9aa6cc');
  }

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
    pr(xx, dy, 1, groundY - dy + 2, desert ? '#9b805e' : '#526b62');
    pr(xx, dy, 1, 1, '#82958a');
  }

  // 엑스포과학공원 언덕과 한빛탑
  const nx = Math.round(lw * 0.9), nw = Math.round(lw * 0.09), nh = Math.round(lh * 0.04);
  for (let xx = nx - nw; xx <= nx + nw; xx++) {
    const t = (xx - nx) / nw;
    const hh = Math.round(nh * (1 - t * t));
    pr(xx, groundY - hh, 1, hh + 2, desert ? '#8a7352' : '#3f6b4a');
    pr(xx, groundY - hh, 1, 1, '#6f9a6a');
  }
  const topY = groundY - nh;
  pr(nx - 1, topY - 30, 2, 30, '#c9ccd8');
  pr(nx - 4, topY - 37, 8, 5, '#e8e2d0');
  pr(nx - 5, topY - 38, 10, 1, '#c9ccd8');
  pr(nx - 3, topY - 46, 6, 7, '#e8e2d0');
  pr(nx, topY - 62, 1, 16, '#c9ccd8');
  pr(nx, topY - 63, 1, 1, '#e0505a');

  const base = desert ? '#a88b62' : (green ? '#4a6b48' : '#59615f');
  const lite = desert ? '#c4a174' : (green ? '#6f9a5a' : '#78817c');
  const dk = desert ? '#806746' : (green ? '#365236' : '#414947');
  pr(0, groundY, lw, groundH, base);
  pr(0, groundY, lw, 1, lite);
  for (let i = 0; i < 170; i++) {
    const sx = Math.floor(r() * lw);
    const sy = groundY + 2 + Math.floor(r() * Math.max(1, groundH - 2));
    pr(sx, sy, r() < 0.4 ? 2 : 1, 1, r() < 0.5 ? lite : dk);
  }

  // 갑천
  const rvH = Math.max(3, Math.round(lh * 0.04));
  pr(0, groundY, lw, rvH, desert ? '#8a7a5a' : '#35629a');
  for (let i = 0; i < 60; i++) pr(Math.floor(r() * lw), groundY + Math.floor(r() * rvH), 2 + Math.floor(r() * 3), 1, r() < 0.5 ? '#7fb0d8' : '#2a4f82');
  pr(0, groundY + rvH, lw, 1, '#9a9b91');

  const roadY = groundY + Math.round(groundH * 0.62);
  pr(0, roadY, lw, Math.max(3, Math.round(groundH * 0.22)), desert ? '#78664e' : '#343b42');
  pr(0, roadY, lw, 1, '#9a9b91');
  for (let rx = 5; rx < lw; rx += 18) pr(rx, roadY + 2, 5, 1, '#d9cda4');
  const treeColor = desert ? '#74654b' : (green ? '#2f6b3a' : '#596f56');
  [0.05, 0.17, 0.39, 0.6, 0.86, 0.95].forEach((tx, idx) => {
    const px = Math.round(lw * tx);
    const py = groundY + 5 + (idx % 2) * 3;
    pr(px, py, 2, 4, '#5b3a22');
    pixDisc(px + 1, py - 1, 4, treeColor);
    pixDisc(px, py - 2, 2, desert ? '#8b7856' : '#4f9a52');
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

  // 달빛 길 (한강 위 달 그림자)
  if (variant === 'night') {
    const mxr = Math.round(lw * 0.78);
    for (let k = 0; k < rvH; k++) pr(mxr - 3 + (k % 2) * 2, groundY + k, 5 - (k % 2) * 2, 1, '#f6f0cf');
  }

  const dim = (variant === 'night' || variant === 'dusk' || variant === 'rain' || variant === 'dust');
  if (dim) {
    g.globalAlpha = variant === 'night' ? 0.95 : 0.6;
    towerLights.forEach(p => pr(p[0], p[1], 1, 1, '#ffd36b'));
    pr(nx - 3, topY - 36, 6, 1, '#ffd36b');
    pr(nx - 2, topY - 44, 4, 1, '#ffd36b');
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
    g.fillRect(x - 1, y + 2, 1, 1);
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

const PETALS = [];
for (let i = 0; i < 70; i++) PETALS.push({ x: Math.random(), y: Math.random(), v: 0.03 + Math.random() * 0.05, ph: Math.random() * 6.28, s: Math.random() < 0.3 ? 2 : 1 });

function drawPetals() {
  const T = Date.now() / 1000;
  PETALS.forEach(p => {
    p.y += p.v * frameDt;
    if (p.y > 1) { p.y = -0.02; p.x = Math.random(); }
    const x = Math.round((p.x + Math.sin(T * 0.8 + p.ph) * 0.02) * lw);
    const y = Math.round(p.y * lh);
    g.globalAlpha = 0.85;
    g.fillStyle = p.s > 1 ? '#ffb8d0' : '#ffd8e6';
    g.fillRect(x, y, p.s, p.s);
  });
  g.globalAlpha = 1;
}

// 점프킹 풍 이끼 낀 돌벽돌 창틀
function brickBar(x, y, w, h, seed) {
  const rb = makeRng(seed);
  pr(x, y, w, h, '#14132a');
  const bh = 4, bw = 9;
  for (let by = 0; by < h; by += bh) {
    const off = ((by / bh) | 0) % 2 ? 4 : 0;
    for (let bx = -off; bx < w; bx += bw) {
      const x0 = Math.max(0, bx), x1 = Math.min(w, bx + bw - 1);
      if (x1 > x0) {
        const lt = rb();
        pr(x + x0, y + by, x1 - x0, Math.min(bh - 1, h - by), lt < 0.2 ? '#59577a' : (lt < 0.55 ? '#46455f' : '#3b3a52'));
        pr(x + x0, y + by, x1 - x0, 1, '#6a688c');
      }
    }
  }
  const mossN = Math.max(2, ((w * h) / 50) | 0);
  for (let i = 0; i < mossN; i++) pr(x + Math.floor(rb() * w), y + Math.floor(rb() * h), 1 + Math.floor(rb() * 2), 1, rb() < 0.5 ? '#3f7a4a' : '#2f5f3b');
}

function drawFrameAndDesk() {
  const fh = Math.round(lh * 0.65);

  g.globalAlpha = 0.07;
  for (let i = 0; i < 4; i++) {
    const px = Math.round(lw / 4 * i) + 10;
    for (let yy = 4; yy < fh - 6; yy++) pr(px + Math.round(yy * 0.35), yy, 3, 1, '#ffffff');
  }
  g.globalAlpha = 1;

  brickBar(0, 0, lw, 6, 1);
  brickBar(0, 0, 6, fh, 2);
  brickBar(lw - 6, 0, 6, fh, 3);
  brickBar(0, fh - 5, lw, 5, 4);
  for (let i = 1; i <= 3; i++) brickBar(Math.round(lw / 4 * i) - 2, 0, 5, fh, 10 + i);

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
  pixelBands(0, lh, [[0, '#0a0d2a'], [0.38, '#222a6b'], [0.66, '#6a4f8a'], [0.85, '#d98aa0'], [1, '#f2c0a0']], 3);
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
  // 보문산 능선
  for (let x = 0; x < lw; x++) {
    const y = Math.round(lh * 0.56 - Math.abs(Math.sin(x * 0.03 + 0.4)) * lh * 0.1 - Math.sin(x * 0.011) * lh * 0.04);
    pr(x, y, 1, lh * 0.8 - y, '#161d4e');
    pr(x, y, 1, 1, '#2f3a82');
  }
  for (let x = 0; x < lw; x++) {
    const y = Math.round(lh * (0.69 + 0.035 * Math.sin(x / lw * 8 + 0.4) + 0.025 * Math.sin(x / lw * 17)));
    pr(x, y, 1, lh - y, '#171c3c');
    pr(x, y, 1, 1, '#3a456e');
  }
  // 엑스포과학공원 언덕과 한빛탑
  const hx = Math.round(lw * 0.88), hw = Math.round(lw * 0.1), hhh = Math.round(lh * 0.05);
  for (let x = hx - hw; x <= hx + hw; x++) {
    const t = (x - hx) / hw;
    const top = Math.round(lh * 0.69) - Math.round(hhh * (1 - t * t));
    pr(x, top, 1, lh - top, '#171c3c');
    pr(x, top, 1, 1, '#3a456e');
  }
  const ttop = Math.round(lh * 0.69) - hhh;
  pr(hx - 1, ttop - 30, 2, 30, '#2a3170');
  pr(hx - 4, ttop - 37, 8, 5, '#3a456e');
  pr(hx - 5, ttop - 38, 10, 1, '#2a3170');
  pr(hx - 3, ttop - 46, 6, 7, '#3a456e');
  pr(hx, ttop - 62, 1, 16, '#2a3170');
  pr(hx, ttop - 63, 1, 1, '#e0505a');
  pr(hx - 3, ttop - 36, 6, 1, '#f3c76a');
  pr(hx - 2, ttop - 44, 4, 1, '#f3c76a');
  list.forEach(b => {
    const bx = Math.round(lw * b.x), bw = Math.max(6, Math.round(lw * b.w));
    const bh = Math.round(lh * b.h), by = baseY - bh;
    pr(bx, by, bw, bh + 14, '#0e1230'); pr(bx + bw - 1, by, 1, bh + 14, '#2a3170');
    pr(bx, by, bw, 1, '#2a3170');
    for (let wy = by + 4; wy < baseY - 2; wy += 4) for (let wx = bx + 2; wx < bx + bw - 2; wx += 3) if (r() < 0.32) pr(wx, wy, 1, 2, r() < 0.8 ? '#f3c76a' : '#6ad0c8');
    if (b.h > 0.3) { pr(bx + 2, by - 2, bw - 4, 2, '#0e1230'); pr(bx + Math.floor(bw / 2), by - 5, 1, 3, '#0e1230'); }
  });
  [0.06].forEach(tx => {
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
  drawPetals();
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
