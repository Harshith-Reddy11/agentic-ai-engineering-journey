from llm_client import generate_response
from prompts import (
    EXPLAIN_PROMPT,
    QUIZ_PROMPT,
    SUMMARIZE_PROMPT
)


def main():

    print("================================")
    print("       AI Study Assistant")
    print("================================")
    print("Commands:")
    print("  explain <topic>")
    print("  quiz <topic>")
    print("  summarize <text>")
    print("  exit")
    print()

    while True:

        user_input = input("You: ").strip()

        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        if user_input.lower().startswith("explain "):

            topic = user_input[8:]

            prompt = EXPLAIN_PROMPT.format(
                topic=topic
            )

            response = generate_response(prompt)

            print("\nAI:", response)

        elif user_input.lower().startswith("quiz "):

            topic = user_input[5:]

            prompt = QUIZ_PROMPT.format(
                topic=topic
            )

            response = generate_response(prompt)

            print("\nAI:", response)

        elif user_input.lower().startswith("summarize "):

            text = user_input[10:]

            prompt = SUMMARIZE_PROMPT.format(
                text=text
            )

            response = generate_response(prompt)

            print("\nAI:", response)

        else:

            print(
                "Unknown command. "
                "Use explain, quiz, summarize, or exit."
            )


if __name__ == "__main__":
    main()