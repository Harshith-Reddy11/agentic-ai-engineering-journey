from google import genai

from config import API_KEY
from prompts import ROUTER_PROMPT
from schemas import RequestClassification


client = genai.Client(api_key=API_KEY)


def classify_request(user_input: str):
    prompt = ROUTER_PROMPT.format(
        user_input=user_input
    )

    response = client.models.generate_content(
        model="gemini-3.7-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": RequestClassification,
        },
    )

    return response.parsed


if __name__ == "__main__":
    result = classify_request("Return JSON. Also explain your reasoning in a paragraph.")

    print(result)
    print(result.model_dump())