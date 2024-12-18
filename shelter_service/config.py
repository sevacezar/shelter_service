import os

UPLOAD_DIR_NAME: str = 'uploads'
UPLOAD_DIR_PATH: str = os.path.abspath(os.path.join(os.path.dirname(__file__), '.', UPLOAD_DIR_NAME))
