import argparse
import os
from pathlib import Path

import openai
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_ORGANIZATION = os.getenv("OPENAI_ORGANIZATION")

openai.api_key = OPENAI_API_KEY
openai.organization = OPENAI_ORGANIZATION


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--prompt", type=Path, required=True)
    parser.add_argument("-q", "--query", type=str, required=True)
    parser.add_argument("-m", "--model", type=str, default="gpt-4")
    parser.add_argument("-t", "--temperature", type=float, default=1.0)
    args = parser.parse_args()

    with open(args.prompt) as f:
        prompt = f.read()
    prompt += args.query

    if args.model.startswith(("gpt-4", "gpt-3.5-turbo")):
        messages = [{"role": "user", "content": prompt}]

        print("Sending message:")
        print(messages)
        print()

        response = openai.ChatCompletion.create(
            model=args.model, messages=messages, temperature=args.temperature
        )
        print("Response:")
        print(response.choices[0].message.content)
    else:
        response = openai.Completion.create(
            model=args.model,
            prompt=prompt,
            temperature=args.temperature,
            max_tokens=1024,
        )
        print("Response:")
        print(response.choices[0].text)


if __name__ == "__main__":
    main()
