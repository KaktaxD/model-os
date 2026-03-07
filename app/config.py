import os
from dotenv import load_dotenv

load_dotenv()

# Имя переменной в .env = "SECRET_KEY"
SECRET_KEY = os.getenv("SECRET_KEY", "b4c09517c62a39dc2df795800dfd09d5450fb73b8bc8f35a11cd79835ab5fc00")
ALGORITHM = "HS256"
