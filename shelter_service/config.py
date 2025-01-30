import os

from dotenv import load_dotenv

UPLOAD_DIR_NAME: str = 'uploads'
UPLOAD_DIR_PATH: str = os.path.abspath(os.path.join(os.path.dirname(__file__), '.', UPLOAD_DIR_NAME))

dotenv_path: str = os.path.join(os.path.dirname(__file__), '../.env')

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path=dotenv_path)
else:
    raise FileNotFoundError(f'Файл с переменными окружения {dotenv_path}не найден')

# Настрока шифрования паролей
SECRET: str = os.getenv('SECRET', 'SECRET')
ALGORITHM: str = os.getenv('ALGORITHM', 'HS256')

# Данные подключения к БД
DB_HOST: str= os.getenv('DB_HOST', 'localhost')
DB_PORT: str = os.getenv('DB_PORT', '27017')
DB_NAME: str = os.getenv('DB_NAME', 'SHELTER')
DB_USERNAME: str = os.getenv('DB_USERNAME', 'admin')
DB_PASSWORD: str = os.getenv('DB_PASSWORD', 'password')

# Данные администратора
ADMIN_EMAIL: str = os.getenv('ADMIN_EMAIL', 'admin@mail.ru')
ADMIN_PASSWORD: str = os.getenv('ADMIN_PASSWORD', 'password')
ADMIN_FIRST_NAME: str = os.getenv('ADMIN_FIRST_NAME', 'Имя')
ADMIN_SECOND_NAME: str = os.getenv('ADMIN_SECOND_NAME', 'Фамилия')
ADMIN_PHONE: str = os.getenv('ADMIN_PHONE', '+79999999999')
