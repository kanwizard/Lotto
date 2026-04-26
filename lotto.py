import streamlit as st
import requests
import random

st.set_page_config(page_title="로또 생성기", page_icon="🎰")

HEADERS = {"User-Agent": "Mozilla/5.0"}


def get_lotto(draw_no):
    url = "https://www.dhlottery.co.kr/common.do?method=getLottoNumber"
    params = {"drwNo": draw_no}

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        res = requests.get(url, params=params, headers=headers, timeout=5)

        # 🔥 먼저 텍스트 확인 (중요)
        text = res.text

        if "drwtNo1" not in text:
            return []

        data = res.json()

        if data.get("returnValue") != "success":
            return []

        return [data.get(f"drwtNo{i}") for i in range(1, 7)]

    except:
        return []


def get_recent_3(latest):
    return [get_lotto(latest - i) for i in range(3)]


def generate(count):
    return [
        sorted(random.sample(range(1, 40), 6))
        for _ in range(count)
    ]


# ================= UI =================

st.title("🎰 로또 생성기")

latest = st.number_input("최신 회차", min_value=1, value=1100)
count = st.number_input("생성 개수", min_value=1, value=5)

# 🔥 버튼 1개로 통합 (중요)
if st.button("📊 최근 3회차 + 생성 실행"):

    recent = get_recent_3(latest)

    st.subheader("📅 최근 3회차")

    for i, r in enumerate(recent):
        st.write(f"{latest - i}회차: {r}")

    st.divider()

    results = generate(count)

    st.subheader("🎯 랜덤 결과")

    for i, r in enumerate(results, 1):
        st.write(f"{i}번: {r}")
