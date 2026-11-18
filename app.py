import streamlit as st
import pandas as pd
import numpy as np
import random

# 페이지 기본 설정
st.set_page_config(
    page_title="레인시티 (Rain City) - 환경 경영 시뮬레이션",
    page_icon="🌧️",
    layout="wide"
)

# --- 게임 상수 및 데이터 정의 ---
ZONES = [
    {"id": "공업지역", "icon": "🏭", "type": "emission"},
    {"id": "발전소", "icon": "⚡", "type": "emission"},
    {"id": "도로망", "icon": "🚗", "type": "emission"},
    {"id": "주거지역", "icon": "🏘️", "type": "urban"},
    {"id": "농경지", "icon": "🌾", "type": "eco"},
    {"id": "산림", "icon": "🌲", "type": "eco"},
    {"id": "호수/하천", "icon": "🏞️", "type": "water"},
    {"id": "중앙공원", "icon": "🌳", "type": "eco"},
    {"id": "기상관측소", "icon": "📡", "type": "infra"},
]

TECH_LIST = {
    "desulfurization": {
        "name": "배연탈황설비 (FGD)",
        "cost": 35,
        "ap": 1,
        "max_lv": 3,
        "desc": "공장·발전소의 SO₂ 배출량을 대폭 저감하여 산성비 원인 물질을 차단합니다."
    },
    "precipitator": {
        "name": "전기집진기 (ESP)",
        "cost": 30,
        "ap": 1,
        "max_lv": 3,
        "desc": "미세먼지(PM2.5)와 황산염 에어로졸 입자를 포집합니다."
    },
    "sensor": {
        "name": "고정밀 대기질 센서망",
        "cost": 20,
        "ap": 1,
        "max_lv": 2,
        "desc": "다음 턴의 예상 강수 pH와 오염 확산 위험도를 사전에 정밀 예측합니다."
    },
    "green_infra": {
        "name": "빗물정원 & 투수성 포장",
        "cost": 25,
        "ap": 1,
        "max_lv": 3,
        "desc": "빗물의 토양 침투를 도와 폭우 시 홍수 피해와 비점오염원 유출을 줄입니다."
    },
    "reservoir": {
        "name": "지하 빗물저류조",
        "cost": 30,
        "ap": 1,
        "max_lv": 3,
        "desc": "최대 물 저장 한도를 늘리고 폭우 시 빗물을 저장해 가뭄에 대비합니다."
    },
    "traffic_policy": {
        "name": "친환경 교통·차량 2부제",
        "cost": 15,
        "ap": 1,
        "max_lv": 3,
        "desc": "도로망의 NOₓ와 미세먼지 배출량을 줄입니다 (시민 만족도 소폭 감소 가능)."
    }
}

# --- 게임 상태 초기화 함수 ---
def init_game(max_turns=10):
    st.session_state.initialized = True
    st.session_state.max_turns = max_turns
    st.session_state.turn = 1
    st.session_state.game_over = False
    st.session_state.victory = False
    st.session_state.end_reason = ""

    # 핵심 자원 및 지표
    st.session_state.budget = 120
    st.session_state.ap = 3
    st.session_state.max_ap = 3
    st.session_state.water = 55.0          # 물 저장량 (%)
    st.session_state.max_water = 100.0
    st.session_state.so2 = 55.0            # SO2 농도 (ppb)
    st.session_state.nox = 50.0            # NOx 농도 (ppb)
    st.session_state.pm25 = 45.0           # PM2.5 농도 (㎍/㎥)
    st.session_state.avg_ph = 5.8          # 도시 평균 강수 pH
    st.session_state.eco_health = 75.0     # 생태계 건강도 (0~100)
    st.session_state.satisfaction = 70.0   # 시민 만족도 (0~100)
    st.session_state.repair_cost_total = 0 # 누적 피해 복구 비용

    # 기술 레벨
    st.session_state.tech_levels = {k: 0 for k in TECH_LIST.keys()}

    # 구역별 상태 초기화 (pH, 생태/시설 건강도)
    st.session_state.zone_status = {}
    for z in ZONES:
        st.session_state.zone_status[z["id"]] = {
            "ph": 5.9 if z["type"] != "emission" else 5.5,
            "health": 80.0
        }

    # 기상 예보 및 이벤트 생성
    st.session_state.logs = ["🎮 레인시티 환경정책 담당관으로 부임했습니다. 물 부족과 산성비 위기로부터 도시를 지키세요!"]
    generate_weather()

def generate_weather():
    # 무작위 이벤트 결정 (1턴 제외)
    events = [
        ("평온한 기상", "특이 기상 이변이 없는 보통의 날씨입니다.", "normal"),
        ("극심한 가뭄 경보", "고온 건조한 날씨가 이어져 물 증발량이 급증합니다!", "drought"),
        ("대기 정체 & 고농도 스모그", "풍속이 약해져 SO₂, NOₓ, 미세먼지가 도시에 축적됩니다!", "smog"),
        ("국지성 집중호우 전선", "강한 비구름이 접근 중입니다. 녹색 인프라가 부족하면 홍수 피해가 발생합니다!", "heavy_rain"),
        ("황사 및 산불 연무 유입", "외부 미세먼지가 유입되고 구름응결핵 성질이 변해 인공강우 효율이 변합니다.", "dust")
    ]
    if st.session_state.turn == 1:
        ev = events[0]
    else:
        ev = random.choices(events, weights=[0.4, 0.2, 0.15, 0.15, 0.1])[0]

    st.session_state.event = ev

    # 구름 유형 (따뜻한 구름 vs 차가운 구름)
    cloud_type = random.choice(["따뜻한 구름 (영상 기온, 0℃ 이상)", "차가운 구름 (과냉각 구름, 0℃ 미만)"])
    cloud_amount = random.randint(25, 90)
    humidity = random.randint(35, 90)
    wind_speed = round(random.uniform(1.0, 9.5), 1)
    natural_rain_prob = random.randint(10, 75)

    if ev[2] == "drought":
        cloud_amount = random.randint(15, 45)
        humidity = random.randint(25, 50)
        natural_rain_prob = random.randint(0, 15)
    elif ev[2] == "heavy_rain":
        cloud_amount = random.randint(75, 95)
        humidity = random.randint(80, 95)
        natural_rain_prob = random.randint(75, 95)
    elif ev[2] == "smog":
        wind_speed = round(random.uniform(0.5, 2.0), 1)

    st.session_state.weather = {
        "cloud_type": cloud_type,
        "cloud_amount": cloud_amount,
        "humidity": humidity,
        "wind_speed": wind_speed,
        "rain_prob": natural_rain_prob
    }

# --- pH 및 상태 색상 판별 함수 ---
def get_ph_status(ph):
    if ph >= 6.5:
        return "안전 (정상)", "🟢"
    elif ph >= 5.6:
        return "주의 (약산성)", "🟡"
    elif ph >= 4.5:
        return "위험 (산성비)", "🟠"
    else:
        return "심각 (강산성 피해)", "🔴"

def get_zone_color(health, ph):
    if health < 40 or ph <= 4.4:
        return "🔴 심각", "#ffcccc"
    elif health < 60 or ph <= 5.5:
        return "🟠 위험", "#ffe5cc"
    elif health < 75 or ph <= 6.4:
        return "🟡 주의", "#ffffcc"
    else:
        return "🟢 양호", "#d4edda"

# --- 턴 시뮬레이션 실행 함수 ---
def run_turn_simulation(seeding_choice):
    w = st.session_state.weather
    ev_type = st.session_state.event[2]
    lv = st.session_state.tech_levels
    turn_logs = [f"--- 📅 {st.session_state.turn}턴 시뮬레이션 결과 ---"]

    # 1. 배출량 및 대기 확산 계산
    so2_emit = max(4.0, 18.0 - lv["desulfurization"] * 4.5)
    nox_emit = max(4.0, 16.0 - lv["traffic_policy"] * 3.5)
    pm_emit = max(3.0, 14.0 - lv["precipitator"] * 3.5 - lv["traffic_policy"] * 1.5)

    # 바람에 의한 자연 희석
    dispersion = w["wind_speed"] * 1.8

    if ev_type == "smog":
        so2_emit += 12.0
        nox_emit += 12.0
        pm_emit += 15.0
        turn_logs.append("⚠️ 대기 정체로 오염물질이 도시 상공에 고농도로 축적되었습니다.")
    elif ev_type == "dust":
        pm_emit += 22.0
        turn_logs.append("🌪️ 황사·산불 연무 유입으로 미세먼지 농도가 급증했습니다.")

    st.session_state.so2 = max(5.0, st.session_state.so2 + so2_emit - dispersion)
    st.session_state.nox = max(5.0, st.session_state.nox + nox_emit - dispersion)
    st.session_state.pm25 = max(5.0, st.session_state.pm25 + pm_emit - dispersion)

    # 2. 인공강우 판정
    rain_occurred = False
    rain_amount = 0.0  # mm 환산 개념 (물 저장량 증가분)

    if seeding_choice != "실시하지 않음":
        if st.session_state.budget < 15:
            turn_logs.append("❌ 예산이 부족하여 인공강우를 실행하지 못했습니다.")
        else:
            st.session_state.budget -= 15
            # 시딩 적합성 판정
            is_warm = "따뜻한 구름" in w["cloud_type"]
            correct_seed = (is_warm and "흡습성" in seeding_choice) or (not is_warm and "빙정핵" in seeding_choice)

            success_prob = (w["cloud_amount"] * 0.5) + (w["humidity"] * 0.4)
            if correct_seed:
                success_prob += 25
            else:
                success_prob -= 25
                turn_logs.append("⚠️ 구름 온도에 맞지 않는 시딩 물질을 살포하여 응결 효율이 크게 떨어졌습니다!")

            if w["wind_speed"] > 7.5:
                success_prob -= 30
                turn_logs.append("💨 강풍으로 인해 시딩 물질이 목표 구름층에서 흩어졌습니다.")

            if ev_type == "dust":
                success_prob -= 10

            if random.uniform(0, 100) <= success_prob:
                rain_occurred = True
                rain_amount += random.uniform(14.0, 22.0) if correct_seed else random.uniform(6.0, 11.0)
                turn_logs.append(f"🛩️ 인공강우 성공! ({seeding_choice}) 구름방울이 성장하여 비가 내립니다.")
            else:
                turn_logs.append(f"☁️ 인공강우 실패: 구름량과 습도 조건이 맞지 않아 강수로 이어지지 못했습니다.")

    # 3. 자연 강수 판정
    if random.randint(1, 100) <= w["rain_prob"] or ev_type == "heavy_rain":
        rain_occurred = True
        nat_rain = random.uniform(22.0, 32.0) if ev_type == "heavy_rain" else random.uniform(8.0, 16.0)
        rain_amount += nat_rain
        turn_logs.append(f"🌧️ 자연 강수가 발생했습니다. (강수량 지수: +{nat_rain:.1f})")

    # 4. 강수에 따른 세정(Washout) 및 산성비(pH) 계산
    repair_cost = 0
    if rain_occurred:
        # 대기 오염물질이 빗물에 녹아 황산/질산 형성 -> pH 저하
        acid_load = (st.session_state.so2 * 0.022) + (st.session_state.nox * 0.016)
        # 비가 많이 올수록 초기 세정 후 희석 효과 소폭 반영
        dilution = min(0.4, rain_amount * 0.01)
        calculated_ph = round(max(3.8, min(6.8, 6.6 - acid_load + dilution)), 2)
        st.session_state.avg_ph = calculated_ph

        # 세정 효과로 대기 농도 감소
        st.session_state.so2 *= 0.65
        st.session_state.nox *= 0.70
        st.session_state.pm25 *= 0.65

        # 물 저장량 증가 (저류조 레벨에 따라 저장 효율 증가)
        capture_eff = 0.7 + (lv["reservoir"] * 0.1)
        water_gain = rain_amount * capture_eff
        st.session_state.water = min(st.session_state.max_water, st.session_state.water + water_gain)

        ph_label, _ = get_ph_status(calculated_ph)
        turn_logs.append(f"🧪 강수 평균 pH는 **{calculated_ph}** ({ph_label})로 측정되었습니다. (대기 오염물질 세정됨)")

        # 산성비 피해 판정
        if calculated_ph < 5.6:
            severity = (5.6 - calculated_ph) * 12.0
            st.session_state.eco_health = max(0.0, st.session_state.eco_health - severity)
            st.session_state.satisfaction = max(0.0, st.session_state.satisfaction - severity * 0.6)
            acid_repair = int(severity * 1.5)
            repair_cost += acid_repair
            turn_logs.append(f"🍂 산성비 침적으로 산림과 호수 생태계가 손상되었습니다! (생태계 -{severity:.1f}, 복구비 -{acid_repair})")
        else:
            st.session_state.eco_health = min(100.0, st.session_state.eco_health + 3.0)
            turn_logs.append("🌿 깨끗한 단비가 내려 도시 생태계가 회복되었습니다!")

        # 폭우 및 홍수 피해 판정
        if rain_amount > 24.0:
            flood_defense = (lv["green_infra"] * 6.0) + (lv["reservoir"] * 5.0)
            flood_damage = max(0.0, (rain_amount - 24.0) * 1.5 - flood_defense)
            if flood_damage > 0:
                flood_repair = int(flood_damage * 2.0)
                repair_cost += flood_repair
                st.session_state.satisfaction = max(0.0, st.session_state.satisfaction - flood_damage)
                turn_logs.append(f"🌊 폭우로 도로 침수 및 오염물질 하천 유출 발생! (녹색 인프라 부족, 복구비 -{flood_repair})")
            else:
                turn_logs.append("🛡️ 빗물정원과 빗물저류조가 폭우를 완벽히 흡수해 홍수를 막았습니다!")
    else:
        turn_logs.append("☀️ 이번 턴에는 비가 내리지 않아 대기 중 오염물질이 그대로 잔류했습니다.")
        # 비가 안 오면 고농도 미세먼지로 시민 만족도 하락
        if st.session_state.pm25 > 65:
            st.session_state.satisfaction = max(0.0, st.session_state.satisfaction - 4.0)

    # 5. 물 소비 및 증발 계산
    water_loss = 13.0 if ev_type == "drought" else 8.0
    st.session_state.water = max(0.0, st.session_state.water - water_loss)
    if st.session_state.water < 25.0:
        st.session_state.satisfaction = max(0.0, st.session_state.satisfaction - 6.0)
        st.session_state.eco_health = max(0.0, st.session_state.eco_health - 4.0)
        turn_logs.append("🚨 심각한 물 부족! 시민 불편과 생태계 건조 피해가 발생하고 있습니다.")

    # 6. 구역별 상태 업데이트
    for z in ZONES:
        zid = z["id"]
        offset = -0.3 if z["type"] == "emission" else (0.15 if z["type"] == "eco" else 0.0)
        if rain_occurred:
            st.session_state.zone_status[zid]["ph"] = round(max(3.8, min(7.0, st.session_state.avg_ph + offset + random.uniform(-0.1, 0.1))), 2)
        z_ph = st.session_state.zone_status[zid]["ph"]
        delta_h = (st.session_state.eco_health - st.session_state.zone_status[zid]["health"]) * 0.35
        st.session_state.zone_status[zid]["health"] = max(0.0, min(100.0, st.session_state.zone_status[zid]["health"] + delta_h))

    # 7. 예산 정산 (기본 세수 +25 - 복구비)
    st.session_state.repair_cost_total += repair_cost
    st.session_state.budget = max(0, st.session_state.budget + 25 - repair_cost)

    # 8. 즉시 패배 조건 체크
    lake_ph = st.session_state.zone_status["호수/하천"]["ph"]
    forest_hp = st.session_state.zone_status["산림"]["health"]

    if st.session_state.water <= 2.0:
        st.session_state.game_over = True
        st.session_state.victory = False
        st.session_state.end_reason = "💧 패배: 극심한 물 부족으로 도시 기능이 완전히 마비되었습니다."
    elif lake_ph <= 4.3:
        st.session_state.game_over = True
        st.session_state.victory = False
        st.session_state.end_reason = f"🐟 패배: 호수/하천의 산성화(pH {lake_ph})가 임계치를 넘어 수생태계가 붕괴했습니다."
    elif forest_hp <= 20.0 or st.session_state.eco_health <= 20.0:
        st.session_state.game_over = True
        st.session_state.victory = False
        st.session_state.end_reason = "🌲 패배: 산림과 도시 생태계 건강도가 회복 불가능한 수준으로 파괴되었습니다."
    elif st.session_state.turn >= st.session_state.max_turns:
        # 최종 턴 종료 판정
        st.session_state.game_over = True
        env_score = calculate_env_score()
        if (st.session_state.water >= 40.0 and st.session_state.avg_ph >= 5.6 and
            st.session_state.eco_health >= 60.0 and st.session_state.satisfaction >= 55.0 and env_score >= 65):
            st.session_state.victory = True
            st.session_state.end_reason = "🏆 승리! 대기질 관리와 인공강우의 조화로 지속가능한 레인시티를 완성했습니다!"
        else:
            st.session_state.victory = False
            st.session_state.end_reason = "📉 임기 종료 (목표 미달): 일부 환경·수자원 지표가 지속가능성 기준에 미치지 못했습니다."
    else:
        # 다음 턴 준비
        st.session_state.turn += 1
        st.session_state.ap = st.session_state.max_ap
        generate_weather()

    st.session_state.logs = turn_logs + [""] + st.session_state.logs

def calculate_env_score():
    air_score = max(0, 100 - (st.session_state.so2 * 0.5 + st.session_state.nox * 0.5 + st.session_state.pm25 * 0.4))
    water_score = min(100, st.session_state.water * 1.2)
    ph_score = max(0, min(100, (st.session_state.avg_ph - 4.0) * 35))
    raw_total = (air_score * 0.25) + (water_score * 0.2) + (ph_score * 0.2) + (st.session_state.eco_health * 0.2) + (st.session_state.satisfaction * 0.15)
    penalty = st.session_state.repair_cost_total * 0.15
    return max(0, round(raw_total - penalty, 1))

# --- 앱 실행 시작 ---
if "initialized" not in st.session_state:
    init_game(10)

# 사이드바: 게임 설정 및 규칙 요약
with st.sidebar:
    st.title("🌧️ 레인시티 (Rain City)")
    st.caption("환경공학 & 인공강우 의사결정 시뮬레이션")

    turn_mode = st.radio("플레이 턴 수 선택", [10, 20], horizontal=True)
    if st.button("🔄 새 게임 시작", use_container_width=True):
        init_game(turn_mode)
        st.rerun()

    st.divider()
    st.subheader("🎯 승리 조건 (종료 시점)")
    st.markdown("""
    - **물 저장량**: 40% 이상
    - **평균 강수 pH**: 5.6 이상
    - **생태계 건강도**: 60 이상
    - **시민 만족도**: 55 이상
    - **환경평가 점수**: 65점 이상
    """)

    st.divider()
    st.subheader("🔬 핵심 학습 포인트")
    st.info(
        "대기 중 SO₂와 NOₓ가 높은 상태에서 무리하게 인공강우를 실행하면, "
        "오염물질이 빗물에 용해되어 **산성비(황산·질산)**로 지표에 침적됩니다. "
        "탈황설비와 대기질 관리를 병행해 깨끗한 비를 만드세요!"
    )

# --- 1. 상단 정보판 (HUD) ---
env_score = calculate_env_score()
ph_status_text, ph_icon = get_ph_status(st.session_state.avg_ph)

st.markdown(f"### 📊 레인시티 종합 현황 — **{st.session_state.turn} / {st.session_state.max_turns} 턴**")

m1, m2, m3, m4, m5, m6, m7 = st.columns(7)
m1.metric("💰 예산", f"{st.session_state.budget} 억", delta="+25/턴")
m2.metric("⚡ 행동력 (AP)", f"{st.session_state.ap} / {st.session_state.max_ap}")
m3.metric("💧 물 저장량", f"{st.session_state.water:.1f}%", f"최대 {int(st.session_state.max_water)}%")
m4.metric("🧪 평균 강수 pH", f"{st.session_state.avg_ph:.2f} {ph_icon}", ph_status_text)
m5.metric("🌿 생태계 건강도", f"{st.session_state.eco_health:.1f} / 100")
m6.metric("😊 시민 만족도", f"{st.session_state.satisfaction:.1f} / 100")
m7.metric("🏅 환경평가 점수", f"{env_score} 점")

# 대기질 세부 지표 바
aq1, aq2, aq3 = st.columns(3)
aq1.info(f"**SO₂ (아황산가스):** {st.session_state.so2:.1f} ppb  *(탈황설비 Lv.{st.session_state.tech_levels['desulfurization']})*")
aq2.info(f"**NOₓ (질소산화물):** {st.session_state.nox:.1f} ppb  *(교통정책 Lv.{st.session_state.tech_levels['traffic_policy']})*")
aq3.info(f"**PM2.5 (초미세먼지):** {st.session_state.pm25:.1f} ㎍/㎥  *(전기집진기 Lv.{st.session_state.tech_levels['precipitator']})*")

st.divider()

# 게임 종료 화면 처리
if st.session_state.game_over:
    if st.session_state.victory:
        st.success(f"## {st.session_state.end_reason}")
        st.balloons()
    else:
        st.error(f"## {st.session_state.end_reason}")

    st.write(f"**최종 환경평가 점수:** {env_score}점 | **누적 피해 복구비:** {st.session_state.repair_cost_total}억")
    if st.button("다시 도전하기", type="primary"):
        init_game(st.session_state.max_turns)
        st.rerun()
    st.stop()

# --- 2. 메인 영역: 좌측(도시 맵 & 기상 예보) / 우측(기술 카드 & 인공강우 실행) ---
left_col, right_col = st.columns([1.35, 1.0])

with left_col:
    # 기상 예보 및 이벤트 패널
    ev_title, ev_desc, ev_code = st.session_state.event
    w = st.session_state.weather
    st.subheader("🌤️ 기상 관측소 예보 & 도시 이벤트")

    if ev_code != "normal":
        st.warning(f"**[기상 특보] {ev_title}**: {ev_desc}")
    else:
        st.success(f"**[기상 양호] {ev_title}**: {ev_desc}")

    w_col1, w_col2, w_col3, w_col4 = st.columns(4)
    w_col1.metric("구름량", f"{w['cloud_amount']}%")
    w_col2.metric("상대습도", f"{w['humidity']}%")
    w_col3.metric("풍속", f"{w['wind_speed']} m/s")
    w_col4.metric("자연 강수확률", f"{w['rain_prob']}%")
    st.caption(f"☁️ 현재 상공 구름 특성: **{w['cloud_type']}**")

    # 센서 레벨에 따른 사전 예측 기능 제공
    if st.session_state.tech_levels["sensor"] >= 1:
        est_acid = (st.session_state.so2 * 0.022) + (st.session_state.nox * 0.016)
        est_ph = round(max(3.8, min(6.8, 6.6 - est_acid + 0.15)), 2)
        st.info(f"📡 **[대기질 센서 예측]** 현 대기 농도에서 강수 발생 시 예상 강수 pH는 약 **{est_ph}** 입니다.")

    st.divider()

    # 도시 맵 (3x3 그리드 시각화)
    st.subheader("🗺️ 레인시티 구역별 환경 상태 맵")
    for row_idx in range(3):
        cols = st.columns(3)
        for col_idx in range(3):
            z = ZONES[row_idx * 3 + col_idx]
            z_stat = st.session_state.zone_status[z["id"]]
            status_badge, bg_color = get_zone_color(z_stat["health"], z_stat["ph"])
            with cols[col_idx]:
                st.markdown(
                    f"""
                    <div style="background-color:{bg_color}; padding:12px; border-radius:10px; border:1px solid #ccc; margin-bottom:10px; color:#111;">
                        <div style="font-size:1.1em; font-weight:bold;">{z['icon']} {z['id']}</div>
                        <div style="font-size:0.9em; margin-top:4px;">상태: <b>{status_badge}</b></div>
                        <div style="font-size:0.85em;">강수 pH: <b>{z_stat['ph']}</b> | 건강도: <b>{z_stat['health']:.0f}%</b></div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    # 시뮬레이션 결과 로그
    st.subheader("📜 시뮬레이션 및 정책 일지")
    log_box = "\n\n".join(st.session_state.logs[:15])
    st.text_area("기록", value=log_box, height=220, disabled=True, label_visibility="collapsed")

with right_col:
    # 환경공학 기술 카드창
    st.subheader("🛠️ 환경공학 기술 & 정책 카드")
    st.caption("행동력(AP)과 예산을 사용해 시설을 설치·업그레이드하세요.")

    for key, tech in TECH_LIST.items():
        cur_lv = st.session_state.tech_levels[key]
        is_max = cur_lv >= tech["max_lv"]
        with st.container(border=True):
            c1, c2 = st.columns([2.3, 1])
            with c1:
                st.markdown(f"**{tech['name']}** `Lv.{cur_lv}/{tech['max_lv']}`")
                st.caption(tech["desc"])
            with c2:
                btn_label = "최대 레벨" if is_max else f"설치 ({tech['cost']}억)"
                disabled = is_max or (st.session_state.budget < tech["cost"]) or (st.session_state.ap < tech["ap"])
                if st.button(btn_label, key=f"btn_{key}", disabled=disabled, use_container_width=True):
                    st.session_state.budget -= tech["cost"]
                    st.session_state.ap -= tech["ap"]
                    st.session_state.tech_levels[key] += 1
                    if key == "reservoir":
                        st.session_state.max_water += 20.0
                    elif key == "traffic_policy":
                        st.session_state.satisfaction = max(0.0, st.session_state.satisfaction - 2.0)
                    st.session_state.logs.insert(0, f"🔧 [{tech['name']}] Lv.{cur_lv + 1} 설치 완료!")
                    st.rerun()

    st.divider()

    # 인공강우 의사결정 & 턴 진행 패널
    st.subheader("🛩️ 인공강우 작전 및 턴 실행")
    with st.container(border=True):
        st.markdown("**시딩(Cloud Seeding) 방식 선택** *(실행 시 예산 15억 소모)*")
        seeding_option = st.radio(
            "구름 온도에 맞는 촉매제를 선택하세요:",
            [
                "실시하지 않음",
                "흡습성 시딩 (염화나트륨·염화칼슘 입자 - 따뜻한 구름용)",
                "빙정핵 시딩 (요오드화은 입자 - 차가운 과냉각 구름용)"
            ],
            label_visibility="collapsed"
        )

        st.caption("💡 팁: SO₂·NOₓ 농도가 높을 때 인공강우를 실행하면 산성비가 내릴 위험이 큽니다.")

        if st.button("▶️ 시뮬레이션 실행 및 다음 턴으로", type="primary", use_container_width=True):
            run_turn_simulation(seeding_option)
            st.rerun()
