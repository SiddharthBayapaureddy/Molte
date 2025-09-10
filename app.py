# Streamlit library for quick frontend development
import streamlit as st

from langchain_core.messages import HumanMessage, AIMessage

# Importing stuff from backend
from main import response, predefined_bot_personas, clear_persona_history


# Building page
st.set_page_config(page_title="Chatbot", page_icon="🤖", layout="centered")
st.title("Molte 🤖")
st.subheader("Built using LangChain and Groq")
st.write("Created by Siddharth")


# Persona selection tool
persona = st.sidebar.radio("Choose a Persona", list(predefined_bot_personas.keys()))

# Initializing session_state only once for storing msgs
if "messages" not in st.session_state:
    st.session_state.messages = []


if st.button("Clear chat"):
    st.session_state.messages = []
    clear_persona_history(persona)
    



# Printing previous msgs
for msg in st.session_state.messages:
    
    if isinstance(msg, HumanMessage):
        st.markdown("User: " + msg.content)

    elif isinstance(msg, AIMessage):
        st.markdown("Chatbot 🤖: " + msg.content)


# Input box for user query
if prompt := st.chat_input("Type your message..."):  # Placeholder
    
    # Adding new user msg
    st.session_state.messages.append(HumanMessage(content=prompt))
    st.markdown("User: " + prompt )

    # AAdding chatbot reply
    bot_reply = response(prompt, st.session_state.messages, persona)
    st.session_state.messages.append(bot_reply[-1])
    st.markdown("Chatbot 🤖: " + bot_reply[-1].content)