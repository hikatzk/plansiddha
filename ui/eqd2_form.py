# ui/eqd2_form.py

# ==== 標準ライブラリ ====
import json

# ==== 外部ライブラリ ====
import streamlit as st

# ==== 自作モジュール ====
from eqd2_utils import calc_eqd2

# ==== JSON読み込み====
with open("data/oar_constraints.json", "r") as f:
    oar_data = json.load(f)

def render_eqd2_form():
    st.subheader("🔢 EQD2計算")

    irradiated = st.radio("照射歴", ["なし", "あり"], horizontal=True)
    
    col1, col2, col3= st.columns([1,2,1])
    with col1:
        oar_list = list(oar_data.keys())
        selected_oar = st.selectbox("評価するOARを選択", oar_list)
        ab_default = oar_data[selected_oar]["alpha_beta"]
        eqd2_limit = oar_data[selected_oar]["eqd2_limit"]
    with col2:
        with st.container():
            dose_col, fr_col = st.columns([1, 1])
            with dose_col:
                D = st.number_input("総線量(Gy)", min_value=0.1, value=30.0, step=1.0, format="%.1f")
            with fr_col:
                fr = st.number_input(f"分割数", min_value=1, value=10, step=1)
            st.caption(f"1回線量 ≒ {D / fr:.2f}Gy/Fr")

        if irradiated == "あり":
            with st.container():
                dose_prev_col, fr_prev_col = st.columns([1, 1])
                with dose_prev_col:
                    D_prev  = st.number_input("前回の総線量(Gy)", min_value=0.1, value=1.0, step=1.0, format="%.1f")
                with fr_prev_col:
                    fr_prev = st.number_input("前回の分割数", min_value=1, value=1, step=1, key="previous_fr")
                st.caption(f"前回の1回線量 ≒ {D_prev / fr_prev:.2f}Gy/Fr")

    with col3:
        ab = st.number_input("α/β比（Gy）", min_value=0.1, value=ab_default, step=0.1, format="%.1f")
        st.markdown(f"🔖 許容EQD2上限: **{eqd2_limit} Gy**")

    if st.button("EQD2を計算"):
        eqd2_current = calc_eqd2(D, fr, ab)
        if irradiated == "あり":
            eqd2_prev = calc_eqd2(D_prev, fr_prev, ab)
            eqd2_total = eqd2_current + eqd2_prev

            st.success(f"📊 合算EQD2: **{eqd2_total:.2f} Gy** (今回**{eqd2_current:.2f}Gy** + 前回**{eqd2_prev:.2f}Gy**)")
            if eqd2_current + eqd2_prev > eqd2_limit:
                st.error(f"⚠️ 許容値超過：上限 {eqd2_limit} Gy を超えています")
            else:
                st.info(f"✅ 許容範囲内です（上限 {eqd2_limit} Gy）")
        else:
            st.success(f"今回のEQD2: **{eqd2_current:.2f} Gy**")
            if eqd2_current > eqd2_limit:
                st.error(f"⚠️ 許容値超過：上限 {eqd2_limit} Gy を超えています")
            else:
                st.info(f"✅ 許容範囲内です（上限 {eqd2_limit} Gy）")