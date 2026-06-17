import os
import argparse
from google.genai import types
from dotenv import load_dotenv
from google import genai
from config import system_prompt
from call_function import available_functions, call_function


def response():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="AI Agent")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    args = parser.parse_args()
    user_prompt = args.user_prompt
    messages: list[types.Content] = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    try:
        while True:
            response = client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], system_instruction=system_prompt
                ),
            )
            if args.verbose:
                usage = response.usage_metadata
                print(f"Prompt tokens: {usage.prompt_token_count}")
                print(f"Response tokens: {usage.candidates_token_count}")

            messages.append(response.candidates[0].content)

            if response.function_calls:
                function_results = []
                for function_call in response.function_calls:
                    result = call_function(function_call, verbose=args.verbose)
                    # your 3 checks here
                    function_results.append(result.parts[0])
                messages.append(types.Content(role="user", parts=function_results))
            else:
                print(response.text)
                break

    except RuntimeError as e:
        raise Exception(f"Gemini API response appears to be malformed{e}")


def main() -> None:
    response()


if __name__ == "__main__":
    main()
