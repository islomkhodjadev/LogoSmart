import requests


import os
from dotenv import load_dotenv

load_dotenv()



def try_3(url, headers, files, data):
    try:
        response = requests.post(url, headers=headers, files=files, data=data)
        if response.status_code == 200:
            return response.json()
        else:
            return False
    except requests.exceptions.Timeout:
        return False


def stt(content, api_key=os.getenv("mohirAi")):
    print(os.getenv("mohirAi"))
    url = 'https://mohir.ai/api/v1/stt'
    headers = {
        "Authorization": api_key
    }

    files = {
        # "file": ("audio.mp3", open(content, "rb")),
        "file": ("audio.mp3", content),
    }
    data = {
        "return_offsets": "true",
        "run_diarization": "false",
        "language": "uz",
        "blocking": "true",
    }

    for i in range(3):
        res = try_3(url, headers, files, data)
        if res:
            return res
    return res


# result = stt("audio.ogg")
# print(result)


# async def main():
#     print(stt("audio.ogg"))
    
    
# import asyncio

# asyncio.run(main())