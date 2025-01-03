import streamlit as st
import os
import sys

def checkSysPathAndAppend(path, stepBack=0):
  if stepBack > 0:
    for istep in range(stepBack):
      if istep == 0:
        pathStepBack = path
      pathStepBack, filename = os.path.split(pathStepBack)
  else:
    pathStepBack = path

  if not pathStepBack in sys.path:
    sys.path.append(pathStepBack)

  return pathStepBack

folderFile, filename = os.path.split(os.path.realpath(__file__))
FOLDER_PROJECT = checkSysPathAndAppend(folderFile, 2)

from src.assistant import *

st.title("Video understanding demo v0.1")

if "my_assistant" not in st.session_state:
    st.session_state.my_assistant = AssistantOpenAI()
    st.session_state.my_assistant.pre_prompt("user will ask about video information or "
                                             "event that occur in vector store"
                                             "please find information in vector store")

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
        stream = st.session_state.my_assistant.stream_message_response_generator(prompt)
        response = st.write_stream(stream)

    # chat of history of assistant
    st.session_state.messages.append({"role": "assistant", "content": response})
