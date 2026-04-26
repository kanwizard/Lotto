import streamlit as st
import requests
import random

st.set_page_config(page_title="안정 로또 생성기", layout="centered")

HEADERS = {"User-Agent": "Mozilla/5.0"}


# 🔥 데이터 1회만 가져오기 (캐시 역할)
def fetch_lotto(draw_no):
    url = "https://www.dhlottery.co.kr/common.do?method=getLottoNumber"
    params = {"drwNo": draw_no}

    try:
        res = requests.get(url, params=params, headers=HEADERS, timeout=5)
        data = res.json()

        if data.get("returnValue") != "success":
            return None

        return [data[f"drwtNo{i}"] for i in range(1, 7)]

    except:
        return None


# 🔥 최근 3회차 (캐시에 저장)
def load_recent(draw_no):
    if "recent_data" not in st.session_state:
        st.session_state.recent_data = []

    if st.button("📥 데이터 불러오기 (1회만)"):
        st.session_state.recent_data = []

        for i in range(3):
            data = fetch_lotto(draw_no - i)
            if data:
                st.session_state.recent_data.append(data)

        st.success("데이터 로딩 완료!")

    return st.session_state.recent_data


# 🔥 번호 생성 (완전 로컬)
def generate(recent):
    all_nums = set(range(1, 40))
    used = set(n for r in recent for n in r)

    available = list(all_nums - used)

    if len(available) < 6:
        return None

    return sorted(random.sample(available, 6))


# ================= UI =================

st.title("🎰 절대 안깨지는 로또 생성기 (1~39)")

latest = st.number_input("최신 회차 입력", min_value=1, value=1100)

recent = load_recent(latest)

if recent:
    st.subheader("📅 최근 3회차")
    for i, r in enumerate(recent):
        st.write(f"{latest - i}회차: {r}")

    if st.button("🎯 번호 생성"):
        result = generate(recent)

        if result:
            st.success(f"추천 번호: {result}")
        else:
            st.error("가능한 숫자가 부족합니다.")
else:
    st.info("📥 먼저 데이터 불러오기 버튼을 눌러주세요")
