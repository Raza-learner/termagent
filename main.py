import os
import time
from dotenv import load_dotenv
from google import genai
import argparse


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)


parser = argparse.ArgumentParser(description="user prompt")
parser.add_argument("user_prompt", type=str, help=" "" to add prompt")
args = parser.parse_args()
     
def response():
    response = client.models.generate_content(
    model='gemini-2.5-flash', 
    contents=args.user_prompt    
    )
    try:
        usage = response.usage_metadata
        print(f"Prompt tokens:{usage.prompt_token_count}")
        print(f"Response tokens:{usage.candidates_token_count}")
        print(response.text)
    except RuntimeError as e:
        if usage is None:
            print(f"Gemini API response appears to be malformed{e}")

    
def main()->None:
    response()

if __name__ == "__main__":
    main()
