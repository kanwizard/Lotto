import streamlit as st
import random


# 로그인 기능 추가
def login():
    st.title("🔐 로그인")
    password = st.text_input("비밀번호를 입력하세요", type="password")
    
    # 비밀번호 확인 버튼
    if st.button("확인"):
        if password == "860716":  # 원하는 비밀번호로 변경 가능
            st.success("로그인 성공!")
            st.session_state.logged_in = True  # 로그인 상태 저장
            return True
        else:
            st.error("비밀번호가 틀렸습니다.")
            return False
    return False  # 로그인 상태가 아닐 경우 계속 대기


st.set_page_config(page_title="로또 생성기", page_icon="🎰")

st.title("🎰 로또 생성기 (연속번호 제한)")

# 조합 개수 입력
count = st.number_input("조합 개수", min_value=1, value=5, step=1)


# 🔥 연속번호 체크 함수
def has_consecutive(nums):
    nums = sorted(nums)

    for i in range(len(nums) - 1):
        if nums[i] + 1 == nums[i + 1]:
            return True

    return False


# 🔥 번호 생성 함수
def generate_numbers():
    while True:
        nums = random.sample(range(1, 40), 6)

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
