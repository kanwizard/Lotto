import streamlit as st
import requests
import random

st.set_page_config(page_title="로또 생성기", page_icon="🎰")

HEADERS = {"User-Agent": "Mozilla/5.0"}


# 🔹 로또 API
def get_lotto(draw_no):
    url = "https://www.dhlottery.co.kr/common.do?method=getLottoNumber"
    params = {"drwNo": draw_no}

    try:
        res = requests.get(url, params=params, headers=HEADERS, timeout=5)
        data = res.json()

        if data.get("returnValue") != "success":
            return []

        return [data[f"drwtNo{i}"] for i in range(1, 7)]

    except:
        return []


# 🔹 최근 3회차 가져오기
def get_recent_3(latest):
    results = []

    for i in range(3):
        nums = get_lotto(latest - i)
        if nums:
            results.append(nums)

    return results


# 🔹 랜덤 생성 (1~39)
def generate(count):
    return [
        sorted(random.sample(range(1, 40), 6))
        for _ in range(count)
    ]


# ================= UI =================

st.title("🎰 로또 랜덤 생성기 + 최근 3회차 참고")

latest = st.number_input("최신 회차 입력", min_value=1, value=1100)

count = st.number_input("생성 개수", min_value=1, value=5)

# 🔥 세션 저장
if st.button("📥 최근 3회차 불러오기"):
    st.session_state.recent = get_recent_3(latest)

recent = st.session_state.get("recent", [])

# 📊 최근 3회차 출력
if recent:
    st.subheader("📅 최근 3회차 (참고용)")

    for i, r in enumerate(recent):
        st.write(f"{latest - i}회차: {r}")

st.divider()

# 🎯 랜덤 생성
if st.button("🎯 번호 생성"):
    results = generate(count)

    st.subheader("🎲 랜덤 추천")

    for i, r in enumerate(results, 1):
        st.write(f"{i}번: {r}")
