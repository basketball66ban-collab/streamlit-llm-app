from dotenv import load_dotenv
load_dotenv()

import os
import streamlit as st
from langchain_community.chat_models import ChatOpenAI  # 最新バージョンに対応
from langchain.schema import SystemMessage, HumanMessage

# --- LLM の初期化 ---
llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

# --- 専門家回答関数 ---
def get_expert_response(user_input: str, expert: str) -> str:
    """ユーザー入力と専門家の選択に応じてLLMの回答を返す"""
    
    if expert == "専門家A（栄養士）":
        system_prompt = (
            "あなたは優秀な栄養士です。"
            "食事、栄養バランス、健康管理について専門的に答えてください。"
        )
    else:  # 専門家B（トレーナー）
        system_prompt = (
            "あなたは優秀なパーソナルトレーナーです。"
            "運動、筋トレ、姿勢改善について専門的に答えてください。"
        )

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_input)
    ]

    result = llm(messages)
    return result.content

# --- Streamlit UI ---
st.title("💬 2人の専門家に相談アプリ")

st.markdown("""
このアプリでは、2人の専門家に質問をすることができます。  
1. 上のラジオボタンで相談したい専門家を選んでください  
2. 入力フォームに質問を入力し、「送信」ボタンを押してください  
3. 選んだ専門家としての回答が表示されます
""")

# 専門家の選択
expert_choice = st.radio(
    "相談したい専門家を選んでください：",
    ["専門家A（栄養士）", "専門家B（トレーナー）"]
)

# 入力フォーム
with st.form("user_input_form"):
    user_input = st.text_input("質問を入力してください")
    submitted = st.form_submit_button("送信")

    if submitted and user_input.strip():
        response = get_expert_response(user_input, expert_choice)
        st.markdown("### 🧑‍⚕️ 回答")
        st.write(response)
