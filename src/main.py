import os
import sys
import subprocess as sp
from os.path import join as pjoin
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
FOLDER_PROJECT = checkSysPathAndAppend(folderFile, 1)
FOLDER_CONFIG = os.path.join(FOLDER_PROJECT, 'config')

filename_ui = 'chatbot.py'
folder_file = pjoin(FOLDER_PROJECT, 'src', 'ui')
path_file = pjoin(folder_file, filename_ui)
sp.run(['streamlit', 'run', path_file])
