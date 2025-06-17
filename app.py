# ==== 標準ライブラリ ====
import os
import json

# ==== 外部ライブラリ ====
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

# ==== 自作モジュール ====
from ui.plan_form import render_plan_form
from ui.eqd2_form import render_eqd2_form

# ==== 設定 ====
VERSION = "0.9.1"

# ==== Streamlitページ構成 ====
st.set_page_config(page_title=f"PlanSiddha | {VERSION}", page_icon="🕉️", layout="wide")
st.title(f"PlanSiddha")
st.caption(f"ver. {VERSION}")
app_mode = st.sidebar.radio("モード選択", ["照射設計チャット", "再照射支援", "その他モード"], index=0)
top_message = st.empty()  # 成功メッセージなどを画面上部に出す用

# ==== GPT応答モードのラベル定義 ====
mode_labels = {"overview": "症例背景の整理", "design": "照射設計の検討", "toxicity": "副作用・予後の予測"}

if app_mode == "照射設計チャット":
    render_plan_form(mode_labels, top_message=top_message)
elif app_mode == "再照射支援":
    render_eqd2_form()
else:
    st.info("今後のモードをここに追加していく予定です。")