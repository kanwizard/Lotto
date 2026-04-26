import streamlit as st
import random

st.set_page_config(page_title="로또 추천기", page_icon="🎰")

st.title("🎰 패턴 + 최근 3회차 제외 로또 생성기")


import requests

HEADERS = {"User-Agent": "Mozilla/5.0"}


# 🔥 회차 1개 조회
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


# 🔥 최근 3회차 자동 가져오기 (여기가 핵심)
def get_recent_3(latest):
    results = []

    for i in range(3):
        nums = get_lotto(latest - i)

        # 정상 데이터만 추가
        if nums and len(nums) == 6:
            results.append(nums)

    return results


# =========================
# 🔥 유틸 함수
# =========================
def has_consecutive(nums):
    nums = sorted(nums)
    return any(nums[i] + 1 == nums[i + 1] for i in range(len(nums) - 1))


def check_odd_even(nums):
    odd = sum(1 for n in nums if n % 2 == 1)
    even = 6 - odd
    return odd, even


def get_pools(excluded):
    full = set(range(1, 40))
    available = list(full - set(excluded))
    return available


# =========================
# 🔥 생성 로직
# =========================
def generate(recent_numbers):

    excluded = set(n for r in recent_numbers for n in r)
    pool = get_pools(excluded)

    if len(pool) < 6:
        return None

    while True:
        nums = random.sample(pool, 6)

        # 홀짝 3:3
        odd, _ = check_odd_even(nums)
        if odd != 3:
            continue

        # 연속번호 제거
        if has_consecutive(nums):
            continue

        return sorted(nums)


# =========================
# UI
# =========================

latest = st.number_input("최신 회차 입력", min_value=1, value=1100)

count = st.number_input("조합 개수", min_value=1, value=5)

# 🔥 최근 3회차 불러오기 (버튼)
if st.button("📥 최근 3회차 가져오기"):

    recent = get_recent_3(latest)
    st.session_state.recent = recent

    st.subheader("📅 최근 3회차")

    for i, r in enumerate(recent):
        st.write(f"{latest - i}회차: {r}")


# 🔥 추천 생성
if st.button("🎯 추천 생성"):

    recent = st.session_state.get("recent", [])

    if not recent:
        st.warning("먼저 최근 3회차를 불러오세요")
        st.stop()

    results = []

    for _ in range(count):
        results.append(generate(recent))

    st.subheader("📊 추천 결과")

    for i, r in enumerate(results, 1):
        st.write(f"{i}번: {r}")
