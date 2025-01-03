import os
import sys
from os.path import join as pjoin

from openai import OpenAI
from dotenv import load_dotenv
import argparse

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

# Ready the files for upload to OpenAI
path_file = pjoin(folder_data, 'content', 'object_detection', 'video_user_upload.json')

parser = argparse.ArgumentParser(
                    prog='upload file to vector storage',
                    description='upload file to vector storage',
                    epilog='Text at the bottom of help')    # positional argument
parser.add_argument('-path', '--path', default=path_file)  # on/off flag
args = parser.parse_args()

file_paths = [path_file]
file_streams = [open(path, "rb") for path in file_paths]

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
  vector_store_id=os.getenv('VECTOR_ID'), files=file_streams
)

# You can print the status and the file counts of the batch to see the result of this operation.
print(file_batch.status)
print(file_batch.file_counts)