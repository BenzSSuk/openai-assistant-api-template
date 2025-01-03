import os
import sys
from os.path import join as pjoin
from dotenv import load_dotenv

import streamlit as st
from openai.types.beta.threads import Text
from typing_extensions import override
from openai import AssistantEventHandler

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

load_dotenv()

class EventHandler(AssistantEventHandler):
    def init__custom(self):
        self.list_delta = []
        self.is_finished_response = False

    @override
    def on_text_created(self, text) -> None:
        print(f"\nassistant: start answering - ", end="", flush=True)

    @override
    def on_text_delta(self, delta, snapshot):
        self.is_finished_response = False
        print(delta.value, end="", flush=True)

    def on_text_done(self, text: Text):
        self.is_finished_response = True

    # def on_tool_call_created(self, tool_call):
    #     print(f"\nassistant > {tool_call.type}\n", flush=True)
    #
    # def on_tool_call_delta(self, delta, snapshot):
    #     if delta.type == 'code_interpreter':
    #         if delta.code_interpreter.input:
    #             print(delta.code_interpreter.input, end="", flush=True)
    #         if delta.code_interpreter.outputs:
    #             print(f"\n\noutput >", flush=True)
    #             for output in delta.code_interpreter.outputs:
    #                 if output.type == "logs":
    #                     print(f"\n{output.logs}", flush=True)
