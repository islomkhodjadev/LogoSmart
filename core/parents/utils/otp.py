from dotenv import load_dotenv

from random import randint
from django.core.cache import cache
import requests

from django.contrib.auth import get_user_model
import os

load_dotenv()


class OTP:

    def __init__(self, username: str, phone_number: str):
        self.phone_number = phone_number
        self.code = randint(1000, 9999)
        self.message_sid = None
        self.user_name = username

        cache.set(self.user_name, self.code)

    def send_code(self):

        headers = {"Authorization": f"Bearer {os.getenv("otpToken")}"}

        data = {
            "mobile_phone": self.phone_number,
            "message": f"Kodni hech kimga bermang! LogoSmart mobil ilovasi ga kirish uchun tasdiqlash kodi: {self.code}",
            "from": "4546",
        }

        send = requests.post(
            url="http://notify.eskiz.uz/api/message/sms/send/",
            data=data,
            headers=headers,
        )

    @staticmethod
    def verify(instance: get_user_model(), code: int):

        actual_code = cache.get(instance.username, default=None)

        if actual_code is not None:
            if int(actual_code) == int(code):
                instance.is_active = True
                instance.save()
                return True
            return False
        return None
