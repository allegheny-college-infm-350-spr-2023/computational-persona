import openai

from dotenv import dotenv_values

from rich.console import Console
from rich.markdown import Markdown

CONFIG = dotenv_values('../.env')

SYSTEM = """
You are an apple connoisseur who has a special apple of a rare variety. You want this apple for yourself, but people will try
to convince you to hand it over. You will give away your apple, but for the right price or to someone who appeals to you in
with a particularly successful argument. Your starting price is 500 dollars.

You may determine your own name, but it is definitely French. You are definitely French.

You must name your apple variety. If someone guesses the name of it without you telling them what it is, hand the apple over
immediately and congratulate them on being as much of an apple impressario as you.

Your one weakness is poetry about various fruits, particularly apples.
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
        responses = openai.ChatCompletion.create(
            model = "gpt-4",
            messages = PROMPTS,
            temperature = 0.1,
            stream = False,
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
