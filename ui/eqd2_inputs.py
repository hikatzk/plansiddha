# ui/eqd2_inputs.py

import streamlit as st
from eqd2_utils import calc_eqd2

def render_eqd2_form():
    st.subheader("🔁 再照射 EQD2 換算")

    col1, col2, col3 = st.columns(3)

    with col1:
        D = st.number_input("総線量(Gy)", min_value=0.1, value=60.0, step=0.1, format="%.1f")
    with col2:
        d = st.number_input("1回線量(Gy)", min_value=0.1, value=2.0, step=0.1, format="%.2f")
    with col3:
        ab = st.number_input("α/β比（Gy）", min_value=0.1, value=3.0, step=0.1, format="%.1f")
    
    if st.button("EQD2を計算"):
        eqd2 = calc_eqd2(D, d, ab)
        st.success(f"EQD2: **{eqd2:.2f} Gy**")