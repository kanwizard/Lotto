import streamlit as st
import requests
import random

st.set_page_config(page_title="로또 추천 시스템", page_icon="🎰")

HEADERS = {"User-Agent": "Mozilla/5.0"}


# ==============================
# 🔥 로또 API (안정 버전)
# ==============================
def get_lotto(draw_no):
    url = "https://www.dhlottery.co.kr/common.do?method=getLottoNumber"
    params = {"drwNo": draw_no}

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        res = requests.get(url, params=params, headers=headers, timeout=5)

        # 🔥 상태 체크
        if res.status_code != 200:
            return []

        # 🔥 JSON 안전 파싱
        try:
            data = res.json()
        except:
            return []

        # 🔥 구조 검증
        if not isinstance(data, dict):
            return []

        if data.get("returnValue") != "success":
            return []

        # 🔥 숫자 추출 안전 처리
        numbers = []
        for i in range(1, 7):
            value = data.get(f"drwtNo{i}")
            if value is None:
                return []
            numbers.append(value)

        return numbers

    except Exception:
        return []


# ==============================
# 🔥 최근 3회차
# ==============================
def get_recent_3(latest):
    results = []

    for i in range(3):
        nums = get_lotto(latest - i)
        if nums:
            results.append(nums)

    return results


# ==============================
# 🔥 추천 번호 생성 (1~39, 최근 번호 제외)
# ==============================
def generate_numbers(recent):
    all_numbers = set(range(1, 40))

    used = set(n for r in recent for n in r)

    available = list(all_numbers - used)

    if len(available) < 6:
        return None

    return sorted(random.sample(available, 6))


# ==============================
# UI
# ==============================

st.title("🎰 실사용 로또 추천 시스템")

latest = st.number_input("최신 회차 입력", min_value=1, value=1100)

col1, col2 = st.columns(2)

# ------------------------------
# 최근 3회차 조회 버튼
# ------------------------------
with col1:
    if st.button("📥 최근 3회차 가져오기"):

        recent = get_recent_3(latest)

        st.session_state.recent = recent

        if not recent:
            st.error("데이터를 가져오지 못했습니다.")
        else:
            st.success("최근 3회차 로딩 완료!")

# ------------------------------
# 번호 생성 버튼
# ------------------------------
with col2:
    if st.button("🎯 추천 번호 생성"):

        recent = st.session_state.get("recent", [])

        if not recent:
            st.warning("먼저 최근 3회차를 불러오세요")
        else:
            result = generate_numbers(recent)

            if result:
                st.success(f"추천 번호: {result}")
            else:
                st.error("가능한 번호가 부족합니다.")


# ==============================
# 최근 데이터 출력
# ==============================
if "recent" in st.session_state and st.session_state.recent:

    st.divider()
    st.subheader("📅 최근 3회차 데이터")

    for i, r in enumerate(st.session_state.recent):
        st.write(f"{latest - i}회차: {r}")
