import streamlit as st
import google.generativeai as genai
from typing import List, Dict

# 페이지 기본 설정
st.set_page_config(
    page_title="Gemini Chat",
    page_icon="🤖",
    layout="wide"
)

# Gemini API 설정
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# 세션 상태 초기화
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "messages" not in st.session_state:
    st.session_state.messages = []

def initialize_chat() -> genai.ChatSession:
    """채팅 세션을 초기화하고 반환합니다."""
    return model.start_chat(history=[])

def add_message(role: str, content: str):
    """채팅 히스토리에 새 메시지를 추가합니다."""
    st.session_state.messages.append({"role": role, "content": content})

def display_chat_history():
    """채팅 히스토리를 화면에 표시합니다."""
    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]
        
        if role == "user":
            st.chat_message("user").write(content)
        else:
            st.chat_message("assistant").write(content)

def main():
    # 헤더
    st.title("🤖 Gemini Chat")
    st.markdown("---")
    
    # 채팅 세션 초기화
    if "chat" not in st.session_state:
        st.session_state.chat = initialize_chat()
    
    # 채팅 히스토리 표시
    display_chat_history()
    
    # 사용자 입력
    if prompt := st.chat_input("메시지를 입력하세요..."):
        # 사용자 메시지 추가
        add_message("user", prompt)
        
        try:
            # Gemini 응답 생성
            response = st.session_state.chat.send_message(prompt)
            
            # AI 응답 추가
            add_message("assistant", response.text)
            
            # 채팅 히스토리 업데이트
            st.session_state.chat_history.append({
                "user": prompt,
                "assistant": response.text
            })
            
        except Exception as e:
            st.error(f"오류가 발생했습니다: {str(e)}")
            return
        
        # 화면 새로고침하여 새 메시지 표시
        st.rerun()

if __name__ == "__main__":
    main()
