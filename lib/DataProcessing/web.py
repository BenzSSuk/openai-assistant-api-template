import os.path
import numpy as np
import requests
import json

def login_web_project(dict_authorize):
  url = dict_authorize["url"]
  payload_email = json.dumps(dict_authorize["email"])

  headers = {
    'Content-Type': 'application/json'
  }

  response = requests.request("POST", url, headers=headers, data=payload_email)
  # content_str = response.content.decode('utf-8')
  content_str = response.text
  content_dict = json.loads(content_str)
  authorization = content_dict["access_token"]

  return authorization, content_dict

def set_url_offset_limit(url, offset, limit):
  head, tail = os.path.split(url)
  new_offset_limit = f'volumes?offset={offset}&limit={limit}'

  url_newsetting = f'{head}/{new_offset_limit}'

  return  url_newsetting

def imread_url(url):
  # get image data and save
  response_img = requests.get(url)
  img_encode_bytes = response_img.content
  img_encode_uint8 = np.frombuffer(img_encode_bytes, dtype=np.uint8)

  return img_encode_uint8