import json
import bcrypt
import streamlit as st
from sqlalchemy import text


def get_conn():
    return st.connection("postgresql", type="sql")


def register_user(username: str, password: str) -> tuple[bool, str]:
    username = username.strip()
    if not username or not password:
        return False, "아이디와 비밀번호를 모두 입력해 주세요."

    conn = get_conn()
    existing = conn.query(
        "SELECT username FROM users WHERE username = :u",
        params={"u": username},
        ttl=0,
    )
    if not existing.empty:
        return False, "이미 존재하는 아이디입니다."

    pw_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    with conn.session as session:
        session.execute(
            text("INSERT INTO users (username, password_hash) VALUES (:u, :p)"),
            {"u": username, "p": pw_hash},
        )
        session.execute(
            text("INSERT INTO game_saves (username, save_data) VALUES (:u, CAST(:d AS jsonb))"),
            {"u": username, "d": json.dumps({})},
        )
        session.commit()

    return True, "회원가입이 완료되었습니다. 로그인해 주세요."


def login_user(username: str, password: str) -> tuple[bool, str]:
    username = username.strip()
    conn = get_conn()
    df = conn.query(
        "SELECT password_hash FROM users WHERE username = :u",
        params={"u": username},
        ttl=0,
    )
    if df.empty:
        return False, "존재하지 않는 아이디입니다."

    stored_hash = df.iloc[0]["password_hash"].encode("utf-8")
    if bcrypt.checkpw(password.encode("utf-8"), stored_hash):
        st.session_state["logged_in"] = True
        st.session_state["username"] = username
        return True, f"{username}님 환영합니다!"

    return False, "비밀번호가 일치하지 않습니다."


def save_game_state(username: str, state_dict: dict) -> None:
    conn = get_conn()
    with conn.session as session:
        session.execute(
            text("""
                INSERT INTO game_saves (username, save_data, updated_at)
                VALUES (:u, CAST(:d AS jsonb), CURRENT_TIMESTAMP)
                ON CONFLICT (username)
                DO UPDATE SET save_data = CAST(:d AS jsonb), updated_at = CURRENT_TIMESTAMP
            """),
            {"u": username, "d": json.dumps(state_dict, ensure_ascii=False)},
        )
        session.commit()


def load_game_state(username: str) -> dict:
    conn = get_conn()
    df = conn.query(
        "SELECT save_data FROM game_saves WHERE username = :u",
        params={"u": username},
        ttl=0,
    )
    if df.empty:
        return {}
    data = df.iloc[0]["save_data"]
    return json.loads(data) if isinstance(data, str) else (data or {})
