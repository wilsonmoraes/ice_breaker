import os

from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()
    print("Hello LangChain!")
    print(f"Hello {os.getenv('COL_API_KEY')}!")
