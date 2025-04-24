from openai import OpenAI
from misc.config import OPENAI_API_KEY, OPENAI_PROJECT_KEY

client = OpenAI(api_key=OPENAI_API_KEY, project=OPENAI_PROJECT_KEY)

def moderate_text_openai(text: str) -> bool:
    response = client.moderations.create(
        input=text,
        model="omni-moderation-latest"
    )
    return response["results"][0]["flagged"]


print(moderate_text_openai("ХУЙ"))


