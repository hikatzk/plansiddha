# ==== 標準ライブラリ ====
import os
import json

# ==== 外部ライブラリ ====
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

# ==== 自作モジュール ====
from gpt_prompt import system_prompt, build_prompt  # GPTのプロンプト定義
from ui.eqd2_inputs import render_eqd2_form

# ==== 設定 ====
VERSION = "0.6.0"
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ==== 表示用ラベル定義 ====
mode_labels = {"overview": "症例背景の整理", "design": "照射設計の検討", "toxicity": "副作用・予後の予測"}

# ==== Streamlitページ構成 ====
st.set_page_config(page_title=f"PlanSiddha | {VERSION}", page_icon="🕉️", layout="wide")
st.title(f"PlanSiddha")
st.caption(f"ver. {VERSION}")
app_mode = st.sidebar.radio("モード選択", ["照射設計チャット", "再照射支援", "その他モード"])
top_message = st.empty()  # 成功メッセージなどを画面上部に出す用

# ==== GPT通信関数 ====
def send_to_gpt(case_data, mode="overview"):
    """症例データをGPTへ送信し、フィードバックを取得する。"""
    with st.spinner("GPT-4oに送信中…"):
        with st.expander("📤 送信内容（確認用）", expanded=False):
            st.json(case_data)
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": build_prompt(case_data, mode=mode)}
        ]
        response = client.chat.completions.create(model="gpt-4o", messages=messages)
    top_message.success(f"✅ GPTからのコメントがありました。")
    return response.choices[0].message.content.strip()

# ==== プラン検討フォーム ====
def render_plan_form():
    """照射設計を入力し、GPTに議論を依頼するフォーム。"""
    with st.form("plan_form"):
        col1, col2, col3 = st.columns([2, 3, 3])

        # ◀️ 左：症例背景（S/O）
        with col1:
            st.subheader("📝 症例情報")
            case_data = {}
            case_data["age"] = st.number_input("年齢", min_value=0, max_value=129, step=1)
            case_data["sex"] = st.radio("性別", ["男性", "女性"], horizontal=True)
            case_data["disease"] = st.text_input("疾患名", placeholder="例：中咽頭癌")
            case_data["staging"] = st.text_input("病期", placeholder="例：cT2N1M0")            
            case_data["treatment_plan"] = st.radio("治療目的", ["根治照射", "緩和照射", "その他"], horizontal=False)
            case_data["irradiation_history"] = st.radio("照射歴", ["なし", "別部位にあり", "重複あり"], horizontal=False)
            case_data["comorbidity"] = st.text_area("合併症", height=80, placeholder="例：腎不全")
            case_data["concurrent_therapy"] = st.text_area("併用療法", height=80, placeholder="例：CDDP併用")

        # ◀️ 中央：治療設計（A/P）
        with col2:
            st.subheader("📐 照射設計案")
            case_data["target_plan"] = st.text_area("ターゲット設計", height=200, placeholder="例：\n左舌根部原発、左II領域LN転移。\n予防域を含む両側全頚部照射")
            case_data["dose_plan"] = st.text_input("処方線量、線量分割", placeholder="例：70Gy/35Fr、D50処方")
            case_data["question"] = st.text_area("気になる点・議論したいこと", height=200, placeholder="例：CTVの範囲が妥当か、Boost必要か？")
            case_data["irradiation_technique"] = st.radio("照射方法", ["3D-CRT", "IMRT", "SRT", "その他"], horizontal=False)
            case_data["gpt_mode"] = st.radio("GPTに聞きたいことは？", ["overview", "design", "toxicity"], format_func=lambda x: mode_labels.get(x, x), horizontal=False)
            st.session_state["gpt_mode"] = case_data["gpt_mode"] 
            submitted = st.form_submit_button("GPTに送信")

    if submitted:
        st.session_state["gpt_feedback"] = send_to_gpt(case_data, mode=case_data["gpt_mode"])

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

if app_mode == "照射設計チャット":
    render_plan_form()
elif app_mode == "再照射支援":
    render_eqd2_form()
else:
    st.info("今後のモードをここに追加していく予定です。")