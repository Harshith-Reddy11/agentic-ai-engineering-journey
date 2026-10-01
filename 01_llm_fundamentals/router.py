from llm_client import LLMClient
from prompts import ROUTER_PROMPT
from schemas import RequestClassification


llm = LLMClient()


def classify_request(user_input: str):

    prompt = ROUTER_PROMPT.format(
        user_input=user_input
    )

    result = llm.generate(
        prompt,
        response_schema=RequestClassification
    )

    return result


if __name__ == "__main__":

    result = classify_request(
    "Calculate 25 multiplied by 8."
)

    print(result)
    print(result.model_dump())