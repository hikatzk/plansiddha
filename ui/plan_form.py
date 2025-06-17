# ui/plan_form.py

# ==== 外部ライブラリ ====
import streamlit as st

# ==== 自作モジュール ====
from core.gpt_client import send_to_gpt

# ==== プラン検討フォーム ====
def render_plan_form(mode_labels, top_message):
    """照射設計を入力し、GPTに議論を依頼するフォーム。"""
    with st.form("plan_form"):
        col1, col2, col3 = st.columns([2, 3, 3])

        # ◀️ 左：症例背景（S/O）
        with col1:
            st.subheader("📝 症例情報")
            case_data = {}
            case_data["age"] = st.number_input("年齢", min_value=0, max_value=129, value=60, step=1)
            case_data["sex"] = st.radio("性別", ["男性", "女性"], horizontal=True)
            case_data["disease"] = st.text_input("疾患名", placeholder="例：中咽頭癌")
            case_data["staging"] = st.text_input("病期", placeholder="例：cT2N1M0")            
            case_data["treatment_plan"] = st.radio("治療目的", ["根治照射", "緩和照射", "その他"], horizontal=False)
            case_data["irradiation_history"] = st.radio("照射歴", ["なし", "別部位にあり", "重複あり"], horizontal=False)
            case_data["comorbidity"] = st.text_area("合併症", height=80, placeholder="例：腎不全")
            case_data["concurrent_therapy"] = st.text_area("併用療法", height=80, placeholder="例：CDDP併用")

        # ◀️ 中央：治療設計（A/P）
        with col2:
            st.subheader("📐 照射計画")
            case_data["target_plan"] = st.text_area("ターゲット設計", height=200, placeholder="例：\n左舌根部原発、左II領域LN転移。\n予防域を含む両側全頚部照射")
            case_data["dose_plan"] = st.text_input("処方線量、線量分割", placeholder="例：70Gy/35Fr")
            case_data["question"] = st.text_area("気になる点・議論したいこと", height=200, placeholder="例：CTVの範囲が妥当か、Boost必要か？")
            case_data["irradiation_technique"] = st.radio("照射方法", ["3D-CRT", "IMRT", "SRT", "その他"], horizontal=False)
            case_data["gpt_mode"] = st.radio("GPTに聞きたいことは？", ["overview", "design", "toxicity"], format_func=lambda x: mode_labels.get(x, x), horizontal=False)
            st.session_state["gpt_mode"] = case_data["gpt_mode"] 
            submitted = st.form_submit_button("GPTに送信")

    if submitted:
        st.session_state["gpt_feedback"] = send_to_gpt(
            case_data,
            mode=case_data["gpt_mode"],
            spinner=st.spinner,
            show_json=lambda d: st.expander("📤 送信内容（確認用）", expanded=False).json(d),
            notify=top_message.success
        )

    # ▶️ 右：GPT応答
    with col3:
        feedback = st.session_state.get("gpt_feedback")
        if feedback:
            selected_mode = st.session_state.get("gpt_mode", "design")
            st.subheader(f"💬 GPTからのコメント（{mode_labels.get(selected_mode, '検討')}）")
            st.markdown(feedback, unsafe_allow_html=False)
        else:
            st.subheader("💬 GPTからのコメント")
            st.markdown("ここにコメントが表示されます", unsafe_allow_html=False)
