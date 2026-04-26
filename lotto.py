import streamlit as st
import requests
import random

st.set_page_config(page_title="로또 생성기", page_icon="🎰")

HEADERS = {"User-Agent": "Mozilla/5.0"}


# 🔹 로또 데이터 가져오기
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
def get_recent(draw_no):
    recent = []

    for i in range(3):
        nums = get_lotto(draw_no - i)
        if nums:
            recent.append(nums)

    return recent


# 🔹 번호 생성 (1~39, 최근 3회차 제외)
def generate(recent):
    all_nums = set(range(1, 40))
    used = set(n for r in recent for n in r)

    available = list(all_nums - used)

    if len(available) < 6:
        return None

    return sorted(random.sample(available, 6))


# ================= UI =================

st.title("🎰 로또 번호 생성기 (1~39)")

latest = st.number_input("최신 회차 입력", min_value=1, value=1100)

if st.button("📥 최근 3회차 불러오기"):
    st.session_state.recent = get_recent(latest)

# 세션 유지
recent = st.session_state.get("recent", [])

# 최근 데이터 출력
if recent:
    st.subheader("📅 최근 3회차 결과")

    for i, r in enumerate(recent):
        st.write(f"{latest - i}회차: {r}")

    st.divider()

    if st.button("🎯 번호 생성"):
        result = generate(recent)

        if result:
            st.success(f"추천 번호: {result}")
        else:
            st.error("사용 가능한 번호가 부족합니다.")

else:
    st.info("📥 먼저 '최근 3회차 불러오기' 버튼을 눌러주세요.")
