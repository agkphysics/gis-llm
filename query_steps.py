import argparse
import json
import os
import re
import traceback
from pathlib import Path

import openai
from dotenv import load_dotenv
from rich.console import Console

import numpy as np

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_ORGANIZATION = os.getenv("OPENAI_ORGANIZATION")

openai.api_key = OPENAI_API_KEY
openai.organization = OPENAI_ORGANIZATION


def json_default(obj):
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    elif np.isscalar(obj):
        return obj.item()
    raise TypeError(f"Cannot serialize object of type {type(obj)}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--prompt", type=Path, required=True)
    parser.add_argument("-m", "--model", type=str, default="gpt-3.5-turbo")
    args = parser.parse_args()

    if not args.model.startswith(("gpt-4", "gpt-3.5-turbo")):
        raise ValueError("This script only supports chat models.")

    console = Console()

    query = console.input("[cyan]Enter query:[/cyan] ")

    with open(args.prompt / "system.txt") as fid:
        system_prompt = fid.read().strip()

    def get_response(prompt: str) -> str:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ]

        console.print("Sending prompt:", style="bold")
        console.print(prompt, style="bright_black", soft_wrap=True, markup=False)

        response = openai.ChatCompletion.create(
            model=args.model, messages=messages, temperature=0
        )
        resp_content = response.choices[0].message.content
        console.print("Response:", style="bold")
        console.print(resp_content, style="bright_black", soft_wrap=True, markup=False)
        console.print()
        return resp_content

    # Step 1
    with open(args.prompt / "data_sources.json") as fid:
        data_sources = json.load(fid)

    data_description = "\n".join(
        [f"{i + 1}. {x['description']}" for i, x in enumerate(data_sources)]
    )
    with open(args.prompt / "step1.txt") as fid:
        prompt = fid.read().strip()
        prompt = prompt.format(data_description=data_description, query=query)

    resp_content = get_response(prompt)
    match = re.search(r"```json(.*)```", resp_content, re.DOTALL)
    if match is None:
        raise ValueError("Could not parse response.")
    obj = json.loads(match.group(1))
    sources = obj["data_sources"]
    area = obj["area"]

    console.input("Press enter to continue...")

    # Step 2
    used_sources = [data_sources[i - 1] for i in sources]
    for source in used_sources:
        stem, ext = os.path.splitext(source["filename"])
        source["filename"] = f"{stem}_{area.lower()}{ext}"
    data_details = "\n".join(
        [f"- `{x['filename']}`: {x['details']}" for x in used_sources]
    )
    with open(args.prompt / "step2.txt") as fid:
        prompt = fid.read().strip().format(data_details=data_details, query=query)

    resp_content = get_response(prompt)
    match = re.search(r"```python\n(.*)```", resp_content, re.DOTALL)
    if match is None:
        raise ValueError("Could not parse response.")
    code = match.group(1)

    console.input("Press enter to continue...")

    # Run generated code
    with open(args.prompt / "error.txt") as fid:
        error_prompt = fid.read().strip()

    def code_reprompt(code, line, error):
        prompt = error_prompt.format(code=code, line=line, error=error)

        resp_content = get_response(prompt)
        match = re.search(r"```python\n(.*)```", resp_content, re.DOTALL)
        if match is None:
            raise ValueError("Could not parse response.")
        code = match.group(1)
        return code

    def try_run_code(code):
        import fiona
        import rasterio as rio
        import rasterio.mask
        import rasterstats
        import pandas as pd
        import geopandas as gpd
        import numpy as np

        _locals = locals()
        exec(code, _locals)
        return json.dumps(_locals["answer"]()["result"], default=json_default)

    while True:
        try:
            console.print("Running code:", style="bold")
            console.print(code, markup=False)
            result = try_run_code(code)
            break
        except Exception as e:
            te = traceback.TracebackException.from_exception(e)
            code_lines = code.split("\n")
            for frame in reversed(te.stack):
                # Only get the most relevant frame
                if frame.name == "answer":
                    error_line = code_lines[frame.lineno - 1].strip()
                    error_msg = next(te.format_exception_only())
                    break
            else:
                raise
            console.print(
                f"Error in line:\n{error_line}\n{error_msg}",
                style="bold red",
                markup=False,
            )
            console.print("Reprompting...", style="bold")
            console.input("Press enter to continue...")
            code = code_reprompt(code, error_line, error_msg)

    # Step 3
    with open(args.prompt / "step3.txt") as fid:
        prompt = (
            fid.read()
            .strip()
            .format(answer=result, data_details=data_details, code=code, query=query)
        )

    resp_content = get_response(prompt)


if __name__ == "__main__":
    main()
