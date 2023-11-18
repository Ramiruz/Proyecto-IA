import requests
import sys
import time

arg_list= sys.argv
filename= arg_list[1]
language= arg_list[2]

upload_endpoint= "https://api.assemblyai.com/v2/upload"
headers= {"authorizathion": "46f3fc0a6e364888acf89978f15a5d24"}

def read_file(filename, chunk_size=5242880):
  with open(filename, 'rb') as _file:
    while True:
      data= _file.read(chunk_size)
      if not data:
        break
      yield data 

upload_response= requests.post(upload_endpoint, headers= headers, data= read_file())
print(upload_response.json())
audio_url= upload_response.json()['upload_url']

transcription_endpoint= "https://api.assemblyai.com/v2/transcript"

json= {"audio_url":audio_url, 
       "language_code":language}

transcription_response= requests.post(transcription_endpoint, headers= headers, json= json)
print(transcription_response,json())

transcript_id= transcription_response.json()['id']

polling_endpoint= transcription_endpoint + "/" + transcript_id

while True:
  polling_response= requests.get(polling_endpoint, headers= headers)
  polling_response.json()['status']

  if status == "completed":

    with open(language + "transcription.txt", "w") as f:
      f.write(polling_response.json()['text'])

  elif status == "error":
    print('The transcription has errored out!')
    break

  else:
    print(status)
    time.sleep(2)
    continue
