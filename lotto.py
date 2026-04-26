import streamlit as st
import requests

st.set_page_config(page_title="로또 최근 3회차", page_icon="🎰")

HEADERS = {"User-Agent": "Mozilla/5.0"}


# 🔥 로또 API 함수 (안정 버전)
def get_lotto(draw_no):
    url = "https://www.dhlottery.co.kr/common.do?method=getLottoNumber"
    params = {"drwNo": draw_no}

    try:
        res = requests.get(url, params=params, headers=HEADERS, timeout=5)

        data = res.json()

        if data.get("returnValue") != "success":
            return []

        return [data.get(f"drwtNo{i}") for i in range(1, 7)]

    except:
        return []


# 🔥 최근 3회차 가져오기
def get_recent_3(latest):
    results = []

    for i in range(3):
        nums = get_lotto(latest - i)

        if nums:
            results.append(nums)

    return results


# ================= UI =================

st.title("🎰 최근 3회차 로또 조회기")

latest = st.number_input("최신 회차 입력", min_value=1, value=1100)

if st.button("📥 최근 3회차 가져오기"):

    recent = get_recent_3(latest)

    if not recent:
        st.error("❌ 데이터를 가져오지 못했습니다")
    else:
        st.success("데이터 로딩 성공!")

        for i, r in enumerate(recent):
            st.write(f"📌 {latest - i}회차: {r}")
