import openai

from dotenv import dotenv_values
from datetime import datetime

from rich.console import Console
from rich.markdown import Markdown

CONFIG = dotenv_values('../.env')

SYSTEM = """
Your persona goes here. You should be descriptive as to all of the ways that you want this persona to exist in digital or, even, physical
space. This should include personality traits, areas of strength or weakness or even expertise.
"""

PROMPTS = [
    {"role": "system", "content": SYSTEM}
]

CONSOLE = Console()

openai.api_key = CONFIG["KEY"]
openai.api_org = CONFIG["ORG"]

def parse(response: dict = {}) -> str:
    for choice in response["choices"]:
        return choice["message"]["content"].strip()

def query(prompt: str = "") -> None:
    with CONSOLE.status("Waiting for response...", spinner = "clock"):
        PROMPTS.append(
            {"role":"user", "content":prompt}
        )
        # MIGHTDO: You might alter the below to use "temperature" or
        #          to use "top_p" -- see README
        responses = openai.ChatCompletion.create(
            model = "gpt-4",
            messages = PROMPTS,
            temperature = 0.1,
            n = 1
        )
        response = parse(responses)
        markdown = Markdown(response)
        CONSOLE.print(response)

def main():
    print(f"""SYSTEM PROMPT:
        {PROMPTS[0]["content"]}
    """)
    while True:
        prompt = input("> ")
        if not prompt:
            break
        query(prompt)

if __name__ == "__main__":
    main()
