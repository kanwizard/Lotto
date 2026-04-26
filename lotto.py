import streamlit as st
import random

st.title("🎰 로또 번호 생성기 (1~39)")

col1, col2 = st.columns(2)

with col1:
    if st.button("1세트 생성"):
        st.session_state.result = sorted(random.sample(range(1, 40), 6))

with col2:
    if st.button("5세트 생성"):
        st.session_state.result = [
            sorted(random.sample(range(1, 40), 6)) for _ in range(5)
        ]

if "result" in st.session_state:
    st.subheader("🎯 결과")
    st.write(st.session_state.result)
