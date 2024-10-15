import requests
from dotenv import load_dotenv, set_key
import os


def get_auth_token(email, password):
    url = "https://notify.eskiz.uz/api/auth/login"
    payload = {"email": email, "password": password}

    response = requests.post(url, data=payload)

    if response.status_code == 200:
        token = response.json().get("data").get("token")

        env_file_path = ".env"
        load_dotenv(env_file_path)
        set_key(env_file_path, "otpToken", token)
        return token
    else:
        raise Exception(
            f"Failed to get token, status code: {response.status_code}, response: {response.text}"
        )


email = "dilbarmatkasimova@gmail.com"
password = "FTSvLtpofq5kjTSlonVAv7nKOEc5bI4ctSyd4iPO"
token = get_auth_token(email, password)
