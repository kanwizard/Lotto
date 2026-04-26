import streamlit as st
import random

st.set_page_config(page_title="로또 랜덤 생성기", page_icon="🎰")

st.title("🎰 완전 랜덤 로또 생성기 (1~39)")

count = st.number_input("생성 개수", min_value=1, value=5)

if st.button("🎯 생성하기"):
    results = []

    for _ in range(count):
        numbers = sorted(random.sample(range(1, 40), 6))
        results.append(numbers)

    st.subheader("📊 결과")

    for i, r in enumerate(results, 1):
        st.write(f"{i}번: {r}")
