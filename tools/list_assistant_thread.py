import os
import sys
import subprocess as sp
from os.path import join as pjoin
from dotenv import load_dotenv

from openai import OpenAI

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
FOLDER_PROJECT = checkSysPathAndAppend(folderFile, 1)
FOLDER_CONFIG = os.path.join(FOLDER_PROJECT, 'config')

load_dotenv()

print("connecting to OpenAI...")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

print("")
print("list assistant...")

assist_object = client.beta.assistants.list()
count = 0
print(f"found {len(assist_object.data)} assistant")
for assist_data in assist_object.data:
    count += 1
    print(f'assistant {count}')
    print(f' name      : {assist_data.name}')
    print(f' id        : {assist_data.id}')
    print(f' created_at: {assist_data.created_at}')
    print(f' model     : {assist_data.model}')

print("#----- Finished -----#")