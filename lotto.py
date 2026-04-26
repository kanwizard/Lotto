import streamlit as st
import random

st.set_page_config(page_title="로또 생성기", page_icon="🎰")

st.title("🎰 로또 생성기 (연속번호 제한)")

# 조합 개수 입력
count = st.number_input("조합 개수", min_value=1, value=5, step=1)

# 🔥 제외할 번호
EXCLUDED_NUMBERS = {10, 20, 30}

# 🔥 연속번호 체크 함수
def has_consecutive(nums):
    nums = sorted(nums)

    for i in range(len(nums) - 1):
        if nums[i] + 1 == nums[i + 1]:
            return True

    return False


# 🔥 번호 생성 함수
def generate_numbers():
    pool = [n for n in range(1, 40) if n not in EXCLUDED_NUMBERS]

    while True:
        nums = random.sample(pool, 6)

        if not has_consecutive(nums):
            return sorted(nums)


# 버튼
if st.button("🎯 조합 생성"):

    results = []

    for _ in range(count):
        results.append(generate_numbers())

    st.subheader("📊 생성 결과")

    for i, r in enumerate(results, 1):
        st.write(f"{i}번: {r}")
