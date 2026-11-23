import streamlit as st
from auth_db import register_user, login_user, save_game_state, load_game_state

st.title("계정 로그인 및 데이터 관리")

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "username" not in st.session_state:
    st.session_state["username"] = ""

if st.session_state["logged_in"]:
    user = st.session_state["username"]
    st.success(f"현재 로그인된 계정: **{user}**")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("현재 진행도 저장하기", use_container_width=True):
            excluded = {"logged_in", "username"}
            save_payload = {
                k: v for k, v in st.session_state.items()
                if k not in excluded and isinstance(v, (int, float, str, bool, list, dict))
            }
            save_game_state(user, save_payload)
            st.toast("클라우드 DB에 저장되었습니다!")

    with col2:
        if st.button("저장된 진행도 불러오기", use_container_width=True):
            loaded = load_game_state(user)
            if loaded:
                for k, v in loaded.items():
                    st.session_state[k] = v
                st.success("저장된 데이터를 불러왔습니다!")
            else:
                st.info("저장된 게임 데이터가 없습니다.")

    st.divider()
    if st.button("로그아웃"):
        st.session_state["logged_in"] = False
        st.session_state["username"] = ""
        st.rerun()

else:
    tab_login, tab_register = st.tabs(["로그인", "회원가입"])

    with tab_login:
        with st.form("login_form"):
            login_id = st.text_input("아이디")
            login_pw = st.text_input("비밀번호", type="password")
            submitted = st.form_submit_button("로그인")
            if submitted:
                ok, msg = login_user(login_id, login_pw)
                if ok:
                    loaded = load_game_state(login_id.strip())
                    for k, v in loaded.items():
                        st.session_state[k] = v
                    st.rerun()
                else:
                    st.error(msg)

    with tab_register:
        with st.form("register_form"):
            reg_id = st.text_input("새 아이디")
            reg_pw = st.text_input("새 비밀번호", type="password")
            reg_pw2 = st.text_input("비밀번호 확인", type="password")
            reg_submitted = st.form_submit_button("가입하기")
            if reg_submitted:
                if reg_pw != reg_pw2:
                    st.error("비밀번호가 서로 다릅니다.")
                else:
                    ok, msg = register_user(reg_id, reg_pw)
                    if ok:
                        st.success(msg)
                    else:
                        st.error(msg)
