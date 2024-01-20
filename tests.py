import re

phone_pattern = re.compile(r'^\+7\(\d{3}\)-\d{3}-\d{2}-\d{2}$')
if not phone_pattern.match('+7(123)-456-78-90'):
    print('Неверный формат телефона')