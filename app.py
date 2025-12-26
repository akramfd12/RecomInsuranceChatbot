from chatbot.chatbot import *
from chatbot.config import *
from chatbot.tools import *
from chatbot.functions import *
from langchain_core.messages import HumanMessage, AIMessage
import streamlit as st
import uuid


# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="InsuraBot",
    page_icon="🤖",
    layout="centered"
)

st.title("InsuraBot")
st.write("Chatbot From Insura Insurance")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
if "thread_id" not in st.session_state:
    st.session_state.thread_id = "user_session_1"

# Sidebar
st.sidebar.title("InsuraBot")

#chat pembuka
st.chat_message("assistant").markdown(
"""
👋 **Selamat datang di InsuraBot**

Silakan pilih informasi yang Anda butuhkan:

Informasi Produk Asuransi  
Informasi Kepesertaan  
Informasi Klaim 
"""
)


#tombol bersihkan layar
if st.sidebar.button("Clear Chat"):
    if "thread_id" in st.session_state:
        tid = st.session_state.thread_id
        if tid in checkpointer.storage:
            del checkpointer.storage[tid]

    st.session_state.thread_id = str(uuid.uuid4())
    st.session_state.messages = []
    st.rerun()

with st.sidebar.expander("Example ID"):
    st.write("Policy Number: PLS-HEALTH-001")
    st.write("Policy Number: PLS-VEHICLE-002")
    st.write("Claim Number: cl0001")
    st.write("Claim Number: cl0002")

# Display chat messages from history
for message in st.session_state.messages:
    role = "user" if isinstance(message, HumanMessage) else "assistant"
    with st.chat_message(role):
        st.markdown(message.content)

# React to user input
if prompt := st.chat_input("Ask something..."):
    # Create HumanMessage
    user_message = HumanMessage(content=prompt)
    st.chat_message("user").markdown(user_message.content)
    st.session_state.messages.append(user_message)

    # Display "thinking..." sementara menunggu response
    thinking_msg = st.empty()
    thinking_msg.markdown("_Thinking..._")

    # Invoke agent
    result = app.invoke({"messages": [user_message]},
                          {"configurable": {"thread_id": st.session_state.thread_id}} 
                          )

    # Ambil jawaban dari agent, contoh pakai result['messages'] atau result['output']
    # Sesuaikan dengan struktur output agentmu
    if "messages" in result:
        ai_content = result["messages"][-1].content
    else:
        ai_content = str(result)

    ai_message = AIMessage(content=ai_content)
    with st.chat_message("assistant"):
        st.markdown(ai_message.content)
    st.session_state.messages.append(ai_message)

    #Token Usage
    with st.sidebar.expander("Token Usage"):    
        token_information = token_usage(ai_message=result["messages"][-1])
        for key, value in token_information.items():
            token = f"{key} = {value}"
            st.write(token)
    
    #tool calss information
    with st.sidebar.expander("Tools Call"):
        tool_information = extract_tool_calls(result)
        st.write(tool_information)


