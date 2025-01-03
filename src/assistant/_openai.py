import os
import sys
from os.path import join as pjoin

import streamlit
from dotenv import load_dotenv

from openai import OpenAI
from typing_extensions import override
from openai import AssistantEventHandler
# from langchain.agents.openai_assistant import OpenAIAssistantRunnable

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
FOLDER_CONFIG = os.path.join(FOLDER_PROJECT, 'config')

load_dotenv()

from src.assistant._event_handler import *

class AssistantOpenAI:
    def __init__(self):
        print("connecting to OpenAI...")
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.assistant_id = os.getenv("ASSISTANT_ID")
        self.thread_id = os.getenv("THREAD_ID")

        print("retrieve assistant...")
        self.assistant = self.client.beta.assistants.retrieve(assistant_id=self.assistant_id)
        self.thread = self.client.beta.threads.retrieve(thread_id=self.thread_id)

    def get_chat_history(self):
        messages = self.client.beta.threads.messages.list(
            thread_id=self.thread_id
        )
        list_chat_history = []

        for message_data in messages.data:
            role = message_data.role
            for message_data_content in message_data.content:
                text = message_data_content.text.value

                dict_content = {
                    "role": role,
                    "text": text
                }
                list_chat_history.insert(0, dict_content)

        return list_chat_history

    def get_lasted_response(self):
        messages = self.client.beta.threads.messages.list(
            thread_id=self.thread_id
        )
        list_chat_lasted = []

        for i in range(0, 2):
            message_data = messages.data[i]
            role = message_data.role
            for message_data_content in message_data.content:
                text = message_data_content.text.value

                dict_content = {
                    "role": role,
                    "text": text
                }
                list_chat_lasted.insert(0, dict_content)
                # list_chat_lasted.append(dict_content)

        return list_chat_lasted

    def print_chat(self, list_chat):
        for dict_chat in list_chat:
            print(dict_chat['role'] + ':' + dict_chat['text'])

    def print_chat_history(self):
        list_chat_history = self.get_chat_history()
        self.print_chat(list_chat_history)

    def add_message_to_thread(self, user_prompt):
        self.lasted_prompt = self.client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role="user",
            content=user_prompt
        )

    def pre_prompt(self, user_prompt):
        self.add_message_to_thread(user_prompt)
        with self.client.beta.threads.runs.stream(
                thread_id=self.thread.id,
                assistant_id=self.assistant.id
        ) as stream:
            stream.until_done()

    def print_message_response_poll(self, user_prompt):
        self.add_message_to_thread(user_prompt)

        print("waiting response...")
        run = self.client.beta.threads.runs.create_and_poll(
            thread_id=self.thread_id,
            assistant_id=self.assistant_id
        )

        while True:
            if run.status == 'completed':
                list_lasted_response = self.get_lasted_response()
                self.print_chat(list_lasted_response)
                break
            else:
                print(run.status)

    def stream_message_response_callback(self, user_prompt):
        self.add_message_to_thread(user_prompt)
        with self.client.beta.threads.runs.stream(
                thread_id=self.thread.id,
                assistant_id=self.assistant.id,
                event_handler=EventHandler(),
        ) as stream:
            stream.until_done()

    def stream_message_response_event(self, user_prompt):
        self.add_message_to_thread(user_prompt)
        with self.client.beta.threads.runs.stream(
                thread_id=self.thread.id,
                assistant_id=self.assistant.id
        ) as stream:
            for event in stream:
                # Print the text from text delta events
                if event.event == "thread.message.delta" and event.data.delta.content:
                    delta = event.data.delta.content[0].text
                    response_word = delta.value
                    print(response_word)

    def stream_message_response_generator(self, user_prompt):
        # use with streamlit for incremental print response message
        # stream = st.session_state.my_assistant.stream_message_response_generator(prompt)
        # st.write_stream(stream)
        self.add_message_to_thread(user_prompt)
        with self.client.beta.threads.runs.stream(
                thread_id=self.thread.id,
                assistant_id=self.assistant.id
        ) as stream:
            for event in stream:
                # Print the text from text delta events
                if event.event == "thread.message.delta" and event.data.delta.content:
                    delta = event.data.delta.content[0].text
                    yield delta.value
