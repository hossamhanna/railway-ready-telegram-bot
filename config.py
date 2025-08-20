import os
from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql+asyncpg://postgres:password@db:5432/mahami')
ADMIN_IDS = {int(x) for x in os.getenv('ADMIN_IDS','').split(',') if x}