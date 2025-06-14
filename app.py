# ==== 標準ライブラリ ====
import os

# ==== 外部ライブラリ ====
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

# ==== 自作モジュール ====
from gpt_prompt import system_prompt, build_prompt  # GPTのプロンプト定義

# ==== 設定 ====
VERSION = "ver.0.1.0"
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ==== Streamlitページ構成 ====
st.set_page_config(layout="wide")
st.title(f"🕉️ PlanSiddha | {VERSION}")
top_message = st.empty()  # 成功メッセージなどを画面上部に出す用

# ==== GPT通信関数 ====
def send_to_gpt(case_data, message="GPT-4oに送信中…"):
    """症例データをGPTへ送信し、フィードバックを取得する。"""
    with st.spinner(message):
        with st.expander("📤 送信内容（確認用）", expanded=False):
            st.json(case_data)
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": build_prompt(case_data)}
    ]
    response = client.chat.completions.create(model="gpt-4o", messages=messages)
    top_message.success(f"✅ GPTからのコメントがありました。")
    return response.choices[0].message.content.strip()

# ==== プラン検討フォーム ====
def render_plan_form():
    """照射設計を入力し、GPTに議論を依頼するフォーム。"""
    with st.form("plan_form"):
        col1, col2, col3 = st.columns([1, 2, 2])

        # ◀️ 左：症例背景（S/O）
        with col1:
            st.subheader("🧍‍♂️ 症例情報")
            age = st.number_input("年齢", min_value=0, max_value=129, step=1)
            sex = st.radio("性別", ["男性", "女性"], horizontal=True)
            disease = st.text_input("疾患名", placeholder="例：中咽頭癌")
            staging = st.text_input("病期", placeholder="例：cT2N1M0")            
            treatment_plan = st.radio("治療目的", ["根治照射", "緩和照射", "その他"], horizontal=True)
            comorbidity = st.text_area("合併症", height=80, placeholder="例：腎不全")
            other_treatment = st.text_area("併用療法", height=80, placeholder="例：CDDP併用")

        # ◀️ 中央：治療設計（A/P）
        with col2:
            st.subheader("📐 照射設計案")
            target_plan = st.text_area("ターゲット設計", height=150, placeholder="左舌根部原発、左II領域LN転移。予防域含む全頚部照射")
            dose_plan = st.text_input("処方線量、線量分割", placeholder="例：70Gy/35Fr")
            question = st.text_area("気になる点・議論したいこと", height=80, placeholder="例：CTVの範囲が妥当か、Boost必要か？")
            device = st.text_input("使用機器・照射法（任意）", placeholder="例：Tomotherapy, VMAT など")
            submitted = st.form_submit_button("GPTに送信")

    gpt_feedback = ""
    if submitted:
        case_data = {
            "age": age,
            "sex": sex,
            "disease": disease,
            "staging": staging,
            "treatment_plan": treatment_plan,
            "comorbidity": comorbidity,
            "other_treatment": other_treatment,
            "target_plan": target_plan,
            "dose_plan": dose_plan,
            "question": question,
            "device": device,
        }
        gpt_feedback = send_to_gpt(case_data)

    # ▶️ 右：GPT応答
    with col3:
        st.subheader("💬 GPTからのコメント")
        st.markdown(gpt_feedback, unsafe_allow_html=False)

render_plan_form()