import os
import sys
from os.path import join as pjoin

from openai import OpenAI
from dotenv import load_dotenv

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
folder_data = pjoin(FOLDER_PROJECT, 'data')

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

vector_storage_data = client.beta.vector_stores.list()
count = 0
print(f"found {len(vector_storage_data.data)} vector storage")
for vs_data in vector_storage_data.data:
    count += 1
    print(f'vector storage {count}')
    print(f' name      : {vs_data.name}')
    print(f' id        : {vs_data.id}')
    print(f' created_at: {vs_data.created_at}')