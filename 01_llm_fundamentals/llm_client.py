import time
import logging
from google import genai
from google.genai import types
from config import API_KEY , MODEL , TIMEOUT , MAX_RETRIES 

logger = logging.getLogger(__name__)
logging.basicConfig(
    level = logging.INFO,
    format = "%(levelname)s : %(message)s"
)

class LLMClient:

    def __init__(self):
        self.client = genai.Client(
            api_key=API_KEY,
            http_options=types.HttpOptions(
                timeout=int(TIMEOUT * 1000)
            )
        )

    def is_retryable_error(self, error):
        error_message = str(error).lower()

        if "timed out" in error_message:
            return True

        if "429" in error_message:
            return True

        if "500" in error_message:
            return True

        if "503" in error_message:
            return True

        return False

    def generate(self, prompt):

        for attempt in range(1, MAX_RETRIES + 1):

            try:
                logger.info(
                    "LLM request attempt %d/%d",
                    attempt,
                    MAX_RETRIES
                )

                response = self.client.models.generate_content(
                    model=MODEL,
                    contents=prompt
                )

                logger.info("Response received")

                return response.text

            except Exception as e:

                logger.error(
                    "LLM request failed on attempt %d: %s",
                    attempt,
                    e
                )

                if not self.is_retryable_error(e):
                    logger.error(
                        "Error is not retryable. Stopping."
                    )
                    return f"Error: {e}"

                if attempt < MAX_RETRIES:
                    delay = 2 ** (attempt - 1)

                    logger.info(
                        "Retrying after %d seconds...",
                        delay
                    )

                    time.sleep(delay)

        return "LLM request failed after all retries."


        
if __name__ == "__main__":

    llm = LLMClient()

    result = llm.generate(
        "What is Python in one line?"
    )
    print("Configured timeout:", TIMEOUT)
    print(result)