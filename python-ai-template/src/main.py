from dotenv import load_dotenv
import os

load_dotenv()
print("App:", os.getenv("APP_NAME"))
print("Debug:", os.getenv("DEBUG"))