from decouple import config

DATABASE_URL = config("DATABASE_URL")
REDIS_URL = config("REDIS_URL")
print(f"REDIS_URL: {REDIS_URL}") 