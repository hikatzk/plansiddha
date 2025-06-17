# core/gpt_client.py

# ==== 標準ライブラリ ====
import os

# ==== 外部ライブラリ ====
from openai import OpenAI
from dotenv import load_dotenv
from contextlib import nullcontext

# ==== 自作モジュール ====
from prompts.gpt_prompt import system_prompt, build_prompt

# ==== 設定 ====
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ==== GPT通信関数 ====
def send_to_gpt(case_data, mode="overview", spinner=None, show_json=None, notify=None):
    spinner_context = spinner("GPT-4oに送信中…") if spinner else nullcontext()
    with spinner_context:
        if show_json: show_json(case_data)
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": build_prompt(case_data, mode=mode)}
        ]
        response = client.chat.completions.create(model="gpt-4o", messages=messages)
        if notify: notify("✅ GPTからのコメントがありました。")
    return response.choices[0].message.content.strip()