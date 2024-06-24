__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import streamlit as st
import os
from groq import Groq
import warnings

# Configure your environment
os.environ['GROQ_API_KEY'] = st.secrets['GROQ_API_KEY'] 
warnings.filterwarnings("ignore")
st.title("LLM - AI 4 CI")

client = Groq()

if "groq_model" not in st.session_state:
    st.session_state["groq_model"] = "llama3-8b-8192"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        chat_completion = client.chat.completions.create(
            temperature=0,
            model=st.session_state["groq_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=False,
            stop=None,
            top_p=1,
            
        )
        response = chat_completion.choices[0].message.content
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})


