from openai import OpenAI
import streamlit as st

st.title("")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o"

system_message = '''
너는 항상 반말을 하는 챗봇이야. 다나까나 요 같은 높임말로 절대 끝내지마.
반말로 대답하되, 친근하게 대답해줘. 영어로 질문해도 무조건 한글로 답변해줘.
모든 답변 끝에는 답변에 알맞는 이모티콘도 추가해줘.
'''

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_message}]

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})