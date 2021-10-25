from random import randint
from config import settings

def generate_random_code():
    code = ''
    length = settings.SMS.get('OTP_LENGTH') or 6
    for _ in range(length):
        code += f'{randint(0, 9)}'
    return code
