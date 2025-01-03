import os

from dotenv import load_dotenv

UPLOAD_DIR_NAME: str = 'uploads'
UPLOAD_DIR_PATH: str = os.path.abspath(os.path.join(os.path.dirname(__file__), '.', UPLOAD_DIR_NAME))

dotenv_path: str = os.path.join(os.path.dirname(__file__), '.env')

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path=dotenv_path)
else:
    raise FileNotFoundError(f'Файл с переменными окружения {dotenv_path}не найден')

SECRET: str = os.getenv('SECRET')
ALGORITHM: str = os.getenv('ALGORITHM')

